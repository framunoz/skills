# Logbook Entry Schemas

All logbook entries share **common fields** plus **type-specific fields**. The logbook's `schema_type` (declared at init) constrains which entry types are valid; `amendment` is always allowed.

---

## Common Fields (every entry)

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | integer | yes | Monotonic per-logbook counter, starting at 1. Assigned by `push.py`. |
| `ulid` | string | yes | ULID (26 Crockford base-32 chars). Assigned by `push.py`. |
| `created_at` | string (RFC 3339 UTC) | yes | Assigned by `push.py`. |
| `type` | string | yes | One of `tests`, `collaboration`, `free`, `amendment`. |
| `title` | string | yes | ≤ 200 chars. |
| `tags` | string[] | no | Lowercase, hyphenated. |
| `author` | string | no | Free-text. Default `"user"`. |

---

## Schema: `tests`

Valid when `schema_type: tests`. At least one of `went_well` or `went_wrong` must be non-empty.

| Field | Type | Required | Notes |
|---|---|---|---|
| `went_well` | string[] | no* | Short sentences describing what worked. |
| `went_wrong` | string[] | no* | Short sentences describing failures. |
| `next_steps` | string[] | no | Follow-up actions. |
| `context` | string | no | Free-form narrative. |

\* At least one of `went_well` or `went_wrong` must be non-empty. Both empty → rejected (exit 11).

**Example entry (JSON)**:
```json
{
  "id": 1,
  "ulid": "01HW0000000000000000000001",
  "created_at": "2026-04-18T10:45:12Z",
  "type": "tests",
  "title": "Smoke test after login rework",
  "went_well": ["OAuth redirect works", "Token refresh within 1s"],
  "went_wrong": ["Refresh loop on stale cookie in Safari"],
  "next_steps": ["Reproduce in staging with Safari 17"],
  "context": "Tested on localhost after PR #42.",
  "tags": ["auth", "smoke"],
  "author": "user"
}
```

---

## Schema: `collaboration`

Valid when `schema_type: collaboration`. At least one of `ai_contribution` or `human_contribution` must be non-empty.

| Field | Type | Required | Notes |
|---|---|---|---|
| `ai_contribution` | string | no* | What the AI produced or proposed. |
| `human_contribution` | string | no* | What the human designed or decided. |
| `human_corrections` | string[] | no | Each item = one correction the human made to the AI. |
| `milestone` | string | no | Optional anchor for retrospectives. |
| `context` | string | no | Free-form narrative. |

\* At least one of `ai_contribution` or `human_contribution` must be non-empty.

**Example entry (JSON)**:
```json
{
  "id": 1,
  "ulid": "01HW0000000000000000000002",
  "created_at": "2026-04-18T11:00:00Z",
  "type": "collaboration",
  "title": "Data model design session",
  "ai_contribution": "Proposed the JSONL append-only format and ULID scheme.",
  "human_contribution": "Decided to keep format_version in meta.json for future migrations.",
  "human_corrections": ["AI initially suggested SQLite; human corrected to plain files."],
  "milestone": "Data model finalized",
  "context": "Session 1 of the logbook feature.",
  "tags": ["design", "data-model"],
  "author": "user+claude"
}
```

---

## Schema: `free`

Valid when `schema_type: free`. `body` is required.

| Field | Type | Required | Notes |
|---|---|---|---|
| `body` | string | yes | Markdown permitted. |

**Example entry (JSON)**:
```json
{
  "id": 1,
  "ulid": "01HW0000000000000000000003",
  "created_at": "2026-04-18T12:00:00Z",
  "type": "free",
  "title": "Decision: use JSONL over SQLite",
  "body": "Chose JSONL because it is human-readable, diff-friendly, and requires no dependencies.\n\nSQLite would require a driver and makes git diffs unreadable.",
  "tags": ["adr"],
  "author": "user"
}
```

---

## Schema: `amendment`

Allowed in any logbook regardless of `schema_type`. Both `amends.id` and `amends.ulid` must match an existing entry.

| Field | Type | Required | Notes |
|---|---|---|---|
| `amends` | `{id: int, ulid: string}` | yes | Must reference an existing entry in the same logbook. |
| `reason` | string | yes | Short explanation (typo, fact correction, clarification, redaction). |
| `body` | string | yes | Corrected or clarifying content. |

**Example entry (JSON)**:
```json
{
  "id": 2,
  "ulid": "01HW0000000000000000000004",
  "created_at": "2026-04-18T11:02:04Z",
  "type": "amendment",
  "title": "Amend #1: refresh loop scope",
  "amends": {"id": 1, "ulid": "01HW0000000000000000000001"},
  "reason": "Clarification",
  "body": "The refresh loop only affects Safari 17; Chrome and Firefox are unaffected.",
  "author": "user"
}
```

---

## Validation Rules Summary

| Schema | Rejection condition | Exit code |
|---|---|---|
| `tests` | Both `went_well` and `went_wrong` are empty | 11 |
| `collaboration` | Both `ai_contribution` and `human_contribution` are empty | 11 |
| `free` | `body` is absent or empty | 11 |
| `amendment` | `amends.id` or `amends.ulid` not found in logbook | 13 |
| any | `type` doesn't match logbook `schema_type` (and isn't `amendment`) | 12 |
| any | Suspected secret in payload (without `--acknowledge-sensitive`) | 14 |
