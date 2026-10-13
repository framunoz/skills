# Statement of Work: notebook → Kedro

## 1. Scope
- Source: `notebooks/<name>.ipynb` (cells N–M)
- Target pipeline(s): `<pipeline_name>` (created with `uv run kedro pipeline create <pipeline_name>`)

## 2. Dependencies
- Project: `uv add <libs>`
- Datasets: `uv add "kedro-datasets[<extras from check_dataset.py>]"`

## 3. Catalog
| Dataset | Type | Filepath | Layer | From cell |
|---|---|---|---|---|
| `raw_obs` | `pandas.CSVDataset` | `data/01_raw/obs.csv` | raw | 2 (`pd.read_csv`) |
| `clean_obs` | `pandas.ParquetDataset` | `data/02_intermediate/clean_obs.parquet` | intermediate | 5 |
| `qc_summary` | `json.JSONDataset` | `data/08_reporting/qc_summary.json` | reporting | 9 (`json.dump`) |

Intermediates left in memory (not persisted): …

## 4. Parameters vs constants
| Name | Notebook value | Decision | Reason |
|---|---|---|---|
| `qc.min_quality` | `2` | parameter (`parameters_<pipeline>.yml`, typed with Pydantic) | tuned per station |
| `TIME_COLUMN` | `"time"` | constant in `nodes.py` | schema fact |

## 5. Nodes
| Node name | Function | Inputs | Outputs | Tags |
|---|---|---|---|---|
| `clean_observations` | `clean_observations(raw, qc)` | `raw_obs`, `params:qc` | `clean_obs` | qc |
| `summarise` | `summarise(clean)` | `clean_obs` | `qc_summary` | qc |

Dropped cells (display/exploration only): …

## 6. Verification
- `uv run kedro run --pipelines <pipeline_name>` reproduces the notebook's key numbers: …
- `uv run python <skill>/scripts/kedro_snapshot.py` → no `memory-output`, `free-input`, `param` findings
- Tests: node unit tests + in-memory pipeline test (`concepts/testing.md`)

## 7. Assumptions / open questions
- …
