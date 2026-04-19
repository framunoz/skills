# Schema: `amendment`

Allowed in **any** logbook regardless of `schema_type`. Amendments do not replace the original entry — they append a correction record that `format.py` renders as a callout beneath the original.

## Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `amends` | `{id: int, ulid: string}` | yes | Must match an existing entry in the same logbook. |
| `reason` | string | yes | Short explanation (typo, fact correction, clarification, redaction). |
| `body` | string | yes | Corrected or clarifying content. |

Both `amends.id` and `amends.ulid` must match an existing entry → otherwise rejected (exit 13).

## Example entry

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

## Rendered output

`format.py` renders a callout under the original entry:

```
> Amended by #2 on 2026-04-18: Clarification
```
