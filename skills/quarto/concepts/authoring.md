# Authoring: cross-refs, figures, tables, layout, callouts, citations, shortcodes

Quarto Markdown = Pandoc Markdown + fenced divs (`::: {.class}`), spans (`[text]{.class}`),
attributes (`{#id .class key=value}`) and shortcodes (`{{< name >}}`). Most features below are
just a div or attribute with a known class.

## Cross-references

A label = type prefix + name. Reference with `@label`; `@Fig-x` capitalises; `[-@fig-x]`
prints only the number.

| Thing | Define | Reference |
|---|---|---|
| Image figure | `![Caption](plot.png){#fig-plot}` | `@fig-plot` |
| Code figure | `#| label: fig-plot` + `#| fig-cap: "Caption"` | `@fig-plot` |
| Code table | `#| label: tbl-sum` + `#| tbl-cap: "Caption"` | `@tbl-sum` |
| Markdown table | caption line `: Caption {#tbl-sum}` under the table | `@tbl-sum` |
| Section | `## Results {#sec-results}` (needs `number-sections: true`; Typst fails without it) | `@sec-results` |
| Equation | `$$ y = x $$ {#eq-line}` | `@eq-line` |
| Code listing | `#| lst-label: lst-fit` + `#| lst-cap:` | `@lst-fit` |
| Callout | `::: {#tip-cache .callout-tip}` (prefixes `nte-` `tip-` `wrn-` `imp-` `cau-`) | `@tip-cache` |
| Theorem-like | `::: {#thm-main}` (`thm-` `lem-` `cor-` `prp-` `def-` `exm-` `exr-`) | `@thm-main` |

Any div can become a float: `::: {#fig-panel}` … content … caption as last paragraph `:::`.
That is how to cross-reference a widget, a combined layout, or a table produced by code
when the cell options don't fit. Custom float types (e.g. "Supplementary Figure") are declared
under `crossref: custom:`.

A cell may produce several figures: `#| fig-subcap: ["A", "B"]` + `#| layout-ncol: 2` gives
`@fig-x-1`, `@fig-x-2`.

## Figures

- Size: `{width=60%}` on images; code figures use `fig-width`/`fig-height` (inches) and
  `fig-dpi`, set per cell or under `format: html:`.
- Alignment `fig-align`, alt text `fig-alt` (always provide — accessibility checks flag it),
  caption position `fig-cap-location: bottom|top|margin`.
- `lightbox: true` (HTML) zooms images on click; per image `{.lightbox}`; group with
  `group="name"`.

## Tables

- Markdown pipe tables with `: Caption {#tbl-x tbl-colwidths="[70,30]"}`.
- Code tables: knitr `knitr::kable()`, `gt`, `flextable`; Python `great_tables`,
  `pandas.DataFrame` (HTML output via `itables` for interactive). Caption and label through cell
  options, not the table function, so Quarto controls numbering.
- **List tables** for cells with paragraphs, lists or code — a `::: {.list-table}` div holding a
  nested bullet list (one top-level bullet per row; `header-rows=0` to drop the header):

  ```markdown
  ::: {.list-table}
  - - Fruit
    - Price
  - - Apple
    - 1.20
  :::
  ```
- Grid tables also allow block content but are harder to edit; prefer list tables.
- `tbl-cap-location: top|bottom|margin`. Subtables: a `::: {#tbl-panel layout-ncol=2}` div
  holding labelled tables.

## Layout

- `::: {layout-ncol=2}` — equal columns; `layout-nrow`.
- `::: {layout="[[1,1],[1]]"}` — explicit grid (rows of relative widths; negatives = spacers).
- `layout-valign="top|center|bottom"`.
- HTML article grid: `column: body | body-outset | page | screen | margin` (cell option
  `#| column: page`, or div `::: {.column-margin}`). Margin notes, `cap-location: margin`,
  `reference-location: margin` for footnotes. See `formats/html.md`.

## Callouts

```markdown
::: {.callout-warning collapse="true" title="Check the units"}
Content.
:::
```

Types: `note`, `tip`, `warning`, `important`, `caution`. Attributes: `title`, `collapse`
(HTML only), `appearance="default|simple|minimal"`, `icon=false`. Document-wide:
`callout-appearance: simple`, `callout-icon: false`.

## Tabsets (HTML, revealjs, dashboards)

```markdown
::: {.panel-tabset group="lang"}
## R
...
## Python
...
:::
```

Same `group` keeps tabs synchronised across the page.

## Code annotations

Add `# <1>` at the end of a code line, then an ordered list right after the block:

````markdown
```r
df |>                     # <1>
  filter(year > 2020)     # <2>
```
1. Start from the raw data.
2. Keep recent years.
````

Style with `code-annotations: below` (default) `| hover | select` (HTML); `none` strips the
markers and list from output; `false` disables processing entirely.

## Citations

`bibliography: refs.bib` (BibTeX, CSL-JSON, YAML), optional `csl: apa.csl`. Cite with
`[@smith2020, p. 4]`, `@smith2020` (in-text), `[-@smith2020]` (year only). Bibliography is
placed at `::: {#refs} :::` or at the end. `nocite: | @*` includes everything;
`citation-location: margin` (HTML). Zotero integration lives in the visual editor.

- Several bibliographies: `bibliography: [refs.bib, software.bib]` (merge across layers).
- Heading for the list: `reference-section-title: References`; omit the list entirely:
  `suppress-bibliography: true` (both Pandoc options — valid though absent from Quarto's schema).
- Hover previews in HTML: `citations-hover` (default on). Linked citations in PDF/docx: `link-citations: true`.
- CSL files: <https://www.zotero.org/styles>; keep the `.csl` in the project.

## Conditional content

```markdown
::: {.content-visible when-format="html"}
Only in HTML (also: `unless-format`, `when-meta`, `unless-meta`, `when-profile`).
:::

::: {.content-hidden when-format="revealjs"}
:::
```

Format aliases: `html` matches all HTML-based formats; `pdf` matches LaTeX PDF; `llms-txt`
targets website `.llms.md` output. Conditional content hides output; to skip *execution* per
format, read `QUARTO_EXECUTE_INFO` (`concepts/execution.md`).

## Raw content

Format-specific markup passes through untouched and is dropped for other formats — fenced
blocks ```` ```{=html} ````, ```` ```{=latex} ````, ```` ```{=typst} ````, ```` ```{=openxml} ```` (docx);
inline `` `<br>`{=html} ``. Pair with conditional content when a fallback is needed.

## Shortcodes (built-in)

| Shortcode | Use |
|---|---|
| `{{< include _file.qmd >}}` | Inline another file before execution |
| `{{< embed nb.ipynb#label echo=true >}}` | Output (and code) of a notebook cell |
| `{{< var key.sub >}}` | Value from `_variables.yml` |
| `{{< meta title >}}` | Value from document metadata |
| `{{< env NAME >}}` | Environment variable |
| `{{< pagebreak >}}` | Native page break (PDF, docx, Typst) |
| `{{< kbd Ctrl-C mac=Cmd-C >}}` | Keyboard shortcut |
| `{{< video URL >}}` | Responsive video embed |
| `{{< contents id >}}` | Move a section/div elsewhere in the document |
| `{{< lipsum 2 >}}`, `{{< placeholder 400 200 >}}` | Filler text / images |
| `{{< version >}}` | Quarto version |

Escape a literal shortcode with triple braces: `{{{< var x >}}}`.

## Diagrams

```` markdown
```{mermaid}
%%| fig-cap: "Pipeline"
flowchart LR
  A[qmd] --> B[md] --> C[html]
```
````

`{mermaid}` (options with `%%|`) and `{dot}` Graphviz (options with `//|`) render without any
engine. Mermaid in PDF/docx needs a headless browser (`quarto install chrome-headless-shell`).

## Other

- Title block: `title`, `subtitle`, `author` (name, affiliations, orcid), `date: today`,
  `date-format`, `abstract`, `keywords`. HTML: `title-block-banner: true`.
- Appendices: `## Section {.appendix}`; license and citation metadata render there.
- Language: `lang: es` translates generated text (Figure → Figura, etc.).
- Footnotes `^[inline note]`; `reference-location: margin` in HTML.

## More detail

`authoring/cross-references`, `authoring/cross-references-divs`, `authoring/figures`,
`authoring/tables`, `authoring/article-layout`, `authoring/callouts`, `authoring/code-annotation`,
`authoring/citations`, `authoring/conditional`, `authoring/shortcodes`, `authoring/diagrams`,
`authoring/includes`, `authoring/variables`, `authoring/title-blocks`, `authoring/front-matter`.
