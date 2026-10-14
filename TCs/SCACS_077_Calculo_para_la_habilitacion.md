# Caso 077 - Cálculo para la habilitación

## Objetivo
Validar que una solicitud **preaprobada** en **estado Calificada** con garantías parciales vencidas, sin check, pueda consultarse y revisarse el cálculo de límites vigentes para confirmar que el valor **Habilitado** sea **0,00** en la pantalla correspondiente.

## Alcance
- Incluye únicamente acciones funcionales dentro del navegador web (SCACS).
- Incluye el flujo principal de login, navegación por menú, búsqueda de propuestas, selección de solicitud, validación de resumen y comprobación de límites vigentes.
- Excluye limpieza técnica de browser, comandos de sistema operativo, apps de escritorio y registro en Excel de resultados.

## Precondiciones
- El usuario de SCACS con permisos de consulta/operación está habilitado para acceder al sistema.
- El cliente con documento `{CP[NroDocumento]}` existe y tiene una solicitud en estado **Calificada** con flujo **Solicitud Preaprobada**.
- El entorno objetivo es **Testing** y la aplicación está disponible.
- Los datos de garantía a validar (Descripcion1, Descripcion2, Monto1 y Monto2) se encuentran definidos para la prueba.

## Test Data / Parámetros
| Variable | Descripción | Valor |
|----------|-------------|-------|
| `{CP[UrlScacs]}` | URL del portal/aplicación utilizada durante la prueba. | *Por favor proveer este valor* |
| `{CP[UsuarioSCACS]}` | Usuario de acceso a la aplicación. | *Por favor proveer este valor* |
| `Password` | Contraseña de acceso a la aplicación. | *Por favor proveer este valor* |
| `{CP[NroDocumento]}` | Número de documento del cliente a evaluar. | 20252658794 |
| `Ambiente` | Ambiente/entorno objetivo de la prueba. | Testing |
| `Estado Propuesta_1` | Estado a seleccionar/filtrar en la búsqueda. | Calificada |
| `Flujo_1` | Flujo a seleccionar en el filtro de búsqueda. | Solicitud Preaprobada |
| `Descripcion1` | Descripción a validar durante la prueba. | *Por favor proveer este valor* |
| `Descripcion2` | Descripción a validar durante la prueba. | *Por favor proveer este valor* |
| `Monto1` | Monto a validar durante la prueba. | *Por favor proveer este valor* |
| `Monto2` | Monto a validar durante la prueba. | *Por favor proveer este valor* |

## Pasos (Step-by-step)
1. **Acción:** Abrir la URL de SCACS en el navegador del entorno **Testing**.
   **Resultado esperado:** La pantalla de login de SCACS se carga correctamente.

2. **Acción:** En la pantalla de ingreso, completar "Usuario" con `{CP[UsuarioSCACS]}` y la contraseña correspondiente en "Password".
   **Resultado esperado:** Los campos quedan con los datos del usuario y se habilita el acceso al sistema.

3. **Acción:** Hacer click en "LOGIN".
   **Resultado esperado:** El sistema autentica al usuario y carga la pantalla principal de SCACS.

4. **Acción:** Hacer click en "Menu Hamburguesa".
   **Resultado esperado:** Se despliega el menú lateral de navegación.

5. **Acción:** Hacer click en "Búsqueda de Propuestas" dentro del menú lateral.
   **Resultado esperado:** Se abre la pantalla de búsqueda de propuestas y queda lista para filtrar registros.

6. **Acción:** Hacer click en "Rueda Filtro Propuestas".
   **Resultado esperado:** Se expande el panel de filtros de propuestas.

7. **Acción:** En el filtro de búsqueda, completar "Número Documento" con `{CP[NroDocumento]}`.
   **Resultado esperado:** El campo muestra el documento del cliente a consultar.

8. **Acción:** Hacer click en "Lupa para buscar Cliente".
   **Resultado esperado:** Se abre la búsqueda del cliente asociado al documento.

9. **Acción:** En la búsqueda del cliente, ingresar `{CP[NroDocumento]}` en "Número Documento" y hacer click en "Buscar".
   **Resultado esperado:** La grilla de resultados muestra al cliente correspondiente y queda disponible para seleccionar.

10. **Acción:** Seleccionar la primera fila de la tabla de resultados del cliente.
    **Resultado esperado:** El cliente queda seleccionado y se retorna a la pantalla de búsqueda de propuestas con el registro listo para continuar.

11. **Acción:** En los filtros, seleccionar "Calificada" en "Estado Propuesta" y "Solicitud Preaprobada" en "Flujo"; luego hacer click en "Buscar".
    **Resultado esperado:** La grilla muestra las propuestas del cliente en el estado y flujo solicitados.

12. **Acción:** Seleccionar la primera fila de la tabla "Tabla Propuestas" cuyo estado sea "Calificada".
    **Resultado esperado:** Se abre la propuesta seleccionada y queda visible el detalle de la solicitud.

13. **Acción:** Hacer click en "Resumen".
    **Resultado esperado:** Se carga la vista resumen de la propuesta con los datos y garantías asociados.

14. **Acción:** Revisar los datos de garantía y validar que se correspondan con los valores de Descripcion1, Descripcion2, Monto1 y Monto2 definidos para la prueba.
    **Resultado esperado:** La pantalla refleja la garantía a evaluar y los valores esperados quedan visibles en el resumen.

15. **Acción:** Hacer click en "Consultar".
    **Resultado esperado:** Se abre la pantalla de detalle de la solicitud asociada a la garantía.

16. **Acción:** Si aparece la pantalla "Inicio Solicitud Garantías", entonces hacer click en "Consultar Solicitud".
    **Resultado esperado:** Se ingresa al detalle de la solicitud y la navegación continúa en la pantalla de gestión de garantías.

17. **Acción:** Hacer click en la pestaña "Límites".
    **Resultado esperado:** Se despliega la vista de límites y se habilita la consulta de límites vigentes.

18. **Acción:** Hacer click en "Límites Vigentes".
    **Resultado esperado:** Se abre la tabla de límites vigentes para la solicitud.

19. **Acción:** Validar la fila correspondiente y comprobar el valor de la columna "Habilitado".
    **Resultado esperado:** El sistema muestra el valor **0,00** para la solicitud analizada, indicando que no hay saldo habilitado.

## Validaciones clave (assertions)
- La pantalla de login de SCACS se carga correctamente para el usuario indicado.
- La búsqueda de propuestas con documento `{CP[NroDocumento]}` devuelve resultados válidos para el cliente.
- La propuesta seleccionada corresponde a **Estado Propuesta = Calificada** y **Flujo = Solicitud Preaprobada**.
- El resumen de la propuesta refleja los datos esperados de garantía y montos definidos por la prueba.
- La pantalla de límites vigentes queda visible y el valor **Habilitado** es **0,00**.

## Observaciones generales
- La navegación se realiza por menú lateral, filtros, tablas y detales de propuesta; no se requieren pasos técnicos de escritorio ni limpieza del browser.
- Se debe respetar la espera de carga de pantallas y tablas, especialmente al abrir filtros, ejecutar búsquedas y mostrar la grilla de límites vigentes.
- La validación de `Habilitado` es la aserción central del caso; cualquier valor distinto de **0,00** debe considerarse un fallo del caso.
- La rama condicional del paso 16 queda habilitada solo si la pantalla "Inicio Solicitud Garantías" aparece como resultado intermedio de la navegación.

## Postcondiciones / Limpieza
- La solicitud queda revisada en pantalla y la validación de límites vigentes se encuentra concluida.
- El estado final del caso queda en **verificado** cuando el valor de **Habilitado** coincide con **0,00**.
- No se ejecutan acciones de sistema operativo ni cierre forzado del browser como parte del caso.
