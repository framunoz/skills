# Common Fields (all entry types)

Every logbook entry, regardless of type, includes these fields:

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | integer | yes | Monotonic per-logbook counter, starting at 1. Assigned by `push.py`. |
| `ulid` | string | yes | ULID (26 Crockford base-32 chars). Assigned by `push.py`. |
| `created_at` | string (RFC 3339 UTC) | yes | Assigned by `push.py`. |
| `type` | string | yes | One of `tests`, `collaboration`, `free`, `amendment`. |
| `title` | string | yes | ≤ 200 chars. |
| `tags` | string[] | no | Lowercase, hyphenated. |
| `author` | string | no | Free-text. Default `"user"`. |

## Type-mismatch rule

If the entry `type` does not match the logbook's `schema_type` (from `meta.json`) and the entry is not `amendment`, `push.py` rejects with **exit 12**.

`amendment` is always allowed regardless of `schema_type`.
