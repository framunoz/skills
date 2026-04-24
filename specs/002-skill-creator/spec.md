# Feature Specification: skill-creator

**Feature Branch**: `002-skill-creator`  
**Created**: 2026-04-23  
**Status**: Draft  
**Input**: User description: "Crear una skill para OpenCode que sirva para crear más skills de OpenCode. Inspirada en las skill-creators de Gemini y Claude, pero adaptada al estándar y flujo de trabajo de este proyecto (speckit, AGENTS.md). Debe permitir crear, editar, validar y mejorar skills. Debe integrarse con el flujo speckit y reducir la carga de contexto del AGENTS.md."

## Clarifications

### Session 2026-04-23

- Q: ¿La skill-creator debe asumir un path por defecto para las skills creadas o preguntar siempre? → A: La skill-creator SIEMPRE pregunta al usuario dónde guardar la skill. No assume ningún path por defecto. El usuario puede especificar cualquier path válido.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Crear una skill nueva desde cero (Priority: P1)

Un usuario del proyecto dice "quiero crear una skill para [propósito]" y necesita que la skill-creator lo guíe desde la extracción del intent hasta la skill validada y lista para usar.

**Why this priority**: Es el caso de uso principal. Sin esto, la skill no tiene valor.

**Independent Test**: Puede probarse completamente ejecutando la skill-creator con un prompt como "quiero una skill para generar changelogs" y verificando que se genera una skill válida en `.opencode/skills/changelog-generator/SKILL.md`.

**Acceptance Scenarios**:

1. **Given** el usuario quiere crear una skill, **When** proporciona una descripción de propósito, **Then** la skill-creator infiere nombre, descripción, recursos necesarios y propone valores por defecto.
2. **Given** la inferencia es ambigua, **When** falta información crítica, **Then** la skill-creator hace como máximo 3 preguntas puntuales para completarla.
3. **Given** la información es completa, **When** la inferencia es clara, **Then** la skill-creator genera un borrador para `/speckit.specify` listo para copiar y pegar.
4. **Given** el usuario ejecuta `/speckit.specify` con el borrador, **When** avanza a `/speckit.plan` y `/speckit.tasks`, **Then** la skill-creator asiste generando el SKILL.md, scripts, references y assets.
5. **Given** la skill está creada, **When** el usuario ejecuta el script de validación, **Then** el resultado es "válida" con exit code 0 y sin warnings de TODOs.
6. **Given** la skill pasa validación, **When** la skill-creator presenta la checklist de calidad, **Then** el usuario puede verificar manualmente nombre/directorio coincidentes, descripción con triggers claros, y sin TODOs.

---

### User Story 2 - Editar o mejorar una skill existente (Priority: P2)

Un usuario que ya tiene una skill quiere iterarla (añadir scripts, mejorar la description, agregar progressive disclosure).

**Why this priority**: La creación es el punto de entrada; la mejora es el ciclo de vida natural.

**Independent Test**: Puede probarse ejecutando la skill-creator con "quiero mejorar la skill efectivo-functions" y verificando que propone cambios relevantes.

**Acceptance Scenarios**:

1. **Given** el usuario quiere mejorar una skill existente, **When** proporciona el nombre de la skill, **Then** la skill-creator lee el SKILL.md existente y presenta un diagnóstico de gaps.
2. **Given** el diagnóstico indica gaps, **When** el usuario confirma qué mejorar, **Then** la skill-creator genera los cambios sugeridos y los aplica.
3. **Given** los cambios se aplican, **When** se re-ejecuta la validación, **Then** la skill actualizada pasa sin errores.

---

### User Story 3 - Validar una skill creada manualmente (Priority: P3)

Un usuario creó archivos a mano (sin usar la skill-creator) y quiere verificar que cumplen el estándar antes de confiar en ella.

**Why this priority**: Permite independencia total; el usuario puede crear skills manualmente y validar después.

**Independent Test**: Puede probarse creando un directorio con SKILL.md a mano y ejecutando `node scripts/validate_skill.cjs <path>`.

**Acceptance Scenarios**:

1. **Given** existe un directorio de skill, **When** el usuario ejecuta `node scripts/validate_skill.cjs <path>`, **Then** el script reporta: "válida" con exit 0, o bien lista de errores específicos con exit 1.
2. **Given** el SKILL.md tiene frontmatter inválido (falta name, description multilínea, nombre con mayúsculas), **When** se ejecuta la validación, **Then** el error reportado indica exactamente qué campo falla y por qué.
3. **Given** la skill tiene TODOs pendientes, **When** se ejecuta la validación, **Then** se reporta un warning indicando en qué archivo y línea está el TODO.

---

### Edge Cases

- ¿Qué pasa si el nombre de skill propuesto contiene caracteres inválidos? → La validación del init script rechaza con mensaje claro y sugiere alternativa hyphen-case.
- ¿Qué pasa si el directorio de la skill ya existe? → El init script falla con error stating que el directorio ya existe, sugiere otro nombre o eliminar el existente.
- ¿Qué pasa si el usuario no tiene Node.js o no ha instalado js-yaml? → El script detecta la dependencia faltante y reporta instrucciones claras de instalación (`npm install`).
- ¿Qué pasa si el proyecto no usa speckit (no existe `.specify/`)? → La skill-creator usa flujo interno standalone: genera archivos directamente con write/edit en lugar de instruir comandos speckit.
- ¿Qué pasa si la descripción del usuario es demasiado vaga ("quiero una skill para cosas")? → La skill-creator detecta la vaguedad y hace preguntas para concretizar antes de proceder.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La skill-creator DEBE extraer de una descripción natural: nombre de skill (inferido del propósito), descripción (qué hace y cuándo se activa), y tipo de recursos necesarios (scripts/references/assets).
- **FR-002**: Si la información inferida es ambigua, la skill-creator DEBE hacer como máximo 3 turnos de preguntas until tener lo necesario para proceder.
- **FR-003**: La skill-creator DEBE generar un borrador de feature description listo para `/speckit.specify` que el usuario pueda copiar y pegar directamente.
- **FR-004**: La skill-creator DEBE detectar si el proyecto usa speckit (existe `.specify/`). Si existe, usar el flujo híbrido instruir + asistir. Si no existe, generar archivos directamente.
- **FR-005**: Un script `scripts/init_skill.cjs` DEBE recibir `<skill-name>` y `--path <output-dir>`, crear la estructura de directorios (`SKILL.md`, `scripts/`, `references/`, `assets/`), y usar js-yaml para generar frontmatter válido.
- **FR-005b**: Antes de ejecutar el init script, la skill-creator DEBE preguntar al usuario cuál es el path de destino para la nueva skill. No DEBE asumir un path por defecto. El usuario puede especificar cualquier path válido del sistema de archivos.
- **FR-006**: Un script `scripts/validate_skill.cjs` DEBE verificar: SKILL.md existe, frontmatter parseable con js-yaml, name presente y matches regex `^[a-z0-9]+(-[a-z0-9]+)*$`, description presente y single-line de 1-1024 chars, ausencia de `TODO:` en todos los archivos del skill (warning si existen).
- **FR-007**: La skill-creator DEBE incluir `references/skill-patterns.md` con patrones de progressive disclosure, domain organization, conditional details y output patterns.
- **FR-008**: La skill-creator DEBE incluir `references/skill-standards.md` con la especificación completa del frontmatter (name, description, license, compatibility, metadata), reglas de nombres y longitudes, y convenciones de directorios.
- **FR-009**: Al finalizar la creación de una skill, la skill-creator DEBE presentar una checklist de calidad markdown y 2-3 test prompts sugeridos con resultado esperado.
- **FR-010**: Tras la implementación de la skill-creator, la sección "Skills" del AGENTS.md DEBE reducirse a una referencia breve que apunte a la skill-creator, delegando el detalle a la skill o sus references.

---

### Key Entities *(include if feature involves data)*

- **Skill**: Paquete modular en `.opencode/skills/<name>/` con SKILL.md requerido y recursos opcionales (`scripts/`, `references/`, `assets/`).
- **SKILL.md**: Archivo requerido con YAML frontmatter (name, description, license, compatibility, metadata) y cuerpo markdown.
- **Frontmatter**: Bloque YAML entre `---` al inicio del SKILL.md con campos definidos por el estándar OpenCode.
- **Init Script**: `scripts/init_skill.cjs` — genera boilerplate de skill con estructura de directorios y template de SKILL.md.
- **Validate Script**: `scripts/validate_skill.cjs` — valida estructura y contenido de una skill existente.
- **References**: Documentación de diseño en `references/skill-patterns.md` y `references/skill-standards.md`, cargada bajo demanda.
- **Speckit Integration**: El flujo de desarrollo del proyecto basado en `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El AGENTS.md DEBE reducir su contenido sobre skills en al menos 100 líneas (medible comparando el archivo antes y después).
- **SC-002**: Un usuario DEBE poder pasar de "quiero crear una skill para X" a skill validada en menos de 15 minutos de interacción (asumiendo que conoce el propósito).
- **SC-003**: El 100% de las skills creadas con la skill-creator DEBEN pasar la validación del script sin errores (name válido, description completa, sin TODOs).
- **SC-004**: La skill-creator DEBE cubrir el 100% de los campos y reglas definidos en https://opencode.ai/docs/skills.md más las convenciones del AGENTS.md de este proyecto.
- **SC-005**: Un usuario nuevo DEBE poder crear su primera skill sin leer documentación externa, siguiendo solo las instrucciones conversacionales de la skill.

---

## Assumptions

- El usuario tiene Node.js instalado (versión 18+).
- El usuario ejecuta `npm install` en el directorio de la skill-creator para instalar js-yaml antes de usar los scripts.
- El proyecto tiene acceso a internet para consultar https://opencode.ai/docs/skills.md si es necesario.
- La skill-creator se instala en `.opencode/skills/skill-creator/` de este proyecto (scope proyecto-local).
- Las skills creadas se almacenan donde el usuario indique, sin asumir un path por defecto.
- El estándar de skills de OpenCode es estable y no cambia frecuentemente.
