# Revealjs slides

HTML slides on reveal.js 5. Same Markdown as HTML documents plus slide structure, fragments,
speaker notes and a presenter view. Starter: `assets/slides.qmd`.

## Slide structure

- `#` heading → **section title slide**; `##` heading → **slide**; `---` → slide without a title.
  Change the level with `slide-level`.
- Title slide comes from `title`/`subtitle`/`author`/`date`; omit `title` to skip it.
- Slide attributes go on the heading: `## Results {.smaller background-color="#111"}`.
- Hide a slide: `{visibility="hidden"}`; don't count it: `{visibility="uncounted"}` (appendix slides).
- Each `#` section and its `##` slides always form a vertical stack, but the default
  `navigation-mode: linear` walks them left/right. For up/down navigation set
  `navigation-mode: vertical` (or `grid`).

## Front matter that works

```yaml
---
title: "Results Q3"
author: "Name"
date: today
format:
  revealjs:
    theme: [default, custom.scss]
    slide-number: c/t
    show-slide-number: all      # all | print | speaker
    footer: "Team · 2026"
    logo:
      path: logo.png
      alt: "Company logo"
    preview-links: auto         # open links in an overlay
    incremental: false
    code-line-numbers: true
    transition: fade            # none | fade | slide | convex | concave | zoom
    width: 1600                 # normal size, default 1050×700; content scales uniformly
    height: 900
execute:
  echo: true
---
```

Code cells do **not** echo by default in revealjs (unlike HTML). Set `echo: true` when the code is the point.

## Reveal content progressively

| Want | Syntax |
|---|---|
| All lists incremental | `incremental: true` |
| One list incremental / not | `::: {.incremental}` / `::: {.nonincremental}` |
| Pause mid-slide | a line with `. . .` (only under slide headings) |
| Fragment any element | `::: {.fragment}`; classes `fade-in`, `fade-up`, `highlight-red`, `semi-fade-out`, …; order with `fragment-index=2` |
| Show code output later | `#| output-location: fragment` |
| Output next to code | `#| output-location: column` or `column-fragment` |
| Output on next slide | `#| output-location: slide` |
| Step through code lines | `#| code-line-numbers: "|1-2|4"` (each `|` is a step) |
| Morph between slides | `{auto-animate=true}` on consecutive slides with matching elements |

## Layout on a slide

```markdown
:::: {.columns}
::: {.column width="40%"}
Text
:::
::: {.column width="60%"}
![](plot.png)
:::
::::
```

- `.r-stretch` on an image fills the remaining vertical space; `auto-stretch` does this
  automatically for a single image/plot on a slide (disable with `auto-stretch: false` or `.nostretch`).
- `::: {.r-stack}` overlays elements (combine with fragments); `.r-fit-text` makes text fill
  the width; `{.center}` on the heading centres the slide content.
- Absolute position: `![](img.png){.absolute top=50 left=100 width=300}`.
- `layout-ncol` from `concepts/authoring.md` works too.

## Too much content

- `{.smaller}` (smaller type) or `{.scrollable}` per slide, or `smaller: true` /
  `scrollable: true` globally.
- Scrollable + auto-stretch miscalculate image sizes → add `.nostretch` to scrollable slides.
- Section title slides are centred and won't scroll unless `center-title-slide: false`.
- Code blocks cap at 500 px tall: `code-block-height: 650px`.
- Prefer splitting the slide over shrinking it.

## Figures

Size for the slide, not the page: `fig-width`/`fig-height` (inches) with the 16:9-ish normal
size in mind, or library-native sizing. With `width: 1600` set `fig-dpi` accordingly.
`.r-stretch` beats guessing heights.

## Speaker notes, asides, footnotes

```markdown
## Slide

Content ^[Footnote at the bottom of the slide]

::: aside
Peripheral comment, small font at the bottom.
:::

::: {.notes}
Only in speaker view (press **S**).
:::
```

`reference-location: document` moves footnotes to the end.

## Backgrounds

On the heading: `background-color`, `background-image` (+ `background-size`,
`background-opacity`), `background-video`, `background-iframe`, `background-gradient`.
Title-slide background: `title-slide-attributes: {data-background-image: img.png, data-background-size: cover}`.

## Presenting

| Key / URL | Does |
|---|---|
| **S** | Speaker view (notes, timer, next slide) |
| **F** | Fullscreen |
| **O** / **Esc** | Overview |
| **E** | Print view (for PDF) |
| **R R** or `?view=scroll` | Scroll view; default it with `scroll-view: true` |
| **Alt+click** | Zoom |
| **C** / **B** | Draw on slide / toggle chalkboard (with `chalkboard: true`) |

Other toggles: `menu`, `controls`, `progress`, `hash-type: number`, `multiplex: true`
(audience follows the presenter), `auto-slide: 5000`.

## Export to PDF

1. Open the HTML in Chrome, press **E** (print view).
2. Print → Save as PDF, Landscape, Margins none, Background graphics on.

Options: `show-notes: separate-page`, `pdf-separate-fragments: true`,
`pdf-max-pages-per-slide: 1`. Headless/CI export: third-party `decktape` on the rendered HTML (not part of Quarto).

## Sharing a single file

`embed-resources: true` gives one `.html` — **incompatible with `chalkboard`** (render error).
Choose one: chalkboard for live teaching, `embed-resources` for distribution. Math is not
embedded unless `self-contained-math: true`.

## Themes

Built-in: `default`, `dark`, `beige`, `blood`, `dracula`, `league`, `moon`, `night`, `serif`,
`simple`, `sky`, `solarized`. Customise with SCSS: `theme: [default, custom.scss]`, or with
`_brand.yml` (`brand-mode: dark` to pick the dark brand, 1.8+). See `concepts/theming-brand.md`.

## Accessibility

`axe: {output: document}` (1.9+) appends a slide with the report. Give every image `fig-alt`.

## More detail

`presentations/revealjs/index`, `presentations/revealjs/advanced`,
`presentations/revealjs/presenting`, `presentations/revealjs/themes`, `extensions/revealjs`
(plugins), `reference/formats/presentations/revealjs` (every option).
