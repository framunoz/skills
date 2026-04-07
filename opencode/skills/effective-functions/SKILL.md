---
name: effective-functions
description: Design clear, maintainable, and effective functions. Focuses on SRP, pure functions, and readable code. Use when writing functions, refactoring complex logic, or reviewing code for readability.
compatibility: OpenCode
metadata:
  author: Francisco Muñoz (@framunoz)
  source: https://github.com/framunoz/skills/blob/main/opencode/skills/effective-functions/
  version: "1.1.1"
  last-updated: "2026-04-06"
  tags: clean-code,functions,functional-programming,readability
  related-with:
    skills:
      - adr-manager
    agents:
      - architect
    commands:
      - adr-manager
---

# Effective Functions (Clean Code)

Build functions that are easy to understand, test, and maintain.

## Core Resources

- **Clean Code Principles**: See [clean-code-principles.md](references/clean-code-principles.md) for detailed guidelines on SRP, Pure Functions, and Readability.

## Workflow

1.  **Draft Signature**: Decide inputs and outputs.
2.  **Apply SRP**: Use the [clean-code-principles.md](references/clean-code-principles.md) to ensure the function does one thing.
3.  **Refactor**: Reduce complexity by using guard clauses and extracting small, focused helper functions.

## Best Practices

- **Guard Clauses**: Exit early.
- **Fail Fast**: Validate early.
- **Isolate Side Effects**: Keep core logic pure.
- **Small is Beautiful**: Keep functions under 20 lines of code.
