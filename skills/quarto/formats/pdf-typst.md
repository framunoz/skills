# PDF: LaTeX or Typst

Two routes to a PDF. Choose with `cheatsheet.md` → "PDF engine"; in short: **Typst** for fast,
modern-looking reports with no TeX install; **LaTeX** (`format: pdf`) for journal templates,
heavy math, or LaTeX packages you already depend on.

## Typst (`format: typst`)

Typst ships inside Quarto — nothing to install. Compiles in seconds.

```yaml
format:
  typst:
    papersize: a4               # Typst paper names: a4, us-letter, a5…
    margin: {x: 2cm, y: 2.5cm}  # or top/bottom/left/right
    columns: 1
    mainfont: "Inter"
    fontsize: 11pt
    toc: true
    section-numbering: 1.1.a
    keep-typ: true              # keep the .typ for debugging
```

- Image sizes may differ from other formats: set widths explicitly (`{width=80%}`).
- Brand: `_brand.yml` applies colours, fonts, logo (`brand-mode: dark` for the dark brand).
- Raw Typst: ```` ```{=typst} ```` blocks; `{{< pagebreak >}}` for page breaks.
- Since 1.9: Skylighting is the default highlighter (`syntax-highlighting: idiomatic` for
  Typst's own); theorems use the `theorion` package (`theorem-appearance: simple | fancy | …`).
- Custom look: Typst format extensions or template partials (`typst-template.typ`,
  `typst-show.typ`) — see `output-formats/typst-custom`. Fonts in a project folder:
  `font-paths: [fonts]`.
- Mermaid/Graphviz become images; HTML widgets don't render — gate them with conditional content.

## LaTeX (`format: pdf`)

Requires a TeX distribution. Recommended: `quarto install tinytex`; missing LaTeX packages
are installed automatically on first use (`latex-auto-install`).

```yaml
format:
  pdf:
    documentclass: scrartcl     # KOMA classes by default (scrartcl / scrreprt / scrbook)
    papersize: a4
    geometry: [margin=2.5cm]
    toc: true
    number-sections: true
    colorlinks: true
    mainfont: "Source Serif 4"  # system fonts work with the default lualatex
    include-in-header:
      text: |
        \usepackage{booktabs}
```

- **Default engine is `lualatex` since 1.8** (was `xelatex`). Override with
  `pdf-engine: xelatex | pdflatex | tectonic | latexmk`.
- Debug: `keep-tex: true`, then compile the `.tex` yourself to see the full LaTeX error.
- Figure placement: `fig-pos: "H"` (exact) or `"t"`; long tables from code need
  `longtable`-friendly packages (`kableExtra`, `gt` handles it).
- Raw LaTeX: ```` ```{=latex} ```` blocks or inline `` `\newpage`{=latex} ``.
- Journal templates: `quarto use template quarto-journals/<name>` (`journals/formats`).

## Common to both

- Interactive output (htmlwidgets, plotly, ojs) does not exist in PDF: render a static
  alternative (`webshot2`/`kaleido`) or hide it with `.content-visible when-format="html"`.
- PDF/A and accessibility: `pdf-standard` (`reference/formats/pdf`, `reference/formats/typst`).
- Fonts must exist on the machine that renders (CI too).

## More detail

`output-formats/typst`, `output-formats/typst-custom`, `advanced/typst/brand-yaml`,
`output-formats/pdf-basics`, `output-formats/pdf-engine`, `journals/formats`,
`reference/formats/pdf`, `reference/formats/typst`.
