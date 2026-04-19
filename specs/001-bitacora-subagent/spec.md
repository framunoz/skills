# Feature Specification: Subagente de Bitácora (Logbook)

**Feature Branch**: `001-bitacora-subagent`
**Created**: 2026-04-18
**Status**: Draft
**Input**: User description: "Quiero hacer un subagente que me ayude a mantener una bitácora. Por ejemplo, que me ayude a registrar qué cosas salieron bien y que cosas salieron mal de algunas pruebas, o que me ayude a registrar el proceso de creación de un proyecto. Digamos, en qué aspectos me ayudó la IA, en qué aspectos yo hice el diseño y le dije que algo estaba mal, etc. Me imagino al agente que solo lo pueda llamar yo, que no se gatille con una falsa alarma por otro agente, pues yo tengo que escribir los registros de la bitacora. Este agente es para claude."

## Clarifications

### Session 2026-04-18

- Q: ¿Cómo se identifica la bitácora objetivo al invocar el subagente? → A: El usuario puede nombrarla explícitamente; si no, el subagente la infiere por contexto y, si no hay contexto claro, pregunta antes de escribir.
- Q: ¿Cómo se organizan y almacenan múltiples bitácoras? → A: Carpeta `logbook/<slug>/` por bitácora. Las entradas se guardan en un archivo estructurado (JSON) al que el subagente añade mediante un comando de "push"; un comando separado de formateo renderiza la vista humana (Markdown). Motivación: eficiencia en tokens y poder re-estructurar la vista sin tocar los datos.
- Q: ¿Esquema por bitácora: fijo o mixto? → A: Fijo. Cada bitácora declara un tipo/esquema al crearse (p. ej. `pruebas`, `colaboracion`, `libre`) y todas sus entradas se validan contra ese esquema.
- Q: ¿Política de edición/corrección de entradas existentes? → A: Inmutable con enmiendas. El subagente no modifica entradas pasadas; las correcciones se añaden como nuevas entradas de tipo "enmienda" que referencian a la original por id.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Registrar resultado de una prueba (Priority: P1)

El usuario acaba de ejecutar una prueba (manual, automatizada, experimento) y quiere dejar constancia de qué funcionó y qué no. Invoca explícitamente al subagente, le dicta lo ocurrido en lenguaje natural, y el subagente genera una entrada estructurada en la bitácora con fecha, contexto, lo que salió bien, lo que salió mal y próximos pasos.

**Why this priority**: Es el caso de uso central mencionado por el usuario. Sin esto, el subagente no cumple su propósito básico. Es también el flujo más frecuente (registro breve y recurrente).

**Independent Test**: El usuario invoca el subagente, dicta resultados de una prueba, y verifica que se crea o actualiza un archivo de bitácora con una entrada bien estructurada, fechada y recuperable.

**Acceptance Scenarios**:

1. **Given** el usuario acaba de ejecutar pruebas y no existe aún una bitácora, **When** invoca explícitamente al subagente con un resumen de resultados, **Then** el subagente crea el archivo de bitácora e inserta una entrada fechada con secciones "Qué salió bien" y "Qué salió mal".
2. **Given** ya existe una bitácora con entradas previas, **When** el usuario invoca el subagente para registrar una nueva prueba, **Then** se añade una nueva entrada sin alterar entradas anteriores y preservando el formato existente.
3. **Given** el usuario proporciona información incompleta (p. ej. sólo lo que falló), **When** invoca al subagente, **Then** el subagente registra lo proporcionado y marca explícitamente las secciones vacías como "sin observaciones" en lugar de inventar contenido.

---

### User Story 2 - Registrar proceso de co-creación con IA (Priority: P2)

El usuario está construyendo un proyecto colaborando con Claude (u otra IA). Quiere dejar trazabilidad de: en qué partes la IA aportó, en qué partes el usuario diseñó o decidió, y en qué momentos el usuario corrigió a la IA. Invoca al subagente que le ayuda a capturar esa atribución de autoría y de decisiones.

**Why this priority**: Es el segundo caso de uso explícito del usuario, orientado a reflexión y aprendizaje sobre la colaboración humano-IA. Menos frecuente que P1 pero con valor alto a mediano plazo (retrospectivas, memoria del proyecto).

**Independent Test**: El usuario invoca el subagente tras una sesión de trabajo, describe el proceso, y verifica que la entrada resultante distingue claramente contribuciones de la IA, contribuciones del usuario, y correcciones realizadas por el usuario a la IA.

**Acceptance Scenarios**:

1. **Given** el usuario terminó una sesión de diseño colaborativa, **When** invoca al subagente y describe lo ocurrido, **Then** la entrada incluye campos diferenciados para "Aporte IA", "Aporte humano" y "Correcciones del humano a la IA".
2. **Given** el usuario quiere vincular el registro a un hito o decisión de proyecto, **When** menciona el hito al invocar el subagente, **Then** la entrada queda etiquetada con ese hito para facilitar búsquedas posteriores.

---

### User Story 3 - Consultar la bitácora (Priority: P3)

El usuario quiere revisar entradas anteriores: qué falló la semana pasada, en qué ayudó la IA en cierto módulo, qué decisiones tomó. Invoca al subagente con una consulta y recibe un resumen o las entradas relevantes.

**Why this priority**: Complementa el valor del registro. Sin consulta, la bitácora sigue siendo útil como archivo, pero la consulta aumenta el retorno del esfuerzo de registrar. No es crítico para el MVP.

**Independent Test**: El usuario pide al subagente "muéstrame qué salió mal en las pruebas del mes pasado" y recibe una lista o resumen basado únicamente en las entradas existentes, sin inventar información.

**Acceptance Scenarios**:

1. **Given** existen varias entradas en la bitácora, **When** el usuario pide un resumen por tema o rango de fechas, **Then** el subagente devuelve sólo información presente en la bitácora, citando las entradas fuente.
2. **Given** no hay entradas que coincidan con la consulta, **When** el usuario consulta, **Then** el subagente responde explícitamente que no hay registros coincidentes en lugar de generar contenido.

---

### Edge Cases

- **Invocación indirecta por otro agente**: si otro subagente o el agente principal intenta delegar en este subagente sin que el usuario lo haya pedido explícitamente, el subagente no debe gatillarse. La descripción del subagente debe estar redactada para evitar emparejamiento automático por el router/orquestador.
- **Bitácora corrupta o con formato alterado manualmente**: el subagente debe preservar el contenido existente y, si no puede parsearlo con seguridad, añadir la nueva entrada al inicio sin reformatear el resto.
- **Información sensible**: si el usuario dicta credenciales, tokens o datos personales, el subagente debe advertir y pedir confirmación antes de escribirlos a disco.
- **Conflicto de fecha/hora**: si el sistema no puede determinar la fecha actual con certeza, el subagente pide confirmación antes de fechar la entrada.
- **Selección de bitácora ambigua**: si hay varias bitácoras y el usuario no nombra una, el subagente intenta inferirla por contexto (tema dictado, archivo activo). Si la inferencia tiene baja confianza o hay empate, pregunta antes de escribir.
- **Bitácora inexistente**: si el usuario menciona una bitácora que no existe, el subagente confirma si debe crearla en lugar de asumirlo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El subagente DEBE estar disponible como subagente de Claude Code, invocable mediante llamada explícita del usuario (referencia por nombre o descripción dirigida).
- **FR-002**: El subagente NO DEBE ser invocado proactivamente por el agente principal ni delegado por otros subagentes. Su descripción/metadatos deben indicar explícitamente "invocar solo cuando el usuario lo pida por nombre" y evitar verbos de activación amplios que provoquen emparejamientos automáticos.
- **FR-003**: El subagente DEBE aceptar descripciones en lenguaje natural de lo ocurrido y transformarlas en entradas estructuradas conforme al esquema de la bitácora objetivo.
- **FR-004**: Cada bitácora DEBE tener un tipo/esquema declarado al crearse. Tipos mínimos soportados (los valores canónicos en código son los ingleses: `tests`, `collaboration`, `free`):
  - `pruebas` / `tests`: fecha, título/contexto, qué salió bien, qué salió mal, próximos pasos, etiquetas.
  - `colaboracion` / `collaboration`: fecha, título/contexto, aporte IA, aporte humano, correcciones del humano a la IA, etiquetas.
  - `libre` / `free`: fecha, título, cuerpo, etiquetas.
- **FR-004a**: El subagente DEBE rechazar (o advertir y pedir confirmación) entradas que no cumplan el esquema declarado por la bitácora objetivo; en ningún caso silenciosamente omite campos requeridos ni fabrica datos.
- **FR-005**: El subagente DEBE escribir las entradas en la bitácora objetivo indicada por el usuario (por nombre/slug). Si el usuario no la nombra, DEBE intentar inferirla por contexto (tema dictado, trabajo reciente) y confirmarlo; si no hay contexto suficiente, DEBE pedirla antes de escribir. Bajo ningún caso escribe en una bitácora ambigua sin confirmación.
- **FR-005a**: El proyecto PUEDE contener múltiples bitácoras coexistiendo (p. ej. una por tarea, o una por tipo de registro). El subagente DEBE poder crear nuevas bitácoras bajo demanda, listar las existentes y operar sobre cualquiera de ellas.
- **FR-005b**: Cada bitácora DEBE vivir bajo `logbook/<slug>/` dentro del proyecto. Las entradas se persisten en un archivo estructurado legible por máquina (formato tipo JSON) al que se añade (append) sin reescribir entradas previas.
- **FR-005c**: El subagente DEBE añadir entradas invocando una operación de "push" que valida el esquema de la entrada y la agrega al archivo estructurado. El subagente NO edita manualmente el archivo estructurado con diffs textuales.
- **FR-005d**: DEBE existir una operación separada de "formateo" que renderiza el archivo estructurado a una vista humana (p. ej. Markdown). El formateo es idempotente y no altera los datos de origen.
- **FR-006**: Las entradas existentes son inmutables. El subagente NO modifica ni elimina entradas ya registradas.
- **FR-006a**: Cada entrada DEBE tener un identificador único estable dentro de su bitácora.
- **FR-006b**: Para corregir una entrada previa, el subagente DEBE registrar una nueva entrada de tipo "enmienda" que referencie por id a la entrada original y contenga el contenido corregido o la aclaración. La entrada original permanece intacta.
- **FR-007**: El subagente DEBE permitir consultar entradas existentes (por fecha, tema o etiqueta) y al responder DEBE basarse únicamente en contenido efectivamente presente en la bitácora, sin fabricar registros.
- **FR-008**: El subagente DEBE advertir al usuario y pedir confirmación antes de registrar contenido que parezca sensible (secretos, credenciales, datos personales identificables).
- **FR-009**: El subagente DEBE dejar evidencia clara cuando la información proporcionada es parcial (p. ej. sección "qué salió bien" vacía), sin inventar contenido para llenar huecos.
- **FR-010**: El subagente DEBE funcionar sin dependencias de red ni servicios externos; toda la información vive como archivos locales del proyecto.

### Key Entities *(include if feature involves data)*

- **Entrada de Bitácora (Logbook Entry)**: unidad atómica de registro. Incluye id único dentro de su bitácora, fecha/hora, título/contexto, campos de contenido conforme al esquema de la bitácora, etiquetas opcionales, y (para entradas de enmienda) una referencia al id de la entrada corregida. Las entradas son inmutables una vez registradas.
- **Bitácora (Logbook)**: colección ordenada cronológicamente de entradas, residente en el proyecto bajo `logbook/<slug>/`. Un proyecto puede contener múltiples bitácoras, cada una identificada por un slug único dentro del proyecto (p. ej. `pruebas-login`, `colaboracion-ia`). Se persiste como datos estructurados (fuente de verdad) y opcionalmente una vista formateada derivada.
- **Subagente de Bitácora**: definición de agente (nombre, descripción, instrucciones) registrada en la configuración de Claude Code del proyecto o del usuario.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El usuario puede registrar una entrada completa de prueba (bien / mal / próximos pasos) en menos de 2 minutos desde la invocación hasta ver el archivo actualizado.
- **SC-002**: En 0 de cada 20 sesiones de trabajo no relacionadas el subagente se activa automáticamente sin que el usuario lo haya invocado por nombre (tasa de falsa activación = 0%).
- **SC-003**: El 100% de las entradas generadas conserva intacto el contenido previo de la bitácora (verificable por diff: sólo se agrega contenido, no se modifica lo existente).
- **SC-004**: En consultas sobre entradas pasadas, el 100% de las afirmaciones devueltas por el subagente son rastreables a una entrada real de la bitácora (cero alucinaciones).
- **SC-005**: El usuario percibe que la estructura de la entrada refleja lo que dictó, sin necesidad de reescritura manual, en al menos el 80% de las invocaciones.

## Assumptions

- El subagente se define en el formato estándar de subagentes de Claude Code (archivo de definición de agente con nombre, descripción e instrucciones), en el scope del proyecto o del usuario según prefiera el usuario al instalarlo.
- La bitácora se almacena como archivo Markdown local en el repositorio del proyecto (p. ej. `BITACORA.md` o bajo `docs/bitacora/`). El formato concreto se decidirá en fase de planificación.
- El subagente opera sobre el working directory actual de Claude Code; no gestiona múltiples proyectos simultáneamente.
- No se asume una única persona por bitácora: al tener múltiples bitácoras (p. ej. por tarea o por tipo), pueden coexistir varios autores a lo largo del tiempo. No hay, sin embargo, mecanismos de concurrencia de escritura simultánea dentro de la misma bitácora (se asume escritura secuencial).
- Las entradas se escriben en el idioma en que el usuario las dicta (el usuario suele trabajar en español).
- El mecanismo para evitar "falsas alarmas" de activación descansa en: (a) una descripción del subagente explícitamente restrictiva ("solo invocar cuando el usuario lo pida por nombre") y (b) ausencia de verbos/keywords genéricos en la descripción que induzcan al router a elegirlo por similitud semántica con tareas comunes.
- El usuario prefiere un único subagente con modos (prueba / co-creación / consulta) antes que varios subagentes separados.
