---
name: quarto
description: >-
  Use proactively for Quarto authoring and rendering: `.qmd` files,
  `_quarto.yml`, `quarto render`, reproducible executable or notebook-backed
  reports, computation engines, and Quarto output formats (HTML, PDF, DOCX,
  Typst, slides). Quarto owns report authoring and rendering when the requested
  target is Quarto; do not route generic documents or reports here without
  Quarto context.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: 1.0.1
  tags: documentation, quarto, reproducibility
---

# Quarto

> Author, configure, and render Quarto projects safely.

## Operating rules

- Inspect the repository before editing: project root, `_quarto.yml`, profile
  files, document YAML, existing output settings, `quarto --version`, and the
  selected computation engine. Follow existing conventions and make the
  smallest viable change.
- Reference files have TOCs. Read the TOC, then only the relevant section.
- Do not assume a Quarto version or format capability. Check the installed
  executable and its release notes/help before proposing version-sensitive
  syntax or support. These references are guidance, not a fixed capability
  contract.
- Ask before executing unfamiliar code, installing/updating extensions, or
  performing a full render. Explain the command's scope and generated files.

## Route the task

| Need | Read first | Then |
| --- | --- | --- |
| Cross-references for sections, figures, tables, equations, subfigures, custom types, or code listings | [cross-references](references/cross-references.md) | Targeted format or engine reference if needed |
| Document content, YAML, citations, figures, tables | [essentials](references/essentials.md), [YAML](references/yaml-front-matter.md) | Targeted core reference below |
| Project settings, profiles, metadata, precedence | [project configuration](references/project-configuration.md) | [profiles and metadata](references/profiles-directory-metadata.md) |
| Output-format choice, portability, or dependencies | [rendering formats](references/rendering-formats.md) | Targeted format or engine reference |
| Slides | [RevealJS](references/revealjs.md) | [figures](references/figures.md) |
| Executable cells or environments | [engines and environments](references/engines-environments.md) | [code cells](references/code-cells.md) |
| Render failure or CLI use | [CLI and troubleshooting](references/cli-troubleshooting.md) | Targeted format/engine reference |
| Typst or extension | [Typst](references/typst.md) or [extensions](references/extensions.md) | Verify installed capability |

Core topics: [code cells](references/code-cells.md), [figures](references/figures.md),
[tables](references/tables.md),
[cross-references](references/cross-references.md),
[layout](references/layout.md), [callouts](references/callouts.md),
[citations](references/citations.md), [shortcodes](references/shortcodes.md),
[divs and spans](references/divs-and-spans.md), and
[conditional content](references/conditional-content.md).

## Configuration and format guardrails

- Treat document YAML as local intent and project/profile configuration as
  shared intent. Resolve conflicts from the effective configuration produced by
  the selected profile; do not duplicate settings merely to override them.
- A format can have distinct HTML, PDF/TeX, Typst, DOCX, and RevealJS
  capabilities. Do not copy options across formats without checking support.
  PDF may require TeX; Typst and RevealJS require their own supported workflow;
  interactive features may not survive static or non-HTML output.
- Keep directory metadata, resources, output directories, and profile names
  consistent with the current project. Avoid changing ignored/generated output
  unless requested.

## Verify and report

- Prefer a targeted render or static configuration check after authorization.
- When reference documentation changes, run the read-only
  [reference-link validator](scripts/validate_reference_links.py):
  `python3 skills/quarto/scripts/validate_reference_links.py`.
- If Quarto is missing, report the missing executable and provide installation
  guidance; do not fabricate render results. If an engine is missing, identify
  the requested engine/environment and stop before installing it. If PDF fails
  because TeX is absent, report that dependency and offer a supported alternate
  output or installation step.
- Report files changed, profile/format/engine used, commands actually run,
  validation result, generated output, and unverified assumptions.
