# Word (docx)

For editable hand-offs: reviewers who comment or track changes in Word, or organisations that
require `.docx`. Layout control is limited — Word styles, not CSS, decide the look.

```yaml
format:
  docx:
    reference-doc: templates/company.docx   # styles template (fonts, headings, margins)
    toc: true
    toc-depth: 2
    number-sections: true
    syntax-highlighting: github
    fig-width: 6.5                          # inches; match the page text width
```

## House style: `reference-doc`

1. `quarto pandoc -o custom-reference-doc.docx --print-default-data-file reference.docx`
2. Open it in Word and edit **styles** (Normal, Heading 1–3, Title, Caption, Table…), not the
   text. Content in the reference doc is ignored; only styles, page setup and headers/footers carry over.
3. Point `reference-doc:` at it. Commit the template with the project.

## What survives in Word

| Works | Doesn't (provide a fallback) |
|---|---|
| Headings, lists, pipe/grid/list tables, footnotes, citations | HTML widgets, plotly, ojs (render static images) |
| Cross-references, captions, equations (native Word math) | Tabsets, margin columns, code folding |
| Callouts (as simple boxes), `{{< pagebreak >}}` | Custom CSS, most `.column-*` layout |
| Images with `width=` | Mermaid/Graphviz need `chrome-headless-shell` (rendered to PNG) |

Hide HTML-only content with `.content-visible when-format="html"`.
Raw Word XML goes in a ```` ```{=openxml} ```` block.

## Tips

- Tables from code: `flextable` (R) converts best; `gt` and `great_tables` are HTML-first.
- `toc` inserts a TOC *field*; Word may ask to update fields on open.
- Several formats from one source: `format: {html: default, docx: default}`; the HTML gets
  "Other Formats" links (`format-links`).

## More detail

`output-formats/ms-word`, `output-formats/ms-word-templates`, `reference/formats/docx`.
