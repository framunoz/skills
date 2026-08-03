# Quarto CLI and Troubleshooting

Use the Quarto CLI to inspect and render Quarto projects only after authorization.

## Table of Contents

- [Safe Diagnostics](#safe-diagnostics)
- [Render Scope](#render-scope)
- [Common Failures](#common-failures)
- [Report Results](#report-results)

## Safe Diagnostics

Start by locating the project root and configuration. With authorization, use
`quarto --version` and relevant `quarto --help` output to establish installed
capabilities. Do not infer support from these references or a remote example.

## Render Scope

Prefer the narrowest authorized command: inspect configuration before rendering a
document, and render one document before a whole project. Explain that rendering
may execute cells and overwrite generated output. Use the selected profile and
format deliberately; see [project configuration](project-configuration.md).

## Common Failures

- **Quarto missing or not on PATH:** report the executable failure and request
  installation or PATH correction; do not fabricate output.
- **Engine/kernel missing:** identify the document, engine, and environment;
  stop before installing dependencies. See [engines and environments](engines-environments.md).
- **PDF failure or missing TeX:** report the TeX dependency and offer an
  authorized installation path or a supported alternate format.
- **Unknown format/option:** confirm the installed version and format-specific
  support; do not copy HTML options into PDF, Typst, or RevealJS.
- **Extension failure:** inspect source and version, then obtain authorization
  before install, update, or removal. See [extensions](extensions.md).

## Report Results

State the command run, project/profile/document/format selected, engine status,
generated location, and the exact remaining failure or validation result.
