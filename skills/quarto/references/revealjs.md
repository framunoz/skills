# Quarto RevealJS Presentations

Quarto RevealJS is the Quarto format for HTML slide presentations.

## Table of Contents

- [Minimal Format](#minimal-format)
- [Slides and Features](#slides-and-features)
- [Capability Warnings](#capability-warnings)
- [Verification](#verification)

## Minimal Format

Choose `format: revealjs` in document YAML or the project configuration, then
follow local title, theme, and slide conventions. For YAML structure, see
[YAML front matter](yaml-front-matter.md).

## Slides and Features

Use headings and explicit slide separators according to existing presentation
style. Reuse [figures](figures.md), [code cells](code-cells.md), and
[shortcodes](shortcodes.md) for their respective syntax. Treat plugins and
extensions as executable third-party code: inspect and obtain authorization
before installation or upgrade.

## Capability Warnings

RevealJS targets HTML. Do not assume RevealJS options, live code, interactive
widgets, or speaker tooling transfer to PDF, DOCX, or other formats. Check the
installed Quarto version before introducing version-sensitive presentation
features.

## Verification

Ask before previewing or rendering. When authorized, verify the selected format,
asset paths, slide navigation, and any executed cells. Use
[CLI and troubleshooting](cli-troubleshooting.md) for render failures.
