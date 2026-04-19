# Changelog — logbook-push

## [0.2.1] — 2026-04-19

### Fixed (PATCH)
- Description restricted to subagent-only per FR-002a ("Invoke ONLY from the logbook subagent").
- Added `references: [references/schemas.md]` to frontmatter; removed stale reference to `logbook-schema` from body.
- `push.py`: removed `schema_type` read from `meta.json` and type-mismatch warning logic (logbooks are typeless containers; entry `type` is validated independently).

## [0.2.0] — 2026-04-19

### Changed (MINOR)
- Added `disable-model-invocation: true`: push operations remain exclusive to explicit user or subagent invocation, matching FR-002a.
- Added `argument-hint` frontmatter field for autocomplete guidance.
- Removed `--type` mismatch enforcement: logbooks are now neutral containers (mixed schema). Any valid entry type is accepted in any logbook; a `warning` field is included in the success response when the type differs from the logbook's declared `schema_type`. Fixes I3 identified in spec analysis.
- Fixed script path: replaced undocumented `${CLAUDE_PLUGIN_ROOT}` variable with `${CLAUDE_SKILL_DIR}` per official Claude Code skills spec.
- Updated `--type` flag description and error code table (removed exit 12).

## [0.1.0] — 2026-04-18

### Added
- Initial release: append one validated entry to `entries.jsonl` with auto-assigned `id`, `ulid`, and `created_at`.
