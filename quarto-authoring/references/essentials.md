# Quarto Essentials

This guide covers the core components and syntax of Quarto documents (.qmd).

## Table of Contents

* [Basic Document Structure](#basic-document-structure)
* [Divs and Spans](#divs-and-spans)
* [Code Cell Options Syntax](#code-cell-options-syntax)
* [Cross-References](#cross-references)
* [Callout Blocks](#callout-blocks)
* [Figures and Tables](#figures-and-tables)
  * [Figures](#figures)
  * [Tables](#tables)
* [Citations](#citations)
* [Resources](#resources)

## Basic Document Structure

A Quarto document consists of two main parts:

1. **YAML Front Matter**: Metadata and configuration at the top, enclosed by `---`.
2. **Markdown Content**: Main body using standard markdown syntax.

```markdown
---
title: "Document Title"
author: "Author Name"
date: today
format: html
---

Content goes here.
```

## Divs and Spans

Divs use fenced syntax with three colons:

```markdown
::: {.class-name}
Content inside the div.
:::
```

Spans use bracketed syntax:

```markdown
This is [important text]{.highlight}.
```

Details: [references/divs-and-spans.md](references/divs-and-spans.md)

## Code Cell Options Syntax

Quarto uses the language's comment symbol + `|` for cell options. Options use **dashes, not dots** (e.g., `fig-cap` not `fig.cap`).

- R, Python: `#|`
- Mermaid: `%%|`
- Graphviz/DOT: `//|`

````markdown
```{r}
#| label: fig-example
#| echo: false
#| fig-cap: "A scatter plot example."
#| fig-width: 8
#| fig-height: 6

plot(x, y)
```
````

Common execution options:

| Option    | Description       | Values                    |
| --------- | ----------------- | ------------------------- |
| `eval`    | Evaluate code     | `true`, `false`           |
| `echo`    | Show code         | `true`, `false`, `fenced` |
| `output`  | Include output    | `true`, `false`, `asis`   |
| `warning` | Show warnings     | `true`, `false`           |
| `error`   | Show errors       | `true`, `false`           |
| `include` | Include in output | `true`, `false`           |

Details: [references/code-cells.md](references/code-cells.md)

## Cross-References

Labels must start with a type prefix. Reference with `@`:

- Figure: `fig-` prefix, e.g., `#| label: fig-plot` → `@fig-plot`
- Table: `tbl-` prefix, e.g., `#| label: tbl-data` → `@tbl-data`
- Section: `sec-` prefix, e.g., `{#sec-intro}` → `@sec-intro`
- Equation: `eq-prefix`, e.g., `{#eq-model}` → `@eq-model`

Details: [references/cross-references.md](references/cross-references.md)

## Callout Blocks

Five types: `note`, `warning`, `important`, `tip`, `caution`.

```markdown
::: {.callout-note}
This is a note callout.
:::
```

Details: [references/callouts.md](references/callouts.md)

## Figures and Tables

### Figures

```markdown
![Caption text](image.png){#fig-name fig-alt="Alt text"}
```

### Tables

```markdown
::: {#tbl-example}

| Column 1 | Column 2 |
| -------- | -------- |
| Data 1   | Data 2   |

Table caption.
:::
```

Details: [references/figures.md](references/figures.md) and [references/tables.md](references/tables.md)

## Citations

```markdown
According to @smith2020, the results show...
Multiple citations [@smith2020; @jones2021].
```

Details: [references/citations.md](references/citations.md)

## Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto Guide](https://quarto.org/docs/guide/)
