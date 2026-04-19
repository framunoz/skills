# Changelog — logbook-format

## [0.2.0] — 2026-04-19

### Changed (MINOR)
- Description updated to explicitly state user+agent+subagent invocable per FR-007c.
- Added `argument-hint: '<slug>'` frontmatter field.
- Added `$ARGUMENTS` parsing block in body showing how slug is extracted and passed to `format.py --logbook`.

## [0.1.1] — 2026-04-19

### Fixed (PATCH)
- Fixed script path: replaced undocumented `${CLAUDE_PLUGIN_ROOT}` variable with `${CLAUDE_SKILL_DIR}` per official Claude Code skills spec.

## [0.1.0] — 2026-04-18

### Added
- Initial release: render `entries.jsonl` to `rendered.md` with sections per entry type, newest-first ordering, and amendment callouts.
