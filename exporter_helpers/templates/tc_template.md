# TC-[ID]: [Título funcional del caso de prueba]

<!-- REEMPLAZAR:
  - [ID]     : número o código del caso (ej. 077, TC-01)
  - [Título] : descripción funcional corta (ej. "Verificar límite habilitado al calificar solicitud")
-->

## Propósito

<!-- REEMPLAZAR: Una oración que exprese el objetivo de verificación del caso.
     Usar negritas para resaltar estados, campos y valores clave.
     Ejemplo: Verificar que las garantías parciales vencidas sin check **no habilitan** límite de crédito. -->

[Descripción del propósito del caso de prueba.]

## Descripción

<!-- REEMPLAZAR: Párrafo que describe el flujo de punta a punta: punto de entrada, navegación principal,
     acciones clave y la verificación final. Sin tecnicismos de automatización. -->

[Descripción narrativa del flujo completo del caso: desde dónde inicia, qué navega, qué filtra, qué valida.]

## Data I/O

<!-- REEMPLAZAR: Listar TODOS los datos que el caso consume (Input) y produce/verifica (Output).
     - Tipo: "Input" para datos que se ingresan, "Output" para valores que se verifican.
     - Campo: nombre técnico/funcional del parámetro (sin llaves, en camelCase).
     - Descripción: explicación legible del dato.
     - Valor: completar con el valor correspondiente o dejar la leyenda indicada.
     Excluir variables internas {B[...]} y técnicas de control. -->

| Tipo   | Campo             | Descripción                                              | Valor                             |
|--------|-------------------|----------------------------------------------------------|-----------------------------------|
| Input  | url               | URL de acceso a la aplicación                            | *Por favor proveer este valor*    |
| Input  | usuario           | Credencial de usuario para login                         | *Por favor proveer este valor*    |
| Input  | password          | Credencial de contraseña para login                      | *Por favor proveer este valor*    |
| Input  | [campoInput1]     | [Descripción del dato de entrada 1]                      | *Por favor proveer este valor*    |
| Input  | [campoInput2]     | [Descripción del dato de entrada 2]                      | *Por favor proveer este valor*    |
| Output | [campoOutput1]    | [Valor o estado que se verifica al final del caso]       | *Por favor proveer este valor*    |
| Output | resultado         | Estado de la prueba: Pass / Fail                         | *Por favor proveer este valor*    |

---

## Precondiciones

<!-- OBLIGATORIO — INDEPENDENCIA Y COMPLETITUD DEL CASO.
     TODO caso DEBE ser ejecutable de forma independiente, de inicio a fin, sin depender
     de la ejecución previa de otros casos ni de estado dejado por ejecuciones anteriores.
     Listar aquí, como checklist verificable:
     1. Estado inicial del entorno de datos (qué debe existir / qué debe estar limpio).
     2. Datos de prueba concretos disponibles (IDs, códigos, credenciales).
     3. Autenticación necesaria (o "no requiere autenticación").
     4. Cualquier recurso o configuración previa requerida por el caso.
     PROHIBIDO: referenciar ejecución de otros casos ("como en TC-XXX") o estado asumido
     ("con el basket ya preparado") sin que el propio caso lo establezca. -->

- [ ] [Estado limpio del navegador / storage requerido — ej. "sin sesión activa, basket vacío"]
- [ ] [Datos de prueba concretos — ej. "cliente con nroDocumento 12345678 en estado Calificada"]
- [ ] [Autenticación requerida — ej. "login con usuario demo (ver Data I/O)"] o [No requiere autenticación]
- [ ] [Recursos/configuración previa adicionales, si aplica]

---

## Steps

<!-- INSTRUCCIONES GENERALES PARA PASOS:
     FORMATO: cada sección tiene UNA tabla de 3 columnas: # | Acción | Resultado esperado
     - Columna #: número de sub-paso (ej. 1.1, 1.2). Alineado a la derecha.
     - Columna Acción: qué hace el usuario. Incluir inline el elemento UI y el valor ({CP[...]}).
       Max ~55 chars por línea; el texto hace wrap automático en la celda.
     - Columna Resultado esperado: qué se observa tras la acción. Conciso y verificable.
     - Pasos condicionales: prefijo *(Condicional)* en la celda Acción.
     - NO usar tablas de 5-6 columnas. NO repetir información ya en Data I/O.
     - Nombrar los elementos de UI tal como aparecen en el sistema (ej. "Menu Hamburguesa").
     - El documento debe leerse sin scroll horizontal en 1366×768.

     COMPLETITUD OBLIGATORIA:
     - La fase 1 SIEMPRE es "Preparación": navegar a la URL base del sistema y asegurar
       el estado limpio declarado en ## Precondiciones (limpiar storage/sesión, verificar
       contadores en cero). El caso NUNCA arranca "a mitad de flujo".
     - Cada fase debe incluir TODOS los pasos necesarios para que un tester, sin conocimiento
       de otros casos, pueda ejecutarlo de inicio a fin (crear/preparar los datos que consume).
     - PROHIBIDO: pasos como "con items en el basket" o "con la orden del caso anterior"
       sin que el propio caso los cree. -->

### 1. Preparación

<!-- SIEMPRE presente. Navegación a la URL base + limpieza del estado previo. -->

| #   | Acción                                                   | Resultado esperado                                  |
|----:|:---------------------------------------------------------|:----------------------------------------------------|
| 1.1 | Navegar a `{CP[url]}`                                    | Página principal cargada                            |
| 1.2 | Limpiar estado previo: storage/sesión/cookies            | Estado limpio: sin datos de ejecuciones anteriores  |
| 1.3 | Verificar estado limpio (contadores, sesión, listas)     | Valores iniciales en cero / estado por defecto      |

---

### 2. [Nombre de la fase — ej. Login]

<!-- Copiar este bloque para cada fase adicional. -->

| #   | Acción                                                   | Resultado esperado                                  |
|----:|:---------------------------------------------------------|:----------------------------------------------------|
| 2.1 | [Acción]                                                 | [Resultado]                                         |
| 2.2 | [Acción]                                                 | [Resultado]                                         |

---

### N. [Fase de validación final]

| #   | Acción                                                   | Resultado esperado                                  |
|----:|:---------------------------------------------------------|:----------------------------------------------------|
| N.1 | [Verificar campo / condición]                            | [Valor esperado — ej. `Habilitado` == **0,00**]     |

---

## Resultado Esperado

<!-- REEMPLAZAR: Tabla de verificaciones críticas. Máx 2-3 filas.
     - Verificación: qué se comprueba.
     - Valor esperado: valor, estado o condición que debe cumplirse. -->

| Verificación                              | Valor esperado      |
|:------------------------------------------|:--------------------|
| [Campo o condición verificada]            | [Valor — ej. 0,00]  |
| [Campo o condición verificada 2]          | [Valor esperado 2]  |

---

## Observaciones generales

<!-- OPCIONAL. Incluir si hay:
     - Popups opcionales que pueden o no aparecer.
     - Tiempos de espera relevantes (TBox Wait).
     - Ramas condicionales que dependen del estado de datos.
     - Comportamientos variables por entorno. -->

- [Observación 1: ej. "Puede aparecer popup de descarga; cerrarlo antes de continuar."]
- [Observación 2: ej. "Los waits de 8-15 s tras cada búsqueda son necesarios para que la tabla se recargue."]

## Postcondiciones / Limpieza

<!-- OBLIGATORIO. Estado final esperado del entorno tras la ejecución y acciones concretas
     de restauración para que el siguiente caso parta de un estado limpio.
     Incluir SOLO acciones funcionales (no desktop/SO ni cierre forzado de procesos).
     Ejemplos: vaciar basket, limpiar storage/sesión, revertir descuentos, cerrar sesión. -->

- [Postcondición 1: ej. "Vaciar el basket (Empty Basket → confirmar) o limpiar localStorage."]
- [Postcondición 2: ej. "La sesión puede permanecer abierta para nuevas ejecuciones."]

---

## Flujo

<!-- REEMPLAZAR: Diagrama ASCII que muestra la secuencia de navegación de punta a punta.
     Usar sangría con → para indicar el avance de pasos.
     Usar [Condicional: ...] para ramas opcionales.
     La secuencia SIEMPRE inicia en Preparación (URL base + estado limpio) y termina
     en la verificación final y la limpieza.
     Ejemplo de formato:

     Preparación (URL base + estado limpio)
       → Fase 1
         → Fase 2
           → [Condicional: acción si aparece X]
             → Fase 3
               → Verificación final
                 → Limpieza / Postcondiciones
-->

[Preparación — URL base / estado limpio]
  → [Fase 1]
    → [Fase 2]
      → [Fase 3]
        → [Condicional: acción opcional]
          → [Fase N — validación]
            → Verificar: [campo] == [valor esperado]
              → Limpieza / Postcondiciones
