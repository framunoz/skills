---
name: mermaid
description: Create and revise supported Mermaid diagrams. Use when a user needs to author, update, or validate a Mermaid diagram, then select the appropriate registered type through this skill's router.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: 2.0.0
  tags: diagrams, documentation, mermaid
---

# Mermaid Diagram Router

> **Start with [the diagram type router](references/router.md).** It selects the registered type and its focused syntax reference.

Use this skill to author or revise supported Mermaid diagrams.

## Global workflow

1. Identify the information structure and select a registered type in the router.
2. Read the selected type's reference before authoring or revising syntax.
3. Use stable identifiers and the simplest constructs that preserve the intended meaning.
4. Apply the validation and compatibility policy below.

## Validation and compatibility

Determine the target renderer and version when relevant. Render when tooling is available; otherwise state that rendering is unverified. Type-specific compatibility and beta/experimental status belong in the selected reference.

## Scope boundary

This skill covers only types registered in [the router](references/router.md). Styling, theming, unrelated Mermaid diagram types, and unregistered requests are out of scope; do not invent guidance for them.
