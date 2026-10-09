# Gotchas

Traps that produce a render that "works" but is wrong, or an error whose cause isn't where it
points. Grouped by pipeline stage. Each entry: symptom → cause → fix.

## Environment and engine

- **`ModuleNotFoundError` / Jupyter not found / wrong Python** → the Quarto CLI uses Python from
  `PATH`; it does not discover `.venv`, even inside a project. → `uv run quarto render`, or
  `QUARTO_PYTHON=.venv/bin/python`. The venv needs `jupyter` (`uv add --dev jupyter`). Verified on 1.10.19.
- **Python cells in an R document use another Python** → any `{r}` cell switches the engine to
  knitr, and reticulate picks its own Python. → `RETICULATE_PYTHON=.venv/bin/python` in
  `.Renviron` or `Sys.setenv()` in `.Rprofile`.
- **R packages "not installed" though `renv::status()` is fine** → no `_quarto.yml`, and
  `quarto` was run from a subdirectory, so R never read the root `.Rprofile` (renv inactive).
  → Add a `_quarto.yml` at the renv root (R then always starts there). Verified on 1.10.19.
- **Relative data paths break when the file moves** → code runs in the *document's* directory.
  → `execute-dir: project` under `project:`, or `here::here()`.
- **Julia cells use IJulia, not the native engine** → `{julia}` defaults to jupyter. →
  `engine: julia`, or `engines: ['julia']` in `_quarto.yml`.
- **Changes in data don't show up on the site** → `freeze` only watches the source file. →
  Delete the matching folder under `_freeze/`, or render that file explicitly
  (single-file renders always execute).
- **Expected freeze, but the file re-executed** → freeze applies only to full project renders;
  `quarto render file.qmd` and `quarto render subdir/` always execute.
- **knitr error "Functions that produce HTML output found in document targeting pdf"** →
  an htmlwidget in a PDF/Typst/docx render. → Hide it with
  `.content-visible when-format="html"`, provide a static version, or install `webshot2`.

## Configuration

- **Option has no effect** → wrong level or wrong format. Options under `format: html:` don't
  reach `revealjs`; options at the top level apply to every format. Check
  `uv run scripts/check_option.py <opt>` (its `formats:` line) and `quarto inspect file.qmd`.
- **Every document renders to several formats** → each format listed under `format:` in
  `_quarto.yml` is a render target for documents without their own `format:`. List only the
  default format in the project; slides declare `format: revealjs` themselves.
- **Option valid but silently ignored because it sits at the wrong level** → Quarto doesn't
  warn. Verified: `execute-dir: project` at the top level of `_quarto.yml` or in document front
  matter is ignored; it only works under `project:`.
  `check_option.py` confirms a key *exists*, not where it goes — for project keys read the
  `nested property … in: project.yml` line, and confirm with
  `quarto inspect file.qmd` (look under `project` / `formats.<fmt>`).
- **A project format disappeared for one document** → `format:` is the one key that doesn't
  merge: a document's `format:` replaces the project list entirely.
- **`highlight-style` ignored or warned** → deprecated in 1.9 (Pandoc 3.8). → `syntax-highlighting`.
- **`self-contained` warned** → deprecated. → `embed-resources: true`.
- **YAML error pointing at a random line** → tabs, unquoted `:` in titles, or a cell option
  block not at the very top of the cell. Quote strings with colons: `title: "Q3: Results"`.
- **`#|` option ignored** → there must be no blank line or code between the opening fence and
  the `#|` lines; mermaid uses `%%|`, dot uses `//|`.
- **File not rendered in the project** → names starting with `_` or `.` are skipped by design
  (partials). Rename or `{{< include >}}` it.

## Cross-references and captions

- **`?@fig-x` in output** (and a `WARNING: Unable to resolve crossref`) → label lacks the type
  prefix (`#fig-x`, not `#x` or `#x-fig`), a typo, or the label is on a cell that produced no
  figure. Treat that warning as a failure.
- **Labels with `_` break PDF** → avoid underscores in labels and IDs; use `-`.
- **Reserved prefixes on non-crossref labels** (`fig-setup` on a setup cell) → the docs warn
  against it (Quarto treats it as a float). Use neutral labels (`setup`, `load-data`) for ordinary cells.
- **`@sec-` breaks Typst** (`error: cannot reference heading without numbering`) while HTML
  renders fine → section crossrefs need `number-sections: true`; set it whenever you use
  `@sec-`. Verified on 1.10.19.
- **`renderings: [light, dark]` breaks captions/crossrefs** → known limitation. Wrap the cell in
  `::: {#fig-x}` with the caption inside the div, and give the cell a non-`fig-` label.

## HTML and revealjs

- **Slides show no code** → revealjs does not echo by default. → `echo: true`.
- **`{.fragment}` printed literally on a list item** (`- Point {.fragment}`) → Pandoc has no
  attributes on list items. → `::: {.incremental}` around the list, or
  `- [Point]{.fragment}`.
- **Vertical slides behave like horizontal ones** → Quarto always nests each `#` section and its
  `##` slides into a vertical stack, but the default `navigation-mode: linear` steps through them
  with left/right. Use `navigation-mode: vertical` (emitted as reveal's `default`) or `grid` for
  up/down navigation. Verified on 1.10.19.
- **`embed-resources: true` + `chalkboard: true` → render error** → incompatible. Pick one.
- **Equations missing in the emailed HTML offline** → math isn't embedded. → `self-contained-math: true`.
- **Huge single-file HTML** → embedded widgets. Drop `embed-resources` or replace heavy widgets.
- **Images oversized on scrollable slides** → auto-stretch miscalculates. → `.nostretch` on the
  slide or `auto-stretch: false`.
- **HTML copied without its `_files/` folder looks broken** → without `embed-resources`, assets
  live beside the HTML.

## PDF / Typst

- **LaTeX font or package behaviour changed after upgrading** → default engine is `lualatex`
  since 1.8 (was `xelatex`). → `pdf-engine: xelatex` to restore.
- **LaTeX error with an unhelpful message** → `keep-tex: true` and read the `.log`/compile the
  `.tex`. `quarto update tinytex` fixes many "package not found" loops.
- **Typst images too large or small** → known sizing difference; set explicit `width`.
- **Mermaid/Graphviz fail in PDF/docx** → need a headless browser:
  `quarto install chrome-headless-shell` (`quarto install chromium` is deprecated in 1.10).

## Rendering and preview

- **Listings or other pages stale after rendering one page** → a single-file render only rebuilds
  that page. → full `quarto render` before publishing.
- **Stray `*.quarto_ipynb` files** → intermediates of the Jupyter engine; ignored by git by
  default since 1.8, cleanup bugs fixed in 1.10. Safe to delete.
- **`[IPKernelApp] WARNING | Kernel is running over TCP without encryption`** → ipykernel noise
  on local renders; harmless, not a Quarto warning.
- **Need more diagnostics** → `QUARTO_LOG_LEVEL=DEBUG`, `QUARTO_PRINT_STACK=true`,
  `quarto check`, `-M keep-md:true` to see what the engine produced.
