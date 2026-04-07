---
name: effective-functions
description: Design clear, maintainable, and effective functions. Focuses on SRP, pure functions, and readable code. Use when writing functions, refactoring complex logic, or reviewing code for readability.
metadata:
  author: Gemini CLI (@architect)
  version: "1.1.0"
  last-updated: "2026-04-06"
  tags: clean-code,functions,functional-programming,readability
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
