---
name: oop-designer
description: Design software using Object-Oriented Programming (OOP) principles. Focuses on SOLID, composition, and domain modeling. Use when designing classes, reviewing code for SOLID, or modeling domain entities.
compatibility: OpenCode
metadata:
  author: Francisco Muñoz (@framunoz)
  source: https://github.com/framunoz/skills/blob/main/opencode/skills/oop-designer/
  version: "1.1.1"
  last-updated: "2026-04-06"
  tags: oop,solid,design-patterns,domain-modeling,ddd
  related-with:
    skills:
      - effective-functions
    agents:
      - architect
    commands:
      - adr-manager
---

# OOP Designer

Design robust, maintainable systems using proven Object-Oriented principles.

## Core Resources

- **OOP & SOLID Principles**: See [oop-principles.md](references/oop-principles.md) for detailed descriptions of SOLID, Composition, and DDD.

## Workflow

1.  **Analyze Domain**: Identify entities and their relationships.
2.  **Apply Principles**: Use the [oop-principles.md](references/oop-principles.md) as a checklist during design.
3.  **Refactor**: Propose changes to existing code to better align with SOLID or to favor composition over inheritance.

## Best Practices

- **Favor Immutability**: Use `dataclasses` (Python) or `readonly` (TS) where possible.
- **Keep Classes Small**: If a class does more than one thing, it's a candidate for refactoring.
- **Abstractions over Concretions**: Always code to an interface (or abstract class) when dependencies are involved.
