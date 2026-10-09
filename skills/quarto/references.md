# References

Official documentation for each topic, as clean Markdown. Fetch the URL (WebFetch or `curl -sL`)
when you need exact syntax, the full option list, or anything this skill doesn't cover.

- Pattern: `https://quarto.org/docs/<path>.llms.md` — the short paths in each file's
  "More detail" section are `<path>`.
- Full index of every page: `https://quarto.org/llms.txt`.
- Every option for a format: `reference/formats/<format>` (e.g. `reference/formats/html`).
- Installed-version truth for option names: `uv run scripts/check_option.py <option>`.
- Changelog per minor version:
  `https://raw.githubusercontent.com/quarto-dev/quarto-cli/main/news/changelog-<X.Y>.md`.
- GitHub Actions for publishing: <https://github.com/quarto-dev/quarto-actions>.

## Computations & execution

- [Execution Context Information](https://quarto.org/docs/advanced/quarto-execute-info.llms.md) — `advanced/quarto-execute-info`
- [Caching](https://quarto.org/docs/computations/caching.llms.md) — `computations/caching`
- [Execution Options](https://quarto.org/docs/computations/execution-options.llms.md) — `computations/execution-options`
- [Inline Code](https://quarto.org/docs/computations/inline-code.llms.md) — `computations/inline-code`
- [Using Julia](https://quarto.org/docs/computations/julia.llms.md) — `computations/julia`
- [Parameters](https://quarto.org/docs/computations/parameters.llms.md) — `computations/parameters`
- [Using Python](https://quarto.org/docs/computations/python.llms.md) — `computations/python`
- [Using R](https://quarto.org/docs/computations/r.llms.md) — `computations/r`
- [Managing Execution](https://quarto.org/docs/projects/code-execution.llms.md) — `projects/code-execution`
- [Virtual Environments](https://quarto.org/docs/projects/virtual-environments.llms.md) — `projects/virtual-environments`
- [Code Cells: Jupyter](https://quarto.org/docs/reference/cells/cells-jupyter.llms.md) — `reference/cells/cells-jupyter`
- [Code Cells: Knitr](https://quarto.org/docs/reference/cells/cells-knitr.llms.md) — `reference/cells/cells-knitr`

## Projects

- [Quarto Environment Variables](https://quarto.org/docs/advanced/environment-vars.llms.md) — `advanced/environment-vars`
- [Quarto Inspect](https://quarto.org/docs/advanced/inspect/index.llms.md) — `advanced/inspect/index`
- [Project Environment Variables](https://quarto.org/docs/projects/environment.llms.md) — `projects/environment`
- [Project Profiles](https://quarto.org/docs/projects/profiles.llms.md) — `projects/profiles`
- [Project Basics](https://quarto.org/docs/projects/quarto-projects.llms.md) — `projects/quarto-projects`
- [Project Scripts](https://quarto.org/docs/projects/scripts.llms.md) — `projects/scripts`
- [Quarto Glob Syntax](https://quarto.org/docs/reference/globs.llms.md) — `reference/globs`
- [Project Options](https://quarto.org/docs/reference/projects/options.llms.md) — `reference/projects/options`

## Authoring

- [Article Layout](https://quarto.org/docs/authoring/article-layout.llms.md) — `authoring/article-layout`
- [Multiformat branding with `_brand.yml`](https://quarto.org/docs/authoring/brand.llms.md) — `authoring/brand`
- [Callout Blocks](https://quarto.org/docs/authoring/callouts.llms.md) — `authoring/callouts`
- [Citations](https://quarto.org/docs/authoring/citations.llms.md) — `authoring/citations`
- [Code Annotation](https://quarto.org/docs/authoring/code-annotation.llms.md) — `authoring/code-annotation`
- [Conditional Content](https://quarto.org/docs/authoring/conditional.llms.md) — `authoring/conditional`
- [Cross References](https://quarto.org/docs/authoring/cross-references.llms.md) — `authoring/cross-references`
- [Cross-Reference Div Syntax](https://quarto.org/docs/authoring/cross-references-divs.llms.md) — `authoring/cross-references-divs`
- [Diagrams](https://quarto.org/docs/authoring/diagrams.llms.md) — `authoring/diagrams`
- [Figures](https://quarto.org/docs/authoring/figures.llms.md) — `authoring/figures`
- [Front Matter](https://quarto.org/docs/authoring/front-matter.llms.md) — `authoring/front-matter`
- [Includes](https://quarto.org/docs/authoring/includes.llms.md) — `authoring/includes`
- [Embedding from Other Documents](https://quarto.org/docs/authoring/notebook-embed.llms.md) — `authoring/notebook-embed`
- [Shortcodes](https://quarto.org/docs/authoring/shortcodes.llms.md) — `authoring/shortcodes`
- [Tables](https://quarto.org/docs/authoring/tables.llms.md) — `authoring/tables`
- [Title Blocks](https://quarto.org/docs/authoring/title-blocks.llms.md) — `authoring/title-blocks`
- [Variables](https://quarto.org/docs/authoring/variables.llms.md) — `authoring/variables`
- [Cross Reference Options](https://quarto.org/docs/reference/metadata/crossref.llms.md) — `reference/metadata/crossref`

## HTML

- [Interactivity](https://quarto.org/docs/interactive/index.llms.md) — `interactive/index`
- [Shiny](https://quarto.org/docs/interactive/shiny/index.llms.md) — `interactive/shiny/index`
- [All Formats](https://quarto.org/docs/output-formats/all-formats.llms.md) — `output-formats/all-formats`
- [HTML Accessibility Checks](https://quarto.org/docs/output-formats/html-accessibility.llms.md) — `output-formats/html-accessibility`
- [HTML Basics](https://quarto.org/docs/output-formats/html-basics.llms.md) — `output-formats/html-basics`
- [HTML Code Blocks](https://quarto.org/docs/output-formats/html-code.llms.md) — `output-formats/html-code`
- [Lightbox Figures](https://quarto.org/docs/output-formats/html-lightbox-figures.llms.md) — `output-formats/html-lightbox-figures`
- [Including Other Formats](https://quarto.org/docs/output-formats/html-multi-format.llms.md) — `output-formats/html-multi-format`
- [Publishing HTML](https://quarto.org/docs/output-formats/html-publishing.llms.md) — `output-formats/html-publishing`
- [HTML Theming](https://quarto.org/docs/output-formats/html-themes.llms.md) — `output-formats/html-themes`
- [More About Quarto Themes](https://quarto.org/docs/output-formats/html-themes-more.llms.md) — `output-formats/html-themes-more`
- [Page Layout](https://quarto.org/docs/output-formats/page-layout.llms.md) — `output-formats/page-layout`
- [HTML Options](https://quarto.org/docs/reference/formats/html.llms.md) — `reference/formats/html`

## Revealjs

- [Revealjs Plugins](https://quarto.org/docs/extensions/revealjs.llms.md) — `extensions/revealjs`
- [Advanced Reveal](https://quarto.org/docs/presentations/revealjs/advanced.llms.md) — `presentations/revealjs/advanced`
- [Revealjs](https://quarto.org/docs/presentations/revealjs/index.llms.md) — `presentations/revealjs/index`
- [Presenting Slides](https://quarto.org/docs/presentations/revealjs/presenting.llms.md) — `presentations/revealjs/presenting`
- [Reveal Themes](https://quarto.org/docs/presentations/revealjs/themes.llms.md) — `presentations/revealjs/themes`
- [Revealjs Options](https://quarto.org/docs/reference/formats/presentations/revealjs.llms.md) — `reference/formats/presentations/revealjs`

## Word (docx)

- [Word Basics](https://quarto.org/docs/output-formats/ms-word.llms.md) — `output-formats/ms-word`
- [Word Templates](https://quarto.org/docs/output-formats/ms-word-templates.llms.md) — `output-formats/ms-word-templates`
- [MS Word Options](https://quarto.org/docs/reference/formats/docx.llms.md) — `reference/formats/docx`

## PDF & Typst

- [Typst Brand YAML](https://quarto.org/docs/advanced/typst/brand-yaml.llms.md) — `advanced/typst/brand-yaml`
- [Journal Formats](https://quarto.org/docs/journals/formats.llms.md) — `journals/formats`
- [PDF Basics](https://quarto.org/docs/output-formats/pdf-basics.llms.md) — `output-formats/pdf-basics`
- [PDF Engines](https://quarto.org/docs/output-formats/pdf-engine.llms.md) — `output-formats/pdf-engine`
- [Typst Basics](https://quarto.org/docs/output-formats/typst.llms.md) — `output-formats/typst`
- [Custom Typst Formats](https://quarto.org/docs/output-formats/typst-custom.llms.md) — `output-formats/typst-custom`
- [PDF Options](https://quarto.org/docs/reference/formats/pdf.llms.md) — `reference/formats/pdf`
- [Typst Options](https://quarto.org/docs/reference/formats/typst.llms.md) — `reference/formats/typst`

## Websites, books, manuscripts, publishing

- [Book Crossrefs](https://quarto.org/docs/books/book-crossrefs.llms.md) — `books/book-crossrefs`
- [Customizing Book Output](https://quarto.org/docs/books/book-output.llms.md) — `books/book-output`
- [Book Structure](https://quarto.org/docs/books/book-structure.llms.md) — `books/book-structure`
- [Using Manuscripts](https://quarto.org/docs/manuscripts/components.llms.md) — `manuscripts/components`
- [Quarto Manuscripts](https://quarto.org/docs/manuscripts/index.llms.md) — `manuscripts/index`
- [Publishing with Continuous Integration (CI)](https://quarto.org/docs/publishing/ci.llms.md) — `publishing/ci`
- [GitHub Pages](https://quarto.org/docs/publishing/github-pages.llms.md) — `publishing/github-pages`
- [Publishing Basics](https://quarto.org/docs/publishing/index.llms.md) — `publishing/index`
- [Book Options](https://quarto.org/docs/reference/projects/books.llms.md) — `reference/projects/books`
- [Website Options](https://quarto.org/docs/reference/projects/websites.llms.md) — `reference/projects/websites`
- [About Pages](https://quarto.org/docs/websites/website-about.llms.md) — `websites/website-about`
- [Website Drafts](https://quarto.org/docs/websites/website-drafts.llms.md) — `websites/website-drafts`
- [Document Listings](https://quarto.org/docs/websites/website-listings.llms.md) — `websites/website-listings`
- [Output for LLMs](https://quarto.org/docs/websites/website-llms.llms.md) — `websites/website-llms`
- [Website Navigation](https://quarto.org/docs/websites/website-navigation.llms.md) — `websites/website-navigation`
- [Website Search](https://quarto.org/docs/websites/website-search.llms.md) — `websites/website-search`
- [Website Tools](https://quarto.org/docs/websites/website-tools.llms.md) — `websites/website-tools`

## Dashboards

- [Dashboard Data Display](https://quarto.org/docs/dashboards/data-display.llms.md) — `dashboards/data-display`
- [Dashboard Deployment](https://quarto.org/docs/dashboards/deployment.llms.md) — `dashboards/deployment`
- [Quarto Dashboards](https://quarto.org/docs/dashboards/index.llms.md) — `dashboards/index`
- [Dashboard Input Layout](https://quarto.org/docs/dashboards/inputs.llms.md) — `dashboards/inputs`
- [Interactive Dashboards](https://quarto.org/docs/dashboards/interactivity/index.llms.md) — `dashboards/interactivity/index`
- [Dashboards with Observable JS](https://quarto.org/docs/dashboards/interactivity/observable.llms.md) — `dashboards/interactivity/observable`
- [Dashboards with Shiny for Python](https://quarto.org/docs/dashboards/interactivity/shiny-python/index.llms.md) — `dashboards/interactivity/shiny-python/index`
- [Dashboards with Shiny for R](https://quarto.org/docs/dashboards/interactivity/shiny-r.llms.md) — `dashboards/interactivity/shiny-r`
- [Dashboard Layout](https://quarto.org/docs/dashboards/layout.llms.md) — `dashboards/layout`
- [Dashboard Parameters](https://quarto.org/docs/dashboards/parameters.llms.md) — `dashboards/parameters`
- [Dashboard Theming](https://quarto.org/docs/dashboards/theming.llms.md) — `dashboards/theming`
- [Dashboard Options](https://quarto.org/docs/reference/formats/dashboard.llms.md) — `reference/formats/dashboard`

## Theming & brand

- [Brand Extensions](https://quarto.org/docs/extensions/brand.llms.md) — `extensions/brand`
- [Brand](https://quarto.org/docs/reference/metadata/brand.llms.md) — `reference/metadata/brand`

## Extensions

- [Quarto AST](https://quarto.org/docs/advanced/quarto-ast.llms.md) — `advanced/quarto-ast`
- [Creating Extensions](https://quarto.org/docs/extensions/creating.llms.md) — `extensions/creating`
- [Engine Extensions](https://quarto.org/docs/extensions/engine.llms.md) — `extensions/engine`
- [Creating Filters](https://quarto.org/docs/extensions/filters.llms.md) — `extensions/filters`
- [Custom Formats](https://quarto.org/docs/extensions/formats.llms.md) — `extensions/formats`
- [Quarto Extensions](https://quarto.org/docs/extensions/index.llms.md) — `extensions/index`
- [Quarto Extensions](https://quarto.org/docs/extensions/listing-filters.llms.md) — `extensions/listing-filters`
- [Lua Development](https://quarto.org/docs/extensions/lua.llms.md) — `extensions/lua`
- [Lua API Reference](https://quarto.org/docs/extensions/lua-api.llms.md) — `extensions/lua-api`
- [Managing Extensions](https://quarto.org/docs/extensions/managing.llms.md) — `extensions/managing`
- [Metadata Extensions](https://quarto.org/docs/extensions/metadata.llms.md) — `extensions/metadata`
- [Creating Shortcodes](https://quarto.org/docs/extensions/shortcodes.llms.md) — `extensions/shortcodes`
- [Starter Templates](https://quarto.org/docs/extensions/starter-templates.llms.md) — `extensions/starter-templates`

## General

- [Guide](https://quarto.org/docs/guide/index.llms.md) — `guide/index`
- [Reference](https://quarto.org/docs/reference/index.llms.md) — `reference/index`
- [Positron](https://quarto.org/docs/tools/positron/index.llms.md) — `tools/positron/index`
- [Troubleshooting](https://quarto.org/docs/troubleshooting/index.llms.md) — `troubleshooting/index`

