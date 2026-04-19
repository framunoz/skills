---
name: logbook-schema
description: Reference skill loaded by the logbook subagent. Provides schema definitions for all entry types. Not user-invocable.
user-invocable: false
disable-model-invocation: true
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/main/plugins/logbook/skills/logbook-schema
  version: "0.1.0"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, schema, reference
---

This skill is a reference document loaded via the `skills:` frontmatter of the `logbook` subagent.
Its content (in `references/schemas.md`) defines the three logbook entry schemas (`tests`, `collaboration`, `free`) and the `amendment` type.

Do not invoke this skill directly. The `logbook` subagent loads it automatically at startup.
