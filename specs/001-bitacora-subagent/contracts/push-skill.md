# Contract: Skill `logbook-push`

Skill at `plugins/logbook/skills/logbook-push/` (shipped as part of the `logbook` plugin) wrapping a deterministic Python script that appends one validated entry to a logbook. Invokable directly as `/logbook-push` by the user or called by the `logbook` subagent.

**`SKILL.md` frontmatter**:

```yaml
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
  source: https://github.com/framunoz/skills/tree/<commit-sha>/plugins/logbook/skills/logbook-push
  version: "0.1.0"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, push, append, jsonl
---
```

## Script invocation

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook-push/scripts/push.py" \
  --logbook <slug> \
  --type <tests|collaboration|free|amendment> \
  [--acknowledge-sensitive] \
  [--project-root <path>]
```

Payload is passed via **stdin** as a single JSON object matching the schema for the given `--type` (see `data-model.md`). Example:

```bash
echo '{"title":"Smoke","went_well":["..."],"went_wrong":["..."]}' \
  | python3 .../push.py --logbook tests-login --type tests
```

Rationale: stdin avoids temp files, is easy to debug (`cat payload.json | push.py ...`), and keeps the skill's `allowed-tools` minimal (no `Write`).

## Preconditions

- `<project-root>/logbook/<slug>/meta.json` exists (created via `logbook-init`).
- `--type` matches the logbook's `schema_type`, OR equals `amendment`.
- stdin is valid JSON and passes schema validation.
- For `amendment`: `amends.id` and `amends.ulid` both exist in `entries.jsonl`.

## Postconditions

- Exactly one new line is appended to `entries.jsonl` with server-assigned `id`, `ulid`, and `created_at`.
- No existing line is modified.
- `rendered.md` is **not** touched (separate `format` pass).

## Outputs

**stdout (on success)** — JSON object:

```json
{"ok": true, "id": 3, "ulid": "01HW...C3", "logbook": "tests-login", "path": "logbook/tests-login/entries.jsonl"}
```

**stdout (on failure)** — JSON object with `ok: false` and an `error` field. Exit code non-zero.

## Error codes

| Exit | Reason |
|---|---|
| 0 | Success. |
| 10 | Logbook not found (no `meta.json`). |
| 11 | Schema validation failed. Details in `error`. |
| 12 | `type` mismatch with logbook's `schema_type`. |
| 13 | Amendment target not found. |
| 14 | Sensitive content detected; re-invoke with `--acknowledge-sensitive` to proceed. |
| 20 | I/O error (permissions, disk). |
| 99 | Unexpected internal error. |

## Idempotency

Not idempotent: each invocation appends a new entry (a new `id`). The subagent MUST NOT retry a failed push with exit code 0–14 without changing the payload, to avoid duplicate entries.

## Security rules

- No network access.
- Writes only under `<project-root>/logbook/<slug>/`.
- Rejects payloads containing suspected secrets unless `--acknowledge-sensitive` is passed.
