# BDD-[ID]: [Título funcional del Feature / Escenario]

<!-- REEMPLAZAR:
  - [ID]     : número o código del caso (ej. 077, BDD-01)
  - [Título] : descripción funcional corta (ej. "Verificar límite no habilitado con garantías vencidas")
  NOTA: Keywords de Gherkin siempre en inglés (Feature, Given, When, Then, And...).
        El contenido de los pasos puede estar en español o inglés según BDD_LANG.
-->

## Propósito

<!-- REEMPLAZAR: Una oración que exprese la regla de negocio o comportamiento que se verifica.
     Usar negritas para resaltar estados, campos y valores clave.
     Ejemplo: Verificar que las garantías parciales vencidas sin check **no habilitan** límite de crédito. -->

[Descripción del propósito: qué comportamiento/regla de negocio se verifica.]

## Descripción

<!-- REEMPLAZAR: Párrafo que describe la regla de negocio y el contexto del escenario BDD desde
     la perspectiva del usuario / negocio. Sin tecnicismos de automatización. -->

[Descripción narrativa del comportamiento a validar: contexto, actor, acción y resultado esperado.]

## Data I/O

<!-- REEMPLAZAR: Listar TODOS los datos que la especificación BDD consume (Input / parámetros
     de los steps y Examples) y verifica (Output / assertions en los Then).
     - Tipo   : "Input" para datos de entrada, "Output" para valores verificados.
     - Campo  : nombre técnico/funcional (sin llaves, en camelCase).
     - Descripción: explicación legible del dato.
     - Valor: completar con el valor correspondiente o dejar la leyenda indicada.
     Los parámetros de Scenario Outline se reflejan aquí como Input. -->

| Tipo   | Campo             | Descripción                                              | Valor                             |
|--------|-------------------|----------------------------------------------------------|-----------------------------------|
| Input  | url               | URL de acceso a la aplicación                            | *Por favor proveer este valor*    |
| Input  | usuario           | Credencial de usuario para login                         | *Por favor proveer este valor*    |
| Input  | password          | Credencial de contraseña para login                      | *Por favor proveer este valor*    |
| Input  | [campoInput1]     | [Descripción del dato de entrada 1]                      | *Por favor proveer este valor*    |
| Input  | [campoInput2]     | [Descripción del dato de entrada 2]                      | *Por favor proveer este valor*    |
| Output | [campoOutput1]    | [Valor o estado que se verifica en el Then]              | *Por favor proveer este valor*    |
| Output | resultado         | Estado de la prueba: Pass / Fail                         | *Por favor proveer este valor*    |

---

## Precondiciones

<!-- OBLIGATORIO — INDEPENDENCIA Y COMPLETITUD DEL ESCENARIO.
     TODO escenario DEBE ser ejecutable de forma independiente.
     El Background de Gherkin SIEMPRE empieza con: URL base + sesión/storage limpio.
     Listar aquí, como checklist verificable antes de ejecutar:
     1. Estado inicial del entorno (qué debe existir / qué debe estar limpio).
     2. Datos de prueba concretos disponibles (IDs, códigos, credenciales).
     3. Autenticación necesaria (o "no requiere autenticación").
     4. Cualquier recurso o configuración previa requerida.
     PROHIBIDO: referenciar otros escenarios ("como en BDD-XXX") o estado asumido. -->

- [ ] [Estado limpio del navegador / storage — ej. "sin sesión activa, sin cookies del sitio"]
- [ ] [Datos de prueba concretos — ej. "cliente con nroDocumento 12345678 en estado Calificada"]
- [ ] [Autenticación requerida — ej. "credenciales en Data I/O"] o [No requiere autenticación]
- [ ] [Recursos / configuración previa adicionales, si aplica]

---

## Especificación Gherkin

INSTRUCCIONES:
     - Keywords SIEMPRE en inglés: Feature, Background, Scenario, Scenario Outline,
       Examples, Given, When, Then, And, But.
     - Contenido (texto de pasos, tablas, títulos) en el idioma definido por BDD_LANG.
     - Background SIEMPRE: navegar a URL base + limpiar sesión/storage.
     - Escenarios declarativos: perspectiva de negocio, sin detalles de implementación técnica.
     - Tags obligatorios: @BDD-[ID] @[Modulo] y al menos uno de @Smoke / @Regression / @E2E.
     - Usar SIEMPRE Scenario Outline + Examples, incluso para un único conjunto de datos.
       Con un único conjunto, Examples debe contener una sola fila de datos; con varios,
       debe contener una fila por combinación.
     - Incluir en Examples todos los parámetros de entrada referenciados por el escenario
       con el formato "<nombre>". No crear filas ficticias ni inventar valores faltantes:
       conservar "Por favor proveer este valor" donde el dato no esté disponible.
     - Pasos condicionales: usar "And if [condición], [acción]" o expresar como step separado.
     - Los parámetros de Examples se referencian con "<nombre>" dentro de los pasos.

```gherkin
@BDD-[ID] @[Modulo/Funcionalidad] @[Smoke|Regression|E2E]
Feature: [Nombre descriptivo de la funcionalidad bajo prueba]
  As a [Rol de usuario / actor del negocio]
  I want to [Acción o funcionalidad que se ejecuta]
  So that [Beneficio o resultado de negocio esperado]

  Background:
    Given the user navigates to the base URL "<url>"
    And the browser session and storage are clean

  @TC-[ID] @[Smoke|Regression]
  Scenario Outline: [Nombre descriptivo del escenario]
    Given [Precondición de negocio con "<campoInput1>"]
    When [Acción principal con "<campoInput2>"]
    Then [Resultado esperado sobre "<campoOutput1>"]

    Examples:
      | url | campoInput1 | campoInput2 | campoOutput1 |
      | [Por favor proveer este valor] | [Valor 1] | [Valor 2] | [Resultado] |
```


---

## Resultado Esperado

<!-- Tabla de verificaciones críticas definidas en los pasos Then. Máx 2-3 filas.
     - Verificación: qué se comprueba (extraído del Then).
     - Valor esperado: valor, estado o condición que debe cumplirse. -->

| Verificación                              | Valor esperado      |
|:------------------------------------------|:--------------------|
| [Campo o condición verificada]            | [Valor — ej. 0,00]  |
| [Campo o condición verificada 2]          | [Valor esperado 2]  |

---

## Observaciones generales

<!-- OPCIONAL. Incluir si hay:
     - Steps condicionales que pueden o no ejecutarse según el estado de datos.
     - Tiempos de espera relevantes para la automatización (explicit wait steps).
     - Ramas del flujo que dependen del estado del entorno.
     - Sugerencias de reutilización de Step Definitions para el equipo de automatización.
     - Comportamientos variables por entorno (QA vs Staging). -->

- [Observación 1: ej. "El step 'And if the popup appears, close it' es condicional."]
- [Observación 2: ej. "Reutilizar el step 'the user is logged in' del shared steps catalog."]

## Postcondiciones / Limpieza

<!-- OBLIGATORIO. Estado final esperado del entorno tras la ejecución.
     Incluir acciones concretas de restauración para que el siguiente escenario
     parta de un estado limpio.
     Incluir SOLO acciones funcionales (no cierre forzado de procesos ni SO). -->

- [Postcondición 1: ej. "Cerrar sesión del usuario (logout)."]
- [Postcondición 2: ej. "Limpiar localStorage / cookies del sitio."]

---

## Flujo BDD

<!-- REEMPLAZAR: Diagrama ASCII que muestra la secuencia Given → When → Then de punta a punta.
     - Usar sangría con → para indicar el avance de cada bloque.
     - Usar [Condicional: ...] para pasos opcionales.
     - La secuencia SIEMPRE inicia en Background (URL base + estado limpio)
       y termina en la limpieza.
     Ejemplo de formato:

     Background (Given: URL base + sesión limpia)
       → Given: [Precondición de negocio]
         → When: [Acción principal]
           → [Condicional: paso opcional]
             → Then: [Verificación del comportamiento]
               → Limpieza / Postcondiciones
-->

[Background — URL base + sesión limpia]
  → [Given: Precondición de negocio / autenticación]
    → [Given: Estado inicial adicional]
      → [When: Acción o evento principal]
        → [When: Filtros / sub-acciones]
          → [Condicional: paso opcional]
            → [Then: Verificación del resultado esperado]
              → Verificar: [campoOutput1] == [valor esperado]
                → Limpieza / Postcondiciones
