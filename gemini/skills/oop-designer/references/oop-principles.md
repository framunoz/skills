# OOP & SOLID Principles

Effective Object-Oriented Programming requires following proven principles.

## 1. SOLID
- **Single Responsibility (SRP)**: A class should have one, and only one, reason to change.
- **Open/Closed (OCP)**: Software entities should be open for extension but closed for modification.
- **Liskov Substitution (LSP)**: Objects of a superclass should be replaceable with objects of its subclasses without affecting the correctness of the program.
- **Interface Segregation (ISP)**: Clients should not be forced to depend on interfaces they do not use.
- **Dependency Inversion (DIP)**: Depend on abstractions, not concretions.

## 2. Composition over Inheritance
Avoid deep inheritance trees. Use composition (has-a) instead of inheritance (is-a) to share behavior. This increases flexibility and reduces coupling.

## 3. Encapsulation
Keep the internal state of an object hidden. Expose only what is necessary through a well-defined public interface.

## 4. Domain Modeling (DDD)
- **Entities**: Objects defined by their identity, not just their attributes.
- **Value Objects**: Objects defined by their attributes, with no identity (e.g., a Money object).
- **Aggregates**: A cluster of domain objects that can be treated as a single unit.
- **Repositories**: Encapsulate the logic required to access data sources.
