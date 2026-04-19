# Changelog — logbook plugin

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
