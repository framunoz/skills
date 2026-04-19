# Schema: `tests`

Valid when `schema_type: tests`.

## Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `went_well` | string[] | no* | Short sentences describing what worked. |
| `went_wrong` | string[] | no* | Short sentences describing failures. |
| `next_steps` | string[] | no | Follow-up actions. |
| `context` | string | no | Free-form narrative. |

\* **At least one of `went_well` or `went_wrong` must be non-empty.** Both empty → rejected (exit 11).

## Example entry

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
