# Extensions, filters, custom formats

Reach for an extension when built-in syntax and options can't express what you need. Search the
listings (`extensions/listing-filters`, `-formats`, `-journals`, `-revealjs`) before writing one.

## Kinds

| Kind | Adds | Used via |
|---|---|---|
| Shortcode | `{{< name args >}}` | automatic once installed |
| Filter | Lua transformation of the Pandoc AST | `filters: [name]` |
| Custom format | Preconfigured format + templates (journals, company reports) | `format: name-html` / `name-pdf` / `name-typst` |
| Revealjs plugin | reveal.js plugin | `revealjs-plugins: [name]` |
| Brand | Shared `_brand.yml` | `brand:` / `quarto use brand` |
| Metadata | Default options | `extensions/metadata` |
| Project type | Custom project type | `project: type:` |
| Engine (1.9+) | A new execution engine for a cell language | `engine: name` |
| Starter template | Scaffold for `quarto use template` | one-off |

## Managing

```bash
quarto add quarto-ext/fontawesome      # GitHub org/repo, URL, or local zip/dir
quarto list extensions
quarto update extension quarto-ext/fontawesome
quarto remove quarto-ext/fontawesome
quarto use template org/repo           # new project from a starter template
```

Installs into `_extensions/` at the project root (or the current directory without a
project). **Commit `_extensions/`** — renders, collaborators and CI need it.

## Installing or updating safely

Extensions are third-party code that runs during every render (Lua filters, JS, engine
TypeScript). A request to "install/update X" is a request to *prepare* the change:

1. Inspect the current state: `_extensions/` contents, `quarto list extensions`, where the
   extension is used.
2. Check it is still needed — several popular extensions are now built in: `lightbox`
   (`lightbox: true`, 1.4+), `video` (`{{< video >}}`), code annotations, `kbd`.
3. Pin the source: a tag or branch (`quarto add org/repo@v1.2`, documented); for an exact
   commit, add the archive URL (`quarto add https://github.com/org/repo/archive/<sha>.zip`; verified on 1.10.19).
   Read its `_extension.yml` and filters.
4. State the exact command and the project path, and get explicit confirmation before running it.
5. Afterwards review the `_extensions/` diff and render only the documents that use it.

## Filters

```yaml
filters:
  - local-filter.lua     # file path
  - quarto               # position of Quarto's own filters (default: user filters run first)
  - fontawesome          # installed extension by name
```

Need a finer position? Target an AST phase (`at: pre-ast | post-ast | pre-quarto |
post-quarto | pre-render | post-render`) — see `advanced/quarto-ast`.

Minimal filter (uppercases level-2 headings):

```lua
function Header(el)
  if el.level == 2 then
    el.content = pandoc.utils.stringify(el.content):upper()
  end
  return el
end
```

Develop with `quarto preview example.qmd` — the preview refreshes when the `.lua` changes.
`quarto.doc.is_format("html")` branches by format; `quarto.log.output(x)` dumps values.

## Creating an extension

```bash
quarto create extension          # prompts for the kind; or e.g. `quarto create extension engine`
```

Layout: `_extensions/<name>/_extension.yml` declares `contributes:` (`filters`, `shortcodes`,
`formats`, `revealjs-plugins`, `metadata`, `project`, `engines`). Engine extensions are written
in TypeScript and built with `quarto call build-ts-extension` (1.9+); still one engine per document.

## More detail

`extensions/index`, `extensions/managing`, `extensions/creating`, `extensions/filters`,
`extensions/shortcodes`, `extensions/formats`, `extensions/revealjs`, `extensions/engine`,
`extensions/lua`, `extensions/lua-api`, `advanced/quarto-ast`, `extensions/starter-templates`.
