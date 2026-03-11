# ⚙️ Parameter Decision Framework

When decomposing logic or building nodes, you must evaluate whether variables should be configurable in `parameters.yml` or hardcoded in `nodes.py`.

## ✅ MAKE CONFIGURABLE (in `parameters.yml`):
These items change frequently over the lifecycle of a project or are subject to experimentation.
- Experimentation values (Learning rates, tree depth, probability thresholds).
- Business logic rules (Scoring cutoffs, approval limits, specific inclusion dates).
- Data processing params (Batch sizes, sampling ratios, window sizes for rolling averages).
- ML parameters (Train/test split sizes, cross-validation folds, random seeds).

## ❌ KEEP HARDCODED (in `nodes.py` or a dedicated `constants.py`):
These items represent the physical structure of the system and rarely change unless the schema itself breaks.
- Data schemas (Column names, expected types).
- Mathematical constants (PI, e).
- System constraints (File extensions).
- String literals (Display text, exact regex patterns).

## 💡 OmegaConfigLoader Interpolation
Kedro 1.0+ uses `OmegaConfigLoader` by default, replacing the legacy `ConfigLoader`. This enables dynamic string interpolation within your YAML configurations (both parameters and catalog).
- **Resolver Syntax**: Use `${my_variable}` to reference another parameter or environment variable.
- **Example**:
  ```yaml
  # parameters.yml
  base_path: "data/05_model_input"
  model_params:
    input_path: "${base_path}/train.csv" # Dynamically resolves
  ```
