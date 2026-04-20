---
name: logbook-query
description: Query logbook entries by slug, date range, tag, or type. Any Claude Code agent may invoke this to read logbook data and enrich its context. Never fabricate entries; respond only from file contents.
model: sonnet
effort: medium
argument-hint: '[logbook-slug] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--type type] [--tag tag] [--limit N]'
allowed-tools: Bash(python3 *), Read
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/main/plugins/logbook/skills/logbook-query
  version: "0.2.0"
  last-updated: "2026-04-19"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, query, search, filter
---

Query entries in a logbook by date range, tag, type, or a combination.

## Usage

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/query.py" \
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
