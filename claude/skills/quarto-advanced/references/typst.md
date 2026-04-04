# Typst

Typst (introduced in v1.4) is a modern typesetting system designed as an alternative to LaTeX. It provides high-performance rendering and a simpler syntax for layout and styling.

## Table of Contents

* [Basic Typst Configuration](#basic-typst-configuration)
* [Typography and Layout](#typography-and-layout)
* [Columns](#columns)
* [Math and Equations](#math-and-equations)
* [Styling with Typst Blocks](#styling-with-typst-blocks)
* [Advanced Customization](#advanced-customization)
* [Typst Features](#typst-features)
* [Comparison with PDF (LaTeX)](#comparison-with-pdf-latex)
* [Resources](#resources)

## Basic Typst Configuration

```yaml
---
title: "My Typst Document"
format: typst
---

## Introduction

Content here.
```

## Typography and Layout

Typst documents can be configured in YAML:

```yaml
format:
  typst:
    papersize: a4
    margin:
      x: 2cm
      y: 2cm
    mainfont: "Linux Libertine"
    fontsize: 11pt
    section-numbering: "1.1"
```

## Columns

Enable multiple columns:

```yaml
format:
  typst:
    columns: 2
```

Or for a specific section:

```markdown
::: {.columns-2}
Content in two columns.
:::
```

## Math and Equations

Typst has native math support, and Quarto translates standard LaTeX math for Typst:

```markdown
$$
E = mc^2
$$ {#eq-energy}

See @eq-energy.
```

## Styling with Typst Blocks

Insert raw Typst code:

```markdown
```{=typst}
#align(center)[
  *Centered and bold* in Typst.
]
```
```

## Advanced Customization

Use a custom Typst template:

```yaml
format:
  typst:
    template: my-template.typ
```

## Typst Features

| Feature | Description |
| --- | --- |
| `format: typst` | Enables Typst output format |
| `papersize` | Set paper dimensions (e.g., `a4`, `us-letter`) |
| `mainfont` | Specify document font |
| `columns` | Set number of columns |
| `include-in-header` | Add custom Typst commands |
| `typst-package` | Use Typst packages |

## Comparison with PDF (LaTeX)

| Feature | PDF (LaTeX) | Typst |
| --- | --- | --- |
| **Speed** | Slower | Very Fast |
| **Syntax** | Complex | Simple/Modern |
| **Fonts** | System dependent | Direct access |
| **Output** | PDF | PDF |

## Resources

- [Quarto Typst](https://quarto.org/docs/output-formats/typst.html)
- [Typst Documentation](https://typst.app/docs/)
- [Typst Universe (Packages)](https://typst.app/universe/)
