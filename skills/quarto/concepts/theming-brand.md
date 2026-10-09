# Theming and brand

Three layers, from broadest to most specific:

1. **`_brand.yml`** — colours, fonts, logos once, applied to HTML, revealjs, dashboards, Typst
   (and partially PDF). Best for organisation-wide identity.
2. **Theme** — Bootswatch theme (HTML: 25 themes, e.g. `cosmo`, `flatly`, `darkly`) or reveal
   theme, plus your SCSS.
3. **Format options** — `mainfont`, `fontsize`, `linestretch`, `linkcolor`, `max-width`…
   quick tweaks without SCSS.

## `_brand.yml`

Place it next to `_quarto.yml` (or next to a lone document) and Quarto applies it automatically.

```yaml
color:
  palette:
    navy: "#1b2a41"
    sand: "#f4efe6"
  background: sand
  foreground: navy
  primary: navy
logo:
  medium: assets/logo.png        # paths relative to the brand file
typography:
  fonts:
    - family: Inter
      source: google
  base: Inter
  headings: Inter
  monospace: JetBrains Mono
```

- Elsewhere: `brand: brand/_brand.yml` in `_quarto.yml`. Disable for a document: `brand: false`.
  A `brand:` map in front matter **replaces** the file's brand entirely.
- **Light/dark in one file** (1.8+): any colour can be `{light: "#fff", dark: "#222"}`.
- revealjs and Typst render the light brand; `brand-mode: dark` selects the dark one.
- Use brand values in content: `{{< brand color primary >}}`, `{{< brand logo medium >}}`.
- Shared org brand: `quarto use brand myorg/shared-brand` copies files into `_brand/`
  (`--dry-run` to preview), or distribute it as a brand extension. All brand assets must live
  inside the project.

## SCSS themes

A theme file has named sections:

```scss
/*-- scss:defaults --*/
$primary: #1b2a41;
$font-size-root: 17px;

/*-- scss:rules --*/
.callout { border-radius: 6px; }
```

- Variables go in `defaults` (they set Bootstrap/Quarto variables *before* compilation); CSS
  rules in `rules`. Also `functions`, `mixins`, `uses`.
- Layer with a list; later entries win: `theme: [cosmo, brand, custom.scss]`.
- Light/dark: `theme: {light: [flatly, light.scss], dark: [darkly, dark.scss]}`;
  `respect-user-color-scheme: true` to follow the OS.
- Content per mode: classes `.light-content` / `.dark-content`.
- revealjs uses the same mechanism with reveal variables (`$body-bg`, `$link-color`,
  `$presentation-heading-font`…). See `presentations/revealjs/themes`.
- Plain `css:` files work too but cannot change Sass variables.

## Syntax highlighting

`syntax-highlighting: github` (1.9+; `highlight-style` is deprecated). Accepts a name
(`a11y`, `arrow`, `atom-one`, `breeze`, `dracula`, `github`, `gruvbox`, `monokai`, `nord`, …),
a `.theme` file, or `{light: github, dark: dracula}`. In Typst, `idiomatic` uses Typst's own
highlighter (Skylighting is the default since 1.9).

## More detail

`authoring/brand`, `reference/metadata/brand`, `output-formats/html-themes`,
`output-formats/html-themes-more`, `presentations/revealjs/themes`, `dashboards/theming`,
`advanced/typst/brand-yaml`, `extensions/brand`.
