---
name: quarto-migrations
description:
  Migrate legacy R Markdown projects (blogdown, bookdown, distill, xaringan)
  to Quarto. Use when converting .Rmd files or existing project structures to Quarto-compatible
  formats.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: 1.0.1
  tags: documentation, publishing, quarto, reproducibility
  related-with:
    skills:
      - quarto-advanced
      - quarto-authoring
---

# Quarto Migrations

> Specialized workflow for converting legacy R Markdown projects to Quarto.

## Navigation Protocol

**CRITICAL**: Every reference file in `references/` contains a **Table of Contents (TOC)**. Always read the TOC first to identify relevant sections before processing the entire file. This minimizes context usage and ensures targeted information retrieval.

## Operational Workflows

### 1. Automated Syntax Conversion

- **Renaming & Chunk Options**: Run `scripts/rmd_to_qmd.py` on your `.Rmd` files to automate the dot-to-dash conversion and hashpipe syntax.
- **R Markdown Base Guide**: Follow general transition steps in [references/conversion-rmarkdown.md](references/conversion-rmarkdown.md).

### 2. Specialized Project Migrations

- **Books (Bookdown)**: Migrate multi-file projects and cross-references via [references/conversion-bookdown.md](references/conversion-bookdown.md).
- **Websites (Blogdown)**: Convert Hugo-based sites to Quarto websites via [references/conversion-blogdown.md](references/conversion-blogdown.md).
- **Academic Articles (Distill)**: Map author metadata and asides using [references/conversion-distill.md](references/conversion-distill.md).
- **Presentations (Xaringan)**: Convert slides to RevealJS using [references/conversion-xaringan.md](references/conversion-xaringan.md).

## Conversion Troubleshooting

Always verify manual changes after running automation, particularly for complex LaTeX math or custom CSS styling that might differ between formats.

## Resources

- [Quarto for R Markdown Users](https://quarto.org/docs/faq/rmarkdown.html)
- [Quarto vs R Markdown](https://quarto.org/docs/faq/rmarkdown.html#quarto-vs.-r-markdown)
