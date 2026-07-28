---
name: quarto-authoring
description:
  Core syntax, formatting, and authoring for Quarto documents (.qmd). Use
  when writing, styling, and organizing figures, tables, and cross-references in standard
  documents.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: 1.0.1
  tags: documentation, publishing, quarto, reproducibility
  related-with:
    skills:
      - quarto-advanced
      - quarto-migrations
---

# Quarto Authoring (Core)

> Core syntax and authoring workflow for Quarto v1.7.x and later.

## Navigation Protocol

**CRITICAL**: Every reference file in `references/` contains a **Table of Contents (TOC)**. Always read the TOC first to identify relevant sections before processing the entire file. This minimizes context usage and ensures targeted information retrieval.

## Operational Workflows

### 1. Document Creation & Setup

- **Quick Start & Core Syntax**: Execute according to [references/essentials.md](references/essentials.md).
- **YAML Front Matter**: Define document metadata and format options via [references/yaml-front-matter.md](references/yaml-front-matter.md).
- **Markdown Linting**: Follow consistency rules in [references/markdown-linting.md](references/markdown-linting.md).

### 2. Code Cell Management

- **Cell Configuration**: Configure execution options (echo, eval, etc.) via [references/code-cells.md](references/code-cells.md).
- **Diagrams**: Implement Mermaid and Graphviz diagrams using [references/diagrams.md](references/diagrams.md).

### 3. Visuals & Cross-References

- **Figures & Layout**: Manage sizing, alignment, and subfigures via [references/figures.md](references/figures.md) and [references/layout.md](references/layout.md).
- **Tables**: Implement pipe tables and list tables using [references/tables.md](references/tables.md).
- **Cross-References**: Apply prefixes and `@` syntax via [references/cross-references.md](references/cross-references.md).

### 4. Components & Citations

- **Callouts**: Use note, warning, and tip blocks via [references/callouts.md](references/callouts.md).
- **Citations & Footnotes**: Manage bibliography and formatting via [references/citations.md](references/citations.md).
- **Shortcodes**: Use built-in commands (video, include, etc.) via [references/shortcodes.md](references/shortcodes.md).

## Project Scaffolding

Use `assets/boilerplate/website/` for base project configurations. For more complex layouts, consult the `quarto-advanced` skill.

## Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto Guide](https://quarto.org/docs/guide/)
