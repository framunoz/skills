# Changelog — logbook plugin

## [0.2.0] — 2026-04-19

### Changed (MINOR)
- `logbook` subagent v0.2.0: removed `logbook-schema` from `skills:`; added `references: [logbook-push/references/schemas.md]` so schema context loads at startup; added shorthand invocation `@logbook <slug>: <msg>` (FR-003a); added context enrichment before persist with user review (FR-003b); added auto-create notification when slug not found (FR-002b).
- `logbook-push` v0.2.1: description restricted to subagent-only (FR-002a); added `references: [references/schemas.md]`; removed stale `schema_type` warning from body and script.
- `logbook-init` v0.2.0: description restricted to subagent-only (FR-002b); removed `--type` required argument (logbooks are typeless); added `argument-hint` and `$ARGUMENTS` parsing; `meta.json` now written without `schema_type`; init.py simplified accordingly.
- `logbook-format` v0.2.0: description updated to user+agent+subagent invocable (FR-007c); added `argument-hint: '<slug>'` and `$ARGUMENTS` parsing block.
- `logbook-list` v0.2.1: removed "with schema type" from description; added `argument-hint`; `list.py` no longer includes `schema_type` in logbook objects.
- Deleted `logbook-schema` skill: schema context now co-located in `logbook-push/references/schemas.md`.
- Added `logbook-push/references/schemas.md` with consolidated entry schemas for `tests`, `collaboration`, `free`, `amendment` (no `schema_type` references).

## [0.1.1] — 2026-04-19

### Changed
- `logbook-list` v0.2.0: removed `disable-model-invocation` so any Claude Code agent can invoke it (FR-007); fixed `${CLAUDE_SKILL_DIR}` script path.
- `logbook-query` v0.2.0: removed `disable-model-invocation` so any Claude Code agent can invoke it (FR-007a); added `argument-hint`; fixed `${CLAUDE_SKILL_DIR}` script path.
- `logbook-push` v0.2.0: added `disable-model-invocation: true` (FR-002a); added `argument-hint`; removed fixed-schema type mismatch enforcement — logbooks now accept mixed entry types with an optional warning; fixed `${CLAUDE_SKILL_DIR}` script path.
- `logbook-format` v0.1.1: fixed `${CLAUDE_SKILL_DIR}` script path.
- `logbook-init` v0.1.1: fixed `${CLAUDE_SKILL_DIR}` script path.
- `logbook` subagent v0.1.1: updated entry-type selection guidance to reflect mixed schema; clarified Python interpreter detection section.

## [0.1.0] — 2026-04-18

### Added
- `logbook` subagent: thin orchestrator (sonnet, cyan, background) that composes user dictation into validated entries and delegates persistence to the skills.
- `logbook-init` skill: create a new logbook with a declared schema type (`tests`, `collaboration`, `free`).
- `logbook-push` skill: append one validated entry to a logbook; supports `tests`, `collaboration`, `free`, and `amendment` types; includes sensitive-content gate.
- `logbook-format` skill: render `entries.jsonl` to `rendered.md`; idempotent; newest-first per section; amendment callouts under original entries.
- `logbook-list` skill: list all logbooks in the project with entry count and last-entry timestamp.
- `logbook-query` skill: filter entries by date range, type, tag, and limit; returns results newest-first.
- `logbook-schema` skill: reference document loaded by the subagent at startup; documents all schemas and validation rules.
- Plugin manifest (`plugin.json`) and marketplace catalog (`marketplace.json`) for one-command install.
