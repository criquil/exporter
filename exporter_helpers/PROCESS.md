# Proceso completo de exportación Tosca → Markdown

Este documento es la **única fuente de verdad** para el proceso de exportación. El agente (`exporter.agent.md`) es solo un trigger que invoca este proceso.

---

## 1. Rol
Agente de documentación/QA Automation. Transforma un export de Tosca en un caso de prueba humano-legible, pensado para ser automatizable luego en Playwright.

## 2. Archivos del proceso
- `exporter_helpers/extract_tosca_excel.py` — extrae Excel a JSON estructurado
- `exporter_helpers/extract_tosca_docx.py` — extrae Docx a JSON de soporte

## 3. Input esperado
- Excel exportado desde Tosca (`.xlsx`) en `./tosca/` — columnas: `Name`, `Value`, `ActionMode`, `DataType`, `WorkState`.
- Secciones posibles: `Pre-Caso`, `Caso`, `Post-Caso`.
- Variables/buffers: `{CP[...]}` y `{B[...]}`.
- Docx opcional de evidencias (`.docx`) en `./tosca/` — comparte nombre base con el `.xlsx`.
- Los archivos pueden tener **cualquier nombre**. No asumir nombres fijos.

## 4. Extracción (paso 1 obligatorio)

> ⚠️ **NUNCA usar `--input` con nombres hardcodeados.** Los scripts auto-descubren archivos en `tosca/`. Ejecutar SIEMPRE sin argumentos.

```powershell
C:/Users/cristian.rosa/exporter/.venv/Scripts/python.exe exporter_helpers/extract_tosca_excel.py
```

```powershell
C:/Users/cristian.rosa/exporter/.venv/Scripts/python.exe exporter_helpers/extract_tosca_docx.py
```

- Ambos escanean `./tosca/` y generan JSON en `exporter_helpers/out/` con nombre sanitizado (ej: `Caso 999 SCACS.xlsx` → `caso_999_scacs_excel.json`).
- Si no hay `.docx`, el script lo indica con `[INFO]` y finaliza sin error.

## 5. Fuentes para redactar el markdown
1. `sections.Caso` del JSON de Excel — fuente principal de pasos.
2. `sections.Pre-Caso` y `sections.Post-Caso` — para filtrar ruido técnico y extraer datos iniciales.
3. `test_data` del JSON de Excel — fuente principal de la tabla de Test Data (ver §6).
4. `buffer_values` del JSON de Docx — valores reales ejecutados (para completar la columna Valor cuando aplique).
5. `lines` del JSON de Docx — solo como apoyo para clarificar pantallas/flujo.

## 6. Reglas de extracción

### Inclusión / Exclusión
- **Incluir solo** acciones de navegador web: navegación, click, input, selección, verify web, popups del browser, descargas del browser.
- **Excluir** limpieza técnica de browser, comandos SO, apps de escritorio (`taskkill`, ventanas Windows, etc.).
- Detectar separadores: `Pre-Caso`, `Caso`, `Post-Caso`, `****Definicion del Caso****`.

### Conversiones
- `Condition ... Exists == True Verify` → aserciones funcionales.
- `If/Then` o `Condition/Then` → ramas: **Si aparece [popup], entonces [acción]**.
- Waits (`TBox Wait`) → "Esperar carga de [pantalla/sección/resultados]".
- Selecciones de tabla (`Select` + `$1` + `{Click}`) → "Seleccionar la primera fila de la tabla [nombre]".

### Variables
- Incluir solo las relevantes al navegador en `Test Data / Parámetros`.
- Excluir variables de contexto desktop/SO.
- No hardcodear valores en pasos.

### Test data (identificación de parámetros)
El script `extract_tosca_excel.py` ya genera la lista `test_data` con **toda** la test data relevante, clasificada y con descripción funcional. No inventarla a mano; usarla como base y completarla si falta algo evidente.

Cada entrada de `test_data` tiene:
- `name`: nombre limpio del parámetro (ej. `UrlScacs`, `Password`, `Flujo_1`).
- `reference`: cómo se referencia (`` `{CP[Nombre]}` `` para variables CP; el nombre del campo para literales/credenciales).
- `kind`: `cp` (parametrizada), `credential` (usuario/contraseña sin valor) o `literal` (valor fijo).
- `category`: `url`, `usuario`, `password`, `documento`, `ambiente`, `estado`, `valor` u `otro`.
- `description`: descripción funcional legible.
- `value`: valor concreto si está presente; `null` si no.
- `value_legend`: `"Por favor proveer este valor"` cuando el valor falta.
- `hint`: nota aclaratoria cuando el "valor" era en realidad una descripción (ej. montos "Se declara por CP…").

**Debe identificarse toda la test data relevante**, incluso cuando el valor no esté presente (URLs, usuario, contraseña, documento, ambiente, estados, montos, valores). Si el valor falta, se coloca la leyenda `"Por favor proveer este valor"`.

**Completar valores desde `buffer_values` del Docx** cuando el nombre coincida (ej. `{CP[NroDocumento]}` ← `buffer_values.NroDocumento = "20252658794"`). Si no hay coincidencia, dejar la leyenda.

**Excluir** de la tabla: variables internas de buffer `{B[...]}`, variables técnicas de control (`Etiqueta`, `Exportar`) y cualquier dato de contexto desktop/SO (rutas de red, nombres de archivo de reporte, `Passed`, `--`, etc.).

## 7. Nivel de detalle de navegación (CRÍTICO)
> ⚠️ **NO colapsar acciones de navegación en pasos genéricos.** El markdown debe ser lo suficientemente detallado para que un automatizador pueda implementarlo sin ambigüedad.

Cada interacción del usuario identificada en el Excel (`{Click}`, `Input`, `Select`, `Verify`) debe reflejarse como paso o sub-paso individual.

**Reglas de granularidad:**
- **Un paso por cada interacción visible** del usuario: click, input, selección de combo, selección de fila en grilla.
- **Nombrar los elementos de interfaz** tal como aparecen en el Excel: "Menu Hamburguesa", "Lupa Buscar Cliente", "Buscar", "Tabla Búsqueda Cliente/Grupo", etc.
- **Incluir la secuencia de menú completa** cuando se navega por un menú (ej: abrir menú → recorrer opciones → click en la opción destino).
- **Describir formularios campo a campo** cuando hay múltiples inputs.
- Los waits (`TBox Wait`) se convierten en: "Esperar carga de [pantalla/sección/resultados]".
- Las selecciones de tabla (`Select` + `$1` + `{Click}`) se redactan como: "Seleccionar la primera fila de la tabla [nombre]".

**Ejemplos:**

| ❌ Incorrecto (genérico)                         | ✅ Correcto (detallado)                                                       |
|--------------------------------------------------|--------------------------------------------------------------------------------|
| "Seleccionar la opción Asociar más Garantías"    | "Hacer click en el botón Hamburguesa (menú lateral)"                           |
|                                                  | "Esperar que se despliegue el menú de navegación"                              |
|                                                  | "Hacer click en 'Sist. Manual Rel. Garantías' del menú lateral"               |

| ❌ Incorrecto (genérico)                         | ✅ Correcto (detallado)                                                       |
|--------------------------------------------------|--------------------------------------------------------------------------------|
| "Ingresar NroDocumento en el campo de búsqueda" | "En Selección de Cliente, ingresar `{CP[NroDocumento]}` en 'Número Documento'" |
|                                                  | "Hacer click en 'Buscar'"                                                     |
|                                                  | "Seleccionar el primer cliente de la tabla de resultados"                      |

## 8. Formato de salida Markdown (obligatorio)

El `.md` final DEBE seguir esta estructura. Cada paso en lenguaje funcional con **Acción** y **Resultado esperado**.

### Plantilla

```markdown
# Caso XXXX - <Título funcional del caso>

## Objetivo
Descripción concisa del propósito de la prueba. Usar negritas (**valor**) para resaltar estados, campos y valores clave.

## Alcance
- Incluye únicamente acciones funcionales dentro del navegador web (<Aplicación>).
- Incluye <resumen de flujo principal: login, búsqueda, navegación, validación>.
- Excluye limpieza técnica de browser, comandos de sistema operativo, apps de escritorio y registro en Excel de resultados.

## Precondiciones
- Condiciones previas necesarias (usuario, datos existentes, entorno disponible, etc.).

## Test Data / Parámetros
| Variable              | Descripción                          | Valor                    |
|-----------------------|--------------------------------------|--------------------------|
| `{CP[Variable]}`      | Descripción funcional del parámetro  | (valor o leyenda)        |

**Reglas para tabla de test data:**
- Construirla desde `test_data` del JSON de Excel (ver §6); incluir **todos** los parámetros relevantes: URLs, usuario, contraseña, documento, ambiente, estados, montos y valores, aunque su valor no esté presente.
- Columna **Descripción**: usar el texto funcional de `description` (no repetir la variable).
- Columna **Valor**: usar `value` si está presente; si `value` es `null`, escribir la leyenda `Por favor proveer este valor` (en cursiva). Si el Docx aporta un valor real en `buffer_values` con el mismo nombre, usarlo.
- Excluir variables internas de buffer `{B[...]}` y variables técnicas de control como `{CP[Etiqueta]}` o `{CP[Exportar]}`.
- Para credenciales sin valor (ej. `Password`), incluir la fila con su leyenda; no omitirlas.
- Envolver cada nombre de variable en backticks: `` `{CP[Nombre]}` ``.
- Alinear columnas para que todas las filas tengan el mismo ancho por columna.

## Pasos (Step-by-step)
Cada paso sigue el formato:
N. **Acción:** Descripción funcional de lo que se hace.
   **Resultado esperado:** Lo que se espera ver/obtener tras la acción.
   - (Opcional) Sub-bullet para ramas condicionales, popups, o aclaraciones.

**Reglas para redactar pasos:**
- **NO agrupar** acciones independientes del navegador en un solo paso. Solo agrupar cuando son inseparables (ej: ingresar usuario + contraseña + click LOGIN = un solo paso de "login").
- Cada click, input, selección o verificación **distinta** del Excel debe ser un paso o sub-paso propio.
- Nombrar los elementos de interfaz **tal como aparecen** en el Excel (ej: "Menu Hamburguesa", "Lupa Buscar Cliente").
- Usar lenguaje funcional, no técnico de Tosca (no usar "Input", "{Click}", "Select", "Constraint").
- Incluir las variables `{CP[...]}` dentro de la redacción cuando aportan contexto.
- Conservar branches de popups como sub-items del paso correspondiente.
- Si existe verificación (Verify), expresarla como resultado esperado del paso.

## Validaciones clave (assertions)
Lista de validaciones críticas del caso, redactadas como condiciones a cumplir.

## Observaciones generales
Notas sobre esperas, popups opcionales, ramas intermedias, sincronización, etc.

## Postcondiciones / Limpieza
Estado final esperado del entorno. Descartar pasos técnicos de SO/cierre forzado.
```

## 9. Output y entrega
- Guardar el `.md` final **siempre** en `./TCs/`.
- Nombre sugerido: `SCACS_<id>_<nombre_normalizado>.md`.
- No guardar el `.md` en `./tosca/`.
- **Crear/guardar el archivo físicamente** en el workspace. No alcanza con responder en el chat.
- Si el archivo ya existe, actualizarlo.
- Lenguaje funcional claro (qué hacer y qué verificar). No generar código, selectores, Page Objects ni estrategias de locator.

## 10. Limpieza post-exportación (obligatorio)
1. Verificar que el `.md` final quedó guardado en `./TCs/`.
2. Eliminar los archivos `*_excel.json` y `*_docx.json` generados en `./exporter_helpers/out/` para el caso procesado.
3. Confirmar al usuario la ruta final del `.md` en `TCs`.

## 11. Checklist de calidad
- [ ] Se ejecutaron los helpers de `exporter_helpers` **sin argumentos**.
- [ ] Se usó JSON de Excel como fuente principal.
- [ ] Solo se incluyeron pasos ejecutables en navegador.
- [ ] Se excluyeron acciones desktop/SO.
- [ ] Variables relevantes centralizadas en `Test Data / Parámetros`.
- [ ] Se identificó **toda** la test data (URL, usuario, contraseña, documento, ambiente, estados, montos, valores) y los valores faltantes llevan la leyenda `Por favor proveer este valor`.
- [ ] Hay aserciones claras y verificables.
- [ ] No hay recomendaciones técnicas de implementación.
- [ ] **Cada interacción del Excel (click, input, select, verify) tiene su propio paso o sub-paso — no hay pasos genéricos que colapsen múltiples acciones.**
- [ ] **Los elementos de interfaz se nombran tal como aparecen en el Excel.**
- [ ] El `.md` quedó guardado en `./TCs/`.
- [ ] Se eliminaron los `.json` temporales de `./exporter_helpers/out/`.
- [ ] Se confirmó en la salida la ruta del archivo creado/actualizado.
