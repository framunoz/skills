#!/usr/bin/env python3
"""Summarise a Kedro project's pipelines, datasets and parameters, and flag common mistakes.

Run with the PROJECT's interpreter, from anywhere:
    uv run python <skill>/scripts/kedro_snapshot.py [--project PATH] [--env ENV] [--pipeline NAME] [--json]

Uses ``kedro.inspection.get_project_snapshot`` (Kedro >= 1.4). Read-only: it imports the
project's pipeline code and resolves config (like ``kedro registry list``) but never runs nodes,
loads data or writes files. Findings:

  memory         intermediate dataset not declared in the catalog -> MemoryDataset, lost after the run
  memory-output  final pipeline output not declared -> returned by session.run() but never saved
  free-input     pipeline input that is not declared and not a parameter -> run fails
  param          ``params:x`` input whose top-level key is not in the parameters -> run fails
  unused         catalog entry no pipeline reads or writes
  auto-name      node without an explicit ``name`` (default ``func__hash``) -> hard to target with --nodes
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import warnings
from pathlib import Path

QUIET_LOGGING = """\
version: 1
disable_existing_loggers: false
handlers:
  stderr: {class: logging.StreamHandler, level: WARNING, stream: ext://sys.stderr}
root: {level: WARNING, handlers: [stderr]}
"""


def quiet_kedro() -> None:
    """Route Kedro's logging to stderr at WARNING so stdout stays machine-readable."""
    if "KEDRO_LOGGING_CONFIG" not in os.environ:
        path = Path(tempfile.gettempdir()) / "kedro_snapshot_logging.yml"
        path.write_text(QUIET_LOGGING, encoding="utf-8")
        os.environ["KEDRO_LOGGING_CONFIG"] = str(path)
    os.environ.setdefault("KEDRO_DISABLE_TELEMETRY", "1")
    warnings.filterwarnings("ignore", category=UserWarning)


def find_project(path: Path) -> Path | None:
    for directory in (path.resolve(), *path.resolve().parents):
        pyproject = directory / "pyproject.toml"
        if pyproject.is_file() and "[tool.kedro]" in pyproject.read_text(encoding="utf-8"):
            return directory
    return None


def analyse(snapshot, only: str | None) -> dict:
    pipelines = {p.name: p for p in snapshot.pipelines}
    if only and only not in pipelines:
        raise SystemExit(f"pipeline {only!r} not registered; available: {', '.join(sorted(pipelines))}")
    selected = [pipelines[only]] if only else list(pipelines.values())
    declared = set(snapshot.datasets)
    param_keys = set(snapshot.parameters)

    used, findings = set(), []
    for pipe in selected:
        produced = {o for n in pipe.nodes for o in n.outputs}
        for node in pipe.nodes:
            if node.name.startswith(f"{node.func_name}__"):
                where = f" ({node.source.filepath}:{node.source.line_start})" if node.source else ""
                findings.append(("auto-name", pipe.name, f"{node.name}{where}"))
            for name in [*node.inputs, *node.outputs]:
                if name == "parameters":
                    continue
                if name.startswith("params:"):
                    top = name[len("params:"):].split(".")[0]
                    if top not in param_keys:
                        findings.append(("param", pipe.name, f"{name} in node {node.name}: no top-level key {top!r}"))
                    continue
                used.add(name)
                if name not in declared:
                    if name in pipe.outputs:
                        findings.append(("memory-output", pipe.name, f"{name}: final output never persisted"))
                    elif name in produced:
                        findings.append(("memory", pipe.name, name))
                    else:
                        findings.append(("free-input", pipe.name, f"{name} (read by {node.name})"))
    if not only:
        findings += [("unused", "-", name) for name in sorted(declared - used)]
    seen, unique = set(), []
    for item in findings:  # same issue repeats across __default__ and the per-pipeline entries
        key = (item[0], item[2])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return {
        "project": vars(snapshot.metadata) if hasattr(snapshot.metadata, "__dict__") else str(snapshot.metadata),
        "pipelines": {
            p.name: {
                "nodes": len(p.nodes),
                "inputs": p.inputs,
                "outputs": p.outputs,
                "namespaces": sorted({n.namespace for n in p.nodes if n.namespace}),
                "tags": sorted({t for n in p.nodes for t in n.tags}),
            }
            for p in selected
        },
        "datasets": {name: {"type": d.type, "filepath": getattr(d, "filepath", None)} for name, d in snapshot.datasets.items()},
        "parameters": sorted(param_keys),
        "findings": [{"kind": k, "pipeline": p, "detail": d} for k, p, d in unique],
    }


def print_text(report: dict) -> None:
    meta = report["project"]
    print(f"project: {meta.get('project_name')} ({meta.get('package_name')}), kedro {meta.get('kedro_version')}")
    print("pipelines:")
    for name, info in report["pipelines"].items():
        extra = "".join(
            f", {label}: {', '.join(info[key])}" for key, label in (("namespaces", "namespaces"), ("tags", "tags")) if info[key]
        )
        print(f"  {name}: {info['nodes']} nodes{extra}")
        print(f"    inputs:  {', '.join(info['inputs']) or '-'}")
        print(f"    outputs: {', '.join(info['outputs']) or '-'}")
    print(f"datasets declared: {len(report['datasets'])}")
    for name, info in report["datasets"].items():
        print(f"  {name}: {info['type']}" + (f" -> {info['filepath']}" if info["filepath"] else ""))
    print(f"parameters (top-level): {', '.join(report['parameters']) or '-'}")
    print("findings:" if report["findings"] else "findings: none")
    for f in report["findings"]:
        print(f"  [{f['kind']}] {f['pipeline']}: {f['detail']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Kedro project snapshot and lint.")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project dir or a path inside it.")
    parser.add_argument("--env", help="Configuration environment (default: project default, usually local).")
    parser.add_argument("--pipeline", help="Analyse only this registered pipeline.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    root = find_project(args.project)
    if root is None:
        print(f"no Kedro project (pyproject.toml with [tool.kedro]) at or above {args.project.resolve()}", file=sys.stderr)
        return 2
    quiet_kedro()
    try:
        from kedro.inspection import get_project_snapshot
    except ImportError:
        print("kedro.inspection not available: needs Kedro >= 1.4 in THIS interpreter "
              f"({sys.executable}). Run with the project's env, e.g. `uv run python ...`.", file=sys.stderr)
        return 2
    snapshot = get_project_snapshot(project_path=root, env=args.env)
    report = analyse(snapshot, args.pipeline)
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        print_text(report)
    return 1 if any(f["kind"] in {"free-input", "param"} for f in report["findings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
