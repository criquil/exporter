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
- Docx opcional de evidencias generado por DokuSnapper (`.docx`) en `./tosca/` — comparte nombre base con el `.xlsx`.
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
- El extractor DOCX lee texto y valores de buffers, extrae las imágenes incrustadas a una carpeta `*_docx_images/` junto al JSON, y registra en `images` sus rutas y el texto del párrafo inmediato y de los párrafos vecinos.
- El extractor solo prepara archivos y contexto: **no interpreta visualmente las imágenes ni llama a un servicio de IA**.
- Si no hay `.docx`, el script lo indica con `[INFO]` y finaliza sin error.

## 5. Fuentes para redactar el markdown
1. `sections.Caso` del JSON de Excel — fuente principal de pasos.
2. `sections.Pre-Caso` y `sections.Post-Caso` — para filtrar ruido técnico y extraer datos iniciales.
3. `test_data` del JSON de Excel — fuente principal de la tabla de Test Data (ver §6).
4. `buffer_values` del JSON de Docx — valores reales ejecutados (para completar la columna Valor cuando aplique).
5. `lines` del JSON de Docx — solo como apoyo textual para clarificar pantallas/flujo.
6. `images` del JSON de Docx y los archivos indicados por sus rutas — evidencia visual opcional para enriquecer pasos y resultados esperados.

### Análisis visual de las evidencias DokuSnapper
- Cuando haya imágenes incrustadas en el DOCX, examina los archivos listados en `images` con el modelo o herramienta de visión disponible para esta sesión; si el entorno permite seleccionar un modelo, elige uno con capacidad visual. Relaciona cada imagen con el párrafo y contexto cercano que aporta el JSON. No simules análisis visual con un modelo de solo texto.
- Si el modelo/herramientas de esta ejecución no permiten recibir o interpretar imágenes, indícalo claramente al usuario y explica que la evidencia visual no fue analizada por esa limitación. **Continúa el flujo habitual** con el Excel de Tosca, el texto y los buffers del DOCX; no detengas la generación ni afirmes haber interpretado las imágenes.
- Integra únicamente detalles visuales que aporten al caso, junto al paso, resultado esperado o validación correspondiente (por ejemplo, nombres visibles de pantallas, campos, botones, mensajes y datos observables). No agregues una descripción genérica por imagen si no mejora la comprensión del flujo.
- No inventes interacciones, valores, estados ni texto ilegible. Distingue lo observado en la imagen de lo inferido por el contexto; si una evidencia no se puede asociar con confianza a un paso, omite ese detalle o indícalo como observación no concluyente.
- Si el JSON incluye `image_warnings`, considera esos avisos: las imágenes externas o con relaciones rotas no se analizaron. No digas que se revisaron imágenes que no estén disponibles.

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

Cada exportación debe generar **dos documentos Markdown** en `./TCs/`: el caso de prueba normal y su variante BDD. Usar como base, respectivamente, `exporter_helpers/templates/tc_template.md` y `exporter_helpers/templates/bdd_template.md`. No reemplazar estas plantillas por una estructura inventada ni dejar sus instrucciones, comentarios HTML o placeholders en la entrega final.

### Caso de prueba normal
- Conservar las secciones, tablas por fase y flujo definidas en `tc_template.md`: Propósito, Descripción, Data I/O, Precondiciones, Steps, Resultado Esperado, Observaciones generales, Postcondiciones / Limpieza y Flujo.
- Organizar los pasos en fases secuenciales. La fase **Preparación** siempre abre con la URL base y la comprobación/obtención del estado limpio indicado en las precondiciones.
- Representar cada interacción distinta del Excel como una fila de paso propia; no agrupar acciones independientes. Usar texto funcional y los nombres de UI del origen.
- En Data I/O, incluir todos los parámetros relevantes como `Input`, los valores verificados como `Output` y la fila `resultado` que indica Pass / Fail. Mantener valores faltantes con la leyenda *Por favor proveer este valor*.
- Completar las secciones Resultado Esperado y Flujo; el diagrama debe comenzar en Preparación y terminar en la validación y limpieza.

### Variante BDD
- Conservar las secciones y especificación Gherkin de `bdd_template.md`: Propósito, Descripción, Data I/O, Precondiciones, Especificación Gherkin, Resultado Esperado, Observaciones generales, Postcondiciones / Limpieza y Flujo BDD.
- Usar keywords Gherkin en inglés (`Feature`, `Background`, `Scenario`, `Given`, `When`, `Then`, etc.) y redactar el contenido en español, salvo que se solicite otro idioma.
- Incluir `@BDD-[ID]`, una etiqueta del módulo y al menos una etiqueta de tipo de prueba (`@Smoke`, `@Regression` o `@E2E`); incluir también `@TC-[ID]` en el escenario principal.
- Hacer el escenario independiente: el `Background` navega a la URL base y declara la sesión/storage limpio; las precondiciones identifican datos, autenticación y recursos necesarios. No referenciar otros casos ni asumir estado previo.
- Mantener el escenario declarativo y orientado a negocio, sin selectores, código, detalles de implementación ni pasos de automatización. Expresar ramas opcionales de forma condicional y completar el flujo BDD hasta postcondiciones/limpieza.
- Usar siempre `Scenario Outline` con una sección `Examples`, incluso cuando el caso tenga un único conjunto de datos. En ese caso, incluir una única fila de datos en `Examples`; para varios conjuntos, incluir una fila por combinación. Referenciar en los pasos los parámetros de entrada mediante `<nombre>` y reflejar en las columnas de `Examples` los datos que varían por conjunto.

### Reglas compartidas para ambos documentos
- Construir Data I/O desde `test_data` del JSON Excel y completarlo con `buffer_values` del DOCX cuando coincida el nombre. Incluir URLs, credenciales, documentos, ambiente, estados, montos, valores de entrada y outputs verificados; excluir buffers `{B[...]}` y variables técnicas de control.
- Envolver en backticks las referencias `{CP[...]}`. Para credenciales y parámetros con nombre de campo, usar el nombre funcional limpio.
- Mantener la discrepancia de datos de entrada como observación si Excel, buffers o evidencias visuales no coinciden; no resolverla inventando un valor.
- Los pasos detallados del documento normal deben preservar granularidad. La variante BDD resume esas acciones en pasos declarativos de negocio sin omitir la condición ni el resultado verificado.

## 9. Output y entrega
- Guardar físicamente **ambos** `.md` siempre en `./TCs/`, nunca en `./tosca/`.
- Caso normal: `SCACS_<id>_<nombre_normalizado>.md`, usando `tc_template.md`.
- Variante BDD: `BDD_SCACS_<id>_<nombre_normalizado>.md`, usando `bdd_template.md`.
- Actualizar cada archivo si ya existe; no basta con responder el contenido en el chat.
- Lenguaje funcional claro (qué hacer y qué verificar). No generar código, selectores, Page Objects ni estrategias de locator.

## 10. Limpieza post-exportación (obligatorio)
1. Verificar que los dos `.md` finales (normal y BDD) quedaron guardados en `./TCs/` y están basados en sus respectivas plantillas.
2. Eliminar los archivos `*_excel.json` y `*_docx.json` generados en `./exporter_helpers/out/` para el caso procesado y la carpeta `*_docx_images/` asociada, si existe.
3. Confirmar al usuario las rutas de ambos archivos en `TCs`.

## 11. Checklist de calidad
- [ ] Se ejecutaron los helpers de `exporter_helpers` **sin argumentos**.
- [ ] Se usó JSON de Excel como fuente principal.
- [ ] Las imágenes DokuSnapper disponibles se analizaron con una capacidad visual cuando estaba disponible; de lo contrario, se informó al usuario y se continuó con las fuentes textuales.
- [ ] Los detalles visuales incorporados son legibles, pertinentes y están respaldados por las imágenes.
- [ ] Solo se incluyeron pasos ejecutables en navegador.
- [ ] Se excluyeron acciones desktop/SO.
- [ ] Variables relevantes centralizadas en Data I/O en ambos documentos.
- [ ] Se identificó **toda** la test data (URL, usuario, contraseña, documento, ambiente, estados, montos, valores) y los valores faltantes llevan la leyenda `Por favor proveer este valor`.
- [ ] Hay aserciones claras y verificables.
- [ ] No hay recomendaciones técnicas de implementación.
- [ ] **En el caso normal, cada interacción del Excel (click, input, select, verify) tiene su propia fila — no hay pasos genéricos que colapsen múltiples acciones.**
- [ ] **En el caso normal, los elementos de interfaz se nombran tal como aparecen en el Excel.**
- [ ] El caso normal se generó con `exporter_helpers/templates/tc_template.md`.
- [ ] La variante BDD se generó con `exporter_helpers/templates/bdd_template.md`.
- [ ] Ambos `.md` quedaron guardados en `./TCs/` con nombres correlacionados.
- [ ] Se eliminaron los `.json` temporales de `./exporter_helpers/out/`.
- [ ] Se eliminó la carpeta de imágenes temporales del DOCX procesado, si se generó.
- [ ] Se confirmaron en la salida las rutas de ambos archivos creados/actualizados.
