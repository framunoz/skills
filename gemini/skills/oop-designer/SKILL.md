---
name: oop-designer
description: Design software using Object-Oriented Programming (OOP) principles correctly. Focuses on SOLID, composition, and domain modeling.
metadata:
  author: Gemini CLI (@architect)
  version: "1.0.0"
  last-updated: "2026-04-06"
  tags: oop,solid,design-patterns,domain-modeling,ddd
---

# OOP Designer

Modeling the world as objects requires discipline. This skill helps you apply the best patterns and avoid common pitfalls.

## Core Principles

### 1. SOLID
- **S**ingle Responsibility: A class should have one reason to change.
- **O**pen/Closed: Open for extension, closed for modification.
- **L**iskov Substitution: Subtypes must be substitutable for their base types.
- **I**nterface Segregation: Prefer specific interfaces over a single large one.
- **D**ependency Inversion: Depend on abstractions, not concretions.

### 2. Composition over Inheritance
Avoid deep inheritance trees. Use composition to share behavior between classes.

### 3. Encapsulation
Keep the state private. Expose only what is necessary through well-defined methods.

## Workflow

1.  **Analyze the Domain**: Identify the entities and their relationships.
2.  **Design the Interface**: Define the public contract of your classes first.
3.  **Review for SOLID**: Audit your proposed classes against the SOLID principles.
4.  **Suggest Refactoring**: If you see high coupling or classes with too many responsibilities, propose a split.

## Best Practices
- **Favor Immutability**: Use `dataclasses` (Python) or `readonly` (TS) where appropriate.
- **Avoid God Objects**: Don't let one class do everything (e.g., `Manager`, `Engine`, `Context`).
- **Domain-Driven Design (DDD)**: Distinguish between Entities (have identity), Value Objects (no identity, defined by values), and Services (logic that doesn't fit in an entity).
