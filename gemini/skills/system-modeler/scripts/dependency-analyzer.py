#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path


def analyze_python(root):
    """Simple AST-based dependency analysis for Python."""
    import ast

    dependencies = {}

    for path in Path(root).rglob("*.py"):
        if ".venv" in str(path) or "__pycache__" in str(path):
            continue

        rel_path = str(path.relative_to(root))
        dependencies[rel_path] = []

        try:
            with open(path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        dependencies[rel_path].append(n.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dependencies[rel_path].append(node.module)
        except Exception:
            # Skip files with syntax errors or encoding issues
            continue

    return dependencies


def analyze_js_ts(root):
    """Regex-based dependency analysis for JS/TS."""
    dependencies = {}
    # Matches: import ... from 'module', import 'module', require('module')
    import_re = re.compile(
        r"(?:import\s+.*?\s+from\s+['\"](.*?)['\"]|import\s+['\"](.*?)['\"]|require\s*\(\s*['\"](.*?)['\"]\s*\))"
    )

    for ext in ["*.js", "*.ts", "*.jsx", "*.tsx"]:
        for path in Path(root).rglob(ext):
            if "node_modules" in str(path) or "dist" in str(path):
                continue

            rel_path = str(path.relative_to(root))
            dependencies[rel_path] = []

            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = import_re.findall(content)
                    for m in matches:
                        # findall with multiple groups returns a tuple, only one will be non-empty
                        dep = next((group for group in m if group), None)
                        if dep:
                            dependencies[rel_path].append(dep)
            except Exception:
                continue

    return dependencies


def analyze_rust(root):
    """Regex-based dependency analysis for Rust."""
    dependencies = {}
    # Matches: use crate::module; use module::submodule; extern crate module;
    use_re = re.compile(r"(?:use\s+([a-zA-Z0-9_:]+)|extern\s+crate\s+([a-zA-Z0-9_]+))")

    for path in Path(root).rglob("*.rs"):
        if "target" in str(path):
            continue

        rel_path = str(path.relative_to(root))
        dependencies[rel_path] = []

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                matches = use_re.findall(content)
                for m in matches:
                    dep = next((group for group in m if group), None)
                    if dep:
                        dependencies[rel_path].append(dep)
        except Exception:
            continue

    return dependencies


def analyze_go(root):
    """Regex-based dependency analysis for Go."""
    dependencies = {}
    # Matches: import "module", import ( "module" )
    import_re = re.compile(r'import\s+(?:\(\s*([^)]*)\)|"([^"]+)")')

    for path in Path(root).rglob("*.go"):
        if "vendor" in str(path):
            continue

        rel_path = str(path.relative_to(root))
        dependencies[rel_path] = []

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                matches = import_re.findall(content)
                for m in matches:
                    # Group 1 is the multi-line import block
                    if m[0]:
                        inner_imports = re.findall(r'"([^"]+)"', m[0])
                        dependencies[rel_path].extend(inner_imports)
                    # Group 2 is the single line import
                    elif m[1]:
                        dependencies[rel_path].append(m[1])
        except Exception:
            continue

    return dependencies


def get_project_deps(root):
    """Extract project-level dependencies from common config files."""
    project_deps: dict[str, list[str] | dict[str, list[str]]] = {}

    # Python - requirements.txt
    req_path = Path(root) / "requirements.txt"
    if req_path.exists():
        try:
            with open(req_path, "r", encoding="utf-8") as f:
                deps = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]
                project_deps["python_requirements"] = deps
        except Exception:
            pass

    # Python - pyproject.toml
    pyproj_path = Path(root) / "pyproject.toml"
    if pyproj_path.exists():
        try:
            import tomllib  # Python 3.11+

            with open(pyproj_path, "rb") as f:
                data = tomllib.load(f)
                deps = data.get("project", {}).get("dependencies", []) + data.get(
                    "tool", {}
                ).get("poetry", {}).get("dependencies", [])
                if deps:
                    project_deps["python_pyproject"] = deps
        except Exception:
            pass

    # Node.js - package.json
    pkg_path = Path(root) / "package.json"
    if pkg_path.exists():
        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                deps = {
                    "dependencies": list(data.get("dependencies", {}).keys()),
                    "devDependencies": list(data.get("devDependencies", {}).keys()),
                }
                project_deps["nodejs_package_json"] = deps
        except Exception:
            pass

    # Rust - Cargo.toml
    cargo_path = Path(root) / "Cargo.toml"
    if cargo_path.exists():
        try:
            import tomllib

            with open(cargo_path, "rb") as f:
                data = tomllib.load(f)
                deps = {
                    "dependencies": list(data.get("dependencies", {}).keys()),
                    "dev-dependencies": list(data.get("dev-dependencies", {}).keys()),
                }
                project_deps["rust_cargo_toml"] = deps
        except Exception:
            pass

    # Go - go.mod
    go_mod_path = Path(root) / "go.mod"
    if go_mod_path.exists():
        try:
            with open(go_mod_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Simple extraction of 'require' statements
                deps = re.findall(r"require\s+([a-zA-Z0-9._/-]+\s+[v0-9.]+)", content)
                project_deps["go_mod"] = deps
        except Exception:
            pass

    return project_deps


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    root = os.path.abspath(root)

    result = {
        "project_root": root,
        "languages": {},
        "project_dependencies": get_project_deps(root),
        "files": {},
    }

    # Python
    py_deps = analyze_python(root)
    if py_deps:
        result["languages"]["python"] = True
        result["files"].update(py_deps)

    # JS/TS
    js_deps = analyze_js_ts(root)
    if js_deps:
        result["languages"]["javascript_typescript"] = True
        result["files"].update(js_deps)

    # Rust
    rs_deps = analyze_rust(root)
    if rs_deps:
        result["languages"]["rust"] = True
        result["files"].update(rs_deps)

    # Go
    go_deps = analyze_go(root)
    if go_deps:
        result["languages"]["go"] = True
        result["files"].update(go_deps)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
