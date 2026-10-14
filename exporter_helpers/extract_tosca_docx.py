from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import unicodedata
from pathlib import Path
from typing import TypedDict
from urllib.parse import unquote
from xml.etree import ElementTree
from zipfile import ZipFile


DEFAULT_TOSCA_DIR = Path("tosca")
DEFAULT_OUTPUT_DIR = Path("exporter_helpers/out")

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
VML_NS = "urn:schemas-microsoft-com:vml"

BUFFER_VALUE_PATTERN = re.compile(r"Buffer with name '([^']+)' has been set to value '([^']*)'")


class ImageContext(TypedDict):
    paragraph: str
    before: str
    after: str


class ImageManifestEntry(TypedDict):
    index: int
    path: str
    context: ImageContext


def clean_text(raw: str) -> str:
    text = (
        raw.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&#39;", "'")
        .replace("&quot;", '"')
    )
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_useful_line(text: str) -> bool:
    if not text:
        return False
    if "<w:" in text or "<v:" in text or "</" in text:
        return False
    if text.startswith("<") and text.endswith(">"):
        return False
    return True


def extract_docx_lines(docx_path: Path) -> list[str]:
    with ZipFile(docx_path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")

    chunks = re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml)
    lines = [clean_text(chunk) for chunk in chunks]
    return [line for line in lines if is_useful_line(line)]


def extract_docx_images(
    docx_path: Path, image_output_dir: Path
) -> tuple[list[ImageManifestEntry], list[str]]:
    """Extrae imágenes incrustadas y devuelve un manifiesto con contexto cercano."""
    with ZipFile(docx_path) as archive:
        names = set(archive.namelist())
        document = ElementTree.fromstring(archive.read("word/document.xml"))
        relationships_path = "word/_rels/document.xml.rels"
        relationships: dict[str, tuple[str, bool]] = {}
        if relationships_path in names:
            relationships_root = ElementTree.fromstring(archive.read(relationships_path))
            for relationship in relationships_root:
                relationship_id = relationship.get("Id")
                target = relationship.get("Target")
                if relationship_id and target:
                    relationships[relationship_id] = (
                        target,
                        relationship.get("TargetMode", "").lower() == "external",
                    )

        paragraphs = document.findall(f".//{{{WORD_NS}}}p")
        paragraph_texts = [
            clean_text(
                "".join(node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t"))
            )
            for paragraph in paragraphs
        ]

        images: list[ImageManifestEntry] = []
        warnings: list[str] = []
        image_output_dir.mkdir(parents=True, exist_ok=True)

        for paragraph_index, paragraph in enumerate(paragraphs):
            context: ImageContext = {
                "paragraph": paragraph_texts[paragraph_index],
                "before": next(
                    (text for text in reversed(paragraph_texts[:paragraph_index]) if text), ""
                ),
                "after": next(
                    (text for text in paragraph_texts[paragraph_index + 1 :] if text), ""
                ),
            }
            for element in paragraph.iter():
                if element.tag not in {
                    f"{{{DRAWING_NS}}}blip",
                    f"{{{VML_NS}}}imagedata",
                }:
                    continue

                relationship_id = element.get(f"{{{REL_NS}}}embed") or element.get(
                    f"{{{REL_NS}}}link"
                ) or element.get(f"{{{REL_NS}}}id")
                relationship = relationships.get(relationship_id or "")
                if relationship is None:
                    warnings.append(
                        f"Se encontró una imagen sin una relación DOCX válida "
                        f"(relación {relationship_id or 'no especificada'})."
                    )
                    continue

                target, is_external = relationship
                if is_external:
                    warnings.append(
                        "Se omitió una imagen vinculada externamente; no está incrustada "
                        "en el DOCX."
                    )
                    continue

                decoded_target = unquote(target)
                part_path = (
                    decoded_target.lstrip("/")
                    if decoded_target.startswith("/")
                    else posixpath.normpath(posixpath.join("word", decoded_target))
                )
                if part_path.startswith("../") or part_path not in names:
                    raise ValueError(
                        f"No se encontró la imagen incrustada '{target}' en {docx_path}."
                    )

                image_index = len(images) + 1
                extension = Path(part_path).suffix.lower() or ".img"
                image_name = f"image_{image_index:03d}{extension}"
                (image_output_dir / image_name).write_bytes(archive.read(part_path))
                images.append(
                    {
                        "index": image_index,
                        "path": f"{image_output_dir.name}/{image_name}",
                        "context": context,
                    }
                )

    return images, warnings


def extract_buffer_values(lines: list[str]) -> dict[str, str]:
    """Extrae los valores reales de buffers asignados durante la ejecución.

    Ej.: "NroDocumento: Buffer with name 'NroDocumento' has been set to value '20252658794'."
    → {"NroDocumento": "20252658794"}
    """
    values: dict[str, str] = {}
    for line in lines:
        match = BUFFER_VALUE_PATTERN.search(line)
        if match:
            values[match.group(1)] = match.group(2)
    return values


def sanitize_name(filename: str) -> str:
    """Convierte un nombre de archivo en un slug seguro para la salida JSON.

    Ejemplo: 'Caso 1000.docx' → 'caso_1000'
    """
    stem = Path(filename).stem
    slug = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^\w\s-]", "", slug).strip().lower()
    slug = re.sub(r"[\s-]+", "_", slug)
    return slug


def extract_case_id(filename: str) -> str | None:
    """Intenta extraer un ID numérico del nombre del archivo (ej. 'Caso 1000.docx' → '1000')."""
    match = re.search(r"(\d+)", Path(filename).stem)
    return match.group(1) if match else None


def discover_docx_files(directory: Path) -> list[Path]:
    """Devuelve todos los archivos .docx dentro del directorio dado."""
    if not directory.is_dir():
        raise FileNotFoundError(f"No existe el directorio: {directory}")
    return sorted(directory.glob("*.docx"))


def resolve_output_path(docx_path: Path, output_dir: Path) -> Path:
    """Genera la ruta de salida JSON a partir del nombre del Docx."""
    slug = sanitize_name(docx_path.name)
    return output_dir / f"{slug}_docx.json"


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Extrae texto e imágenes de DokuSnapper (.docx) para soporte del caso."
    )
    parser.add_argument("--input", default=None, help="Ruta del .docx (opcional si se usa --dir)")
    parser.add_argument("--output", default=None, help="Ruta de salida JSON (opcional, se auto-genera)")
    parser.add_argument(
        "--dir",
        default=None,
        help=f"Directorio donde buscar archivos .docx (default: {DEFAULT_TOSCA_DIR})",
    )
    args = parser.parse_args()

    # --- Resolver lista de archivos a procesar ---
    if args.input:
        docx_files = [Path(args.input)]
    else:
        scan_dir = Path(args.dir) if args.dir else DEFAULT_TOSCA_DIR
        docx_files = discover_docx_files(scan_dir)

    output_dir = DEFAULT_OUTPUT_DIR

    if not docx_files:
        print(f"[INFO] No se encontraron archivos .docx en: {scan_dir if not args.input else 'input'}")
        return

    for docx_path in docx_files:
        if not docx_path.exists():
            raise FileNotFoundError(f"No existe el archivo: {docx_path}")

        if args.output and len(docx_files) == 1:
            out_path = Path(args.output)
        else:
            out_path = resolve_output_path(docx_path, output_dir)

        lines = extract_docx_lines(docx_path)
        image_dir = out_path.parent / f"{out_path.stem}_images"
        images, image_warnings = extract_docx_images(docx_path, image_dir)
        payload = {
            "source": str(docx_path),
            "line_count": len(lines),
            "lines": lines,
            "buffer_values": extract_buffer_values(lines),
            "images": images,
            "image_warnings": image_warnings,
        }

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        case_id = extract_case_id(docx_path.name) or "?"
        print(
            f"[OK] {docx_path.name}  →  {out_path}  "
            f"(caso {case_id}, imágenes: {len(images)})"
        )
        for warning in image_warnings:
            print(f"[WARN] {warning}")


if __name__ == "__main__":
    main()
