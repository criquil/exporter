# TC-01: Verificar garantías parciales vencidas no habilitan límite

## Propósito

Verificar que las garantías parciales vencidas sin check *no habilitan* límite de crédito para el cliente en el sistema SCACS.

## Descripción

El caso inicia en la URL base de SCACS con el navegador en estado limpio, navega hasta el login, y desde allí hasta la sección de Límites Vigentes de una solicitud preaprobada en estado "Calificada". Se aplica un flujo de búsqueda por documento del cliente, se filtran las propuestas por flujo "Solicitud Preaprobada" y estado "Calificada", se ingresa al detalle de la solicitud y se valida que el monto habilitado sea 0,00, confirmando que las garantías parciales vencidas sin check no generan habilitación de límite. Al finalizar se restaura el estado del entorno.

## Data I/O

| Tipo | Campo | Descripción | Valor |
|------|-------|-------------|-------|
| Input | url | URL de acceso a SCACS | *Por favor proveer este valor* |
| Input | usuario | Credencial de usuario para login | *Por favor proveer este valor* |
| Input | password | Credencial de contraseña para login | *Por favor proveer este valor* |
| Input | nroDocumento | Número de documento del cliente | *Por favor proveer este valor* |
| Output | montoHabilitado | Valor de "Habilitado" en Límites Vigentes | *Por favor proveer este valor* |
| Output | resultado | Estado de la prueba: Pass / Fail | *Por favor proveer este valor* |

---

## Precondiciones

- [ ] Navegador en estado limpio: sin sesión activa en SCACS (cerrar sesión previa o limpiar cookies/storage del sitio)
- [ ] Cliente de prueba disponible con nroDocumento 98765432 y solicitud preaprobada en estado "Calificada"
- [ ] Login con usuario demo (ver Data I/O)
- [ ] No requiere configuración adicional

---

## Steps

### 1. Preparación

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 1.1 | Navegar a `{CP[url]}` | Se carga la página de login de SCACS |
| 1.2 | Limpiar estado previo: cerrar sesión si existe (o limpiar cookies del sitio) | Sin sesión activa: pantalla de login visible |
| 1.3 | Verificar estado limpio | Pantalla de login visible, sin datos de la sesión anterior |

---

### 2. Iniciar sesión

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 2.1 | Ingresar `{CP[usuario]}` en el campo `Usuario` | Campo completado con el valor ingresado |
| 2.2 | Ingresar `{CP[password]}` en el campo `Contraseña` | Campo completado (oculto) |
| 2.3 | Click en botón `LOGIN` | Pantalla principal de SCACS visible |

---

### 3. Navegar a Búsqueda de Propuestas

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 3.1 | Click en ícono `Menu Hamburguesa` | Menú lateral desplegado |
| 3.2 | Click en `Búsqueda de Propuestas` | Pantalla de búsqueda abierta |

---

### 4. Abrir panel de filtros

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 4.1 | Click en `Rueda Filtro Propuestas` | Panel de filtros desplegado |

---

### 5. Buscar cliente por documento

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 5.1 | Click en `Lupa para buscar Cliente` | Modal de búsqueda abierto |
| 5.2 | Ingresar `{CP[nroDocumento]}` en `Número Documento` | Campo completado |
| 5.3 | Click en `Buscar` | Resultados en tabla |
| 5.4 | Click en primera fila | Cliente seleccionado |

---

### 6. Aplicar filtro de Flujo

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 6.1 | En `Flujo` seleccionar `Solicitud Preaprobada` | Flujo filtrado |
| 6.2 | Click en `Buscar` | Tabla con preaprobadas |

---

### 7. Aplicar filtro de Estado

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 7.1 | En `Estado Propuesta` seleccionar `Calificada` | Estado filtrado |
| 7.2 | Click en `Buscar` | Tabla con calificadas |

---

### 8. Ingresar a solicitud calificada

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 8.1 | Ubicar fila con Estado `Calificada` | Fila encontrada |
| 8.2 | Click en `Calificada` de esa fila | Detalle de solicitud abierto |

---

### 9. Acceder al Resumen

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 9.1 | Click en `Resumen` | Resumen de propuesta visible |

---

### 10. Consultar solicitud

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 10.1 | Click en `Consultar` | Detalle con pestañas abierto |
| 10.2 | *(Condicional)* Si aparece `Inicio Solicitud Garantías`, click en `CONSULTAR SOLICITUD` | Detalle accesible |

---

### 11. Navegar a pestaña Límites

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 11.1 | Click en pestaña `Límites` | Sección de Límites visible |

---

### 12. Verificar monto habilitado

| # | Acción | Resultado esperado |
|--:|:-------|:-------------------|
| 12.1 | Click en `LÍMITES VIGENTES` | Tabla de límites desplegada |
| 12.2 | Leer `Habilitado` en última fila | Valor igual a **0,00** |

---

## Resultado Esperado

| Verificación | Valor Esperado |
|--------------|----------------|
| Monto "Habilitado" en Límites Vigentes (última fila) | 0,00 |

---

## Observaciones generales

- El paso 10.2 es condicional: solo aparece si la solicitud posee sección "Inicio Solicitud Garantías".
- Los tiempos de carga de la tabla de resultados pueden variar según entorno; esperar la recarga completa tras cada "Buscar".

## Postcondiciones / Limpieza

- Cerrar sesión de SCACS al finalizar (logout) para dejar el entorno sin sesión activa.
- La búsqueda y consulta realizadas no modifican datos; no se requieren restauraciones adicionales.

---

## Flujo

Preparación (URL base + sesión limpia)
  → Login
    → Menú → Búsqueda de Propuestas
      → Abrir filtros → Buscar cliente por documento
        → Filtro Flujo: "Solicitud Preaprobada"
          → Filtro Estado: "Calificada"
            → Seleccionar solicitud
              → Resumen → Consultar
                → [Condicional: CONSULTAR SOLICITUD]
                  → Pestaña "Límites"
                    → "LÍMITES VIGENTES"
                      → Verificar: Habilitado == 0,00
                        → Limpieza: cerrar sesión
