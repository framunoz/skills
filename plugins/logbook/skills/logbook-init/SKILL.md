---
name: logbook-init
description: Create a new logbook under logbook/<slug>/ with a declared schema type (tests, collaboration, free). Only invoke on explicit user/subagent request to create a logbook.
model: haiku
effort: low
disable-model-invocation: true
allowed-tools: Bash(python3 *), Read
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/main/plugins/logbook/skills/logbook-init
  version: "0.1.0"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, init, create
---

Create a new logbook in the current project.

## Usage

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook-init/scripts/init.py" \
  --logbook <slug> \
  --type <tests|collaboration|free> \
  [--title "<title>"] \
  [--description "<description>"] \
  [--project-root <path>]
```

- `--logbook`: slug matching `^[a-z0-9]+(-[a-z0-9]+)*$` (lowercase, hyphens only).
- `--type`: one of `tests`, `collaboration`, `free`.
- `--title`: optional human-readable title (defaults to slug).
- `--description`: optional description.
- `--project-root`: defaults to `$CLAUDE_PROJECT_DIR` or current working directory.

## Output (success)

```json
{"ok": true, "logbook": "<slug>", "path": "logbook/<slug>/", "schema_type": "<type>"}
```

## Error codes

| Exit | Reason |
|---|---|
| 0 | Success. |
| 16 | Invalid slug. |
| 17 | Logbook already exists. |
| 18 | Invalid `--type`. |
| 20 | I/O error. |
