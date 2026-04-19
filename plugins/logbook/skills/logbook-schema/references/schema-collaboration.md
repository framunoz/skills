# Schema: `collaboration`

Valid when `schema_type: collaboration`.

## Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `ai_contribution` | string | no* | What the AI produced or proposed. |
| `human_contribution` | string | no* | What the human designed or decided. |
| `human_corrections` | string[] | no | Each item = one correction the human made to the AI. |
| `milestone` | string | no | Optional anchor for retrospectives. |
| `context` | string | no | Free-form narrative. |

\* **At least one of `ai_contribution` or `human_contribution` must be non-empty.** Both empty → rejected (exit 11).

## Example entry

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
