---
name: logbook-format
description: Render a logbook's entries.jsonl to rendered.md. Invoke only when the user or the logbook subagent asks to format/render a logbook.
model: haiku
effort: low
disable-model-invocation: true
allowed-tools: Bash(python3 *), Read
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/main/plugins/logbook/skills/logbook-format
  version: "0.1.0"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, format, render, markdown
---

Render a logbook's `entries.jsonl` to a human-readable `rendered.md`. Idempotent: same input → same bytes.

## Usage

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook-format/scripts/format.py" \
  --logbook <slug> \
  [--project-root <path>] \
  [--output <path>]
```

- `--logbook`: target logbook slug.
- `--project-root`: defaults to `$CLAUDE_PROJECT_DIR` or current working directory.
- `--output`: override output path (default: `<project-root>/logbook/<slug>/rendered.md`).

## Output (success)

```json
{"ok": true, "entries_rendered": 42, "output": "logbook/<slug>/rendered.md"}
```

## Rendering rules

- Entries grouped by type: Tests, Collaboration, Free notes, Amendments.
- Within each section: newest first.
- Header: `### [#<id>] <title> — <date>`.
- Amendment entries also render a callout under the original entry: `> Amended by #<N> on <date>: <reason>`.
- Missing optional fields render as `*No observations*`.

## Error codes

| Exit | Reason |
|---|---|
| 0 | Success. |
| 10 | Logbook not found. |
| 15 | Corrupt JSONL (exits non-zero only if zero entries rendered). |
| 20 | I/O error. |
