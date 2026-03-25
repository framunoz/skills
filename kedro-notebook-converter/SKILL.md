---
name: kedro-notebook-converter
description: Strict workflow for converting Jupyter Notebooks (.ipynb) or .qmd scripts into Kedro pipelines. Use this skill whenever the user explicitly asks to convert, migrate, or translate a notebook into Kedro nodes, pipelines, and a data catalog. Do NOT use this skill for general Kedro project creation unless notebooks are involved.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: "1.0.0"
  source: https://github.com/framunoz/my-skills
  inspiration: The [Kedro MCP server](https://docs.kedro.org/en/stable/develop/vibe_coding_with_mcp/)
---

# Notebook to Kedro Conversion Guide

When converting Jupyter Notebooks into Kedro pipelines, the primary challenge is decoupling monolithic code blocks into Modular Data, Parameters, and Pure Functions. To manage this complexity, this guide provides a 6-step Statement of Work (SOW) workflow designed to ensure clear alignment with the user before writing massive amounts of code.

## Step 1: Analyze & Create Statement of Work
Before writing any Kedro code, perform a scan of the notebook:
1. **Dependency Analysis**: Scan imports (e.g., `import pandas` requires `kedro-datasets[pandas]`).
2. **Identify Configurable Parameters vs. Hardcoded Specs**: Extract hardcoded variables that data scientists might want to tune (learning rates, thresholds) versus structural constants (col names).
3. **Data IO Mapping**: Identify where files are read or written; these become explicit entries in `catalog.yml`.

**Important**: Draft your SOW following the structure in `references/sow_template.md`. This ensures consistent alignment with the user.

## Step 2: SOW Approval
Present the SOW to the user via the `notify_user` tool and request explicit confirmation to proceed. Attempting to convert massive notebooks directly to code without first establishing the architecture often introduces deep bugs and wastes generation tokens. Ensuring the user agrees with the proposed pipeline shape and parameters is a critical step for success.

## Step 3: Project & Pipeline Structure Setup
If initializing a completely new Kedro project, use the strict command to avoid obsolete boilerplate:
```bash
kedro new --name <PROJECT> --tools=data,lint,test --example=no --telemetry=no
```
For each identified pipeline within the project, construct the scaffold strictly via the CLI:
```bash
kedro pipeline create <pipeline_name>
```

## Step 4: SOW Implementation
Execute the SOW systematically:
- **nodes.py**: Write the logic of the Jupyter cells as pure functions. Remove I/O and display calls (`df.head()`, `plt.show()`). Return the data frames or objects.
- **pipeline.py**: Wire the nodes together using the Kedro 1.0 `Node` and `Pipeline` class imports. (Do NOT use `kedro.pipeline.node()`).
- **catalog.yml**: Declare the inputs and outputs mapped in the SOW using Kedro 1.0+ datasets (e.g., `pandas.CSVDataset`, not `CSVDataSet`).
- **parameters.yml**: Insert the identified parameters.

## Step 5: Quality Assurance
Verify every piece:
- Every pipeline has equivalent logic to the notebook.
- No dataset is saved using `.to_csv()` or `.savefig()` within the python code. Nodes must be pure functions.
- All classes use capitalized `Node` and `Pipeline`.

## Step 6: Delivery & Testing
Run the execution command:
```bash
kedro run
```
Confirm the outputs are correctly placed exactly as specified in the SOW.
