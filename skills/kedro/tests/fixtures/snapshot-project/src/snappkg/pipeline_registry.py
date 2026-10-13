from kedro.framework.project import find_pipelines


def register_pipelines():
    pipelines = find_pipelines(raise_errors=True)
    pipelines["__default__"] = sum(pipelines.values())
    return pipelines
