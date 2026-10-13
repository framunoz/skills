#!/usr/bin/env python3
"""Check catalog dataset types against the kedro-datasets installed in THIS interpreter.

Run with the project's interpreter (stdlib only):
    uv run python <skill>/scripts/check_dataset.py pandas.CSVDataset polars.EagerPolarsDataset
    uv run python <skill>/scripts/check_dataset.py --list [module]

For each type prints: whether it exists in the installed kedro-datasets (or
kedro-datasets-experimental), the constructor arguments with defaults, whether its optional
dependencies import, the pip/uv extra to add, and the docs URL for the installed version.
Classes are found by parsing source files, so a type is reported even when its extra is not
installed. Unknown names get close-match suggestions (including old ``DataSet`` casing).
"""

from __future__ import annotations

import argparse
import ast
import difflib
import importlib
import importlib.metadata as md
import importlib.util
import sys
from pathlib import Path

PACKAGES = {"kedro_datasets": "kedro-datasets", "kedro_datasets_experimental": "kedro-datasets-experimental"}
DOCS = "https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-{version}/api/{package}/{module}.{cls}/index.md"


def package_root(name: str) -> Path | None:
    spec = importlib.util.find_spec(name)
    return Path(spec.origin).parent if spec and spec.origin else None


def init_signature(node: ast.ClassDef) -> list[str]:
    for item in node.body:
        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
            a = item.args
            positional = a.posonlyargs + a.args
            defaults = [None] * (len(positional) - len(a.defaults)) + list(a.defaults)
            params = [
                arg.arg + ("" if d is None else f"={ast.unparse(d)}")
                for arg, d in zip(positional, defaults) if arg.arg != "self"
            ]
            params += [
                arg.arg + ("" if d is None else f"={ast.unparse(d)}")
                for arg, d in zip(a.kwonlyargs, a.kw_defaults)
            ]
            return params
    return []


def index() -> dict[str, dict]:
    """Map 'module.Class' -> info for every *Dataset class defined in the installed packages."""
    found: dict[str, dict] = {}
    for package, dist in PACKAGES.items():
        root = package_root(package)
        if root is None:
            continue
        dist = next(iter(md.packages_distributions().get(package, [])), dist)
        try:
            version = md.version(dist)
        except md.PackageNotFoundError:
            continue
        for path in sorted(root.rglob("*.py")):
            rel = path.relative_to(root)
            if rel.parts[0].startswith("_") or len(rel.parts) < 2:
                continue
            module = ".".join(rel.parts[:-1])
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            for node in tree.body:
                if isinstance(node, ast.ClassDef) and node.name.endswith("Dataset") and not node.name.startswith("_"):
                    doc = (ast.get_docstring(node) or "").strip().split("\n\n")[0].replace("\n", " ")
                    found.setdefault(f"{module}.{node.name}", {
                        "package": package, "dist": dist, "version": version, "module": module,
                        "cls": node.name, "args": init_signature(node), "doc": doc,
                    })
    return found


def extras(dist: str) -> set[str]:
    try:
        return set(md.metadata(dist).get_all("Provides-Extra") or [])
    except md.PackageNotFoundError:
        return set()


def normalise(name: str) -> str:
    for prefix in ("kedro_datasets_experimental.", "kedro_datasets."):
        if name.startswith(prefix):
            return name[len(prefix):]
    return name


def report(name: str, idx: dict[str, dict]) -> bool:
    print(f"== {name}")
    if name.startswith("kedro.extras.datasets"):
        print("   REMOVED: kedro.extras.datasets was dropped (Kedro 0.19). Use kedro-datasets: "
              f"{normalise(name.replace('kedro.extras.datasets.', '')).replace('DataSet', 'Dataset')}")
        return False
    key = normalise(name)
    info = idx.get(key)
    if info is None:
        hint = key.replace("DataSet", "Dataset")
        if hint != key and hint in idx:
            print(f"   NOT FOUND — old casing. Since kedro-datasets 2.0 it is `{hint}`.")
            return False
        close = difflib.get_close_matches(key, idx, n=5, cutoff=0.5)
        cls = key.rsplit(".", 1)[-1].lower()
        close += [k for k in idx if k.rsplit(".", 1)[-1].lower() == cls and k not in close]
        print("   NOT FOUND in installed kedro-datasets." + (f" Did you mean: {', '.join(close)}" if close else ""))
        return False
    print(f"   package:  {info['dist']} {info['version']}")
    if info["package"] == "kedro_datasets":
        print(f"   catalog:  type: {key}")
    else:  # the short form only resolves inside kedro_datasets
        print(f"   catalog:  type: {info['package']}.{key}   (experimental: full path required; "
              f"`type: {key}` fails with \"No module named '{info['module'].split('.')[0]}'\")")
    print(f"   args:     {', '.join(info['args']) or '(none parsed)'}")
    if info["doc"]:
        print(f"   doc:      {info['doc'][:220]}")
    extra = f"{info['module'].replace('.', '-')}-{info['cls']}".lower()
    available = extras(info["dist"])
    if extra in available:
        print(f"   extra:    {info['dist']}[{extra}]  (uv add \"{info['dist']}[{extra}]\")")
    else:
        print(f"   extra:    no '{extra}' extra found; check the package's optional dependencies")
    try:  # kedro-datasets imports lazily: touch the class to load its dependencies
        getattr(importlib.import_module(f"{info['package']}.{info['module']}"), info["cls"])
        print("   imports:  OK (dependencies installed)")
    except Exception as error:  # noqa: BLE001 - report any import failure verbatim
        print(f"   imports:  FAILS here -> {type(error).__name__}: {str(error)[:160]}")
    print("   docs:     " + DOCS.format(version=info["version"], package=info["package"], module=info["module"], cls=info["cls"]))
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Kedro dataset types against installed kedro-datasets.")
    parser.add_argument("types", nargs="*", help="e.g. pandas.CSVDataset or kedro_datasets.pandas.CSVDataset")
    parser.add_argument("--list", nargs="?", const="", metavar="MODULE", help="List types (optionally one module).")
    args = parser.parse_args()

    idx = index()
    print(f"interpreter: {sys.executable}")
    if not idx:
        print("kedro-datasets is not installed in this interpreter. Run with the project's env "
              "(`uv run python ...`) or install it.")
        return 2
    if args.list is not None:
        for key in sorted(k for k in idx if k.startswith(args.list)):
            print(f"  {key}  [{idx[key]['dist']}]")
        return 0
    if not args.types:
        parser.print_help()
        return 2
    ok = [report(t, idx) for t in args.types]
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
