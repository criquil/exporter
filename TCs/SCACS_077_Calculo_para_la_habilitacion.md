# TC-077: Verificar garantías parciales vencidas sin check

## Propósito

Verificar que la solicitud preaprobada calificada del cliente no habilita límite de crédito: el valor de **Habilitado** en la última fila de **LÍMITES VIGENTES** debe ser **0,00**.

## Descripción

El caso abre SCACS en una sesión limpia, inicia sesión y navega a **Búsqueda de Propuestas**. Busca al cliente por documento, filtra las propuestas por flujo **Solicitud Preaprobada** y estado **Calificada**, abre el resumen y consulta la solicitud. Si aparece la pantalla **Inicio Solicitud Garantías**, continúa mediante **CONSULTAR SOLICITUD**. Finalmente abre las pestañas **Límites** y **LÍMITES VIGENTES** y comprueba que **Habilitado** en la última fila sea **0,00**.

## Data I/O

| Tipo | Campo | Descripción | Valor |
|------|-------|-------------|-------|
| Input | UrlScacs | URL base de SCACS | *Por favor proveer este valor* |
| Input | UsuarioSCACS | Usuario de acceso a la aplicación | *Por favor proveer este valor* |
| Input | Password | Contraseña de acceso a la aplicación | *Por favor proveer este valor* |
| Input | NroDocumento | Número de documento del cliente | `20252658794` (buffer DOCX; ver discrepancia en Observaciones) |
| Input | Ambiente | Ambiente/entorno objetivo de la prueba | Testing |
| Input | Flujo_1 | Flujo a seleccionar en el filtro | Solicitud Preaprobada |
| Input | Estado Propuesta_1 | Estado a seleccionar en el filtro | Calificada |
| Input | Descripcion1 | Descripción de la garantía 1 a validar; el origen indica que se declara por CP | *Por favor proveer este valor* |
| Input | Descripcion2 | Descripción de la garantía 2 a validar; el origen indica que se declara por CP | *Por favor proveer este valor* |
| Input | Monto1 | Monto asociado a la garantía 1; el origen indica que se declara por CP | *Por favor proveer este valor* |
| Input | Monto2 | Monto asociado a la garantía 2; el origen indica que se declara por CP | *Por favor proveer este valor* |
| Output | Habilitado | Valor verificado en la última fila de LÍMITES VIGENTES | 0,00 |
| Output | resultado | Estado de la prueba: Pass / Fail | *Por favor proveer este valor* |

---

## Precondiciones

- [ ] Iniciar en una sesión de navegador limpia, sin una sesión previa de SCACS.
- [ ] Tener acceso a la URL de SCACS y credenciales válidas en Data I/O.
- [ ] Tener disponible el cliente correspondiente al parámetro `NroDocumento` y una solicitud **Solicitud Preaprobada** en estado **Calificada**.
- [ ] Confirmar el número de documento que se usará: los archivos fuente presentan valores distintos (ver Observaciones).
- [ ] No se requiere modificar la solicitud; la consulta del caso es de solo lectura.

---

## Steps

### 1. Preparación

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 1.1 | Navegar a `{CP[UrlScacs]}` | Se muestra la página de inicio de sesión de SCACS |
| 1.2 | Verificar que no haya una sesión anterior activa | Se muestra la pantalla **SCACS - Login** |

---

### 2. Iniciar sesión

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 2.1 | Ingresar `{CP[UsuarioSCACS]}` en `Usuario` | El campo Usuario queda completado |
| 2.2 | Esperar 5 segundos | La pantalla de login queda lista para continuar |
| 2.3 | Ingresar la contraseña provista en `Password` | El campo Password queda completado |
| 2.4 | Hacer click en `LOGIN` | SCACS acepta el acceso y muestra la página principal |
| 2.5 | Esperar 8 segundos | La página principal termina de cargar |

---

### 3. Abrir Búsqueda de Propuestas

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 3.1 | Hacer click en `Menu Hamburguesa` | Se despliega el menú de navegación |
| 3.2 | Esperar 7,5 segundos | El menú queda disponible |
| 3.3 | Hacer click en `Búsqueda de Propuestas` | Se abre la pantalla de búsqueda |
| 3.4 | Esperar 3 segundos | La pantalla termina de cargar |

---

### 4. Abrir el filtro de propuestas

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 4.1 | Hacer click en `Rueda Filtro Propuestas` | Se despliega el panel Filtro Propuestas |
| 4.2 | Esperar 2 segundos | El panel queda disponible |

---

### 5. Buscar el cliente por documento

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 5.1 | Hacer click en `Lupa para buscar Cliente` | Se abre el modal **Selección de Cliente** |
| 5.2 | Ingresar `{CP[NroDocumento]}` en `Número Documento` | El campo Número Documento queda completado |
| 5.3 | Esperar 2 segundos | El dato ingresado queda listo para buscar |
| 5.4 | Hacer click en `Buscar` del modal | Se muestran los resultados de clientes |
| 5.5 | Esperar 15 segundos | La búsqueda de clientes termina |
| 5.6 | Seleccionar la primera fila de la tabla de resultados | El cliente queda seleccionado |
| 5.7 | Esperar 10 segundos | Se actualiza el filtro con el cliente seleccionado |
| 5.8 | Esperar 2 segundos | El filtro queda listo para continuar |

---

### 6. Filtrar por flujo

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 6.1 | En `Flujo_1`, seleccionar `Solicitud Preaprobada` | Queda seleccionado el flujo Solicitud Preaprobada |
| 6.2 | Hacer click en `Buscar` | Se muestran las propuestas que cumplen el filtro |
| 6.3 | Esperar 5 segundos | La tabla de propuestas termina de actualizarse |

---

### 7. Filtrar por estado

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 7.1 | En `Estado Propuesta_1`, seleccionar `Calificada` | Queda seleccionado el estado Calificada |
| 7.2 | Hacer click en `Buscar` | Se muestran las propuestas calificadas |
| 7.3 | Esperar 2 segundos | La tabla de propuestas termina de actualizarse |

---

### 8. Abrir la solicitud calificada

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 8.1 | Verificar que la fila seleccionada tenga `Estado` igual a `Calificada` | La fila corresponde a una solicitud calificada |
| 8.2 | Hacer click en `Estado` de esa fila | Se abre la solicitud calificada |

---

### 9. Abrir el resumen de la propuesta

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 9.1 | Hacer click en `Resumen` | Se muestra el Resumen de Propuesta |
| 9.2 | Esperar 3 segundos | El resumen termina de cargar |

---

### 10. Consultar la solicitud

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 10.1 | Hacer click en `Consultar` | Se abre la consulta de la solicitud |
| 10.2 | Esperar 3 segundos | La pantalla de consulta termina de cargar |
| 10.3 | *(Condicional)* Si aparece `Inicio Solicitud Garantías`, hacer click en `CONSULTAR SOLICITUD` | Se muestra la solicitud para continuar |
| 10.4 | *(Condicional)* Si se ejecutó 10.3, esperar 2 segundos | La solicitud termina de cargar |

---

### 11. Abrir la pestaña Límites

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 11.1 | Hacer click en la pestaña `Límites` | Se muestra la sección Límites |
| 11.2 | Esperar 2 segundos | La sección termina de cargar |

---

### 12. Verificar el límite habilitado

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 12.1 | Hacer click en `LÍMITES VIGENTES` | Se muestra la tabla de límites vigentes |
| 12.2 | Esperar 3 segundos | La tabla termina de cargar |
| 12.3 | Seleccionar la última fila de `Tabla con Limites` | Queda seleccionada la última fila |
| 12.4 | Verificar `Habilitado` en la última fila | El valor es **0,00** |

---

## Resultado Esperado

| Verificación | Valor esperado |
|:-------------|:---------------|
| `Habilitado` en la última fila de LÍMITES VIGENTES | 0,00 |
| Resultado de la prueba | Pass si la verificación coincide; en caso contrario, Fail |

---

## Observaciones generales

- La búsqueda contiene una discrepancia de datos: el Excel usa `{CP[NroDocumento]}` sin valor; el buffer del DOCX aporta `20252658794`, mientras que el texto y las capturas de DokuSnapper muestran `44145555`. Se conserva el valor del buffer como referencia y debe confirmarse el número correcto antes de ejecutar; no se deben tratar ambos valores como equivalentes.
- La captura de login muestra el usuario `2225`, pero el Excel define `{CP[UsuarioSCACS]}` sin valor. Se mantiene la leyenda de dato faltante en Data I/O y no se toma la captura como sustituto de la parametrización.
- Los waits de 2, 3, 5, 7,5, 8, 10 y 15 segundos reflejan las esperas del flujo Tosca tras las acciones correspondientes.
- La ruta condicional `Inicio Solicitud Garantías` solo se sigue cuando aparece esa pantalla.
- Se revisaron evidencias visuales DokuSnapper de login, filtros, selección del cliente, resumen y límites. Las capturas respaldan la pantalla de consulta y el valor verificado; no se incorporan acciones de limpieza de escritorio ni manejo de ventanas del sistema operativo.

## Postcondiciones / Limpieza

- La consulta no debe modificar la solicitud ni los límites.
- Si el entorno requiere cerrar la sesión, usar la opción funcional `Salir` del menú de SCACS.

---

## Flujo

Preparación (URL base + sesión limpia)
  → Iniciar sesión
    → Menu Hamburguesa → Búsqueda de Propuestas
      → Filtro Propuestas → buscar cliente por documento
        → Seleccionar primera fila del cliente
          → Filtrar Flujo: Solicitud Preaprobada
            → Filtrar Estado: Calificada
              → Abrir solicitud → Resumen → Consultar
                → [Condicional: Inicio Solicitud Garantías → CONSULTAR SOLICITUD]
                  → Pestaña Límites → LÍMITES VIGENTES
                    → Verificar: Habilitado en última fila == 0,00
                      → Limpieza / Postcondiciones
