# Copilot Instructions for `exporter`

## Big picture
- This repository converts Tosca exports into human-readable functional test cases.
- Core flow: Tosca files in `tosca/` → helper extraction scripts → JSON intermediates in `exporter_helpers/out/` → final Markdown in `TCs/`.
- `exporter_helpers/PROCESS.md` is the single source of truth for behavior, format, and quality checks.
- `.github/agents/exporter.agent.md` is only a trigger; it delegates all logic to `PROCESS.md`.

## Main components and boundaries
- `exporter_helpers/extract_tosca_excel.py`: parses `.xlsx` (first worksheet), builds sectioned JSON (`Pre-Caso`, `Caso`, `Post-Caso`) and extracts `{CP[...]}`/`{B[...]}` variables.
- `exporter_helpers/extract_tosca_docx.py`: parses `word/document.xml` from `.docx` and emits support lines JSON.
- `TCs/*.md`: final deliverables in functional language (no automation code, no selectors, no POM strategy).
- `tosca/`: input drop folder; file names are variable and must never be hardcoded.

## Required workflow (do not skip)
1. Read `exporter_helpers/PROCESS.md` fully before changing export behavior.
2. Run extraction helpers without hardcoded input names (auto-discovery in `tosca/`):
   - `C:/Users/cristian.rosa/exporter/.venv/Scripts/python.exe exporter_helpers/extract_tosca_excel.py`
   - `C:/Users/cristian.rosa/exporter/.venv/Scripts/python.exe exporter_helpers/extract_tosca_docx.py`
3. Build/update the test case Markdown in `TCs/` using Excel JSON as primary source, Docx JSON as support.
4. Delete generated `*_excel.json` and `*_docx.json` for the processed case from `exporter_helpers/out/`.

## Project-specific authoring rules
- Keep only browser-functional actions; exclude desktop/OS cleanup commands (`taskkill`, window management, etc.).
- Preserve step granularity from Tosca interactions: each independent click/input/select/verify becomes its own step or sub-step.
- Convert Tosca semantics consistently:
  - `Condition ... Exists == True Verify` → expected-result/assertion statements.
  - `If/Then` and popup handling → conditional sub-bullets in the same step.
  - `TBox Wait` → explicit “Esperar carga de …” style functional wait.
  - `Select` with `$1` + `{Click}` → select first row wording.
- Use `{CP[...]}` variables in steps and in `Test Data / Parámetros`; avoid hardcoding data values when parameterized.
- Exclude buffer/internal variables (`{B[...]}`) and technical control variables from the test-data table when PROCESS says to exclude them.

## Naming and output conventions
- JSON outputs are slugified from source names (`Caso 999 SCACS.xlsx` → `caso_999_scacs_excel.json`).
- Final Markdown files must be physically saved under `TCs/` (never in `tosca/`).
- Follow the full section template from `exporter_helpers/PROCESS.md` (`Objetivo`, `Alcance`, `Precondiciones`, `Test Data / Parámetros`, detailed `Pasos`, validations, observations, postconditions).

## When modifying helper scripts
- Preserve current defaults:
  - Input scan dir: `tosca/`
  - Output dir: `exporter_helpers/out/`
- Keep support for optional CLI args (`--input`, `--dir`, `--output`) but do not change default auto-discovery behavior.
- Maintain compatibility with current dependencies and style (`openpyxl`, `pathlib`, UTF-8 JSON with `ensure_ascii=False`, `indent=2`).

## Key reference files
- `exporter_helpers/PROCESS.md`
- `.github/agents/exporter.agent.md`
- `exporter_helpers/extract_tosca_excel.py`
- `exporter_helpers/extract_tosca_docx.py`
- Example output style: `TCs/SCACS_077_Calculo_para_la_habilitacion.md`
