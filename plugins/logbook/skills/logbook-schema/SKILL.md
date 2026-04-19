---
name: logbook-schema
description: >
  Schema reference for the logbook subagent. Read this skill whenever you need
  to know field names, required vs optional, validation rules, or example payloads
  for any logbook entry type (tests, collaboration, free, amendment). Load the
  relevant reference file — not the whole set — before composing or validating any
  entry. When in doubt about whether a field is valid or required, read the schema
  first rather than guessing.
user-invocable: false
disable-model-invocation: true
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/main/plugins/logbook/skills/logbook-schema
  version: "0.1.1"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, schema, reference
---

# Schema Reference Index

Schema definitions are split into per-type files. **Load only the file you need.**

| Entry type                                                | Reference file                       |
| --------------------------------------------------------- | ------------------------------------ |
| Common fields (id, ulid, created_at, title, tags, author) | `references/schema-common.md`        |
| `tests`                                                   | `references/schema-tests.md`         |
| `collaboration`                                           | `references/schema-collaboration.md` |
| `free`                                                    | `references/schema-free.md`          |
| `amendment`                                               | `references/schema-amendment.md`     |

## When to read each file

- **Before composing any entry** — read `schema-common.md` (once per session is enough) plus the file for the target entry type.
- **Before pushing an amendment** — read `schema-amendment.md`; you do not need to re-read the logbook's base type file.
- **When validating user dictation** — read the type file matching the logbook's `schema_type` to confirm required fields are satisfied.

## Quick validation summary

| Type            | Rejection condition                                   | Exit |
| --------------- | ----------------------------------------------------- | ---- |
| `tests`         | Both `went_well` and `went_wrong` empty               | 11   |
| `collaboration` | Both `ai_contribution` and `human_contribution` empty | 11   |
| `free`          | `body` absent or empty                                | 11   |
| `amendment`     | `amends.id` / `amends.ulid` not found                 | 13   |
| any             | Type ≠ logbook `schema_type` (and not `amendment`)    | 12   |
| any             | Suspected secret without `--acknowledge-sensitive`    | 14   |
