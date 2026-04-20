# Contract: Skill `logbook-format`

Skill at `claude/plugins/logbook/skills/logbook-format/` (shipped as part of the `logbook` plugin). Renders `entries.jsonl` for a given logbook to `rendered.md`. Pure read → transform → overwrite of the derived file. Invokable as `/logbook-format` or called by the `logbook` subagent after a push.

**`SKILL.md` frontmatter**:

```yaml
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
  source: https://github.com/framunoz/skills/tree/<commit-sha>/plugins/logbook/skills/logbook-format
  version: "0.1.0"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, format, render, markdown
---
```

## Script invocation

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/format.py" \
  --logbook <slug> \
  [--project-root <path>] \
  [--output <path>]
```

Defaults: `--output` = `<project-root>/logbook/<slug>/rendered.md`.

## Preconditions

- `meta.json` and `entries.jsonl` exist for `<slug>`.

## Postconditions

- `rendered.md` is overwritten with a Markdown rendering of all entries.
- `entries.jsonl` and `meta.json` are not modified.
- Running `format` twice with no new entries produces byte-identical output (idempotent).

## Rendering rules

- Sections grouped by entry `type`: `Tests`, `Collaboration`, `Free notes`, `Amendments` — or chronological if the logbook mixes types (only `amendment` entries mix).
- Within each section, entries listed **newest first**.
- Each entry header: `### [#<id>] <title> — <created_at as local date>`.
- `amendment` entries also render a callout under the original entry: `> Amended by #<amendment-id> on <date>: <reason>`.
- Missing optional fields render as `*No observations*` (FR-009) — never fabricated.
- Preserve the original input language of each field.

## Outputs

stdout on success:

```json
{"ok": true, "entries_rendered": 42, "output": "logbook/tests-login/rendered.md"}
```

## Error codes

| Exit | Reason |
|---|---|
| 0 | Success. |
| 10 | Logbook not found. |
| 15 | Corrupt JSONL line(s) encountered; renders what it can, lists skipped line numbers in `error`. Exit non-zero only if zero entries could be rendered. |
| 20 | I/O error. |

## Idempotency

Idempotent. No side effects other than overwriting `rendered.md`.
