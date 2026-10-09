# Execution: engines, environments, freeze, parameters

## Engines

An engine runs the code cells and hands Pandoc a plain `.md`. One engine per document.

| Document contains | Engine chosen | Notes |
|---|---|---|
| Any `{r}` cell (with or without `{python}`/`{bash}`) | `knitr` | Python cells run via **reticulate**; objects shared both ways |
| Only `{python}` | `jupyter` | One kernel per document (default `python3`) |
| `{julia}` | `jupyter` (IJulia) by default | Native engine needs `engine: julia`, or `engines: ['julia']` in `_quarto.yml` (1.7+); bundled as an extension since 1.9 |
| No executable cells | `markdown` | No execution at all |

Override in front matter: `engine: knitr` / `engine: jupyter` / `engine: markdown`, or
`jupyter: python3` (picks a kernel, implies jupyter), or `knitr: true`.

Observable JS (`{ojs}`) is not an engine: it runs in the browser on any engine; pass data to it
with `ojs_define(df)` from R or Python.

### R and Python in one document

This is a Quarto + knitr feature (not an IDE feature — Positron just lets R and Python consoles run
side by side while you work interactively).

```{r}
library(reticulate)
df <- data.frame(x = 1:3)
```

```{python}
import pandas as pd
r.df.describe()        # R objects from Python: r.<name>
py_list = [1, 2, 3]
```

```{r}
py$py_list             # Python objects from R: py$<name>
```

The Python used by reticulate is **not** automatically the project's `.venv`. Pin it — see
Environments below.

## Environments (verified on 1.10.19, macOS)

### Python with uv

The Quarto CLI picks Python from `PATH` (or `QUARTO_PYTHON`). It does **not** discover a
project `.venv` by itself, even with a `_quarto.yml` present. The venv needs Jupyter:
`uv add --dev jupyter`.

- `uv run quarto render` / `uv run quarto preview` — puts `.venv/bin` on `PATH`. Preferred.
- Or `QUARTO_PYTHON=.venv/bin/python quarto render`.
- For reticulate (mixed R + Python): `Sys.setenv(RETICULATE_PYTHON = ".venv/bin/python")` in the
  project `.Rprofile`, or `RETICULATE_PYTHON=.venv/bin/python` in `.Renviron`.
- `quarto check jupyter` reports which Python and Jupyter Quarto sees — run it through `uv run` too.

IDEs (Positron, VS Code, RStudio) auto-select a venv for *their* sessions; that does not change
what the CLI uses in a terminal or CI.

### R with renv

knitr starts R, and R reads `.Rprofile` (which activates renv) from its startup directory:

- **With a `_quarto.yml`**: R starts at the project root, so the root `.Rprofile` loads for every
  document, whatever directory you invoke `quarto` from.
- **Without a `_quarto.yml`**: R starts in the shell's current directory. Running
  `cd sub && quarto render doc.qmd` skips the root `.Rprofile` → renv inactive → wrong library.

So: put a `_quarto.yml` (even just `project: {type: default}`) at the renv root.

### Working directory

Code runs with the **document's directory** as working directory. Set `execute-dir: project`
under `project:` to run from the project root instead (useful when data paths are root-relative).
Prefer root-relative paths built with `here::here()` (R) or `pathlib` from a known anchor (Python).

## Execution options

Set under `execute:` (document or `_quarto.yml`) or per cell with `#|`.

| Option | Values | Effect |
|---|---|---|
| `eval` | `true`/`false`/line numbers | Run the code |
| `echo` | `true`/`false`/`fenced` | Show source (`fenced` shows the ```` ```{r} ```` fence too) |
| `output` | `true`/`false`/`asis` | Show results; `asis` emits raw Markdown |
| `warning`, `message` | bool | Show warnings / messages (`message` is knitr-only) |
| `error` | bool | `true` renders the error instead of failing the render |
| `include` | bool | `false` = run but hide everything (setup cells) |
| `cache` | bool | Per-cell (knitr) / per-document (jupyter, via `jupyter-cache`) cache |
| `freeze` | `true`/`false`/`auto` | Project-level reuse of results (below) |

Document-level example:

```yaml
execute:
  echo: false
  warning: false
```

Cell-level always wins over document-level.

## Freeze vs cache

- **`freeze`** (project only, set in `_quarto.yml` under `execute:`) stores results in
  `_freeze/` and reuses them on **full project renders**. `auto` re-executes when the source
  file changes; `true` never re-executes. Commit `_freeze/` so CI can publish without R/Python.
  Rendering a single file or a subdirectory **always executes** regardless of freeze.
  Freeze does not track data changes — delete the relevant `_freeze/` entry to force a rerun.
- **`cache`** speeds up iteration within one document; invalidated by code changes. Use it
  for slow cells during authoring; use freeze for publishing pipelines.

## Parameters

| Engine | Define | Use |
|---|---|---|
| knitr | `params:` in front matter | `params$region` |
| jupyter | A cell tagged `#\| tags: [parameters]` with default assignments | top-level variables |
| julia | `params:` in front matter | each key becomes a constant (`region`); keys must be valid Julia names |

Render variants: `quarto render report.qmd -P region:north -P year:2026`, or
`--execute-params params.yml`. For batch output name each file:
`quarto render report.qmd -P region:north --output report-north.html`.

## Inline code

- knitr: `` `r nrow(df)` ``
- jupyter / julia: `` `{python} len(df)` `` / `` `{julia} length(x)` ``

Inline values are evaluated after the cells above them; keep formatting (rounding, thousands
separators) in the expression.

## Execution context

`QUARTO_EXECUTE_INFO` (1.8+) points to a JSON file describing the render (target format, etc.).
Read it in a cell to skip expensive work for some formats. Visibility-only differences belong
in conditional content instead (`concepts/authoring.md`).

## More detail

`computations/execution-options`, `computations/python`, `computations/r`, `computations/julia`,
`computations/parameters`, `computations/caching`, `computations/inline-code`,
`projects/code-execution`, `projects/virtual-environments`, `advanced/quarto-execute-info`,
`reference/cells/cells-knitr`, `reference/cells/cells-jupyter` — see `references.md` for URLs.
