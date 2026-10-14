from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from exporter_helpers.extract_tosca_docx import extract_docx_images, main


DOCUMENT_XML = """\
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>Pantalla de búsqueda</w:t></w:r></w:p>
    <w:p><w:r><w:drawing><a:blip r:embed="rId1"/></w:drawing></w:r></w:p>
    <w:p><w:r><w:t>Resultado esperado: se muestra el cliente.</w:t></w:r></w:p>
  </w:body>
</w:document>
"""

RELATIONSHIPS_XML = """\
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Target="media/screenshot.png"
   Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"/>
</Relationships>
"""


def write_docx(path: Path, relationships: str | None, media: bytes = b"image-data") -> None:
    with ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", DOCUMENT_XML)
        if relationships is not None:
            archive.writestr("word/_rels/document.xml.rels", relationships)
        if media:
            archive.writestr("word/media/screenshot.png", media)


class ExtractDocxImagesTests(unittest.TestCase):
    def test_main_writes_image_manifest_and_extracted_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            docx_path = root / "evidencia.docx"
            output_path = root / "output" / "evidencia_docx.json"
            write_docx(docx_path, RELATIONSHIPS_XML)

            with patch(
                "sys.argv",
                ["extract_tosca_docx.py", "--input", str(docx_path), "--output", str(output_path)],
            ):
                main()

            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["images"][0]["path"],
                "evidencia_docx_images/image_001.png",
            )
            self.assertEqual(
                (output_path.parent / payload["images"][0]["path"]).read_bytes(),
                b"image-data",
            )

    def test_extracts_embedded_image_and_neighboring_paragraph_context(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            docx_path = root / "evidencia.docx"
            write_docx(docx_path, RELATIONSHIPS_XML)

            images, warnings = extract_docx_images(docx_path, root / "evidencia_images")

            self.assertEqual(warnings, [])
            self.assertEqual(len(images), 1)
            self.assertEqual(
                images[0]["context"],
                {
                    "paragraph": "",
                    "before": "Pantalla de búsqueda",
                    "after": "Resultado esperado: se muestra el cliente.",
                },
            )
            extracted_path = root / images[0]["path"]
            self.assertEqual(extracted_path.read_bytes(), b"image-data")

    def test_warns_when_image_relationship_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            docx_path = root / "evidencia.docx"
            write_docx(docx_path, None)

            images, warnings = extract_docx_images(docx_path, root / "evidencia_images")

            self.assertEqual(images, [])
            self.assertEqual(len(warnings), 1)
            self.assertIn("sin una relación DOCX válida", warnings[0])

    def test_warns_and_skips_externally_linked_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            docx_path = root / "evidencia.docx"
            external_relationships = RELATIONSHIPS_XML.replace(
                'Target="media/screenshot.png"',
                'Target="https://example.test/screenshot.png" TargetMode="External"',
            )
            write_docx(docx_path, external_relationships, media=b"")

            images, warnings = extract_docx_images(docx_path, root / "evidencia_images")

            self.assertEqual(images, [])
            self.assertEqual(len(warnings), 1)
            self.assertIn("vinculada externamente", warnings[0])


if __name__ == "__main__":
    unittest.main()
