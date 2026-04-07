---
name: effective-functions
description: Design clear, maintainable, and effective functions. Focuses on SRP, pure functions, and readable code.
metadata:
  author: Gemini CLI (@architect)
  version: "1.0.0"
  last-updated: "2026-04-06"
  tags: clean-code,functions,functional-programming,readability
---

# Effective Functions (Clean Code)

Functions are the building blocks of every software. This skill helps you build them to be solid and easy to understand.

## Core Principles

### 1. Single Responsibility Principle (SRP)
- A function should do **one** thing and do it well.
- If a function is too long (e.g., > 20 lines), it probably does too much.

### 2. Pure Functions
- Given the same input, always return the same output.
- No side effects (don't modify global state, don't perform I/O unless that is the function's explicit purpose).

### 3. Clear Names
- Names should describe what the function **does**, not how it does it.
- Prefer verbs for function names (e.g., `calculate_total`, `fetch_user`).

### 4. Minimal Arguments
- Prefer 0-2 arguments. If you need more, consider passing an object/dictionary.

## Workflow

1.  **Draft the Signature**: Decide what the function needs (input) and what it provides (output).
2.  **Review for SRP**: Can the function be split into smaller, more focused functions?
3.  **Check for Side Effects**: Is it clear where side effects (like database writes) occur?
4.  **Refactor for Readability**: Use guard clauses to reduce nesting. Use descriptive names for intermediate variables.

## Best Practices
- **Guard Clauses**: Exit early to avoid deeply nested `if` statements.
- **Fail Fast**: Validate inputs at the beginning of the function.
- **Avoid Boolean Flags**: Instead of `process_data(data, is_admin)`, use two separate functions: `process_data_as_admin(data)` and `process_data_as_user(data)`.
- **Command-Query Separation (CQS)**: A function should either be a command (does something) or a query (returns something), but not both.
