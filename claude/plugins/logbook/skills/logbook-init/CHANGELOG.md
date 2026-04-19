# Changelog — logbook-init

## [0.2.0] — 2026-04-19

### Changed (MINOR — breaking)
- Description restricted to subagent-only per FR-002b ("Only the logbook subagent may invoke this skill").
- Removed `--type` required argument: logbooks are neutral containers with no declared type per data-model.md. **Existing callers must drop `--type`.**
- Added `argument-hint: '<slug> [<title>] [<description>]'` frontmatter field.
- Added `$ARGUMENTS` parsing block in body.
- `init.py`: `meta.json` now written without `schema_type`; only `slug`, `title`, `description`, `created_at`, `format_version` are stored.
- Success output no longer includes `schema_type` field.
- Removed exit code 18 (invalid `--type`).

## [0.1.1] — 2026-04-19

### Fixed (PATCH)
- Fixed script path: replaced undocumented `${CLAUDE_PLUGIN_ROOT}` variable with `${CLAUDE_SKILL_DIR}` per official Claude Code skills spec.

## [0.1.0] — 2026-04-18

### Added
- Initial release: create a new logbook directory with `meta.json` and empty `entries.jsonl`.
