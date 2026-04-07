# Guía de Migración: Ecosistema "Software Architect" a OpenCode

Este documento detalla el proceso paso a paso para migrar el subagente `@architect`, sus skills y comandos desde Gemini CLI hacia el entorno de OpenCode, respetando sus estándares nativos de configuración y seguridad.

---

## 📋 Fase 1: Infraestructura de Skills (Capa de Acción)

OpenCode busca las skills en el directorio `opencode/skills/`. Debemos asegurar que la lógica de los scripts sea accesible desde estas nuevas rutas.

### 1.1 Replicación de Archivos
Copiar el contenido de las siguientes carpetas desde `gemini/skills/` hacia `opencode/skills/`:
- `adr-manager/`
- `tradeoff-analyzer/`
- `system-modeler/` (Asegurar que incluya la subcarpeta `scripts/` con el analizador)
- `oop-designer/`
- `effective-functions/`

### 1.2 Actualización de Referencias Internas
En los archivos `SKILL.md` de `adr-manager` y `system-modeler`, actualizar cualquier comando de ejecución para que use la ruta de OpenCode:
- **Ruta Antigua:** `uv run gemini/skills/system-modeler/scripts/dependency-analyzer.py`
- **Ruta Nueva:** `uv run opencode/skills/system-modeler/scripts/dependency-analyzer.py`

---

## ⌨️ Fase 2: Interfaz de Comandos (Capa de Usuario)

A diferencia de Gemini CLI (que usa `.toml`), OpenCode utiliza archivos **Markdown (.md)** para definir comandos personalizados.

### 2.1 Crear el Comando `analyze-deps.md`
Crear el archivo en `opencode/commands/analyze-deps.md` con la siguiente estructura:

```markdown
---
description: Analiza la arquitectura y dependencias del proyecto (Python/JS).
agent: architect
---
Analiza el siguiente mapa de dependencias del proyecto y resume la salud arquitectónica. 
Identifica dependencias circulares, acoplamiento alto o violaciones de arquitectura en capas.

Mapa de Dependencias:
!{uv run opencode/skills/system-modeler/scripts/dependency-analyzer.py $ARGUMENTS}
```

---

## 🧠 Fase 3: Definición del Agente `@architect`

Refactorizaremos el agente para que sea compatible con el sistema de permisos y modos de OpenCode.

### 3.1 Crear el Perfil del Agente
Crear el archivo en `opencode/agents/architect.md` con el siguiente frontmatter YAML:

```yaml
---
description: Senior Software Architect and Technical Mentor. Specialized in system design, trade-offs, and clean code principles.
mode: all
permission:
  bash:
    "*": ask
    "uv run opencode/skills/system-modeler/scripts/dependency-analyzer.py *": allow
  edit: deny
  read: allow
  skill: allow
---
```

### 3.2 Adaptar el System Prompt
El cuerpo del archivo Markdown debe mantener la filosofía "It Depends", pero las instrucciones de herramientas deben apuntar a las carpetas de `opencode/`.

---

## ✅ Fase 4: Verificación Final

Para confirmar que la migración ha sido exitosa:
1.  **Cargar OpenCode**: Asegurarse de que el comando `/analyze-deps` esté disponible.
2.  **Prueba de Comando**: Ejecutar `/analyze-deps .` y verificar que el script de Python se ejecute correctamente.
3.  **Prueba de Agente**: Invocar `@architect` y pedirle: *"¿Qué opinas de la organización de este código?"*. El agente debe ser capaz de invocar la skill `system-modeler` (ahora en la ruta de OpenCode) para responder.
