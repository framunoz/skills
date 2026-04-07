---
name: adr-manager
description: Create and manage Architecture Decision Records (ADRs). Use this skill when a technical decision needs to be documented for the long term.
metadata:
  author: Gemini CLI (@architect)
  version: "1.0.0"
  last-updated: "2026-04-06"
  tags: architecture,documentation,decision,adr
---

# ADR Manager

Documentation is the soul of architecture. Use this skill to formalize decisions, capture context, and explain trade-offs.

## When to Use
- When selecting a new library or framework.
- When changing the project's directory structure.
- When deciding between competing design patterns (e.g., REST vs GraphQL).
- Whenever a decision has a long-term impact on the codebase.

## Workflow

1.  **Identify the Decision**: The `@architect` agent should proactively suggest using this skill when it detects a significant design choice.
2.  **Gather Context**: Interview the user (or search the codebase/web) for:
    - **Title**: Short and descriptive (e.g., "Use PostgreSQL for session storage").
    - **Status**: Proposed, Accepted, Rejected, Deprecated, Superseded.
    - **Context**: What is the problem we are solving? Why now?
    - **Decision**: What exactly was decided?
    - **Consequences**: What are the pros and cons? What technical debt are we accepting?
3.  **Draft the ADR**: Create a file in `docs/decisions/` with the following format:

```markdown
# [Number]. [Title]

Date: YYYY-MM-DD

## Status
[Status]

## Context
[The issue at hand.]

## Decision
[The solution chosen.]

## Consequences
[Pros and cons of this decision.]
```

4.  **Version Control**: Ensure the file is saved with a sequential prefix (e.g., `0001-use-react.md`).

## Tools & Commands
- **`uv run gemini/commands/dependency-analyzer.py`**: Use this to understand the current architecture before making a decision.
- **`glob` / `list_directory`**: Check `docs/decisions/` to find the next available number for the new ADR.
