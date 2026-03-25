---
name: python-formatter
description: Python code formatting and linting using black, ruff, pyrefly, and nbstripout. Use this to enforce project standards, auto-fix style issues, or clean notebooks (.ipynb).
metadata:
  author: Francisco Muñoz (@framunoz)
  version: "1.0.0"
  source: https://github.com/framunoz/skills
---

# Python Formatter

This skill provides a standardized way to format and lint Python code using a pre-defined toolset.

## Core Tools
- **Black**: Formatting with `--preview` and `--unstable`. ([scripts/blackp](scripts/blackp))
- **Ruff**: Fast linting and automatic fixes (including unsafe). ([scripts/ruffp](scripts/ruffp))
- **Pyrefly**: Structural type checking and linting. ([scripts/pyreflyp](scripts/pyreflyp))
- **nbstripout**: Optional cleaning of Jupyter Notebook outputs. ([scripts/nbstripoutp](scripts/nbstripoutp))

## Workflow
1. **Locate Scripts**: Use the relative `scripts/` directory within this skill's path.
2. **Execution**:
   - **General Request**: Run `scripts/format [target]`. This executes Black, Ruff, and Pyrefly in sequence.
   - **Specific Tool**: Run the corresponding script if only one tool or `nbstripoutp` is requested.
3. **Report**: Summarize changes from stdout. If unfixed issues remain, list them briefly and **ask for permission** before making manual edits.

> [!IMPORTANT]
> **Black Box**: Treat all `.sh` scripts as black boxes. Do NOT analyze their internal logic or manually re-run their commands. Execute the script and interpret its final output.
