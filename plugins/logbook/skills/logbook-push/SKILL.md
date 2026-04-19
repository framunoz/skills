---
name: logbook-push
description: Append one validated entry to a named logbook under logbook/<slug>/. Only invoke when the user or the logbook subagent explicitly asks for a push. Never auto-fire.
model: haiku
effort: low
disable-model-invocation: true
allowed-tools: Bash(python3 *), Read
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/main/plugins/logbook/skills/logbook-push
  version: "0.1.0"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, push, append, jsonl
---

Append one validated entry to a logbook. Payload is supplied via stdin as a single JSON object.

## Usage

```bash
echo '<json-payload>' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook-push/scripts/push.py" \
  --logbook <slug> \
  --type <tests|collaboration|free|amendment> \
  [--acknowledge-sensitive] \
  [--project-root <path>]
```

- `--logbook`: target logbook slug (must already exist via `logbook-init`).
- `--type`: entry type. Must match the logbook's `schema_type`, or be `amendment`.
- `--acknowledge-sensitive`: suppress the secrets gate (exit 14) and proceed anyway.
- `--project-root`: defaults to `$CLAUDE_PROJECT_DIR` or current working directory.

## Stdin

A single JSON object matching the schema for `--type`. See `logbook-schema` for full field documentation.

## Output (success)

```json
{"ok": true, "id": 3, "ulid": "01HW...", "logbook": "<slug>", "path": "logbook/<slug>/entries.jsonl"}
```

## Error codes

| Exit | Reason |
|---|---|
| 0 | Success. |
| 10 | Logbook not found (no `meta.json`). |
| 11 | Schema validation failed. |
| 12 | `--type` mismatch with logbook's `schema_type`. |
| 13 | Amendment target not found. |
| 14 | Sensitive content detected; re-invoke with `--acknowledge-sensitive`. |
| 20 | I/O error. |
| 99 | Unexpected internal error. |

**Not idempotent** — each call appends a new entry.
