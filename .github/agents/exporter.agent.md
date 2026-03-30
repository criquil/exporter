# Agente: Tosca Export → Markdown (trigger)

Este agente es un **trigger**. Toda la lógica, reglas, formato y checklist están definidos en `exporter_helpers/PROCESS.md`.

## Instrucción única

Al recibir la orden de exportar:

1. **Leer** `exporter_helpers/PROCESS.md` completo.
2. **Ejecutar** el proceso definido ahí paso a paso (extracción → redacción → guardado → limpieza).
3. **No inventar reglas propias.** Si algo no está en PROCESS.md, no hacerlo.

## Referencia

- Proceso completo: `exporter_helpers/PROCESS.md`
- Scripts: `exporter_helpers/extract_tosca_excel.py`, `exporter_helpers/extract_tosca_docx.py`
- Input: `./tosca/` (auto-descubrimiento, nunca hardcodear nombres)
- Output: `./TCs/`