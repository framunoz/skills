---
name: mermaid
description: Create, edit, fix, and validate supported Mermaid diagrams and Mermaid code blocks. Use proactively when users ask to explain a concept simply or visually, or to diagram workflows, architectures, dependencies, sequences, states, or relationships. This is the primary skill when a diagram is the requested artifact; it can support document-writing skills when a Mermaid diagram is embedded in the document. Select the appropriate registered type through this skill's router.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: 2.0.0
  mermaid_baseline: 11.16.0
  last_verified: 2026-07-28
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

Use this reproducible protocol for every authored or revised diagram:

1. Record the target host/renderer and its Mermaid version when known; then read the selected reference for its minimum-version and beta or experimental constraints.
2. Check the source before rendering: use the selected declaration, retain stable identifiers on revisions, and confirm referenced nodes or participants, delimiters, indentation, and labels are valid for that type.
3. Use repository-provided renderer tooling when it exists. Record the exact command, renderer name and version, input source, and rendered output or error. Do not install a renderer or invent a command solely for validation.
4. If no renderer tooling or target version is available, report `rendering unverified` and record the source review, the unavailable renderer/tooling, the assumed or unknown target version, and any type-specific compatibility risk. Do not represent source review as a successful render.
5. Report validation as `passed`, `failed`, or `rendering unverified`; include warnings for beta, experimental, or version-gated syntax.

Repository tooling is discovered from the available project scripts and installed commands. This repository currently provides no Mermaid renderer command, so use the conditional no-renderer branch unless a target host supplies one.

## Security and accessibility

- Add `click` interactions only when the requested target supports them and interaction is necessary. Link only to trusted, appropriate destinations; do not embed callbacks or executable JavaScript, and do not expose sensitive data in URLs or labels.
- Treat interaction as an enhancement, not the only path to meaning: keep the diagram understandable without clicking and describe its destination or action in nearby text when it is material.
- Do not assume Mermaid syntax provides accessible names, descriptions, or keyboard behavior in every host. Supply a concise surrounding textual summary when needed, and verify the target host's rendered accessibility separately before claiming it.

## Scope boundary

This skill covers only types registered in [the router](references/router.md). Styling, theming, unrelated Mermaid diagram types, and unregistered requests are out of scope; do not invent guidance for them.
