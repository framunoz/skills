---
name: adr-manager
description: Create and manage Architecture Decision Records (ADRs). Use when a technical decision needs long-term documentation in `docs/decisions/`.
compatibility: OpenCode
metadata:
  author: Francisco Muñoz (@framunoz)
  source: https://github.com/framunoz/skills/blob/main/opencode/skills/adr-manager/
  version: "1.1.1"
  last-updated: "2026-04-06"
  tags: architecture,documentation,decision,adr
  related-with:
    skills:
      - tradeoff-analyzer
    agents:
      - architect
    commands:
      - adr-manager
---

# ADR Manager

Documentation is critical for long-term project maintainability. Use this skill to formalize decisions, capture context, and explain trade-offs.

## Core Resources

- **ADR Guidelines**: See [adr-guidelines.md](references/adr-guidelines.md) for when and how to document.
- **ADR Template**: Use [adr-template.md](assets/adr-template.md) for the file structure.

## Workflow

1.  **Identify the Decision**: Propose an ADR when a significant design choice is made.
2.  **Gather Context**: Discuss the title, status, problem context, and solution details with the user.
3.  **Draft the ADR**:
    - Determine the next sequential number by listing files in `docs/decisions/`.
    - Apply the [adr-template.md](assets/adr-template.md) to a new file named `XXXX-title-slug.md`.
4.  **Save & Review**: Save the file and confirm with the user.

## Best Practices

- **Proactive Documentation**: If the conversation leads to a major choice, offer to create an ADR.
- **Clear Status**: Always specify if the decision is `Proposed`, `Accepted`, etc.
- **Link Decisions**: If a new ADR supersedes an old one, update the status of the old one and link them.
