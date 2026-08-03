---
name: quarto
description: >-
  Use proactively for Quarto authoring and rendering: `.qmd` files,
  `_quarto.yml`, `quarto render`, reproducible executable or notebook-backed
  reports, websites, books, dashboards, manuscripts, computation engines,
  render/publish workflows, and Quarto output formats (HTML, PDF, DOCX, Typst,
  slides). Quarto owns report authoring and rendering when the requested target
  is Quarto; do not route generic documents or reports here without Quarto
  context.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: 1.0.1
  tags: documentation, publishing, quarto, reproducibility
---

# Quarto

> Author, configure, render, and publish Quarto projects safely.

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
- Ask before executing unfamiliar code, installing/updating extensions,
  performing a full render, or publishing/deploying. Explain the command's
  scope, network effects, generated files, and credentials required.

## Route the task

| Need | Read first | Then |
| --- | --- | --- |
| Document content, YAML, citations, figures, tables | [essentials](references/essentials.md), [YAML](references/yaml-front-matter.md) | Targeted core reference below |
| Project settings, profiles, metadata, precedence | [project configuration](references/project-configuration.md) | [profiles and metadata](references/profiles-directory-metadata.md) |
| Website, blog, navigation, listings | [websites, blogs, listings](references/websites-blogs-listings.md) | [project configuration](references/project-configuration.md) |
| Book or chapters | [books](references/books.md) | [cross-references](references/cross-references.md) |
| Slides | [RevealJS](references/revealjs.md) | [diagrams](references/diagrams.md) |
| Executable cells or environments | [engines and environments](references/engines-environments.md) | [code cells](references/code-cells.md) |
| Render failure or CLI use | [CLI and troubleshooting](references/cli-troubleshooting.md) | Targeted format/engine reference |
| Dashboard, manuscript, Typst, extension | [dashboards](references/dashboards.md), [manuscripts](references/manuscripts.md), [Typst](references/typst.md), or [extensions](references/extensions.md) | Verify installed capability |
| Hosting or release | [publishing and deployment](references/publishing-deployment.md) | Ask before publish |

Core topics: [code cells](references/code-cells.md), [diagrams](references/diagrams.md),
[figures](references/figures.md), [tables](references/tables.md),
[layout](references/layout.md), [callouts](references/callouts.md),
[citations](references/citations.md), [shortcodes](references/shortcodes.md),
[divs and spans](references/divs-and-spans.md), and
[conditional content](references/conditional-content.md).

## Configuration and format guardrails

- Treat document YAML as local intent and project/profile configuration as
  shared intent. Resolve conflicts from the effective configuration produced by
  the selected profile; do not duplicate settings merely to override them.
- A format can have distinct HTML, PDF/TeX, Typst, DOCX, RevealJS, and dashboard
  capabilities. Do not copy options across formats without checking support.
  PDF may require TeX; Typst and RevealJS require their own supported workflow;
  interactive features may not survive static or non-HTML output.
- Keep directory metadata, resources, output directories, and profile names
  consistent with the current project. Avoid changing ignored/generated output
  or deployment configuration unless requested.

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
