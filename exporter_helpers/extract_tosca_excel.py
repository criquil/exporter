from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import openpyxl


SECTION_MARKERS = {"Pre-Caso", "Caso", "Post-Caso"}
NOISE_PREFIXES = ("Page ",)
DEFAULT_TOSCA_DIR = Path("tosca")
DEFAULT_OUTPUT_DIR = Path("exporter_helpers/out")


@dataclass
class RowData:
    row_number: int
    values: dict[int, str]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return re.sub(r"\s+", " ", text)


def row_to_values(row: tuple[Any, ...]) -> dict[int, str]:
    values: dict[int, str] = {}
    for idx, cell in enumerate(row, start=1):
        text = normalize_text(cell)
        if text:
            values[idx] = text
    return values


def is_noise(values: dict[int, str]) -> bool:
    if not values:
        return True
    joined = " | ".join(values.values())
    return any(prefix in joined for prefix in NOISE_PREFIXES)


def extract_variables(rows: list[RowData]) -> list[str]:
    tokens: set[str] = set()
    pattern = re.compile(r"\{(?:CP|B)\[[^\]]+\]\}")
    for row in rows:
        for value in row.values.values():
            tokens.update(pattern.findall(value))
    return sorted(tokens)


# --- Test data (parámetros, credenciales y valores) --------------------------

TECHNICAL_CP_NAMES = {"etiqueta", "exportar"}
DESCRIPTIVE_VALUE_PREFIXES = ("se declara por",)
VALUE_LEGEND = "Por favor proveer este valor"
VALUE_NOISE = {
    "x", "close", "maximize", "taskkill", "/f", "/im", "chrome.exe",
    "*google chrome*", "*microsoft*edge*", "*squirrel*", "restore pages?",
    "verify window exists", "exists == true", "save & close",
}
PASSWORD_NAMES = {"password", "pass", "contrasena", "contrase", "clave", "pwd", "pin", "secret"}
USER_NAMES = {"usuario", "user", "username", "login", "nick"}
CATEGORY_ORDER = {
    "url": 0, "usuario": 1, "password": 2, "documento": 3,
    "ambiente": 4, "estado": 5, "valor": 6, "otro": 7,
}


def norm(value: str) -> str:
    """Normaliza a minúsculas y sin acentos para comparaciones robustas."""
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return normalized.lower()


def classify_name(name: str) -> str:
    """Clasifica una variable/campo por su nombre en una categoría funcional."""
    n = norm(name)
    if any(k in n for k in ("password", "contrase", "pass", "clave", "pwd", "secret", "pin")):
        return "password"
    if any(k in n for k in ("usuario", "user", "username", "login", "nick")):
        return "usuario"
    if any(k in n for k in ("url", "link", "enlace", "http", "host", "site", "pagina", "address")):
        return "url"
    if any(k in n for k in ("documento", "nrodoc", "nrodocumento", "dni", "cuit", "cuil")):
        return "documento"
    if any(k in n for k in ("estado", "state", "situacion", "flujo")):
        return "estado"
    if any(k in n for k in ("ambiente", "environment", "entorno")):
        return "ambiente"
    if any(k in n for k in ("monto", "importe", "valor", "habilitado", "limite", "descripcion")):
        return "valor"
    return "otro"


def describe_test_data(name: str, category: str) -> str:
    """Genera una descripción funcional legible para la tabla de test data."""
    n = norm(name)
    if category == "url":
        return "URL del portal/aplicación utilizada durante la prueba."
    if category == "usuario":
        return "Usuario de acceso a la aplicación."
    if category == "password":
        return "Contraseña de acceso a la aplicación."
    if category == "documento":
        return "Número de documento del cliente a evaluar."
    if category == "estado":
        if "flujo" in n:
            return "Flujo a seleccionar en el filtro de búsqueda."
        return "Estado a seleccionar/filtrar en la búsqueda."
    if category == "ambiente":
        return "Ambiente/entorno objetivo de la prueba."
    if category == "valor":
        if "monto" in n:
            return "Monto a validar durante la prueba."
        if "descripcion" in n:
            return "Descripción a validar durante la prueba."
        return "Valor a validar durante la prueba."
    return "Parámetro de prueba."


def field_name(row: RowData) -> str:
    """Devuelve el nombre de campo: la celda de nombre más profunda (columnas 3-13)."""
    for col in range(13, 2, -1):
        text = row.values.get(col, "")
        if text:
            return text
    return ""


def extract_test_data(rows: list[RowData]) -> list[dict[str, Any]]:
    """Identifica toda la test data relevante: variables {CP[...]}, credenciales
    (usuario/password) y valores literales (estados, montos, ambiente, etc.).

    Cada entrada incluye categoría, descripción funcional y valor. Cuando el valor
    no está presente se agrega `value_legend` para sugerir su relleno.
    """
    entries: dict[str, dict[str, Any]] = {}
    cp_categories: set[str] = set()
    cp_pattern = re.compile(r"\{CP\[([^\]]+)\]\}")

    # 1) Variables parametrizadas {CP[...]}
    cp_names: set[str] = set()
    for row in rows:
        for value in row.values.values():
            cp_names.update(cp_pattern.findall(value))

    for name in sorted(cp_names):
        if norm(name) in TECHNICAL_CP_NAMES:
            continue
        category = classify_name(name)
        cp_categories.add(category)
        entries[norm(name)] = {
            "name": name,
            "reference": f"{{CP[{name}]}}",
            "kind": "cp",
            "category": category,
            "description": describe_test_data(name, category),
            "value": None,
            "hint": None,
            "value_legend": VALUE_LEGEND,
        }

    # 2) Credenciales y valores literales (solo en Pre-Caso / Caso)
    current_section = "SinSeccion"
    section_skip = {"caso", "pre-caso", "post-caso", "sinseccion", "definicion del caso"}
    for row in rows:
        marker = row.values.get(4, "")
        if marker in SECTION_MARKERS:
            current_section = marker
        if current_section == "Post-Caso":
            continue

        name = field_name(row)
        if not name:
            continue
        n = norm(name)
        if n in section_skip or n in TECHNICAL_CP_NAMES:
            continue

        category = classify_name(name)
        mode = row.values.get(16, "")
        value = row.values.get(14, "")

        # Credenciales sin valor (ej. campo Password vacío)
        if not value and (n in PASSWORD_NAMES or n in USER_NAMES):
            cat = "password" if n in PASSWORD_NAMES else "usuario"
            if cat in cp_categories or n in entries:
                continue
            entries[n] = {
                "name": name,
                "reference": name,
                "kind": "credential",
                "category": cat,
                "description": describe_test_data(name, cat),
                "value": None,
                "hint": None,
                "value_legend": VALUE_LEGEND,
            }
            continue

        # Valores literales de campos Input concretos
        if mode != "Input" or not value or value.startswith("{"):
            continue
        v = value.strip()
        vnorm = norm(v)
        if vnorm in VALUE_NOISE or re.fullmatch(r"\d+", v) or (v.startswith("*") and v.endswith("*")):
            continue

        if vnorm.startswith(DESCRIPTIVE_VALUE_PREFIXES):
            entries.setdefault(n, {
                "name": name,
                "reference": name,
                "kind": "literal",
                "category": category,
                "description": describe_test_data(name, category),
                "value": None,
                "hint": v,
                "value_legend": VALUE_LEGEND,
            })
            continue

        entries.setdefault(n, {
            "name": name,
            "reference": name,
            "kind": "literal",
            "category": category,
            "description": describe_test_data(name, category),
            "value": v,
            "hint": None,
            "value_legend": None,
        })

    ordered = sorted(
        entries.values(),
        key=lambda e: (CATEGORY_ORDER.get(e["category"], 9), norm(e["name"])),
    )
    return ordered


def parse_sections(rows: list[RowData]) -> dict[str, list[RowData]]:
    current = "SinSeccion"
    sections: dict[str, list[RowData]] = {"SinSeccion": []}

    for row in rows:
        marker = row.values.get(4, "")
        if marker in SECTION_MARKERS:
            current = marker
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(row)

    return sections


def build_payload(excel_path: Path) -> dict[str, Any]:
    workbook = openpyxl.load_workbook(excel_path, data_only=True)
    worksheet = workbook.worksheets[0]

    rows: list[RowData] = []
    for row_number, row in enumerate(worksheet.iter_rows(values_only=True), start=1):
        values = row_to_values(row)
        if is_noise(values):
            continue
        rows.append(RowData(row_number=row_number, values=values))

    sections = parse_sections(rows)
    variables = extract_variables(rows)
    test_data = extract_test_data(rows)

    serializable_sections: dict[str, list[dict[str, Any]]] = {}
    for key, section_rows in sections.items():
        serializable_sections[key] = [
            {"row": item.row_number, "values": item.values} for item in section_rows
        ]

    return {
        "source": str(excel_path),
        "sheet": worksheet.title,
        "rows_total": worksheet.max_row,
        "sections": serializable_sections,
        "variables": variables,
        "test_data": test_data,
    }


def sanitize_name(filename: str) -> str:
    """Convierte un nombre de archivo en un slug seguro para la salida JSON.

    Ejemplo: 'Caso 999 SCACS.xlsx' → 'caso_999_scacs'
    """
    stem = Path(filename).stem
    slug = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^\w\s-]", "", slug).strip().lower()
    slug = re.sub(r"[\s-]+", "_", slug)
    return slug


def extract_case_id(filename: str) -> str | None:
    """Intenta extraer un ID numérico del nombre del archivo (ej. 'Caso 999 SCACS.xlsx' → '999')."""
    match = re.search(r"(\d+)", Path(filename).stem)
    return match.group(1) if match else None


def discover_excel_files(directory: Path) -> list[Path]:
    """Devuelve todos los archivos .xlsx dentro del directorio dado."""
    if not directory.is_dir():
        raise FileNotFoundError(f"No existe el directorio: {directory}")
    files = sorted(directory.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError(f"No se encontraron archivos .xlsx en: {directory}")
    return files


def resolve_output_path(excel_path: Path, output_dir: Path) -> Path:
    """Genera la ruta de salida JSON a partir del nombre del Excel."""
    slug = sanitize_name(excel_path.name)
    return output_dir / f"{slug}_excel.json"


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Extrae estructura utilizable de un Excel exportado desde Tosca."
    )
    parser.add_argument("--input", default=None, help="Ruta del .xlsx de Tosca (opcional si se usa --dir)")
    parser.add_argument(
        "--output",
        default=None,
        help="Ruta de salida JSON (opcional, se auto-genera a partir del nombre del input)",
    )
    parser.add_argument(
        "--dir",
        default=None,
        help=f"Directorio donde buscar archivos .xlsx (default: {DEFAULT_TOSCA_DIR})",
    )
    args = parser.parse_args()

    # --- Resolver lista de archivos a procesar ---
    if args.input:
        excel_files = [Path(args.input)]
    else:
        scan_dir = Path(args.dir) if args.dir else DEFAULT_TOSCA_DIR
        excel_files = discover_excel_files(scan_dir)

    output_dir = DEFAULT_OUTPUT_DIR

    for excel_path in excel_files:
        if not excel_path.exists():
            raise FileNotFoundError(f"No existe el archivo: {excel_path}")

        # Si se dio --output explícito y es un solo archivo, usarlo
        if args.output and len(excel_files) == 1:
            out_path = Path(args.output)
        else:
            out_path = resolve_output_path(excel_path, output_dir)

        payload = build_payload(excel_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        case_id = extract_case_id(excel_path.name) or "?"
        print(f"[OK] {excel_path.name}  →  {out_path}  (caso {case_id})")


if __name__ == "__main__":
    main()
