# Websites, blogs, books, manuscripts

Project types built on the HTML format — everything in `formats/html.md` applies to each page.
Project mechanics (render lists, freeze, profiles) are in `concepts/projects.md`.

## Website

`quarto create project website mysite` (or `blog`). Output in `_site/`.

```yaml
project:
  type: website
website:
  title: "Team Analytics"
  site-url: https://example.org        # needed for sitemap, social cards, RSS
  repo-url: https://github.com/org/repo
  repo-actions: [edit, issue]
  navbar:
    left:
      - href: index.qmd
        text: Home
      - reports.qmd
      - text: "Slides"
        menu: [slides/q1.qmd, slides/q2.qmd]
  sidebar:                             # optional; for docs-style sites
    contents: auto                     # or an explicit tree / directory name
  page-footer: "© 2026 Team"
  search: true                         # default on
  open-graph: true
  llms-txt: true                       # 1.9+: llms.txt + .llms.md per page
format:
  html:
    theme: cosmo
    toc: true
execute:
  freeze: auto
```

- **Listings** (blog index, gallery): on a page,
  `listing: {contents: posts, type: default | grid | table, sort: "date desc", categories: true, feed: true}`.
- **Drafts**: `draft: true` on a page; `website: draft-mode: gone | unlinked | visible`.
- Slides inside a site: give the page `format: revealjs` in its own front matter.
- About pages: `about: {template: jolla | trestles | solana | marquee | broadside}`.
- Redirects: `aliases: [old-url.html]` on a page.

## Book

`quarto create project book mybook`. HTML in `_book/`, plus PDF/EPUB/docx from the same source.

```yaml
project:
  type: book
book:
  title: "Methods"
  author: "Team"
  chapters:
    - index.qmd                  # required: the preface / landing page
    - part: "Data"
      chapters: [data.qmd, cleaning.qmd]
    - models.qmd
    - references.qmd
  appendices: [appendix-a.qmd]
  downloads: [pdf, epub]
  repo-url: https://github.com/org/book
bibliography: references.bib
format:
  html: {theme: cosmo}
  pdf: {documentclass: scrreprt}
```

- One `#` heading per chapter file = the chapter title; sections inside are `##`.
- Cross-references work across chapters and are numbered per chapter (`Figure 2.3`).
  Unnumbered chapter: `# Preface {.unnumbered}`.
- References page: a chapter containing `::: {#refs} :::`.
- Render one chapter while writing: `quarto preview` and edit; full `quarto render` before publishing.

## Manuscript

Scholarly article + notebooks + multiple formats + MECA bundle for journals.

```yaml
project:
  type: manuscript
manuscript:
  article: index.qmd
  notebooks: [notebooks/analysis.ipynb]
format:
  html: default
  docx: default
  jats: default
```

Embed results from notebooks into the article with `{{< embed notebooks/analysis.ipynb#fig-map >}}`.

## Publishing

| Target | How |
|---|---|
| GitHub Pages | `quarto publish gh-pages` (renders, pushes to `gh-pages` branch), or `output-dir: docs` and commit, or GitHub Actions with `quarto-dev/quarto-actions` |
| Quarto Pub | `quarto publish quarto-pub` |
| Netlify | `quarto publish netlify` |
| Posit Connect / Connect Cloud | `quarto publish connect` / `posit-connect-cloud` |
| Confluence | `quarto publish confluence` |
| Hugging Face Spaces | `quarto publish huggingface` |

`posit-cloud` was removed as a publish target in 1.8. CI without R/Python: commit `_freeze/`
and let CI render with frozen results (`publishing/ci`).

## More detail

`websites/website-navigation`, `websites/website-listings`, `websites/website-tools`,
`websites/website-search`, `websites/website-llms`, `websites/website-drafts`,
`websites/website-about`, `reference/projects/websites`, `books/book-structure`,
`books/book-output`, `books/book-crossrefs`, `reference/projects/books`, `manuscripts/index`,
`manuscripts/components`, `publishing/index`, `publishing/github-pages`, `publishing/ci`.
