---
name: logbook-push
description: Append one validated entry to a named logbook under logbook/<slug>/. Invoke ONLY from the logbook subagent — never directly by the user or another agent (FR-002a). Never auto-fire.
model: haiku
effort: low
disable-model-invocation: true
argument-hint: '{"logbook":"<slug>","type":"<tests|collaboration|free|amendment>","payload":{...}}'
allowed-tools: Bash(python3 *), Bash(python *), Bash(command *), Read
references:
  - references/schemas.md
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/main/plugins/logbook/skills/logbook-push
  version: "0.2.1"
  last-updated: "2026-04-19"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, push, append, jsonl
---

Append one validated entry to a logbook.

You receive the entry data via `$ARGUMENTS` as a JSON object with this shape:

```json
{
  "logbook": "<slug>",
  "type": "<tests|collaboration|free|amendment>",
  "payload": { ... },
  "acknowledge_sensitive": false
}
```

Parse `$ARGUMENTS`, extract the fields, and run the push script piping `payload` as JSON via stdin. Example:

```bash
echo '<payload-json>' | python3 "${CLAUDE_SKILL_DIR}/scripts/push.py" \
  --logbook <slug> --type <type> [--acknowledge-sensitive] [--project-root <path>]
```

Return the script's stdout JSON to the caller verbatim.

## Script usage reference

```bash
echo '<json-payload>' | python3 "${CLAUDE_SKILL_DIR}/scripts/push.py" \
  --logbook <slug> \
  --type <tests|collaboration|free|amendment> \
  [--acknowledge-sensitive] \
  [--project-root <path>]
```

- `--logbook`: target logbook slug (must already exist via `logbook-init`).
- `--type`: entry type. Any valid type is accepted in any logbook (mixed schema).
- `--acknowledge-sensitive`: suppress the secrets gate (exit 14) and proceed anyway.
- `--project-root`: defaults to `$CLAUDE_PROJECT_DIR` or current working directory.

## Stdin

A single JSON object matching the schema for `--type`. See `references/schemas.md` for full field documentation.

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
| 13 | Amendment target not found. |
| 14 | Sensitive content detected; re-invoke with `--acknowledge-sensitive`. |
| 20 | I/O error. |
| 99 | Unexpected internal error. |

**Not idempotent** — each call appends a new entry.
