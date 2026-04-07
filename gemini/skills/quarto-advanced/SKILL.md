---
name: quarto-advanced
description:
  Advanced Quarto formats and features including Dashboards, Manuscripts,
  Typst, and Extensions. Use for complex project layouts, interactive dashboards,
  or modern PDF typesetting.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: 1.0.1
  tags: documentation, publishing, quarto, reproducibility
  related-with:
    skills:
      - quarto-authoring
      - quarto-migrations
---

# Quarto Advanced

> Specialized layouts and modern features for Quarto v1.4+ and later.

## Navigation Protocol

**CRITICAL**: Every reference file in `references/` contains a **Table of Contents (TOC)**. Always read the TOC first to identify relevant sections before processing the entire file. This minimizes context usage and ensures targeted information retrieval.

## Operational Workflows

### 1. Specialized Formats

- **Dashboards**: Create responsive layouts and value boxes via [references/dashboards.md](references/dashboards.md).
- **Manuscripts**: Author scholarly articles with integrated notebooks via [references/manuscripts.md](references/manuscripts.md).
- **Typst**: Utilize the modern PDF engine for high-performance typesetting via [references/typst.md](references/typst.md).

### 2. Project Enhancements

- **Extensions**: Install and manage custom filters, shortcodes, and formats using [references/extensions.md](references/extensions.md).
- **Complex Layouts**: Configure advanced project structures for Books and Multi-format outputs.

## Project Scaffolding

Leverage boilerplate configurations from `assets/boilerplate/` for:

- `dashboard/`: Base YAML for interactive dashboards.
- `manuscript/`: Scholarly publication setup with notebook integration.
- `book/`: Chapter-based project structure.

## Resources

- [Quarto Extensions](https://quarto.org/docs/extensions/)
- [Quarto Manuscripts](https://quarto.org/docs/manuscripts/)
- [Quarto Dashboards](https://quarto.org/docs/dashboards/)
