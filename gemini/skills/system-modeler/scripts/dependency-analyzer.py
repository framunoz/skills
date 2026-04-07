#!/usr/bin/env python3
import os
import sys
import json
import re
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


def get_project_deps(root):
    """Extract project-level dependencies from common config files."""
    project_deps = {}

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
                deps = data.get("project", {}).get("dependencies", [])
                if deps:
                    project_deps["python_pyproject"] = deps
        except Exception:
            # Fallback for older python or missing tomllib (unlikely in 3.13)
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

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
