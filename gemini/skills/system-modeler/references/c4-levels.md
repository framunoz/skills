# C4 Model Levels

The C4 model is a lean graphical notation technique for modelling the architecture of software systems.

## 1. System Context Diagram (L1)
Shows the system as a whole and its interactions with external users and systems.
- **Focus**: Scope and high-level boundaries.
- **Audience**: Technical and non-technical people, both inside and outside of the software development team.

## 2. Container Diagram (L2)
Shows the high-level technical building blocks (web apps, databases, file systems, microservices).
- **Focus**: Technology choices and communication protocols.
- **Audience**: Technical people, both inside and outside of the software development team.

## 3. Component Diagram (L3)
Shows the internal components within a container (e.g., controllers, services, repositories).
- **Focus**: Internal structure and responsibilities.
- **Audience**: Software architects and developers.

## 4. Code Diagram (L4)
Shows how a component is implemented using code (e.g., class diagrams, entity-relationship diagrams).
- **Focus**: Detailed implementation.
- **Audience**: Software architects and developers.
- **Note**: This level is often optional and can be generated directly from code.
