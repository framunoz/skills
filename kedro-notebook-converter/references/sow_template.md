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
