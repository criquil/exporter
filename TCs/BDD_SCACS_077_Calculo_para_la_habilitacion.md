# BDD-077: Verificar garantías parciales vencidas sin check

## Propósito

Comprobar que la consulta de la solicitud preaprobada calificada no presenta un monto habilitado distinto de **0,00** en la última fila de límites vigentes.

## Descripción

Una persona usuaria de SCACS localiza al cliente por número de documento, consulta su solicitud **Solicitud Preaprobada** en estado **Calificada** y revisa los límites vigentes. El resultado esperado es que el valor **Habilitado** de la última fila sea **0,00**. La consulta es de solo lectura.

## Data I/O

| Tipo | Campo | Descripción | Valor |
|------|-------|-------------|-------|
| Input | UrlScacs | URL base de SCACS | *Por favor proveer este valor* |
| Input | UsuarioSCACS | Usuario de acceso a la aplicación | *Por favor proveer este valor* |
| Input | Password | Contraseña de acceso a la aplicación | *Por favor proveer este valor* |
| Input | NroDocumento | Número de documento del cliente | `20252658794` (buffer DOCX; ver discrepancia en Observaciones) |
| Input | Ambiente | Ambiente/entorno objetivo de la prueba | Testing |
| Input | Flujo_1 | Flujo a seleccionar en la búsqueda | Solicitud Preaprobada |
| Input | Estado Propuesta_1 | Estado a seleccionar en la búsqueda | Calificada |
| Input | Descripcion1 | Descripción de la garantía 1 a validar; el origen indica que se declara por CP | *Por favor proveer este valor* |
| Input | Descripcion2 | Descripción de la garantía 2 a validar; el origen indica que se declara por CP | *Por favor proveer este valor* |
| Input | Monto1 | Monto asociado a la garantía 1; el origen indica que se declara por CP | *Por favor proveer este valor* |
| Input | Monto2 | Monto asociado a la garantía 2; el origen indica que se declara por CP | *Por favor proveer este valor* |
| Output | Habilitado | Valor verificado en la última fila de LÍMITES VIGENTES | 0,00 |
| Output | resultado | Estado de la prueba: Pass / Fail | *Por favor proveer este valor* |

---

## Precondiciones

- [ ] Sesión de navegador limpia, sin autenticación previa en SCACS.
- [ ] URL de SCACS y credenciales válidas disponibles en Data I/O.
- [ ] Cliente correspondiente al parámetro `NroDocumento` con una solicitud **Solicitud Preaprobada** en estado **Calificada**.
- [ ] Número de documento confirmado antes de ejecutar, debido a la discrepancia indicada en Observaciones.
- [ ] La consulta no necesita modificar la solicitud ni sus límites.

---

## Especificación Gherkin

```gherkin
@BDD-077 @SCACS @E2E
Feature: Verificar límites vigentes de una solicitud preaprobada calificada
  As a usuario de SCACS
  I want to consultar los límites vigentes de una solicitud calificada
  So that pueda verificar que el monto habilitado sea cero

  Background:
    Given the user opens the SCACS base URL "{CP[UrlScacs]}"
    And the browser session is clean and there is no active SCACS session

  @TC-077 @Regression
  Scenario Outline: El límite habilitado de la solicitud calificada es cero
    Given the user has valid SCACS credentials for "<usuario>" and "<password>"
    And there is a client identified by "<nroDocumento>" with a "<flujo>" in "<estado>" status
    When the user signs in and opens "Búsqueda de Propuestas"
    And the user searches for the client and filters proposals by "<flujo>" and "<estado>"
    And the user opens the qualified proposal summary and consults the request
    And if "Inicio Solicitud Garantías" appears, the user continues with "CONSULTAR SOLICITUD"
    And the user opens "Límites" and "LÍMITES VIGENTES"
    Then "Habilitado" in the last row equals "<habilitadoEsperado>"
    And the test result is recorded as Pass when the value matches, otherwise Fail

    Examples:
      | url                              | usuario                        | password                       | nroDocumento | flujo                 | estado     | habilitadoEsperado |
      | *Por favor proveer este valor*   | *Por favor proveer este valor*  | *Por favor proveer este valor* | 20252658794  | Solicitud Preaprobada | Calificada | 0,00               |
```

---

## Resultado Esperado

| Verificación | Valor esperado |
|:-------------|:---------------|
| `Habilitado` en la última fila de LÍMITES VIGENTES | 0,00 |
| Resultado de la prueba | Pass si la verificación coincide; en caso contrario, Fail |

---

## Observaciones generales

- El número de documento no es consistente entre las fuentes: el Excel solo referencia `{CP[NroDocumento]}`, el buffer del DOCX indica `20252658794` y el texto/capturas de la ejecución muestran `44145555`. Debe confirmarse el dato antes de ejecutar; no se resuelve la discrepancia por inferencia.
- La captura de login muestra `2225`, pero el Excel parametriza el usuario como `{CP[UsuarioSCACS]}` sin informar un valor. Se conserva la leyenda de dato faltante.
- La condición de `Inicio Solicitud Garantías` es opcional; se continúa desde esa pantalla solo si aparece.
- La evidencia visual revisada confirma el flujo de búsqueda y la pantalla de límites con **Habilitado = 0,00**. Las acciones de desktop/SO presentes en la ejecución no forman parte del escenario funcional.

## Postcondiciones / Limpieza

- La consulta es de solo lectura y no modifica la solicitud ni los límites.
- Si el entorno requiere finalizar la sesión, usar `Salir` desde el menú de SCACS.

---

## Flujo BDD

Background (Given: URL base + sesión limpia)
  → Given: credenciales válidas y cliente con solicitud preaprobada calificada
    → When: buscar cliente por documento
      → When: filtrar por flujo Solicitud Preaprobada y estado Calificada
        → When: consultar la solicitud
          → [Condicional: si aparece Inicio Solicitud Garantías, continuar con CONSULTAR SOLICITUD]
            → When: abrir Límites y LÍMITES VIGENTES
              → Then: verificar Habilitado en la última fila == 0,00
                → Registrar Pass / Fail
                  → Limpieza / Postcondiciones
