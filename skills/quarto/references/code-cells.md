# Code Cells

Quarto uses a hashpipe (`#|`) syntax for code cell options, providing a clean, YAML-based approach that works across R, Python, Julia, and other languages.

## Table of Contents

* [Hashpipe Syntax](#hashpipe-syntax)
* [Execution Options](#execution-options)
  * [Examples](#examples)
* [Figure Options](#figure-options)
  * [Figure Example](#figure-example)
  * [Multiple Figures](#multiple-figures)
* [Table Options](#table-options)
  * [Table Example](#table-example)
* [Caching and Freeze](#caching-and-freeze)
  * [Caching Example](#caching-example)
  * [Project-Level Freeze](#project-level-freeze)
  * [Cache Limits and Invalidation](#cache-limits-and-invalidation)
  * [Execution Directory](#execution-directory)
  * [Fresh Execution or Saved Results](#fresh-execution-or-saved-results)
* [Document-Level Defaults](#document-level-defaults)
* [Code Display Options](#code-display-options)
  * [Code Folding](#code-folding)
  * [Code Tools](#code-tools)
  * [Line Numbers](#line-numbers)
* [Code Annotations](#code-annotations)
* [Filename Display](#filename-display)
* [Resources](#resources)

## Hashpipe Syntax

Code cell options are specified with `#|` at the start of lines within the code block:

````markdown
```{r}
#| label: fig-scatter
#| echo: false
#| fig-cap: "A scatter plot of x versus y."
#| fig-width: 8
#| fig-height: 6

plot(x, y)
```
````

````markdown
```{python}
#| label: fig-histogram
#| fig-cap: "Distribution of values."

import matplotlib.pyplot as plt
plt.hist(data)
plt.show()
```
````

**Important:** Options use **dashes, not dots**. Use `fig-cap` not `fig.cap`, `fig-width` not `fig.width`.

## Execution Options

Control whether and how code is executed:

| Option    | Description                               | Values                    |
| --------- | ----------------------------------------- | ------------------------- |
| `eval`    | Evaluate the code                         | `true`, `false`           |
| `echo`    | Include source code in output             | `true`, `false`, `fenced` |
| `output`  | Include results in output                 | `true`, `false`, `asis`   |
| `warning` | Include warnings                          | `true`, `false`           |
| `error`   | Include errors (stop on error if `false`) | `true`, `false`           |
| `include` | Include cell in output at all             | `true`, `false`           |

### Examples

Show code but don't run it:

````markdown
```{r}
#| eval: false

# This code is displayed but not executed
x <- 1 + 1
```
````

Run code but hide it:

````markdown
```{r}
#| echo: false

# This code runs but is not shown
library(ggplot2)
```
````

Show fenced code block with attributes:

````markdown
```{r}
#| echo: fenced

plot(1:10)
```
````

## Figure Options

Options for controlling figure output:

| Option             | Description                      | Example                         |
| ------------------ | -------------------------------- | ------------------------------- |
| `fig-cap`          | Figure caption                   | `"A descriptive caption."`      |
| `fig-subcap`       | Subcaptions for multiple figures | `["Plot A", "Plot B"]`          |
| `fig-width`        | Width in inches                  | `8`                             |
| `fig-height`       | Height in inches                 | `6`                             |
| `fig-alt`          | Alt text for accessibility       | `"Scatter plot showing..."`     |
| `fig-align`        | Alignment                        | `"left"`, `"center"`, `"right"` |
| `fig-cap-location` | Caption position                 | `"top"`, `"bottom"`, `"margin"` |
| `fig-format`       | Output format                    | `"png"`, `"svg"`, `"pdf"`       |
| `fig-dpi`          | Resolution in DPI                | `300`                           |

### Figure Example

````markdown
```{r}
#| label: fig-analysis
#| fig-cap: "Analysis results showing the relationship between variables."
#| fig-alt: "Scatter plot with trend line showing positive correlation."
#| fig-width: 10
#| fig-height: 6
#| fig-align: center

ggplot(data, aes(x, y)) +
  geom_point() +
  geom_smooth()
```
````

### Multiple Figures

````markdown
```{r}
#| label: fig-panels
#| fig-cap: "Multiple panel figure."
#| fig-subcap:
#|   - "Distribution of X"
#|   - "Distribution of Y"
#| layout-ncol: 2

hist(x)
hist(y)
```
````

## Table Options

Options for controlling table output:

| Option             | Description                     | Example                         |
| ------------------ | ------------------------------- | ------------------------------- |
| `tbl-cap`          | Table caption                   | `"Summary statistics."`         |
| `tbl-subcap`       | Subcaptions for multiple tables | `["Table A", "Table B"]`        |
| `tbl-colwidths`    | Column widths                   | `[40, 60]` or `"auto"`          |
| `tbl-cap-location` | Caption position                | `"top"`, `"bottom"`, `"margin"` |

### Table Example

````markdown
```{r}
#| label: tbl-summary
#| tbl-cap: "Summary statistics by group."

knitr::kable(summary_data)
```
````

## Caching and Freeze

Control caching of code cell results:

| Option       | Description                         | Values                    |
| ------------ | ----------------------------------- | ------------------------- |
| `cache`      | Cache results                       | `true`, `false`           |
| `cache-lazy` | Use lazy loading for cached objects | `true`, `false`           |
| `freeze`     | Reuse previously computed execution results | `true`, `false`, `"auto"` |

### Caching Example

````markdown
```{r}
#| label: slow-computation
#| cache: true

# This expensive computation is cached
result <- slow_function(data)
```
````

### Project-Level Freeze

In `_quarto.yml`:

```yaml
execute:
  freeze: auto # Re-execute when the source changes
```

`freeze: true` keeps saved execution results until an explicit refresh;
`freeze: auto` refreshes when Quarto detects a source change; and `freeze: false`
allows normal execution. Freeze controls execution results, not every generated
file or external dependency.

### Cache Limits and Invalidation

`cache` is engine-specific and is not a correctness guarantee. It can avoid
recomputing cells, but it cannot reliably detect changes to remote data, local
files read outside tracked inputs, environment variables, credentials, package
versions, or nondeterministic code. Confirm the engine's established cache
layout before enabling it, and do not manually edit cache artifacts.

Invalidate or bypass saved results by choosing a fresh authorized execution when
the code, input data, parameters, environment, kernel, packages, or expected
result has changed. Prefer the engine's documented cache-clear mechanism over
deleting unknown generated directories. Record what was refreshed and why.
For a targeted refresh where supported, use `--cache-refresh` with an explicit
document and format after checking `quarto render --help`.

### Execution Directory

Set `execute-dir` deliberately when code uses relative paths. `file` resolves
relative paths from the document's directory; `project` resolves them from the
project root. Use the repository's existing convention and avoid relying on the
current shell directory.

```yaml
execute-dir: project

execute:
  freeze: auto
```

### Fresh Execution or Saved Results

Use saved results only when the document source and known inputs are unchanged,
the existing output is the intended review artifact, and the task does not need
to verify current computation. Choose a fresh execution when validating a
result, changing data or dependencies, investigating a failure, or producing a
new reproducible result. Before either choice, state the selected engine,
profile, execution directory, expected side effects, and output location.

For a narrow, authorized refresh, use the target document and format explicitly:

```bash
quarto render report.qmd --to html --execute
```

To render without executing cells, use `--no-execute` only when saved results
are present and appropriate. Confirm supported execution flags with
`quarto render --help` for the installed version.

## Document-Level Defaults

Set defaults for all code cells in YAML front matter:

```yaml
title: "My Document"
execute:
  echo: false
  warning: false
  message: false
```

Or per-format:

```yaml
format:
  html:
    code-fold: true
  pdf:
    echo: false
```

## Code Display Options

Control how code is displayed in HTML output:

| Option              | Description          | Values                    |
| ------------------- | -------------------- | ------------------------- |
| `code-fold`         | Collapsible code     | `true`, `false`, `"show"` |
| `code-summary`      | Text for fold toggle | `"Show code"`             |
| `code-tools`        | Code tools menu      | `true`, `false`           |
| `code-line-numbers` | Show line numbers    | `true`, `false`           |
| `code-overflow`     | Handle overflow      | `"scroll"`, `"wrap"`      |

### Code Folding

In YAML front matter:

```yaml
format:
  html:
    code-fold: true
    code-summary: "Click to see code"
```

Per cell override:

````markdown
```{r}
#| code-fold: show

# This code is visible by default
plot(1:10)
```
````

### Code Tools

Enable the code tools dropdown menu:

```yaml
format:
  html:
    code-tools: true
```

This adds a menu to toggle all code visibility and view source.

### Line Numbers

````markdown
```{r}
#| code-line-numbers: true

# Lines will be numbered
x <- 1
y <- 2
z <- x + y
```
````

Or highlight specific lines:

````markdown
```{r}
#| code-line-numbers: "2-3"

x <- 1
y <- 2  # highlighted
z <- 3  # highlighted
```
````

## Code Annotations

Add annotations to explain code:

````markdown
```{r}
#| code-annotations: hover

library(tidyverse)
mtcars |>                 # <1>
  filter(mpg > 20) |>     # <2>
  select(mpg, cyl, hp)    # <3>
```
````

1. Start with the mtcars dataset
2. Filter to cars with MPG over 20
3. Select only the columns we need

Annotation styles: `hover`, `select`, `below`, `beside`.

## Filename Display

Show a filename above the code block:

````markdown
```{python}
#| filename: "analysis.py"

import pandas as pd
df = pd.read_csv("data.csv")
```
````

## Resources

- [Quarto Code Cells](https://quarto.org/docs/computations/execution-options.html)
- [Quarto Figures](https://quarto.org/docs/authoring/figures.html)
- [Code Annotation](https://quarto.org/docs/authoring/code-annotation.html)
