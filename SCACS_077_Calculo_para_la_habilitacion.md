# Caso 077 - Calculo para la habilitacion > Verificar garantias parciales vencidas sin check

## Objetivo
Verificar que, al buscar una solicitud preaprobada en SCACS con estado **Calificada** y navegar hasta la pestaña de **Límites Vigentes**, la columna **Habilitado** muestra **0,00**, confirmando que no existen garantías parciales activas sin marcar.

## Alcance
- Incluye el login en SCACS, la navegación hacia **Búsqueda de Propuestas**, el filtrado por documento/flujo/estado y la consulta de la solicitud.
- Incluye la apertura de la vista de **Resumen**, la acción **Consultar Solicitud** y la verificación del valor `Habilitado` en **Límites Vigentes**.
- Excluye la limpieza técnica de navegadores, comandos de sistema operativo y la escritura de resultados en Excel.

## Precondiciones
- La URL `{CP[UrlScacs]}` apunta al entorno de Testing y la cuenta `{CP[UsuarioSCACS]}` tiene permisos para ingresar al portal.
- No hay ventanas de Chrome/Edge abiertas ni popups de descargas pendientes (`Guardar Como`, `downloadTramite`, etc.) que impidan la apertura del login.

## Test Data / Parámetros
| Variable | Descripción | Valor |
|----------|-------------|-------|
| `{CP[UsuarioSCACS]}` | Usuario válido para acceder a SCACS en el entorno de Testing. | (vacío) |
| `{CP[NroDocumento]}` | Número de documento del cliente cuya solicitud se evaluará. | (vacío) |

## Pasos (Step-by-step)
1. **Acción:** Navegar a `{CP[UrlScacs]}` en Chrome, maximizar la ventana y cerrar el modal `Restore pages?` si aparece para llegar a la pantalla `Login`.
   **Resultado esperado:** Se presenta la pantalla `Login` de SCACS con los campos `Usuario`, `Password` y el botón `LOGIN`.
2. **Acción:** Completar el campo `Usuario` con `{CP[UsuarioSCACS]}` y llenar el campo `Password` con la contraseña segura.
   **Resultado esperado:** Ambos campos quedan rellenados y el botón `LOGIN` está habilitado.
3. **Acción:** Hacer click en `LOGIN`.
   **Resultado esperado:** El portal carga la página principal y aparece el icono `Menu Hamburguesa` en el margen superior izquierdo.
4. **Acción:** Hacer click en `Menu Hamburguesa`.
   **Resultado esperado:** Se despliega el menú lateral donde figuran opciones como `Agenda de Propuestas` y `Búsqueda de Propuestas`.
5. **Acción:** Seleccionar `Búsqueda de Propuestas` en el menú.
   **Resultado esperado:** Se abre la pantalla de búsqueda con el listado, la tabla vacía y el botón `Rueda Filtro Propuestas` visible.
6. **Acción:** Hacer click en `Rueda Filtro Propuestas`.
   **Resultado esperado:** Aparece el panel de filtros que incluye la acción `Lupa para buscar Cliente` y campos como `Tipo Documento`.
7. **Acción:** Hacer click en `Lupa para buscar Cliente`, ingresar `{CP[NroDocumento]}` en `Número Documento` y hacer click en `Buscar`.
   **Resultado esperado:** La ventana de búsqueda muestra resultados con el botón `CERRAR` activo.
8. **Acción:** Seleccionar la primera fila (`$1`) de la grilla de resultados.
   **Resultado esperado:** La ventana se cierra y el cliente seleccionado queda cargado en el panel principal.
9. **Acción:** En el panel principal, establecer `Flujo_1` en `Solicitud Preaprobada` y hacer click en `Buscar`.
   **Resultado esperado:** La grilla se refresca mostrando exclusivamente solicitudes con ese flujo.
10. **Acción:** Establecer `Estado Propuesta_1` en `Calificada` y hacer click en `Buscar`.
    **Resultado esperado:** La tabla contiene únicamente filas cuyo `Estado` es `Calificada`.
11. **Acción:** En la grilla de propuestas, seleccionar la fila cuyo `Estado` contiene `Calificada` y pulsar el botón `Resumen`.
    **Resultado esperado:** Se abre la vista `Resumen` de la propuesta seleccionada.
12. **Acción:** En `Resumen de Propuesta`, hacer click en `Consultar`.
    **Resultado esperado:** Se despliega la pantalla `Inicio Solicitud Garantías` y aparece el botón `CONSULTAR SOLICITUD`.
13. **Acción:** Confirmar que `CONSULTAR SOLICITUD` está disponible y hacer click en él.
    **Resultado esperado:** Se carga la pantalla de la solicitud con pestañas como `Datos Generales`, `Checklist` y `Límites`.
14. **Acción:** Hacer click en la pestaña `Límites`.
    **Resultado esperado:** Se muestra la sección con el botón `LÍMITES VIGENTES`.
15. **Acción:** Hacer click en `LÍMITES VIGENTES`.
    **Resultado esperado:** Se abre el panel `Límites del Cliente - Límites Vigentes` con la tabla correspondiente.
16. **Acción:** Seleccionar la última fila de la tabla (`$last`) y revisar la columna `Habilitado`.
    **Resultado esperado:** El renglón seleccionado presenta `Habilitado` igual a **0,00**, confirmando que no hay límites habilitados.

## Validaciones clave
- La fila seleccionada en la grilla de propuestas muestra `Estado` igual a `Calificada` antes de ir a `Resumen`.
- El botón `CONSULTAR SOLICITUD` está presente en la pantalla `Inicio Solicitud Garantías` y permite abrir la solicitud.
- En `Límites del Cliente - Límites Vigentes`, la columna `Habilitado` del último registro es **0,00**.

## Observaciones generales
- Durante el inicio pueden aparecer popups de descarga (`Guardar Como`, `downloadTramite`, `Download is in progress`); cerrarlos antes de proceder para que el login y la búsqueda no se vean bloqueados.
- Las esperas (`TBox Wait`) que siguen a cada búsqueda o selección deben respetarse (8-15 segundos) para asegurar que la tabla se recarga antes de la siguiente interacción.

## Postcondiciones / Limpieza
- La sesión puede permanecer abierta para nuevas ejecuciones, pero cerrar Chrome/Edge y cualquier popup generado antes de finalizar la jornada.
- No se realizan modificaciones al estado de la propuesta; sólo se consultan datos de límites sensibles.
