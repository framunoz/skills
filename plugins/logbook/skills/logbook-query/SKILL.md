---
name: logbook-query
description: Query one logbook — list or summarize entries by date range, tag, or type. Only invoke when the user or the logbook subagent explicitly asks to query a logbook by name. Never fabricate entries; respond only from file contents.
model: sonnet
effort: medium
disable-model-invocation: true
allowed-tools: Bash(python3 *), Read
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/main/plugins/logbook/skills/logbook-query
  version: "0.1.0"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, query, search, filter
---

Query entries in a logbook by date range, tag, type, or a combination.

## Usage

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook-query/scripts/query.py" \
  --logbook <slug> \
  [--since <ISO-date>] \
  [--until <ISO-date>] \
  [--type <tests|collaboration|free|amendment>] \
  [--tag <tag>] \
  [--limit <N>] \
  [--project-root <path>]
```

## Behavior

1. Parse the user's natural-language query into the appropriate flags above.
2. Call the script via `Bash`.
3. If `count: 0`, respond verbatim: "No entries match this query in `<slug>`." Do NOT fabricate.
4. Otherwise, produce a summary that:
   - Cites each referenced entry by its `id` (e.g., "Entry #3, #7").
   - Preserves the original language of the quoted text.
   - Never introduces claims absent from the returned JSON.

## Output (success)

```json
{"ok": true, "logbook": "<slug>", "count": 3, "entries": [{...}, {...}, {...}]}
```

Zero matches: `count: 0, entries: []` — exit 0, not an error.

## Error codes

| Exit | Reason |
|---|---|
| 0 | Success (including zero matches). |
| 10 | Logbook not found. |
| 15 | Corrupt JSONL; returns parseable entries + `warnings`. Exit 0 unless zero parsed. |
| 20 | I/O error. |
