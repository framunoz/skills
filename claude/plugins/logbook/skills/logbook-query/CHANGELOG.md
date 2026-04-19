# Changelog — logbook-query

## [0.2.0] — 2026-04-19

### Changed (MINOR)
- Removed `disable-model-invocation: true`: any Claude Code agent may now invoke this skill to query logbook entries for context, matching FR-007a.
- Updated description to reflect open invocation policy.
- Added `argument-hint` frontmatter field for autocomplete guidance.
- Fixed script path: replaced undocumented `${CLAUDE_PLUGIN_ROOT}` variable with `${CLAUDE_SKILL_DIR}` per official Claude Code skills spec.

## [0.1.0] — 2026-04-18

### Added
- Initial release: filter logbook entries by date range, type, tag, and limit; returns results newest-first.
