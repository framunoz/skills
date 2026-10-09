# HTML reports

The default format and the most capable one: interactive widgets, tabsets, margin content,
folding code, light/dark themes. Starter: `assets/report.qmd`.

## A good default front matter

```yaml
---
title: "Quarterly sales"
subtitle: "Region North"
author: "Name"
date: today
lang: es
format:
  html:
    toc: true
    toc-location: left
    number-sections: true
    code-fold: true
    code-tools: true
    embed-resources: true      # one portable file; see trade-offs below
    lightbox: true
    theme:
      light: flatly
      dark: darkly
execute:
  echo: true
  warning: false
---
```

For an audience that never reads code: `execute: echo: false` and drop `code-fold`/`code-tools`.

## Navigation

| Option | Values / notes |
|---|---|
| `toc` | `true`; `toc-depth: 3`; `toc-title`; `toc-expand: 1` (levels expanded) |
| `toc-location` | `right` (default), `left`, `body`, `left-body`, `right-body` |
| `number-sections` | `true`; skip a heading with `{.unnumbered}`, hide from TOC with `{.unlisted}` |
| `anchor-sections` | Link icon on headings (default on) |
| `smooth-scroll` | `true` |
| `link-external-icon`, `link-external-newwindow` | Mark/open external links |
| `crossrefs-hover`, `citations-hover`, `footnotes-hover` | Popups on hover (default on) |

## Code display

| Option | Effect |
|---|---|
| `code-fold` | `true` (collapsed), `show` (expanded but collapsible), `false`; `code-summary: "Show code"` |
| `code-tools` | Header menu: show/hide all code, view source. `code-tools: {source: repo-url}` |
| `code-copy` | Copy button (`hover` default, `true`, `false`) |
| `code-link` | Link functions to docs (knitr + `downlit`, Python not supported) |
| `code-overflow` | `scroll` (default) / `wrap`; per block `.code-overflow-wrap` |
| `code-line-numbers` | `true` |
| `syntax-highlighting` | Theme name (`github`, `a11y`, …) or `{light: x, dark: y}`. **Replaces `highlight-style` (1.9+)** |
| `code-annotations` | `below` / `hover` / `select` — see `concepts/authoring.md` |

All of these can be set per cell with `#|`.

## Page layout and the article grid

- `page-layout: article` (default) | `full` (no margins reserved) | `custom`.
- Place content on the grid with cell option `#| column: page` or div classes
  `.column-body`, `.column-body-outset`, `.column-page`, `.column-page-inset`, `.column-screen`,
  `.column-screen-inset`, `.column-margin` (suffixes `-left`/`-right` exist for most).
- Margin content: `::: {.column-margin}`, `#| column: margin`, `cap-location: margin`,
  `reference-location: margin` (footnotes), `citation-location: margin`.
- Grid widths: `grid: {body-width: 900px, margin-width: 300px, sidebar-width: 250px}`.

Wide tables or plots that feel cramped → `#| column: page` before shrinking fonts.

## Interactivity without a server

- R: any htmlwidget (`plotly`, `leaflet`, `DT`, `reactable`) works directly.
- Python: `plotly`, `bokeh`, `altair`, `itables`, ipywidgets (no live kernel → static state).
- Observable JS (`{ojs}`) for client-side reactivity on any engine (`ojs_define()` to pass data).
- Tabsets for "same thing, several views" (`concepts/authoring.md`).
- Shiny (`server: shiny`) needs a running server — see `interactive/shiny/index`.

## Light / dark

```yaml
theme:
  light: [flatly, custom.scss]
  dark: [darkly, custom-dark.scss]
respect-user-color-scheme: true    # follow OS preference (needs JS); otherwise first listed wins
```

Plots don't follow automatically: produce two outputs and tag them with
`#| renderings: [light, dark]`. `renderings` conflicts with `fig-`/`tbl-` labels and captions —
wrap the cell in a `::: {#fig-x}` div and give the cell a non-crossref label.
Brand-based themes: `concepts/theming-brand.md`.

## Self-contained output: `embed-resources`

`embed-resources: true` inlines CSS, JS, images and fonts into one `.html` you can email.
Trade-offs:

- Math libraries are **not** embedded unless `self-contained-math: true` (large).
- Slower renders; turn on only for the deliverable (or via a profile).
- Large htmlwidgets inflate the file (tens of MB is possible).
- `self-contained` is the deprecated name — use `embed-resources`.

Without it, the HTML depends on a `<name>_files/` folder that must travel with it.

## Other formats from one source

With several formats (`format: {html: ..., pdf: ...}`) the HTML shows "Other Formats" links by
default; restrict with `format-links: [pdf]` or hide with `format-links: false`. Each format keeps
its own block of options.

## Comments and accessibility

- `comments: {hypothesis: true}` (also `utterances`, `giscus`).
- `axe: true` runs accessibility checks in the browser console;
  `axe: {output: document}` (1.9+) shows a report on the page; `standard: wcag21aa` (1.10+)
  scopes it to a WCAG level. Alt text (`fig-alt`) is the most common violation.

## Head/body injection and CSS

- `css: styles.css`; SCSS belongs in `theme:` (see `concepts/theming-brand.md`).
- `include-in-header: analytics.html` (or `{text: "<script>…</script>"}`),
  `include-before-body`, `include-after-body`.

## More detail

`output-formats/html-basics`, `output-formats/html-code`, `output-formats/page-layout`,
`authoring/article-layout`, `output-formats/html-themes`, `output-formats/html-publishing`,
`output-formats/html-accessibility`, `output-formats/html-lightbox-figures`,
`output-formats/html-multi-format`, `interactive/index`, `reference/formats/html`.
