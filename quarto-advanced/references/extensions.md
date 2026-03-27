# Extensions

Quarto extensions add custom functionality including shortcodes, filters, formats, and RevealJS plugins.

## Table of Contents

* [Extension Types](#extension-types)
* [Finding Extensions](#finding-extensions)
  * [Official Repository](#official-repository)
  * [Community Extensions](#community-extensions)
* [Installing Extensions](#installing-extensions)
  * [Basic Installation](#basic-installation)
  * [From GitHub](#from-github)
  * [Specific Version](#specific-version)
  * [From URL](#from-url)
  * [Interactive Installation](#interactive-installation)
* [Using Extensions](#using-extensions)
  * [In Document YAML](#in-document-yaml)
  * [Shortcode Extensions](#shortcode-extensions)
  * [Format Extensions](#format-extensions)
* [Managing Extensions](#managing-extensions)
  * [Location](#location)
  * [List Installed Extensions](#list-installed-extensions)
  * [Update Extensions](#update-extensions)
  * [Remove Extensions](#remove-extensions)
* [Project vs Document Extensions](#project-vs-document-extensions)
  * [Project-Wide](#project-wide)
  * [Global Extensions](#global-extensions)
* [Popular Extensions](#popular-extensions)
  * [Icons](#icons)
  * [Lightbox](#lightbox)
  * [Include Code from Files](#include-code-from-files)
  * [Fancy Text](#fancy-text)
  * [Social Cards](#social-cards)
* [Extension Configuration](#extension-configuration)
* [Creating Custom Extensions](#creating-custom-extensions)
  * [Basic Structure](#basic-structure)
  * [Extension YAML](#extension-yaml)
  * [Shortcode Lua](#shortcode-lua)
  * [Use](#use)
* [Troubleshooting](#troubleshooting)
  * [Extension Not Found](#extension-not-found)
  * [Trust Warning](#trust-warning)
  * [Conflicts](#conflicts)
* [Extension Sources](#extension-sources)
  * [GitHub Organizations](#github-organizations)
  * [Popular Repositories](#popular-repositories)
* [Best Practices](#best-practices)
  * [Before Installing](#before-installing)
  * [In Projects](#in-projects)
  * [Updating](#updating)
* [Resources](#resources)

## Extension Types

| Type             | Description                               |
| ---------------- | ----------------------------------------- |
| Shortcodes       | Custom `{{< shortcode >}}` commands       |
| Filters          | Pandoc filters for content transformation |
| Formats          | Custom output formats                     |
| RevealJS Plugins | Presentation enhancements                 |

## Finding Extensions

### Official Repository

- [Quarto Extensions](https://quarto.org/docs/extensions/)
- Browse by category: filters, shortcodes, formats, etc.

### Community Extensions

- [Community Extensions List](https://m.canouil.dev/quarto-extensions/)
- [Extensions JSON](https://m.canouil.dev/quarto-extensions/extensions.json)
- Search GitHub for `quarto-extension`

## Installing Extensions

### Basic Installation

```bash
quarto add username/repository
```

### From GitHub

```bash
quarto add quarto-ext/fontawesome
quarto add shafayetShafee/bsicons
```

### Specific Version

```bash
quarto add username/repository@v1.0.0
```

### From URL

```bash
quarto add https://github.com/user/repo/archive/main.zip
```

### Interactive Installation

When prompted, confirm trust in the extension source.

## Using Extensions

### In Document YAML

```yaml
---
filters:
  - extension-name
---
```

### Shortcode Extensions

After installing, use in document:

````markdown
{{< fa brands github >}} # Font Awesome icon
````

### Format Extensions

```yaml
format: custom-format
```

## Managing Extensions

### Location

Extensions are stored in `_extensions/` directory:

```txt
project/
├── _extensions/
│   └── fontawesome/
│       ├── _extension.yml
│       └── fontawesome.lua
├── document.qmd
└── _quarto.yml
```

### List Installed Extensions

```bash
ls _extensions/
```

### Update Extensions

```bash
quarto add username/repository  # Re-run to update
```

### Remove Extensions

Delete the folder from `_extensions/`:

```bash
rm -rf _extensions/extension-name
```

## Project vs Document Extensions

### Project-Wide

Install in project root. Available to all documents:

```txt
project/
├── _extensions/
├── chapter1.qmd
└── chapter2.qmd
```

### Global Extensions

Install in user config (less common):

```bash
quarto add --global username/repository
```

Location: `~/.local/share/quarto/extensions/`

## Popular Extensions

### Icons

```bash
quarto add quarto-ext/fontawesome
```

````markdown
{{< fa brands github >}} GitHub
{{< fa solid envelope >}} Email
````

### Lightbox

```bash
quarto add quarto-ext/lightbox
```

```yaml
lightbox: true
```

### Include Code from Files

```bash
quarto add quarto-ext/include-code-files
```

````markdown
{{< include-code example.py >}}
````

### Fancy Text

```bash
quarto add quarto-ext/fancy-text
```

````markdown
{{< lipsum 1 >}}
````

### Social Cards

```bash
quarto add gadenbuie/quarto-social-embeds
```

````markdown
{{< tweet user=username id=123456789 >}}
````

## Extension Configuration

Some extensions have configuration options:

```yaml
lightbox:
  match: auto
  effect: zoom
  loop: true

fontawesome:
  version: 6
```

## Creating Custom Extensions

### Basic Structure

```txt
_extensions/
└── my-extension/
    ├── _extension.yml
    └── my-extension.lua
```

### Extension YAML

In `_extension.yml`:

```yaml
title: My Extension
author: Your Name
version: 1.0.0
contributes:
  shortcodes:
    - my-extension.lua
```

### Shortcode Lua

In `my-extension.lua`:

```lua
return {
  ['my-shortcode'] = function(args)
    local text = args[1] or "default"
    return pandoc.Str("Processed: " .. text)
  end
}
```

### Use

````markdown
{{< my-shortcode "Hello" >}}
````

## Troubleshooting

### Extension Not Found

```txt
ERROR: Extension not found
```

- Check extension is in `_extensions/`
- Verify extension name matches folder

### Trust Warning

When installing, Quarto asks about trust. Extensions run code during render.

### Conflicts

If extensions conflict, try:

1. Check extension documentation for compatibility
2. Update extensions to latest versions
3. Report issue to extension maintainer

## Extension Sources

### GitHub Organizations

- `quarto-ext` - Official Quarto extensions
- `quarto-journals` - Academic journal formats

### Popular Repositories

| Extension                       | Description           |
| ------------------------------- | --------------------- |
| `quarto-ext/fontawesome`        | Font Awesome icons    |
| `quarto-ext/lightbox`           | Image lightbox        |
| `quarto-ext/include-code-files` | Include external code |
| `shafayetShafee/bsicons`        | Bootstrap icons       |
| `mcanouil/quarto-letter`        | Letter format         |
| `jmbuhr/quarto-molstar`         | Molecular viewer      |

## Best Practices

### Before Installing

1. Check extension source is trustworthy
2. Read the documentation
3. Check compatibility with your Quarto version

### In Projects

1. Document which extensions are used
2. Include `_extensions/` in version control
3. Pin versions for reproducibility

### Updating

1. Test updates in development first
2. Check changelogs for breaking changes
3. Update one at a time

## Resources

- [Quarto Extensions Guide](https://quarto.org/docs/extensions/)
- [Creating Extensions](https://quarto.org/docs/extensions/creating.html)
- [Community Extensions](https://m.canouil.dev/quarto-extensions/)
- [Extensions JSON API](https://m.canouil.dev/quarto-extensions/extensions.json)
