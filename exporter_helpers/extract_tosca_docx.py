from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from zipfile import ZipFile


DEFAULT_TOSCA_DIR = Path("tosca")
DEFAULT_OUTPUT_DIR = Path("exporter_helpers/out")


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
    parser = argparse.ArgumentParser(
        description="Extrae texto plano de Docu Snaper (.docx) para soporte del caso."
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
        payload = {
            "source": str(docx_path),
            "line_count": len(lines),
            "lines": lines,
        }

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        case_id = extract_case_id(docx_path.name) or "?"
        print(f"[OK] {docx_path.name}  →  {out_path}  (caso {case_id})")


if __name__ == "__main__":
    main()
