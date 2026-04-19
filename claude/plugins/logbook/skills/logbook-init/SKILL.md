---
name: logbook-init
description: Create a new logbook under logbook/<slug>/. Only the logbook subagent may invoke this skill — not directly user-invocable (FR-002b). Invoked automatically when a push targets a non-existent slug.
model: haiku
effort: low
disable-model-invocation: true
argument-hint: '<slug> [<title>] [<description>]'
allowed-tools: Bash(python3 *), Bash(python *), Bash(command *), Read
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/main/plugins/logbook/skills/logbook-init
  version: "0.2.0"
  last-updated: "2026-04-19"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, init, create
---

Create a new logbook in the current project.

Parse `$ARGUMENTS` to extract slug and optional title/description:

```bash
# $ARGUMENTS format: <slug> [<title>] [<description>]
# First word is slug; remaining words form title (if provided)
SLUG=$(echo "$ARGUMENTS" | awk '{print $1}')
TITLE=$(echo "$ARGUMENTS" | cut -d' ' -f2-)  # optional; omit if same as slug
```

Then run the init script:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/init.py" \
  --logbook <slug> \
  [--title "<title>"] \
  [--description "<description>"] \
  [--project-root <path>]
```

- `--logbook`: slug matching `^[a-z0-9]+(-[a-z0-9]+)*$` (lowercase, hyphens only).
- `--title`: optional human-readable title (defaults to slug).
- `--description`: optional description.
- `--project-root`: defaults to `$CLAUDE_PROJECT_DIR` or current working directory.

## Output (success)

```json
{"ok": true, "logbook": "<slug>", "path": "logbook/<slug>/"}
```

## Error codes

| Exit | Reason |
|---|---|
| 0 | Success. |
| 16 | Invalid slug. |
| 17 | Logbook already exists. |
| 20 | I/O error. |
