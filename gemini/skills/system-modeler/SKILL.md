---
name: system-modeler
description: Visualize software architecture using Mermaid.js and the C4 model. Use when asked to create diagrams, explain system structure, or visualize dependencies.
metadata:
  author: Gemini CLI (@architect)
  version: "1.1.0"
  last-updated: "2026-04-06"
  tags: architecture,visualization,diagram,mermaid,c4
---

# System Modeler (C4 & Mermaid)

This skill provides the workflow and tools for visualizing software architecture at different levels of abstraction.

## Core Resources
- **C4 Model Levels**: See [c4-levels.md](references/c4-levels.md) for detailed descriptions of L1 to L4 levels.
- **Dependency Analyzer**: Use `scripts/dependency-analyzer.py` to extract structured project data.

## Workflow

1. **Analyze Structure**: Run the dependency analyzer to map the current system.
   ```bash
   uv run gemini/skills/system-modeler/scripts/dependency-analyzer.py .
   ```
2. **Select C4 Level**: Refer to [c4-levels.md](references/c4-levels.md) and choose the appropriate abstraction level (L1, L2, or L3).
3. **Generate Mermaid.js**: Create the diagram using C4-specific Mermaid syntax.
   ```mermaid
   C4Context
       title System Context Diagram
       Person(customer, "Customer", "Uses the system")
       System(system, "My System", "Provides features")
       Rel(customer, system, "Uses", "HTTPS")
   ```
4. **Output**: Include the code in your response or save it to `docs/architecture/`.

## Best Practices
- **Label Everything**: Every relationship (Rel) must specify the protocol or action.
- **Consistent Scope**: Don't mix containers and components in the same diagram.
- **Simplicity**: If a diagram requires more than 15-20 nodes, split it by bounded context.
