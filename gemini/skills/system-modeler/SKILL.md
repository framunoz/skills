---
name: system-modeler
description: Visualize software architecture using Mermaid.js and the C4 model. Use this to create Context, Container, and Component diagrams.
metadata:
  author: Gemini CLI (@architect)
  version: "1.0.0"
  last-updated: "2026-04-06"
  tags: architecture,visualization,diagram,mermaid,c4
---

# System Modeler (C4 & Mermaid)

A picture is worth a thousand lines of code. This skill helps you visualize the system's structure at different levels of abstraction.

## Diagram Types (C4 Model)

### 1. System Context Diagram (L1)
Shows the system as a whole and its interactions with external users and systems.
- **Focus**: Scope and high-level boundaries.

### 2. Container Diagram (L2)
Shows the high-level technical building blocks (web apps, databases, file systems, microservices).
- **Focus**: Technology choices and communication protocols.

### 3. Component Diagram (L3)
Shows the internal components within a container (e.g., controllers, services, repositories).
- **Focus**: Internal structure and responsibilities.

## Workflow

1.  **Analyze**: Run `uv run gemini/commands/dependency-analyzer.py .` to get a structured view of the current files and dependencies.
2.  **Select Level**: Decide which C4 level is most appropriate for the current task.
3.  **Generate Mermaid**: Create the diagram using Mermaid.js syntax.

```mermaid
C4Context
    title System Context Diagram for [Project]
    Person(customer, "Customer", "Uses the system")
    System(system, "Software System", "Provides features")
    System_Ext(ext_system, "External System", "External service")
    
    Rel(customer, system, "Uses")
    Rel(system, ext_system, "Sends data to")
```

4.  **Save/Render**: Include the Mermaid code in your response or save it to a `.md` file in `docs/architecture/`.

## Best Practices
- **Consistent Naming**: Use the same names for systems and containers across all diagrams.
- **Explain Arrows**: Always label relationships with a description (e.g., "Uses HTTPS", "Sends JSON").
- **Simplicity**: Avoid "spaghetti" diagrams. If a diagram is too complex, split it into smaller ones.
