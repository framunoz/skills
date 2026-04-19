# Schema: `free`

Valid when `schema_type: free`.

## Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `body` | string | yes | Markdown permitted. Must be non-empty. |

`body` absent or empty → rejected (exit 11).

## Example entry

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
