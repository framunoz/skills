---
name: quarto
description: Quarto authoring, configuration, rendering and troubleshooting — `.qmd` documents, `_quarto.yml` projects, HTML reports, revealjs slides, docx, PDF/Typst, websites, books, manuscripts, dashboards, cross-references, brand.yml theming, extensions, and code execution with knitr/jupyter/julia (R and Python in one document, freeze, uv/renv environments). Use whenever the user writes, renders, styles or debugs anything Quarto — `quarto render/preview/publish` errors, YAML options that don't take effect, migrating R Markdown or Jupyter notebooks — even if they never say "Quarto" but a `.qmd` or `_quarto.yml` is involved. Not for generic documents, reports or slides with no Quarto context.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: 2.0.0
  quarto-version: 1.10.19
  created: 2026-10-09
  last-reviewed: 2026-10-09
  tags: documentation, quarto, reproducibility
---

# Quarto

Distilled, version-checked notes for Quarto output that renders on the first try. Concepts in
`concepts/` and `formats/`; traps in `gotchas.md`; proven patterns in `recipes.md`; decision
tables in `cheatsheet.md`; terms in `glossary.md`; official docs per topic in `references.md`.
Paths are relative to this skill's directory.

## 1. Preflight — do this first

Run `python3 scripts/quarto_preflight.py --project <path>`. It reports the installed Quarto,
compares it with **1.10.19** (the version this skill was written and tested against, reviewed
2026-10-09), and lists project root, type, profiles, `_metadata.yml`, brand, extensions,
`_freeze/` and nearby `.venv` / `renv.lock` / `.Rprofile`. Read-only.

- **Same version** — option names here are current.
- **Newer** — before writing an option this skill mentions, confirm it with
  `uv run scripts/check_option.py <option>` (reads the schemas bundled with the installed
  Quarto), and skim each newer changelog:
  `https://raw.githubusercontent.com/quarto-dev/quarto-cli/main/news/changelog-<X.Y>.md`.
- **Older** — tell the user; `syntax-highlighting` (1.9+), engine extensions (1.9+) and
  `axe: {standard: …}` (1.10+) won't exist.
- **Quarto missing** — report it and give install guidance; never describe a render that didn't run.

## 2. Operating rules

- **Inspect before editing**: `_quarto.yml`, profiles, `_metadata.yml`, front matter, engine and
  environment. Follow the project's conventions and make the smallest change that works; put
  each setting in the one layer that owns it rather than repeating it to override.
- **Render to verify**: rendering the document you changed (or one format of it) is the normal
  check. Prefer one file over the whole project; say when a render executes code with side
  effects (writes data, calls APIs) before running it.
- **Confirm first** — state the exact command and get an explicit yes for anything that
  mutates beyond the document: installing/updating/removing extensions (see
  `concepts/extensions.md` → "Installing or updating safely"), `quarto publish`, installing
  TeX/Chrome/packages, creating or changing environments, deleting `_freeze/` or output dirs.
- **Missing dependency** — name it (engine, kernel, package, TeX) and stop before installing.
  PDF without TeX → offer `format: typst` (bundled) or `quarto install tinytex`.

## 3. Mental model: the render pipeline

```
.qmd ──engine (knitr | jupyter | julia)──▶ .md ──Pandoc + Lua filters──▶ HTML / revealjs / docx / PDF / Typst …
         runs code, captures output          crossrefs, callouts, layout, shortcodes, theming
```

| Symptom | Stage | Probe |
|---|---|---|
| Code errors, wrong package/Python, missing output | Engine | `quarto check`; render with `-M keep-md:true` and read `<name>.<fmt>.md` |
| `?@fig-x` unresolved, callout/layout ignored | Pandoc/filters | label syntax, div fences, format support |
| Option silently ignored | Config | `uv run scripts/check_option.py <opt>` (exists? which formats?); `quarto inspect <file>` (where did it land?) |
| Looks wrong only in one format | Format | option may be format-specific — check its `formats:` line |

**Option precedence** (later wins): `_quarto.yml` → selected profile `_quarto-<name>.yml` →
`_metadata.yml` in the directory → document front matter → cell options (`#|`). Within a file,
keys under `format: <fmt>:` apply only to that format and override the top-level key.
`format:` itself never merges: a document that sets it replaces the project's format list.

**Engine binding**: any `{r}` cell → knitr (Python cells then run through reticulate); only
`{python}` → jupyter; `{julia}` → jupyter (IJulia) unless `engine: julia`. One engine per
document. Override with `engine:`.

## 4. Writing rules

- **Verify, don't recall.** Check any option you're not certain about with
  `scripts/check_option.py`. Hidden in schema = deprecated: use the replacement. NOT FOUND is
  strong evidence, not proof — a few documented options (`callout-appearance`, Pandoc's
  `reference-section-title`) are absent from the schema; confirm on the docs page.
- **Treat render warnings as failures** — an unresolved crossref still exits 0 with a `WARNING`.
- **Cell options as `#|` YAML** at the very top of the cell, dashes not dots (`fig-cap`, not `fig.cap`).
- **Labels carry their type prefix**: `fig-`, `tbl-`, `sec-`, `eq-`, `lst-`, callouts `nte-`
  `tip-` `wrn-` `imp-` `cau-`; no underscores. Reference with `@fig-sales`.
- **Run the right interpreter.** Python: `uv run quarto render` (or `QUARTO_PYTHON`) — the CLI
  does not find `.venv` on its own. R with renv: keep a `_quarto.yml` at the renv root.
  Details in `concepts/execution.md`.
- **Format capabilities differ**: don't copy HTML options into revealjs, docx, PDF or Typst
  without checking; interactive output needs a static fallback outside HTML.

## 5. Where to look

Read only the files the task touches.

| Task | Read |
|---|---|
| Single HTML report: layout, code folding, tabsets, TOC, self-contained file | `formats/html.md` |
| Slides (revealjs): structure, fragments, columns, notes, code steps, PDF export | `formats/revealjs.md` |
| Word output, reference-doc styles | `formats/docx.md` |
| PDF via LaTeX or Typst | `formats/pdf-typst.md` |
| Website, blog, book, manuscript, publishing | `formats/websites-books.md` |
| Dashboard | `formats/dashboards.md` |
| Engines, R + Python together, uv/renv, freeze/cache, parameters, inline code | `concepts/execution.md` |
| `_quarto.yml`, project types, profiles, metadata layers, includes, pre/post-render | `concepts/projects.md` |
| Cross-refs, figures/tables, layout, callouts, citations, shortcodes, raw blocks, conditional content | `concepts/authoring.md` |
| Themes, SCSS, `_brand.yml`, light/dark, syntax highlighting | `concepts/theming-brand.md` |
| Extensions (install/update safely), Lua filters, custom formats, engine extensions | `concepts/extensions.md` |
| Something renders wrong or errors | `gotchas.md` first, then the topic file |
| "How do I…" for a common workflow | `recipes.md` |
| Choosing format, engine, freeze/cache, PDF engine, where an option goes | `cheatsheet.md` |
| Starting a new document or project | `assets/`: `report.qmd`, `slides.qmd` + `slides.scss`, `project/_quarto.yml` + production profile (render-tested on 1.10.19) |

**Beyond this skill**: `references.md` maps each topic to the official page. Every page exists
as clean Markdown at `https://quarto.org/docs/<path>.llms.md` — fetch that instead of the
HTML. Full index: `https://quarto.org/llms.txt`.

## 6. Report

End with: files changed; project root, profile, format and engine used; commands actually run
and their result (including warnings); outputs produced and side effects; anything assumed or
left unverified.
