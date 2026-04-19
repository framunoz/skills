# Tasks: Logbook Subagent — Correctivos post-spec 2026-04-19

**Input**: Design documents from `/specs/001-bitacora-subagent/`
**Prerequisites**: plan.md ✅, spec.md ✅, data-model.md ✅, contracts/ ✅

**Context**: Spec artifacts were updated 2026-04-19 to formalize mixed-schema (no `schema_type`),
correct access control (init + push subagent-only), relocate plugin to `claude/plugins/logbook/`,
remove `logbook-schema` skill, and add FRs 002b, 003a, 003b, 007c. These tasks bring the
implementation into alignment with the updated spec, without adding new features.

**Organization**: Tasks follow dependency order. Structural changes first, then data model fixes,
then per-user-story adjustments, then polish.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Setup — Relocate Plugin to Correct Directory

**Purpose**: Move the plugin to the path declared in plan.md (`claude/plugins/logbook/`).
All subsequent tasks reference the new path.

**⚠️ CRITICAL**: All other phases depend on this relocation. Run Phase 1 before touching any plugin files.

- [ ] T001 Move `plugins/logbook/` to `claude/plugins/logbook/` (rename/mv; preserve git history with `git mv`)
- [ ] T002 Update `.claude-plugin/marketplace.json` — change `plugins[0].source` from `"./plugins/logbook"` to `"./claude/plugins/logbook"`
- [ ] T003 Delete `claude/plugins/logbook/skills/logbook-schema/` directory entirely (plan.md: "A dedicated logbook-schema skill is not needed")
- [ ] T004 Create `claude/plugins/logbook/skills/logbook-push/references/schemas.md` with consolidated schema definitions for `tests`, `collaboration`, `free`, and `amendment` entry types (content migrated from the now-deleted logbook-schema references; match field specs in data-model.md)

**Checkpoint**: Plugin lives at `claude/plugins/logbook/`. `logbook-schema/` is gone. Schema reference file exists inside `logbook-push/references/`.

---

## Phase 2: Foundational — Data Model & Access Control Corrections

**Purpose**: Remove `schema_type` from all code paths, enforce correct access control per FRs 002a/002b/007c, and wire schema context into the subagent correctly.

**⚠️ CRITICAL**: These corrections block all story-level work. Fixtures, scripts, and SKILL.md files must be consistent before story tasks run.

- [ ] T005 Fix `claude/plugins/logbook/agents/logbook.md` — remove `logbook-schema` from `skills:` list (keep logbook-push, logbook-format, logbook-init, logbook-list, logbook-query); add `references: [logbook-push/references/schemas.md]` or equivalent so schema context loads at startup
- [ ] T006 Fix `claude/plugins/logbook/agents/logbook.md` — expand subagent instructions to cover: (a) shorthand invocation `@logbook <slug>: <message>` (FR-003a), (b) context enrichment from active session before persisting (FR-003b — must show enrichment to user first), (c) auto-create logbook when slug not found (FR-002b — notify user before creating)
- [ ] T007 Fix `claude/plugins/logbook/skills/logbook-push/SKILL.md` — description must be subagent-only ("Invoke ONLY from the logbook subagent — never directly by the user or another agent", FR-002a); add `references: [references/schemas.md]` field
- [ ] T008 Fix `claude/plugins/logbook/skills/logbook-init/SKILL.md` — (a) description must be subagent-only ("Only the logbook subagent may invoke this skill", FR-002b); (b) remove `--type` flag from script invocation in the body (no `schema_type`); (c) add `argument-hint: '<slug> [<title>] [<description>]'` frontmatter field; (d) add `$ARGUMENTS` parsing block in body showing how to extract slug/title/description; (e) update output JSON example to remove `schema_type` field
- [ ] T009 Fix `claude/plugins/logbook/skills/logbook-format/SKILL.md` — (a) description must be user+agent+subagent-invocable (FR-007c); (b) add `argument-hint: '<slug>'` frontmatter field; (c) add `$ARGUMENTS` parsing block showing how slug is extracted and passed to `format.py --logbook`; (d) confirm `user-invocable` is not set to false
- [ ] T009b Fix `claude/plugins/logbook/skills/logbook-list/SKILL.md` — (a) remove "with schema type" from description (logbooks have no declared type); (b) add `argument-hint: '[--project-root <path>]'` frontmatter field; (c) fix output JSON example to remove `schema_type` field from each logbook object; (d) confirm skill is user+agent-invocable (FR-007)
- [ ] T010 Fix `claude/plugins/logbook/skills/logbook-init/scripts/init.py` — remove `schema_type` from the `meta.json` written on disk; output only `slug`, `title`, `description`, `created_at`, `format_version: 1` per data-model.md
- [ ] T011 Fix `claude/plugins/logbook/skills/logbook-push/scripts/push.py` — remove any code that reads or validates `schema_type` from `meta.json`; entry `type` is validated against `["tests","collaboration","free","amendment"]` independently of the logbook metadata
- [ ] T012 [P] Fix `tests/logbook/fixtures/meta_tests.json` — remove `schema_type` field
- [ ] T013 [P] Fix `tests/logbook/fixtures/meta_collab.json` — remove `schema_type` field
- [ ] T014 [P] Fix `tests/logbook/fixtures/meta_free.json` — remove `schema_type` field
- [ ] T015 [P] Fix `tests/logbook/conftest.py` — remove any `schema_type` from fixture helpers or factory functions

**Checkpoint**: No `schema_type` anywhere in scripts or fixtures. Access control is correct in all SKILL.md descriptions. Schema context loads via `logbook-push/references/schemas.md`.

---

## Phase 3: User Story 1 — Registrar resultado de una prueba (P1) 🎯 MVP

**Goal**: User sends `@logbook tests-login: salió bien X, salió mal Y` and gets a correctly structured `tests`-type entry persisted in `logbook/tests-login/entries.jsonl`.

**Independent Test**: Invoke subagent with shorthand, verify `entries.jsonl` has exactly one new line of type `tests` with `went_well`/`went_wrong` fields; verify no `schema_type` in `meta.json`.

- [ ] T016 [P] [US1] Fix `tests/logbook/test_init.py` — remove assertions that expect `schema_type` in `meta.json`; assert only `slug`, `title`, `description`, `created_at`, `format_version`
- [ ] T017 [P] [US1] Fix `tests/logbook/test_push.py` (tests-type section) — ensure push validation accepts `tests` type without any `schema_type` check; assert `went_well`/`went_wrong` constraint (at least one non-empty); assert empty sections render as "No observations" not fabricated content (FR-009)
- [ ] T017b [P] [US1] Fix `tests/logbook/test_push.py` (sensitive-content section) — verify `push.py` exits with code 14 when payload contains credential-like content and `--acknowledge-sensitive` is not passed; verify a second call with `--acknowledge-sensitive` succeeds (FR-008)
- [ ] T018 [P] [US1] Fix `tests/logbook/test_format.py` — verify `format.py` renders `tests`-type entries with "Went well" and "Went wrong" sections; verify empty sections produce "No observations" label
- [ ] T019 [US1] Fix `tests/logbook/test_amendment.py` — ensure amendment tests pass without any `schema_type` dependency; confirm `amends.id` + `amends.ulid` validation still enforced (FR-006b)
- [ ] T020 [US1] Run `uvx pytest tests/logbook/test_init.py tests/logbook/test_push.py tests/logbook/test_format.py tests/logbook/test_amendment.py` and confirm all pass

**Checkpoint**: Full push → format flow works for `tests`-type entries. Amendment flow verified. Zero `schema_type` references in test output or code paths.

---

## Phase 4: User Story 2 — Registrar proceso de co-creación con IA (P2)

**Goal**: User logs a collaboration session (`@logbook collab-v1: la IA propuso X, yo decidí Y`); subagent produces a `collaboration`-type entry with `ai_contribution`, `human_contribution`, `human_corrections`, and optional `milestone`.

**Independent Test**: Push a collaboration entry and verify all required fields present; verify at least one of `ai_contribution`/`human_contribution` is non-empty; verify `milestone` is optional and preserved when provided.

- [ ] T021 [P] [US2] Fix `tests/logbook/test_push.py` (collaboration section) — remove `schema_type` dependency; assert `ai_contribution`/`human_contribution` constraint (at least one); test `milestone` field roundtrip; test `human_corrections` as list
- [ ] T022 [P] [US2] Fix `tests/logbook/fixtures/entries_collab.jsonl` — ensure no `schema_type` field in any entry line; ensure `type: "collaboration"` is present on each line
- [ ] T023 [US2] Run `uvx pytest tests/logbook/test_push.py -k collab` and confirm pass

**Checkpoint**: Collaboration entries push and validate correctly. Mixed-schema invariant holds (collaboration entries can coexist in any logbook, regardless of slug name).

---

## Phase 5: User Story 3 — Consultar la bitácora (P3)

**Goal**: User or any agent calls `/logbook-query` or `/logbook-list` directly without going through the subagent; responses are grounded in actual entries, no fabrication.

**Independent Test**: Run `logbook-list` and `logbook-query` scripts directly; verify they return only data present in `entries.jsonl`; verify empty results explicitly state no matching entries (SC-004, FR-007a).

- [ ] T024 [P] [US3] Verify `claude/plugins/logbook/skills/logbook-list/SKILL.md` is correct after T009b (already fixed in Phase 2); confirm `list.py` output matches the updated contract (no `schema_type` in JSON output)
- [ ] T025 [P] [US3] Verify `claude/plugins/logbook/skills/logbook-query/SKILL.md` — confirm it is user-invocable per FR-007a; confirm `argument-hint` matches the CLI signature (`[logbook-slug] [--since ...] [--until ...] [--type ...] [--tag ...] [--limit N]`); confirm no-results behavior is documented
- [ ] T026 [P] [US3] Fix `tests/logbook/test_list.py` — remove any `schema_type` from expected list output (per updated contract in init-list-skills.md: no `schema_type` in list JSON)
- [ ] T027 [P] [US3] Fix `tests/logbook/test_query.py` — remove any `schema_type` dependency; ensure no-results case returns explicit `{"ok": true, "entries": []}` or equivalent (not silence)
- [ ] T028 [US3] Run `uvx pytest tests/logbook/test_list.py tests/logbook/test_query.py` and confirm pass

**Checkpoint**: All three user stories independently functional. Full test suite can pass end-to-end.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Version bumps, source URL corrections, final validation against spec scenarios.

- [ ] T029 [P] Update `claude/plugins/logbook/.claude-plugin/plugin.json` — bump `version` to `0.2.0`; update CHANGELOG.md at plugin root with entry for this release
- [ ] T030 [P] Bump `version` and add CHANGELOG entry in each skill that changed: `logbook-push`, `logbook-init`, `logbook-format` (logbook-list and logbook-query only if their SKILL.md changed)
- [ ] T031 [P] Update `metadata.source` URLs in `logbook.md` and all changed SKILL.md files — replace branch-tip URLs (`tree/main/...`) with a stable commit permalink after this branch is merged (note: T037 in original plan; defer URL update to post-merge)
- [ ] T032 Run full test suite `uvx pytest tests/logbook/` and confirm zero failures
- [ ] T033 Manually validate quickstart.md Scenario 7 (false activation) — issue "Can you log this error for me and help me track what I did today?" and confirm `logbook` subagent is NOT invoked
- [ ] T034 Manually validate triggering.md test set — run 12 must-fire and 10 must-not-fire prompts against the router; pass criteria: ≥ 10/12 true positives, 0/10 false positives

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately. BLOCKS all other phases.
- **Phase 2 (Foundational)**: Depends on Phase 1 completion. BLOCKS phases 3–5.
- **Phases 3, 4, 5 (User Stories)**: All depend on Phase 2. Can proceed in any order; US1 → US2 → US3 is recommended (priority order).
- **Phase 6 (Polish)**: Depends on all story phases passing.

### Within Each Phase

- Tasks marked `[P]` within a phase have no intra-phase dependencies and can run in parallel.
- Tasks without `[P]` depend on prior tasks in the same phase completing first.
- Run script (T020, T023, T028, T032) must be last within its phase.

### Parallel Opportunities

```
Phase 1:  T001 → T002, T003 (parallel) → T004

Phase 2:  T005, T006 (parallel) → T007, T008, T009, T009b (parallel) →
          T010, T011 (parallel) → T012, T013, T014, T015 (all parallel)

Phase 3:  T016, T017, T017b, T018 (parallel) → T019 → T020

Phase 4:  T021, T022 (parallel) → T023

Phase 5:  T024, T025, T026, T027 (all parallel) → T028

Phase 6:  T029, T030, T031 (parallel) → T032 → T033, T034 (parallel)
```

---

## Implementation Strategy

### MVP Scope (deliver User Story 1 first)

1. Complete Phase 1 (relocation — required for everything)
2. Complete Phase 2 (data model + access control fixes)
3. Complete Phase 3 (US1: test-entry push flow)
4. **Validate**: `uvx pytest tests/logbook/` passing for US1 paths
5. Then proceed with US2 (Phase 4) and US3 (Phase 5)

### What is NOT in scope

- New features beyond spec (no new entry types, no network calls)
- Changes to `logbook/<slug>/` data files already written in existing logbooks
  (a separate migration tool would be needed for that — not planned)
- Automated triggering tests (triggering.md uses manual review, per the contract)

---

## Notes

- All Python scripts invoked via `uvx pytest` per project convention (see CLAUDE.md)
- `git mv plugins/logbook claude/plugins/logbook` preserves git history for T001
- Source URL commit pinning (T031) must be done post-merge — use the merge commit SHA
- `logbook-schema/` content must be read before deletion (T003) to ensure T004 captures all field definitions
