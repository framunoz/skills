# Quarto Computation Engines and Environments

Quarto can render executable cells through project-selected engines and kernels.

## Table of Contents

- [Inspect the Engine](#inspect-the-engine)
- [Environment Boundaries](#environment-boundaries)
- [Kernel and Environment Discovery](#kernel-and-environment-discovery)
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

## Kernel and Environment Discovery

Start with the document and repository evidence: identify its engine, existing
environment manager and lockfile, configured kernel name, and any project-level
execution settings. For Jupyter documents, distinguish the kernel recorded by
the notebook or document from the Python executable currently on `PATH`; they
need not be the same environment.

With authorization, inspect rather than install: run `quarto check`, use
`quarto inspect <document>` when available in the installed version, and query
the existing environment's kernel listing with its own tool. Record the exact
kernel name and executable selected. If discovery disagrees with repository
configuration, stop before changing kernels or dependencies and report both
sources of evidence.

## Execution Safety

Rendering may execute code, download data, mutate files, or consume resources.
Before running cells or a full render, state the engine, scope, expected side
effects, network use, and output location, then obtain authorization. Prefer a
non-executing or targeted check when it is sufficient.

## Failures

If a kernel, runtime, or package is unavailable, report the exact missing
dependency and the selected document/engine. Do not silently install it. Use
[CLI and troubleshooting](cli-troubleshooting.md) for Quarto-level diagnosis.
