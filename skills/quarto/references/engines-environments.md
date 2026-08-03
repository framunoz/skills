# Quarto Computation Engines and Environments

Quarto can render executable cells through project-selected engines and kernels.

## Table of Contents

- [Inspect the Engine](#inspect-the-engine)
- [Environment Boundaries](#environment-boundaries)
- [Execution Safety](#execution-safety)
- [Failures](#failures)

## Inspect the Engine

Determine whether the document uses Jupyter, Knitr/R, Julia, Observable, or
another configured engine. Inspect existing environment and dependency files,
kernel names, and execution settings before editing. See [code cells](code-cells.md)
for Quarto cell options and [project configuration](project-configuration.md)
for shared execution settings.

## Environment Boundaries

Use the project's existing environment manager, lockfile, and kernel rather than
creating a replacement environment. Do not claim an engine is available because
its syntax appears in a document; verify the executable or kernel only with
authorization. Keep credentials, local paths, and secrets out of documents and
rendered output.

## Execution Safety

Rendering may execute code, download data, mutate files, or consume resources.
Before running cells or a full render, state the engine, scope, expected side
effects, network use, and output location, then obtain authorization. Prefer a
non-executing or targeted check when it is sufficient.

## Failures

If a kernel, runtime, or package is unavailable, report the exact missing
dependency and the selected document/engine. Do not silently install it. Use
[CLI and troubleshooting](cli-troubleshooting.md) for Quarto-level diagnosis.
