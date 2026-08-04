# Quarto Project Configuration

Quarto projects are configured from the project root, normally in
`_quarto.yml`. This guide is about Quarto configuration, not generic YAML.

## Table of Contents

- [Inspect First](#inspect-first)
- [Configuration Layers](#configuration-layers)
- [Precedence and Conflicts](#precedence-and-conflicts)
- [Format Capabilities](#format-capabilities)
- [Version and Provenance](#version-and-provenance)

## Inspect First

Locate `_quarto.yml`, profile files, document front matter, metadata files, and
the project output directory. Run `quarto --version` only when execution is
authorized. Preserve the existing project type, naming, and output convention.

## Configuration Layers

Use `_quarto.yml` for project-wide `project`, `format`, `execute`, and shared
metadata settings. Use a document's YAML only for local metadata or intentional
local variation. See [YAML front matter](yaml-front-matter.md) for document
syntax and [profiles and directory metadata](profiles-directory-metadata.md) for
profiles and `_metadata.yml`.

## Precedence and Conflicts

Resolve the effective configuration rather than guessing. In practical order,
shared project defaults are specialized by the selected profile, directory
metadata, document YAML, format-specific settings, and explicit command-line
input. A more-specific setting can replace or merge with a broader one depending
on its YAML shape; verify a conflict with the installed Quarto version.

Avoid copying a setting into every layer. Put shared values at project scope,
format-specific values under `format`, and one-document changes in that document.
When two layers disagree, retain the established owner unless the task requires a
deliberate override; document the selected profile and format in the change.

## Format Capabilities

`html`, `pdf`, `docx`, `typst`, and `revealjs` do not accept the same options or
runtime features. Confirm an option is supported by the chosen format before
reuse. PDF often depends on TeX; interactive content is generally an HTML
concern; Typst and RevealJS have format-specific configuration. See
[Typst](typst.md), [RevealJS](revealjs.md), and [CLI troubleshooting](cli-troubleshooting.md).

## Version and Provenance

These documents are maintained guidance, not a promise for a fixed Quarto
release. Check installed Quarto capabilities, `quarto --help`, and current local
project conventions before using version-sensitive options. Record the installed
version and any authoritative source consulted when behavior is uncertain.
