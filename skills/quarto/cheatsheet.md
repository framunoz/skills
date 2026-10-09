# Cheatsheet: decisions

## Which format?

| Need | Format |
|---|---|
| Analysis report read on screen, interactive plots, code optional | `html` |
| Same, as one file to email | `html` + `embed-resources: true` |
| Talk / meeting deck | `revealjs` |
| Deck that must be edited in PowerPoint by others | `pptx` (limited layout control) |
| Printed / formal PDF, fast, no TeX | `typst` |
| PDF with journal template, heavy LaTeX math or packages | `pdf` (LaTeX) |
| Reviewers want tracked changes | `docx` |
| KPI overview, at-a-glance cards | `dashboard` |
| Collection of reports/notes with navigation | `website` project |
| Long structured text with chapters | `book` project |
| Journal article with notebooks | `manuscript` project |

## Which engine?

| Situation | Choose |
|---|---|
| R only | knitr (automatic) |
| Python only | jupyter (automatic); run through `uv run` |
| Mostly R, a few Python steps | knitr + reticulate (automatic when `{r}` present) |
| Mostly Python, one R step | jupyter for the doc; do the R step in a separate `.qmd`/script and `{{< embed >}}` or read its output |
| Julia | `engine: julia` (native) or jupyter IJulia (default) |
| No code | `engine: markdown` (or nothing) |

## freeze vs cache

| Goal | Use |
|---|---|
| CI/publishing must not need R/Python | `freeze: auto` + commit `_freeze/` |
| Old posts must never re-run | `freeze: true` (per directory via `_metadata.yml`) |
| Iterate faster on one slow document | `cache: true` (knitr per cell; jupyter needs `jupyter-cache`) |
| Results depend on changing data | neither — render explicitly, or clear `_freeze/` on data updates |

## PDF engine

| Situation | Choose |
|---|---|
| No TeX installed, want speed | `format: typst` |
| Default LaTeX | `pdf` → `lualatex` (1.8+) |
| Legacy doc built for `xelatex` (fontspec/CJK setups) | `pdf-engine: xelatex` |
| Strict pdflatex-only template | `pdf-engine: pdflatex` |

## Where does this option go?

| Scope | Place |
|---|---|
| Every document in the project | `_quarto.yml` |
| Every document in one folder | `folder/_metadata.yml` |
| Only my machine | `_quarto.yml.local` |
| Only for a deliverable build | `_quarto-<profile>.yml` + `--profile` |
| One document | front matter |
| One format of one document | `format: <fmt>:` block |
| One cell | `#|` cell option |

## Code visibility (reports)

| Audience | Settings |
|---|---|
| Executives | `echo: false`, `warning: false`, `message: false` |
| Analysts who may audit | `code-fold: true`, `code-tools: true` |
| Teaching / tutorials | `echo: true`, `code-annotations: hover`, `code-copy: true` |
| Slides | revealjs default `echo: false`; `echo: true` + `code-line-numbers` steps when showing code |

## Interactive in HTML?

| Need | Use |
|---|---|
| Hover/zoom on a plot | plotly / htmlwidgets / altair |
| Filterable table | `DT`, `reactable` (R); `itables` (Python) |
| Linked filters, no server | Observable JS (`{ojs}`) |
| Server-side computation on input | Shiny (`server: shiny`) — needs hosting |
