# References

Official documentation as clean Markdown. Fetch a page (WebFetch or `curl -sL`) when you need
exact signatures, every option, or a topic this skill doesn't cover.

- Pattern: `https://docs.kedro.org/en/stable/<path>/index.md` — the short paths in each file's
  "More detail" section are `<path>`. For the installed version replace `stable` with the
  version (e.g. `en/1.7.0/`) if the behaviour differs.
- Full index: `https://docs.kedro.org/en/stable/llms.txt`.
- kedro-datasets: index `https://docs.kedro.org/projects/kedro-datasets/en/stable/llms.txt`;
  one dataset: `https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-<version>/api/kedro_datasets/<module>.<Class>/index.md`
  (experimental: `.../api/kedro_datasets_experimental/...`) — `scripts/check_dataset.py` prints it.
- kedro-viz: `https://docs.kedro.org/projects/kedro-viz/en/stable/llms.txt`.
- Release notes (what changed between versions): `https://raw.githubusercontent.com/kedro-org/kedro/main/RELEASE.md`.
- API reference pages: `https://docs.kedro.org/en/stable/api/<area>/<object>/index.md`
  (e.g. `api/io/kedro.io.DataCatalog`); prefer `help()`/`inspect.signature` in the project env.
- Official agent guidance: `kedro-skills` (catalog-config, parameters-and-config, llm-context-nodes)
  at <https://github.com/kedro-org/kedro-skills>; `kedro-mcp` for migrations/notebook conversion.


## Get Started

- [Installation](https://docs.kedro.org/en/stable/getting-started/install/index.md) — `getting-started/install` — Installation guide for pip, conda, and development setup
- [Kedro concepts](https://docs.kedro.org/en/stable/getting-started/kedro_concepts/index.md) — `getting-started/kedro_concepts` — Core concepts - nodes, pipelines, catalog, and more
- [Cheatsheet](https://docs.kedro.org/en/stable/getting-started/cheatsheet/index.md) — `getting-started/cheatsheet` — Two-page Kedro cheatsheet, available as a SVG file
- [FAQs](https://docs.kedro.org/en/stable/getting-started/faq/index.md) — `getting-started/faq` — Frequently asked questions
- [Video course](https://docs.kedro.org/en/stable/getting-started/course/index.md) — `getting-started/course` — Learn about Kedro from our video course
- [Build a pipeline visually](https://docs.kedro.org/en/stable/getting-started/pipeline_builder/index.md) — `getting-started/pipeline_builder` — Design Kedro pipelines visually in the browser and export a project

## Essential Tutorials

- [Spaceflight tutorial](https://docs.kedro.org/en/stable/tutorials/spaceflights_tutorial/index.md) — `tutorials/spaceflights_tutorial` — Complete tutorial building a spaceflight price prediction project
- [Spaceflight tutorial template](https://docs.kedro.org/en/stable/tutorials/tutorial_template/index.md) — `tutorials/tutorial_template` — Tutorial project template guide
- [Set up data](https://docs.kedro.org/en/stable/tutorials/set_up_data/index.md) — `tutorials/set_up_data` — Setting up data for the tutorial
- [Create a pipeline](https://docs.kedro.org/en/stable/tutorials/create_a_pipeline/index.md) — `tutorials/create_a_pipeline` — Step-by-step guide to creating pipelines
- [Add another pipeline](https://docs.kedro.org/en/stable/tutorials/add_another_pipeline/index.md) — `tutorials/add_another_pipeline` — Adding multiple pipelines to a project
- [Settings](https://docs.kedro.org/en/stable/tutorials/settings/index.md) — `tutorials/settings` — Configuring project settings
- [Test a project](https://docs.kedro.org/en/stable/tutorials/test_a_project/index.md) — `tutorials/test_a_project` — Testing your Kedro project
- [Notebook tutorial](https://docs.kedro.org/en/stable/tutorials/notebooks_tutorial/index.md) — `tutorials/notebooks_tutorial` — Using Kedro with Jupyter notebooks
- [FAQs](https://docs.kedro.org/en/stable/tutorials/spaceflights_tutorial_faqs/index.md) — `tutorials/spaceflights_tutorial_faqs` — Tutorial FAQs

## Creating Projects

- [Create a Kedro project](https://docs.kedro.org/en/stable/create/new_project/index.md) — `create/new_project` — How to create a new Kedro project
- [Create a minimal Kedro project](https://docs.kedro.org/en/stable/create/minimal_kedro_project/index.md) — `create/minimal_kedro_project` — Creating minimal projects without boilerplate
- [Customise a new project](https://docs.kedro.org/en/stable/create/customise_project/index.md) — `create/customise_project` — Customizing project templates
- [Project tools](https://docs.kedro.org/en/stable/create/new_project_tools/index.md) — `create/new_project_tools` — Tools included in new projects
- [Kedro starters](https://docs.kedro.org/en/stable/create/starters/index.md) — `create/starters` — Using and creating Kedro starters (project templates)

## Configuration

- [Configuration](https://docs.kedro.org/en/stable/configure/configuration_basics/index.md) — `configure/configuration_basics` — Configuration management fundamentals
- [Parameters and credentials](https://docs.kedro.org/en/stable/configure/parameters_and_credentials/index.md) — `configure/parameters_and_credentials` — Understanding pipeline parameters and credentials
- [Templating](https://docs.kedro.org/en/stable/configure/templating/index.md) — `configure/templating` — Understanding templating with OmegaConfigLoader
- [Configuration](https://docs.kedro.org/en/stable/configure/how_to_configure_project/index.md) — `configure/how_to_configure_project` — How to configure your Kedro project
- [Parameters and credentials](https://docs.kedro.org/en/stable/configure/how_to_use_parameters_and_credentials/index.md) — `configure/how_to_use_parameters_and_credentials` — How to work with parameters and credentials
- [Templating](https://docs.kedro.org/en/stable/configure/how_to_use_templating/index.md) — `configure/how_to_use_templating` — How to work with templating
- [Config loader migration](https://docs.kedro.org/en/stable/configure/config_loader_migration/index.md) — `configure/config_loader_migration` — Migrating between config loaders

## Data Management

- [Introduction](https://docs.kedro.org/en/stable/catalog-data/introduction/index.md) — `catalog-data/introduction` — Introduction to the Data Catalog
- [Data Catalog](https://docs.kedro.org/en/stable/catalog-data/data_catalog/index.md) — `catalog-data/data_catalog` — Data Catalog concepts and structure
- [Dataset factories](https://docs.kedro.org/en/stable/catalog-data/kedro_dataset_factories/index.md) — `catalog-data/kedro_dataset_factories` — How dataset factories generalise catalog entries
- [Partitioned and incremental datasets](https://docs.kedro.org/en/stable/catalog-data/partitioned_and_incremental_datasets/index.md) — `catalog-data/partitioned_and_incremental_datasets` — Partitioned and incremental dataset concepts
- [Lazy loading](https://docs.kedro.org/en/stable/catalog-data/lazy_loading/index.md) — `catalog-data/lazy_loading` — Lazy loading for performance optimization
- [Validate datasets](https://docs.kedro.org/en/stable/catalog-data/dataset_validation/index.md) — `catalog-data/dataset_validation` — How to validate datasets with declared validators
- [Configure the Data Catalog](https://docs.kedro.org/en/stable/catalog-data/how_to_configure_the_data_catalog/index.md) — `catalog-data/how_to_configure_the_data_catalog` — How to configure load/save arguments, credentials, versioning, and environments
- [Use dataset factories](https://docs.kedro.org/en/stable/catalog-data/how_to_use_dataset_factories/index.md) — `catalog-data/how_to_use_dataset_factories` — How to apply dataset factory patterns
- [Use partitioned and incremental datasets](https://docs.kedro.org/en/stable/catalog-data/how_to_use_partitioned_and_incremental_datasets/index.md) — `catalog-data/how_to_use_partitioned_and_incremental_datasets` — How to configure and use partitioned and incremental datasets
- [Access the Data Catalog in code](https://docs.kedro.org/en/stable/catalog-data/how_to_access_the_data_catalog_in_code/index.md) — `catalog-data/how_to_access_the_data_catalog_in_code` — How to use the DataCatalog programmatically
- [Data Catalog YAML examples](https://docs.kedro.org/en/stable/catalog-data/data_catalog_yaml_examples/index.md) — `catalog-data/data_catalog_yaml_examples` — YAML configuration examples

## Nodes and Pipelines

- [Nodes](https://docs.kedro.org/en/stable/build/nodes/index.md) — `build/nodes` — Creating and using nodes - the building blocks of pipelines
- [Pipeline object](https://docs.kedro.org/en/stable/build/pipeline_introduction/index.md) — `build/pipeline_introduction` — Understanding the pipeline object
- [Run a pipeline](https://docs.kedro.org/en/stable/build/run_a_pipeline/index.md) — `build/run_a_pipeline` — Running pipelines with different options
- [Modular pipelines](https://docs.kedro.org/en/stable/build/modular_pipelines/index.md) — `build/modular_pipelines` — Creating reusable, modular pipelines
- [Namespaces](https://docs.kedro.org/en/stable/build/namespaces/index.md) — `build/namespaces` — Reusing pipelines with namespaces
- [Pipeline registry](https://docs.kedro.org/en/stable/build/pipeline_registry/index.md) — `build/pipeline_registry` — Registering and discovering pipelines
- [Slice a pipeline](https://docs.kedro.org/en/stable/build/slice_a_pipeline/index.md) — `build/slice_a_pipeline` — Slicing pipelines for partial execution
- [LLM context node](https://docs.kedro.org/en/stable/build/llm_context_node/index.md) — `build/llm_context_node` — Using LLM Context Nodes to construct LLMContext

## Development Practices

- [Inspect a project](https://docs.kedro.org/en/stable/inspect/inspect-project/) — `inspect/inspect-project` — `kedro.inspection.get_project_snapshot` (HTML only; no `index.md`)

- [Dependency management](https://docs.kedro.org/en/stable/develop/dependencies/index.md) — `develop/dependencies` — Managing project dependencies
- [Logging](https://docs.kedro.org/en/stable/develop/logging/index.md) — `develop/logging` — Logging configuration and best practices
- [Automated testing](https://docs.kedro.org/en/stable/develop/automated_testing/index.md) — `develop/automated_testing` — Writing tests for Kedro projects
- [Formatting and linting](https://docs.kedro.org/en/stable/develop/linting/index.md) — `develop/linting` — Code formatting and linting setup
- [Debugging](https://docs.kedro.org/en/stable/develop/debugging/index.md) — `develop/debugging` — Debugging Kedro pipelines
- [Vibe coding with MCP](https://docs.kedro.org/en/stable/develop/vibe_coding_with_mcp/index.md) — `develop/vibe_coding_with_mcp` — Vibe coding with MCP
- [Vibe coding with skills](https://docs.kedro.org/en/stable/develop/vibe_coding_with_skills/index.md) — `develop/vibe_coding_with_skills` — Vibe coding with skills

## Deployment

- [Overview](https://docs.kedro.org/en/stable/deploy/index.md) — `deploy` — Deployment overview and strategies
- [How to package your project](https://docs.kedro.org/en/stable/deploy/package_a_project/index.md) — `deploy/package_a_project` — Packaging Kedro projects for deployment
- [How to group your nodes effectively](https://docs.kedro.org/en/stable/deploy/nodes_grouping/index.md) — `deploy/nodes_grouping` — Grouping nodes effectively for deployment
- [Single-machine deployment](https://docs.kedro.org/en/stable/deploy/single_machine/index.md) — `deploy/single_machine` — Single-machine deployment guide
- [Distributed deployment](https://docs.kedro.org/en/stable/deploy/distributed/index.md) — `deploy/distributed` — Distributed deployment strategies
- [Apache Airflow](https://docs.kedro.org/en/stable/deploy/supported-platforms/airflow/index.md) — `deploy/supported-platforms/airflow` — Apache Airflow integration
- [Amazon SageMaker](https://docs.kedro.org/en/stable/deploy/supported-platforms/amazon_sagemaker/index.md) — `deploy/supported-platforms/amazon_sagemaker` — Amazon SageMaker deployment
- [Amazon EMR Serverless](https://docs.kedro.org/en/stable/deploy/supported-platforms/amazon_emr_serverless/index.md) — `deploy/supported-platforms/amazon_emr_serverless` — Amazon EMR Serverless guide
- [AWS Step Functions](https://docs.kedro.org/en/stable/deploy/supported-platforms/aws_step_functions/index.md) — `deploy/supported-platforms/aws_step_functions` — AWS Step Functions integration
- [Azure ML pipelines](https://docs.kedro.org/en/stable/deploy/supported-platforms/azure/index.md) — `deploy/supported-platforms/azure` — Azure ML pipelines deployment
- [Dagster](https://docs.kedro.org/en/stable/deploy/supported-platforms/dagster/index.md) — `deploy/supported-platforms/dagster` — Dagster deployment
- [Dask](https://docs.kedro.org/en/stable/deploy/supported-platforms/dask/index.md) — `deploy/supported-platforms/dask` — Dask integration for parallel computing
- [Databricks](https://docs.kedro.org/en/stable/deploy/supported-platforms/databricks/index.md) — `deploy/supported-platforms/databricks` — Databricks deployment
- [Kubeflow Pipelines](https://docs.kedro.org/en/stable/deploy/supported-platforms/kubeflow/index.md) — `deploy/supported-platforms/kubeflow` — Kubeflow Pipelines integration
- [Prefect](https://docs.kedro.org/en/stable/deploy/supported-platforms/prefect/index.md) — `deploy/supported-platforms/prefect` — Prefect workflow orchestration
- [VertexAI](https://docs.kedro.org/en/stable/deploy/supported-platforms/vertexai/index.md) — `deploy/supported-platforms/vertexai` — Google VertexAI deployment
- [Argo Workflows](https://docs.kedro.org/en/stable/deploy/supported-platforms/argo/index.md) — `deploy/supported-platforms/argo` — Argo Workflows integration
- [AWS Batch](https://docs.kedro.org/en/stable/deploy/supported-platforms/aws_batch/index.md) — `deploy/supported-platforms/aws_batch` — AWS Batch deployment

## Extending Kedro

- [Use cases](https://docs.kedro.org/en/stable/extend/common_use_cases/index.md) — `extend/common_use_cases` — Common extension patterns
- [Custom datasets](https://docs.kedro.org/en/stable/extend/how_to_create_a_custom_dataset/index.md) — `extend/how_to_create_a_custom_dataset` — Creating custom dataset implementations
- [Introduction](https://docs.kedro.org/en/stable/extend/hooks/introduction/index.md) — `extend/hooks/introduction` — Introduction to Kedro hooks
- [Common use cases](https://docs.kedro.org/en/stable/extend/hooks/common_use_cases/index.md) — `extend/hooks/common_use_cases` — Common hook use cases
- [Examples](https://docs.kedro.org/en/stable/extend/hooks/examples/index.md) — `extend/hooks/examples` — Hook implementation examples
- [Kedro sessions](https://docs.kedro.org/en/stable/extend/session/index.md) — `extend/session` — Programmatic usage with KedroSession
- [Serving over HTTP](https://docs.kedro.org/en/stable/extend/serving/index.md) — `extend/serving` — Serving pipelines over HTTP
- [Custom plugins](https://docs.kedro.org/en/stable/extend/plugins/index.md) — `extend/plugins` — Creating Kedro plugins
- [Custom starters](https://docs.kedro.org/en/stable/extend/create_a_starter/index.md) — `extend/create_a_starter` — Creating custom project starters

## API Reference

- [Overview](https://docs.kedro.org/en/stable/api/index.md) — `api`
- [Overview](https://docs.kedro.org/en/stable/api/config/kedro.config/index.md) — `api/config/kedro.config`
- [AbstractConfigLoader](https://docs.kedro.org/en/stable/api/config/kedro.config.AbstractConfigLoader/index.md) — `api/config/kedro.config.AbstractConfigLoader`
- [OmegaConfigLoader](https://docs.kedro.org/en/stable/api/config/kedro.config.OmegaConfigLoader/index.md) — `api/config/kedro.config.OmegaConfigLoader`
- [MissingConfigException](https://docs.kedro.org/en/stable/api/config/kedro.config.MissingConfigException/index.md) — `api/config/kedro.config.MissingConfigException`
- [Overview](https://docs.kedro.org/en/stable/api/framework/kedro.framework/index.md) — `api/framework/kedro.framework`
- [CLI](https://docs.kedro.org/en/stable/api/framework/kedro.framework.cli/index.md) — `api/framework/kedro.framework.cli`
- [Context](https://docs.kedro.org/en/stable/api/framework/kedro.framework.context/index.md) — `api/framework/kedro.framework.context`
- [Hooks](https://docs.kedro.org/en/stable/api/framework/kedro.framework.hooks/index.md) — `api/framework/kedro.framework.hooks`
- [Project](https://docs.kedro.org/en/stable/api/framework/kedro.framework.project/index.md) — `api/framework/kedro.framework.project`
- [Session](https://docs.kedro.org/en/stable/api/framework/kedro.framework.session/index.md) — `api/framework/kedro.framework.session`
- [Startup](https://docs.kedro.org/en/stable/api/framework/kedro.framework.startup/index.md) — `api/framework/kedro.framework.startup`
- [Overview](https://docs.kedro.org/en/stable/api/io/kedro.io/index.md) — `api/io/kedro.io`
- [DataCatalog](https://docs.kedro.org/en/stable/api/io/kedro.io.DataCatalog/index.md) — `api/io/kedro.io.DataCatalog`
- [CatalogProtocol](https://docs.kedro.org/en/stable/api/io/kedro.io.CatalogProtocol/index.md) — `api/io/kedro.io.CatalogProtocol`
- [SharedMemoryDataCatalog](https://docs.kedro.org/en/stable/api/io/kedro.io.SharedMemoryDataCatalog/index.md) — `api/io/kedro.io.SharedMemoryDataCatalog`
- [SharedMemoryCatalogProtocol](https://docs.kedro.org/en/stable/api/io/kedro.io.SharedMemoryCatalogProtocol/index.md) — `api/io/kedro.io.SharedMemoryCatalogProtocol`
- [CatalogConfigResolver](https://docs.kedro.org/en/stable/api/io/kedro.io.CatalogConfigResolver/index.md) — `api/io/kedro.io.CatalogConfigResolver`
- [AbstractDataset](https://docs.kedro.org/en/stable/api/io/kedro.io.AbstractDataset/index.md) — `api/io/kedro.io.AbstractDataset`
- [AbstractVersionedDataset](https://docs.kedro.org/en/stable/api/io/kedro.io.AbstractVersionedDataset/index.md) — `api/io/kedro.io.AbstractVersionedDataset`
- [CachedDataset](https://docs.kedro.org/en/stable/api/io/kedro.io.CachedDataset/index.md) — `api/io/kedro.io.CachedDataset`
- [MemoryDataset](https://docs.kedro.org/en/stable/api/io/kedro.io.MemoryDataset/index.md) — `api/io/kedro.io.MemoryDataset`
- [Version](https://docs.kedro.org/en/stable/api/io/kedro.io.Version/index.md) — `api/io/kedro.io.Version`
- [DatasetAlreadyExistsError](https://docs.kedro.org/en/stable/api/io/kedro.io.DatasetAlreadyExistsError/index.md) — `api/io/kedro.io.DatasetAlreadyExistsError`
- [DatasetError](https://docs.kedro.org/en/stable/api/io/kedro.io.DatasetError/index.md) — `api/io/kedro.io.DatasetError`
- [DatasetNotFoundError](https://docs.kedro.org/en/stable/api/io/kedro.io.DatasetNotFoundError/index.md) — `api/io/kedro.io.DatasetNotFoundError`
- [Overview](https://docs.kedro.org/en/stable/api/ipython/kedro.ipython/index.md) — `api/ipython/kedro.ipython`
- [load_ipython_extension](https://docs.kedro.org/en/stable/api/ipython/kedro.ipython.load_ipython_extension/index.md) — `api/ipython/kedro.ipython.load_ipython_extension`
- [magic_load_node](https://docs.kedro.org/en/stable/api/ipython/kedro.ipython.magic_load_node/index.md) — `api/ipython/kedro.ipython.magic_load_node`
- [magic_reload_kedro](https://docs.kedro.org/en/stable/api/ipython/kedro.ipython.magic_reload_kedro/index.md) — `api/ipython/kedro.ipython.magic_reload_kedro`
- [reload_kedro](https://docs.kedro.org/en/stable/api/ipython/kedro.ipython.reload_kedro/index.md) — `api/ipython/kedro.ipython.reload_kedro`
- [kedro.logging](https://docs.kedro.org/en/stable/api/kedro.logging/index.md) — `api/kedro.logging`
- [Overview](https://docs.kedro.org/en/stable/api/pipeline/kedro.pipeline/index.md) — `api/pipeline/kedro.pipeline`
- [Node](https://docs.kedro.org/en/stable/api/pipeline/kedro.pipeline.node/index.md) — `api/pipeline/kedro.pipeline.node`
- [Pipeline](https://docs.kedro.org/en/stable/api/pipeline/kedro.pipeline.Pipeline/index.md) — `api/pipeline/kedro.pipeline.Pipeline`
- [Overview](https://docs.kedro.org/en/stable/api/runner/kedro.runner/index.md) — `api/runner/kedro.runner`
- [AbstractRunner](https://docs.kedro.org/en/stable/api/runner/kedro.runner.AbstractRunner/index.md) — `api/runner/kedro.runner.AbstractRunner`
- [SequentialRunner](https://docs.kedro.org/en/stable/api/runner/kedro.runner.SequentialRunner/index.md) — `api/runner/kedro.runner.SequentialRunner`
- [ParallelRunner](https://docs.kedro.org/en/stable/api/runner/kedro.runner.ParallelRunner/index.md) — `api/runner/kedro.runner.ParallelRunner`
- [ThreadRunner](https://docs.kedro.org/en/stable/api/runner/kedro.runner.ThreadRunner/index.md) — `api/runner/kedro.runner.ThreadRunner`
- [Overview](https://docs.kedro.org/en/stable/api/server/kedro.server/index.md) — `api/server/kedro.server`
- [Models](https://docs.kedro.org/en/stable/api/server/kedro.server.models/index.md) — `api/server/kedro.server.models`
- [kedro.utils](https://docs.kedro.org/en/stable/api/kedro.utils/index.md) — `api/kedro.utils`
- [kedro.load_ipython_extension](https://docs.kedro.org/en/stable/api/kedro.load_ipython_extension/index.md) — `api/kedro.load_ipython_extension`
- [kedro.KedroDeprecationWarning](https://docs.kedro.org/en/stable/api/kedro.KedroDeprecationWarning/index.md) — `api/kedro.KedroDeprecationWarning`
- [kedro.KedroPythonVersionWarning](https://docs.kedro.org/en/stable/api/kedro.KedroPythonVersionWarning/index.md) — `api/kedro.KedroPythonVersionWarning`

## Integrations and Tools

- [Introduction](https://docs.kedro.org/en/stable/integrations-and-plugins/notebooks_and_ipython/index.md) — `integrations-and-plugins/notebooks_and_ipython` — Jupyter integration overview
- [Kedro and Jupyter notebooks](https://docs.kedro.org/en/stable/integrations-and-plugins/notebooks_and_ipython/kedro_and_notebooks/index.md) — `integrations-and-plugins/notebooks_and_ipython/kedro_and_notebooks` — Using Kedro with notebooks
- [How to add Kedro to Jupyter Notebook](https://docs.kedro.org/en/stable/integrations-and-plugins/notebooks_and_ipython/notebook-example/add_kedro_to_a_notebook/index.md) — `integrations-and-plugins/notebooks_and_ipython/notebook-example/add_kedro_to_a_notebook` — Adding Kedro to notebooks
- [PySpark](https://docs.kedro.org/en/stable/integrations-and-plugins/pyspark_integration/index.md) — `integrations-and-plugins/pyspark_integration` — PySpark integration guide
- [MLflow](https://docs.kedro.org/en/stable/integrations-and-plugins/mlflow/index.md) — `integrations-and-plugins/mlflow` — MLflow experiment tracking
- [DVC](https://docs.kedro.org/en/stable/integrations-and-plugins/dvc/index.md) — `integrations-and-plugins/dvc` — DVC data versioning integration
- [Delta Lake](https://docs.kedro.org/en/stable/integrations-and-plugins/deltalake_versioning/index.md) — `integrations-and-plugins/deltalake_versioning` — Delta Lake versioning
- [Iceberg](https://docs.kedro.org/en/stable/integrations-and-plugins/iceberg_versioning/index.md) — `integrations-and-plugins/iceberg_versioning` — Apache Iceberg versioning
- [Visual Studio Code & Cursor](https://docs.kedro.org/en/stable/ide/set_up_vscode/index.md) — `ide/set_up_vscode` — Visual Studio Code and Cursor setup for Kedro
- [PyCharm](https://docs.kedro.org/en/stable/ide/set_up_pycharm/index.md) — `ide/set_up_pycharm` — PyCharm setup for Kedro

## About Kedro

- [Kedro architecture](https://docs.kedro.org/en/stable/getting-started/architecture_overview/index.md) — `getting-started/architecture_overview` — Understanding Kedro's architecture
- [Glossary](https://docs.kedro.org/en/stable/getting-started/glossary/index.md) — `getting-started/glossary` — Kedro terminology glossary
- [Kedro's Technical Steering Committee](https://docs.kedro.org/en/stable/about/technical_steering_committee/index.md) — `about/technical_steering_committee` — Kedro's Technical Steering Committee
- [Migration guide](https://docs.kedro.org/en/stable/about/migration/index.md) — `about/migration` — Migration guide between Kedro versions
- [Kedro telemetry](https://docs.kedro.org/en/stable/about/telemetry/index.md) — `about/telemetry` — Understanding Kedro telemetry
- [Kedro security model](https://docs.kedro.org/en/stable/about/security_model/index.md) — `about/security_model` — Kedro security model
- [Experimental APIs](https://docs.kedro.org/en/stable/about/experimental/index.md) — `about/experimental` — Experimental APIs in Kedro
