---
name: logbook-list
description: List logbooks in the current project with entry count and last-entry date. Any Claude Code agent may invoke this skill to enrich its context with an inventory of available logbooks.
model: haiku
effort: low
argument-hint: '[--project-root <path>]'
allowed-tools: Bash(python3 *), Read
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/main/plugins/logbook/skills/logbook-list
  version: "0.2.0"
  last-updated: "2026-04-19"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, list, inventory
---

List all logbooks in the current project.

## Usage

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/list.py" \
  [--project-root <path>]
```

- `--project-root`: defaults to `$CLAUDE_PROJECT_DIR` or current working directory.

## Output (success)

```json
{"ok": true, "logbooks": [
  {"slug": "tests-login", "entries": 12, "last_entry_at": "2026-04-18T12:00:00Z"},
  {"slug": "collab-v1",   "entries": 3,  "last_entry_at": "2026-04-17T09:15:00Z"}
]}
```

Empty project returns `{"ok": true, "logbooks": []}` — not an error.

## Error codes

| Exit | Reason |
|---|---|
| 0 | Success (including empty list). |
| 20 | I/O error. |
