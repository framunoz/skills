# Contract: Skill `logbook-query`

Skill at `plugins/logbook/skills/logbook-query/` (shipped as part of the `logbook` plugin). Reads a logbook and returns a grounded summary or filtered list of entries. This is the only logbook skill that does real cognitive work (summarization, filtering with natural-language intent), so it uses Sonnet.

**`SKILL.md` frontmatter**:

```yaml
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
  source: https://github.com/framunoz/skills/tree/<commit-sha>/plugins/logbook/skills/logbook-query
  version: "0.1.0"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, query, search, filter
---
```

## Script invocation

The skill invokes a helper script that extracts the matching raw entries as JSON; the skill's own LLM turn then composes a human-readable summary strictly from that JSON.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook-query/scripts/query.py" \
  --logbook <slug> \
  [--since <ISO-date>] [--until <ISO-date>] \
  [--type <tests|collaboration|free|amendment>] \
  [--tag <tag>] \
  [--limit <N>] \
  [--project-root <path>]
```

## Preconditions

- `meta.json` and `entries.jsonl` exist for `<slug>`.

## Script output

stdout on success — a JSON array of matching entries in chronological order (newest first):

```json
{"ok": true, "logbook": "tests-login", "count": 3, "entries": [ {...}, {...}, {...} ]}
```

If zero entries match, `count: 0`, `entries: []`. Not an error.

## Skill behavior on top of the script

1. Parse the user's natural-language query into script flags (`--since`, `--type`, etc.).
2. Call the script via `Bash`.
3. If the script returns `count: 0`, respond verbatim: "No entries match this query in `<slug>`." Do NOT fabricate.
4. Otherwise, produce a summary that:
   - Cites each referenced entry by its `id` (e.g. "Entry #3, #7").
   - Preserves the original language of the quoted text.
   - Never introduces claims absent from the returned JSON (FR-007, SC-004).

## Error codes (script)

| Exit | Reason |
|---|---|
| 0 | Success (including zero matches). |
| 10 | Logbook not found. |
| 15 | Corrupt JSONL line(s) encountered; returns parseable entries + a `warnings` list. Exit 0 unless zero entries could be parsed. |
| 20 | I/O error. |

## Idempotency

Idempotent. Read-only script; the skill's summary is not cached.
