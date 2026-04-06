# 🗂️ Data Catalog & Layering Standards

## 1. Data Layering Convention

Kedro encourages a strict layered approach to data engineering. Each folder in the `data/` directory has a specific purpose and ruleset:

- **`01_raw`**: Source data model. **Never mutate the data here**, only work on copies. Treat as immutable.
- **`02_intermediate`**: Typed mirror of the raw layer (e.g., converted to Apache Parquet). Still within the source data model. Minor transformations permitted (cleaning column names, parsing dates, dropping completely null columns).
- **`03_primary`**: Domain-level data. Data is engineered into a structure fit for the analytical purpose. Redundant source-level datapoints are discarded.
- **`04_feature`**: Constructed exclusively from the primary layer. Features are engineered at a consistent level of aggregation (unit of analysis / grain). Target variables also reside here.
- **`05_model_input`**: Where all features are joined together to create the inputs to the models. Often includes joining tables (spine tables) to anchor inputs to the correct grain.
- **`06_models`**: Serialized trained models (e.g., Pickles) saved for reproducibility.
- **`07_model_output`**: The results, predictions, or recommendations of the model runs.
- **`08_reporting`**: Descriptive reporting, metrics, and visualizations (e.g., HTML, PNG) providing a helicopter view for the business.

## 2. Dataset Type Standards

- Use proper casing for Kedro 1.0+: `pandas.CSVDataset` (not `CSVDataSet`). All dataset classes must end exclusively in `Dataset`.
- Match dataset type exactly to the use case based on file extension.
- **Dependency Reminder**: Most datasets now live in `kedro-datasets`. E.g., `pandas.CSVDataset` requires installing `kedro-datasets[pandas]`.

### Common Dataset Types Reference Table

| Target Framework | Kedro 1.0+ Python Type | Recommended `data/` Layer Use Case | Requires |
| :--- | :--- | :--- | :--- |
| **Pandas CSV** | `pandas.CSVDataset` | `01_raw` / `08_reporting` (Human readable) | `kedro-datasets[pandas]` |
| **Pandas Parquet** | `pandas.ParquetDataset` | `02_intermediate` through `05_model_input` (Performance) | `kedro-datasets[pandas]` |
| **Pandas Excel** | `pandas.ExcelDataset` | `01_raw` | `kedro-datasets[pandas]` |
| **Pickle** | `pickle.PickleDataset` | `06_models` (Model artifacts) | `kedro-datasets` |
| **JSON** | `json.JSONDataset` | `08_reporting` (Metrics docs) | `kedro-datasets` |
| **YAML** | `yaml.YAMLDataset` | `01_raw` (Config inputs) | `kedro-datasets` |
| **Matplotlib** | `matplotlib.MatplotlibDataset` | `08_reporting` (Static plots `.png`) | `kedro-datasets[matplotlib]` |
| **Plotly JSON/HTML** | `plotly.JSONDataset` / `plotly.HTMLDataset` | `08_reporting` (Interactive plots) | `kedro-datasets[plotly]` |
| **API** | `api.APIDataset` | `01_raw` (External REST pulls) | `kedro-datasets[api]` |
| **SQL Table** | `pandas.SQLTableDataset` | `01_raw` / `03_primary` | `kedro-datasets[pandas]` |

## 3. Comprehensive Dataset Examples

Robust, copy-pasteable YAML examples for every standard dataset type (including configuration parameters, credentials, and metadata) have been extracted into the `examples/` directory to keep this reference clean.

Please view the relevant file in the `examples/` directory for exact syntax:
- `pandas_csv.yml`
- `pandas_parquet.yml`
- `pandas_excel.yml`
- `pickle.yml`
- `json.yml`
- `yaml_dataset.yml`
- `matplotlib.yml`
- `plotly.yml`
- `api.yml`
- `sql_table.yml`

## 4. Advanced Catalog Examples

When building real-world pipelines, you will often need more than simple I/O. Use these exact yaml configurations as a template:

### Versioned Datasets
Versioning keeps a history of the dataset instead of overwriting it on every run.
```yaml
model_training.trained_model:
  type: pickle.PickleDataset
  filepath: data/06_models/model.pkl
  versioned: true
```

### Metadata (Kedro-Viz Layers)
In Kedro 1.0+, visual layer metadata belongs strictly inside the `metadata` block. 
```yaml
data_processing.cleaned_data:
  type: pandas.ParquetDataset
  filepath: data/02_intermediate/cleaned_data.parquet
  metadata:
    kedro-viz:
      layer: intermediate
```

### Partitioned Datasets
When a node needs to process a directory of multiple files iteratively, use `partitions.PartitionedDataset`.
```yaml
data_science.model_inputs:
  type: partitions.PartitionedDataset
  path: data/05_model_input/
  dataset: pandas.CSVDataset
  filename_suffix: ".csv"
```

### Dataset Factories
To avoid repeating boilerplate in `catalog.yml` for multiple datasets of the same type/layer, use Dataset Factories. This allows a single registry entry to dynamically match multiple strings.
```yaml
"{name}_factory_data":
  type: pandas.CSVDataset
  filepath: data/01_raw/{name}_data.csv
```
*(This single entry automatically resolves any request for `sales_factory_data`, `users_factory_data`, etc.)*

## 4. Advanced Catalog Configurations

Beyond standard `load_args` and `save_args`, Kedro's `catalog.yml` supports powerful native parameters at the root level of the dataset definition:

### A. Versioning (`versioned: true`)
When enabled, Kedro avoids overwriting the filepath. Instead, it saves new outputs into timestamped subdirectories (e.g., `data/06_models/random_forest.pkl/2023-10-27T12.00.00Z/random_forest.pkl`).
- **Use Case:** Machine learning models, critical compliance reports, tracking data drift over time.
- **Important:** When loading a versioned dataset, Kedro automatically fetches the *latest* version unless explicitly overridden in the code.

### B. Memory Management (`copy_mode`)
By default, when a node returns a dataset (MemoryDataset or otherwise), Kedro passes a deep copy to the next node to ensure immutability. You can override this to save RAM on massive datasets:
- `copy_mode: assign` (No copying, passes the exact object reference. Danger: mutability).
- `copy_mode: copy` (Shallow copy).
- `copy_mode: deepcopy` (Default, safest but highest RAM usage).

### C. File System Arguments (`fs_args`)
Kedro uses `fsspec` under the hood. You can pass arbitrary configuration to the underlying filesystem (AWS S3, Google GCS, Azure Blob, SFTP) directly from the catalog.
- **Example:** Passing S3 endpoint URLs, SSL configurations, or custom authentication tokens.

### D. Data Layer Visibility (`metadata.kedro-viz.layer`)
This does not affect execution, but it is strictly required by our authoring standards so that frontend tools like `kedro-viz` can render the DAG correctly grouped into visualswimlanes (`raw`, `intermediate`, `primary`, `feature`, `model_input`, `models`, `model_output`, `reporting`).

## 5. Useful Documentation Links
To "learn more" about these standards and how to implement advanced I/O (e.g., partitioning, remote S3 storage), consult the official documentation:
- [Kedro Documentation - Data Catalog](https://docs.kedro.org/en/stable/data/data_catalog.html)
- [Kedro-Datasets API Reference](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-3.0.0/api/kedro_datasets.html)
