# Plan de Implementación: Ecosistema "Software Architect" (@architect)

## 1. Visión y Estrategia
El objetivo es desplegar un **Mentor de Arquitectura** capaz de razonar sobre el sistema de forma holística. El ecosistema se divide en tres capas de abstracción para garantizar modularidad y cumplimiento de los estándares de Gemini CLI:
*   **Capa de Acción (Scripts):** Lógica pura de análisis (ej. grafos de dependencias).
*   **Capa de Habilidad (Skills):** Encapsulación de flujos de trabajo (ADRs, Modelado C4).
*   **Capa de Interfaz (Comandos y Agente):** Puntos de entrada para el usuario y orquestación inteligente de herramientas.

---

## 2. Definición del Agente (`gemini/agents/architect.md`)
El agente será el cerebro central del sistema, configurado estrictamente bajo el estándar de subagentes de Gemini CLI.
*   **Identidad:** Se define como un "Staff Engineer" consultivo. Su prompt evitará dar soluciones directas sin antes preguntar por el contexto de negocio y técnico ("It Depends").
*   **Configuración Técnica (Frontmatter):** 
    *   `name`: `architect`.
    *   `description`: Explicación detallada para que el agente principal sepa cuándo delegar decisiones de diseño.
    *   `tools`: Declaración explícita de `read_file`, `run_shell_command`, `glob`, `grep_search` y `web_fetch`.
    *   `kind`: `local`.
*   **Mandato:** Aplicar el principio de "Progressive Disclosure": primero analiza la estructura general mediante herramientas de análisis, luego profundiza en archivos específicos.

---

## 3. Arquitectura de Skills (`gemini/skills/`)
Cada skill será un módulo independiente en su propio directorio con su respectivo `SKILL.md` (YAML frontmatter incluido):

### 🌟 `system-modeler/` (Visualización Estructural)
*   **Concepto:** Implementar el **Modelo C4** mediante código.
*   **Componentes:** Alojará scripts de análisis de dependencias en su subcarpeta `scripts/`. Las instrucciones enseñarán al agente a traducir los datos técnicos a diagramas Mermaid.js de Nivel 1 (Contexto) y Nivel 2 (Contenedores).

### 🌟 `adr-manager/` (Gobernanza y Documentación)
*   **Concepto:** Registro de Decisiones Arquitectónicas (ADR).
*   **Flujo:** Instrucciones para detectar "puntos de decisión técnica", entrevistar al usuario sobre alternativas/consecuencias y persistir la decisión en formato MADR (Markdown Any Decision Record) dentro de `docs/decisions/`.

### 🌟 `tradeoff-analyzer/` (Análisis de Decisiones)
*   **Concepto:** Análisis multi-criterio.
*   **Flujo:** Evaluación sistemática de opciones tecnológicas basándose en ejes de Escalabilidad, Experiencia de Desarrollo (DX), Costo de Mantenimiento y Seguridad.

### 🌟 `oop-designer` & `effective-functions` (Mentoría de Calidad)
*   **Concepto:** Guardianes de la integridad del código.
*   **Enfoque:** Mentoría activa sobre principios SOLID, patrones de diseño y programación funcional limpia, adaptándose automáticamente al lenguaje detectado en el proyecto.

---

## 4. Integración de Comandos (`gemini/commands/*.toml`)
Se crearán comandos nativos para facilitar el acceso rápido a las capacidades del arquitecto:
*   **`/analyze-deps`**: Comando que inyecta el análisis de dependencias directamente en el chat. Usa una inyección `!{...}` para ejecutar el script de la skill `system-modeler`.
*   **`/visualize`**: Comando que activa el flujo de generación de diagramas Mermaid a partir del estado actual del código o de una propuesta de diseño.

---

## 5. Fases de Ejecución (Enfoque Orgánico Bottom-Up)

1.  **Fase 1: Reorganización Estructural**
    *   Mover los scripts de análisis existentes a `gemini/skills/system-modeler/scripts/`.
    *   Crear la jerarquía de carpetas para todas las skills planificadas.

2.  **Fase 2: Implementación de Contratos (Metadatos)**
    *   Redactar los archivos `SKILL.md` con frontmatter YAML validado y descriptivo.
    *   Crear el archivo `gemini/agents/architect.md` con su frontmatter y sistema de instrucciones.

3.  **Fase 3: Activación de Comandos TOML**
    *   Crear los archivos `.toml` en `gemini/commands/` vinculándolos a los scripts mediante inyecciones dinámicas.

4.  **Fase 4: Políticas y Autorizaciones**
    *   Asegurar que `.gemini/policies/architect-commands.toml` autorice la ejecución de los comandos y scripts en las nuevas rutas.
