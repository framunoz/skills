# Projects

A project is any directory with a `_quarto.yml`. It gives shared options, a single
`quarto render` for everything, freeze, an output directory, and a stable R/Python startup
directory (see `concepts/execution.md`).

## Project types

| `project: type:` | Output | Use for |
|---|---|---|
| `default` | Each document rendered next to its source (or into `output-dir`) | Groups of reports, slides; shared config |
| `website` | `_site/` with navbar/sidebar, search, listings | Docs, blogs, portfolios |
| `book` | `_book/`; chapters with numbering and cross-chapter crossrefs; HTML + PDF/EPUB/docx | Long-form, multi-chapter |
| `manuscript` | Article + embedded notebooks, multiple formats, MECA bundle | Scholarly articles |

Scaffold with `quarto create project <type> <dir>`.

## `_quarto.yml` skeleton

```yaml
project:
  type: default
  output-dir: _output          # omit to render beside sources
  render:                      # optional explicit list / order; globs and !negation allowed
    - "*.qmd"
    - "!drafts/"
  execute-dir: project         # optional: run code from the project root
  pre-render: uv run python prepare.py
  post-render: scripts/copy-assets.sh
  resources:                   # extra files copied to the output dir
    - data/*.csv

execute:
  freeze: auto

format:
  html:
    toc: true
```

## Metadata layering

Merged in order, later wins: `_quarto.yml` → `dir/_metadata.yml` → document front matter.
Objects and arrays merge (e.g. bibliographies accumulate); scalars are replaced. **Exception:
`format`** — if a document defines `format:`, it must list every format it should render to.

- **`metadata-files: [_website.yml]`** — split a long `_quarto.yml` into pieces.
- **`_quarto.yml.local`** — uncommitted local overrides (e.g. `execute: cache: true`); Quarto
  adds it to `.gitignore`.
- **Profiles** — `_quarto-<name>.yml` merged on top when `--profile <name>` or
  `QUARTO_PROFILE=<name>` is active; several at once with `--profile a,b`. Code can read
  `QUARTO_PROFILE`. Content can be shown per profile with `.content-visible when-profile="name"`.
- **Environment files** — `_environment`, `_environment-<profile>`, `_environment.local`
  set environment variables for renders.

## File naming conventions

- Files and directories starting with `_` or `.` are **not rendered** as standalone documents —
  use `_partial.qmd` for content included elsewhere.
- `{{< include _section.qmd >}}` inlines another file *before* execution (cells inside run in the
  including document's engine and environment).
- `{{< embed notebook.ipynb#cell-label >}}` pulls a cell's *output* from a notebook (with
  `echo=true` to show code).

## Rendering

| Command | Effect |
|---|---|
| `quarto render` | Whole project (respects `freeze`, runs pre/post-render) |
| `quarto render subdir/` | Only that subdirectory (always executes) |
| `quarto render doc.qmd --to revealjs` | One file, one format |
| `quarto preview` | Live-reload server; renders on save |
| `quarto inspect [file]` | JSON of resolved project/format config — use to debug merging |

Pre/post-render scripts receive `QUARTO_PROJECT_RENDER_ALL`, `QUARTO_PROJECT_OUTPUT_DIR`,
`QUARTO_PROJECT_INPUT_FILES` (pre) and `QUARTO_PROJECT_OUTPUT_FILES` (post). `.py`/`.R`/`.ts`
scripts run with the matching interpreter; anything else runs as a shell command (`make prepare`).

## Engine priority

`engines: ['julia']` in `_quarto.yml` (1.7+) makes the native Julia engine preferred
project-wide; listed engines are checked first, the rest keep the default order.

## More detail

`projects/quarto-projects`, `projects/profiles`, `projects/scripts`, `projects/environment`,
`projects/code-execution`, `reference/projects/options`, `reference/globs`,
`authoring/includes`, `authoring/notebook-embed`, `advanced/inspect/index`.
