# Notebook → Kedro Conversion (6-step SOW workflow)

When converting Jupyter Notebooks (`.ipynb`) or `.qmd` scripts into Kedro pipelines, the primary challenge is decoupling monolithic code blocks into modular data, parameters, and pure functions. This workflow uses a 6-step **Statement of Work (SOW)** to align with the user *before* writing large amounts of code.

> **Do NOT** dump a notebook into a single giant node, and do NOT start writing modular code before the SOW is approved. Attempting to convert a large notebook directly to code without first agreeing on the architecture introduces deep bugs and wastes generation tokens.

## Step 1: Analyze & create the Statement of Work

Before writing any Kedro code, scan the notebook:

1. **Dependency analysis**: Scan imports (e.g. `import pandas` requires `kedro-datasets[pandas]`).
2. **Identify configurable parameters vs. hardcoded specs**: Extract values a data scientist might tune (learning rates, thresholds, split sizes) versus structural constants (column names). See `parameters.md` for the decision matrix.
3. **Data I/O mapping**: Identify where files are read or written — each becomes an explicit entry in `catalog.yml`. Watch for code smells like manual `pickle.dump`, `pd.read_csv`, `.to_csv()`, or hardcoded paths; these are exactly what the Catalog should own.

Draft the SOW using the template at the bottom of this file. This ensures consistent alignment with the user.

## Step 2: SOW approval

Present the SOW to the user via the `notify_user` tool and **stop there** — do not continue into Step 4 (writing code) in the same turn. Wait for the user to confirm the pipeline shape, datasets, and parameters.

Why this is a hard stop and not a formality: the SOW *is* the fast path. Decomposition choices (where node boundaries fall, what becomes a dataset vs. a parameter, which layer each output belongs to) ripple across every file you then generate. Getting them wrong means rewriting `nodes.py`, `pipeline.py`, `catalog.yml`, and `parameters.yml` together — far more expensive than the few seconds of confirmation. A quick "looks good" from the user is cheap insurance against a costly rewrite.

This holds **even when the user says "just write the code now"**. A direct request for code is not the same as agreement with a decomposition the user hasn't seen yet — the whole risk is in the structure they can't evaluate until you show it. So still lead with the SOW; treat the urgency as a signal to be concise, not to skip the gate.

Two situations where you may proceed past the SOW in the same turn:
- The user has *already seen and approved* a SOW (e.g. they say "I approved the SOW, go").
- The user has clearly pre-authorized autonomous work / you are running non-interactively and cannot receive a reply. In that case, still **put the SOW first in your output**, then implement — and explicitly call out the key assumptions you made (node boundaries, dataset types, param vs. constant splits) so they remain easy to review and correct after the fact.

## Step 3: Project & pipeline structure setup

If initializing a brand-new Kedro project, use the strict command to avoid obsolete boilerplate:

```bash
kedro new --name <PROJECT> --tools=data,lint,test --example=no --telemetry=no
```

For each identified pipeline, build the scaffold strictly via the CLI:

```bash
kedro pipeline create <pipeline_name>
```

## Step 4: SOW implementation

Execute the SOW systematically (consult `migration_and_syntax.md` for correct 1.0+ syntax and `architecture.md` for standards):

- **`nodes.py`**: Write each notebook cell's logic as a pure function. Remove I/O and display calls (`df.head()`, `plt.show()`). Return the data frames or objects.
- **`pipeline.py`**: Wire nodes using the Kedro 1.0+ `Node` and `Pipeline` classes (do NOT use `kedro.pipeline.node()`).
- **`catalog.yml`**: Declare the inputs/outputs from the SOW using Kedro 1.0+ datasets (e.g. `pandas.CSVDataset`, not `CSVDataSet`). See `data_catalog.md` and `assets/catalog/`.
- **`parameters.yml`**: Insert the identified parameters.

## Step 5: Quality assurance

Verify every piece:

- Every pipeline reproduces the notebook's logic.
- No dataset is saved with `.to_csv()` or `.savefig()` inside Python code — nodes must be pure functions.
- All classes use capitalized `Node` and `Pipeline`, and all datasets end in `Dataset`.

## Step 6: Delivery & testing

Run the pipeline:

```bash
kedro run
```

Confirm the outputs land exactly where the SOW specified.

---

## SOW Template

Use this exact structure when drafting the Statement of Work in Step 1:

```markdown
# Statement of Work: Notebook to Kedro Conversion

## 1. Overview
- **Source Notebook:** [path/to/notebook.ipynb]
- **Target Pipeline:** [pipeline_name]

## 2. Infrastructure & Dependencies
- [ ] Required datasets packages (e.g., `kedro-datasets[pandas]`)
- [ ] Other libraries (e.g., `scikit-learn`, `matplotlib`)

## 3. Data Catalog Mapping
| Dataset Name | Type | Layer | Description |
| :--- | :--- | :--- | :--- |
| `raw_data` | `pandas.CSVDataset` | `01_raw` | Initial raw CSV |
| `processed_data` | `pandas.ParquetDataset` | `02_intermediate` | Cleaned data |

## 4. Parameter Mapping
| Parameter Name | Value (Hardcoded in NB) | Recommendation |
| :--- | :--- | :--- |
| `test_size` | `0.2` | Move to `parameters.yml` |
| `target_column` | `"target"` | Keep as node constant? |

## 5. Proposed Pipeline DAG
- **Node 1:** `preprocess` (Inputs: `raw_data`, `parameters:test_size` -> Outputs: `train`, `test`)
- **Node 2:** `train_model` (Inputs: `train` -> Outputs: `regressor`)
- **Node 3:** `evaluate` (Inputs: `regressor`, `test` -> Outputs: `metrics`)
```
