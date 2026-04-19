# Changelog — logbook-list

## [0.2.1] — 2026-04-19

### Fixed (PATCH)
- Description no longer mentions "schema type" (logbooks have no declared type).
- Added `argument-hint: '[--project-root <path>]'` frontmatter field.
- `list.py`: removed `schema_type` field from logbook objects in JSON output; output now contains only `slug`, `entries`, `last_entry_at`.

## [0.2.0] — 2026-04-19

### Changed (MINOR)
- Removed `disable-model-invocation: true`: any Claude Code agent may now invoke this skill to enrich context with a logbook inventory, matching FR-007.
- Updated description to reflect open invocation policy.
- Fixed script path: replaced undocumented `${CLAUDE_PLUGIN_ROOT}` variable with `${CLAUDE_SKILL_DIR}` per official Claude Code skills spec.

## [0.1.0] — 2026-04-18

### Added
- Initial release: list all logbooks in the project with slug, schema type, entry count, and last entry timestamp.
