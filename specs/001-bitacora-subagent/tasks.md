# Tasks: Logbook Subagent (Subagente de Bitácora)

**Input**: Design documents from `/specs/001-bitacora-subagent/`
**Prerequisites**: plan.md ✓ spec.md ✓ research.md ✓ data-model.md ✓ contracts/ ✓ quickstart.md ✓

**Tests**: Included — plan.md specifies `pytest` for all helper scripts.

**Organization**: Tasks grouped by user story to enable independent implementation and testing. All paths are relative to repo root.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no shared state)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Setup and Foundational phases carry no story label

---

## Phase 1: Setup

**Purpose**: Create plugin skeleton, marketplace catalog, and plugin manifest. No code yet — only directories and JSON metadata files.

- [X] T001 Create all directories for the plugin: `plugins/logbook/{.claude-plugin,agents,skills/logbook-push/scripts,skills/logbook-format/scripts,skills/logbook-init/scripts,skills/logbook-list/scripts,skills/logbook-query/scripts,skills/logbook-schema/references}` and `tests/logbook/fixtures/` (use `mkdir -p`)
- [X] T002 Create `.claude-plugin/marketplace.json` at repo root per `contracts/plugin-manifest.md` §2 (fields: `name: "my-skills"`, `owner.name`, `plugins[0]` pointing to `./plugins/logbook`)
- [X] T003 Create `plugins/logbook/.claude-plugin/plugin.json` per `contracts/plugin-manifest.md` §1 (fields: `name: "logbook"`, `version: "0.1.0"`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `category: "productivity"`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared schema validation module + logbook-schema reference skill. Every script depends on `_schemas.py`; every skill that pushes entries relies on the schema content. All tests depend on fixtures.

**⚠️ CRITICAL**: Complete before any user story implementation begins.

- [X] T004 Create `plugins/logbook/skills/logbook-schema/SKILL.md` with frontmatter `name: logbook-schema`, no `model`, `user-invocable: false`, `disable-model-invocation: true`, and a `metadata:` block (author, original-author, source permalink, version: "0.1.0", last-updated, status: active, replaced-by: null, license, tags) per Constitution Principle I — content is a reference loaded by the subagent's `skills:` list
- [X] T005 Create `plugins/logbook/skills/logbook-schema/references/schemas.md` documenting all three entry schemas (`tests`, `collaboration`, `free`) and the `amendment` type: required fields, optional fields, validation rules, and example JSON for each (mirrors `data-model.md` exactly)
- [X] T006 [P] Create `plugins/logbook/skills/logbook-push/scripts/_schemas.py` — shared stdlib-only module with predicate functions `validate_tests(payload) -> (ok, errors)`, `validate_collaboration(payload) -> (ok, errors)`, `validate_free(payload) -> (ok, errors)`, `validate_amendment(payload, existing_ids) -> (ok, errors)`, plus `SENSITIVE_PATTERNS` regex list (AWS key, private key PEM, long bearer tokens adjacent to `token`/`key`/`secret` words)
- [X] T006b Create `plugins/logbook/skills/logbook-schema/CHANGELOG.md` (v0.1.0 — initial release) per Constitution Principle II
- [X] T007 [P] Create `tests/logbook/fixtures/meta_tests.json`, `tests/logbook/fixtures/meta_collab.json`, `tests/logbook/fixtures/meta_free.json` (sample `meta.json` for each schema type) and `tests/logbook/fixtures/entries_tests.jsonl`, `tests/logbook/fixtures/entries_collab.jsonl` (sample JSONL with 3 entries each, including one amendment)
- [X] T008 [P] Create `tests/logbook/conftest.py` — shared pytest fixtures: `tmp_logbook(tmp_path, schema_type)` helper that copies the right fixture files into a temp dir and returns the logbook path; `PUSH_SCRIPT`, `FORMAT_SCRIPT`, `INIT_SCRIPT`, `LIST_SCRIPT`, `QUERY_SCRIPT` path constants pointing to the plugin scripts

**Checkpoint**: `_schemas.py` importable; fixture dirs and conftest ready for all test phases.

---

## Phase 3: User Story 1 — Registrar resultado de una prueba (Priority: P1) 🎯 MVP

**Goal**: User can initialize a `tests`-type logbook, dictate test results to the `logbook` subagent in natural language, get a validated entry appended to `entries.jsonl`, and view it rendered in `rendered.md`.

**Independent Test**: `python3 .../init.py --logbook smoke --type tests` → meta.json + entries.jsonl created. Then `echo '{...}' | python3 .../push.py --logbook smoke --type tests` → one line appended, `id: 1`. Then `python3 .../format.py --logbook smoke` → `rendered.md` shows "went_well" and "went_wrong" sections. All prior lines in entries.jsonl byte-identical. `pytest tests/logbook/test_init.py tests/logbook/test_push.py tests/logbook/test_format.py` passes.

### Tests for User Story 1

- [X] T009 [P] [US1] Create `tests/logbook/test_init.py` — tests: valid slug creates `meta.json` (correct fields) + empty `entries.jsonl`; invalid slug (uppercase, spaces) exits 16; duplicate logbook exits 17; invalid `--type` exits 18; `schema_type` matches argument; `format_version: 1`
- [X] T010 [P] [US1] Create `tests/logbook/test_push.py` — tests: valid `tests` entry appended with auto `id`, `ulid`, `created_at`; schema validation rejects entry with both `went_well` and `went_wrong` empty (exit 11); type mismatch exits 12; logbook not found exits 10; sensitive content pattern triggers exit 14 but proceeds with `--acknowledge-sensitive`; pushing two entries yields `id: 1`, `id: 2` with prior line unchanged
- [X] T011 [P] [US1] Create `tests/logbook/test_format.py` — tests: all entries rendered to `rendered.md`; empty optional fields render as `*No observations*` not empty string; running format twice produces byte-identical output; corrupt JSONL line (partial JSON) skipped and counted in `error` list but script exits 0 if at least one line parsed; entries sorted newest-first within each section

### Implementation for User Story 1

- [X] T012 [US1] Create `plugins/logbook/skills/logbook-init/SKILL.md` with frontmatter per `contracts/init-list-skills.md` (`name: logbook-init`, `model: haiku`, `effort: low`, `disable-model-invocation: true`, `allowed-tools: Bash(python3 *), Read`) plus `metadata:` block (author, original-author, source permalink, version: "0.1.0", last-updated, status: active, replaced-by: null, license, tags) per Constitution Principle I; skill body instructs it to call `init.py` with `--logbook`, `--type`, optional `--title`, `--description`, `--project-root`
- [X] T013 [US1] Create `plugins/logbook/skills/logbook-init/scripts/init.py` — validates slug regex `^[a-z0-9]+(-[a-z0-9]+)*$` (exit 16 on fail); refuses if `logbook/<slug>/` already exists (exit 17); validates `--type` ∈ `{tests,collaboration,free}` (exit 18); creates `meta.json` with `slug`, `schema_type`, `title`, `description`, `created_at` (UTC ISO 8601), `format_version: 1`; creates empty `entries.jsonl`; prints JSON `{"ok":true,"logbook":"<slug>","path":"logbook/<slug>/","schema_type":"<type>"}` on stdout; exit 20 on I/O error
- [X] T014 [US1] Create `plugins/logbook/skills/logbook-init/CHANGELOG.md` (v0.1.0 — initial release)
- [X] T015 [US1] Create `plugins/logbook/skills/logbook-push/SKILL.md` with frontmatter per `contracts/push-skill.md` (`name: logbook-push`, `model: haiku`, `effort: low`, `disable-model-invocation: true`, `allowed-tools: Bash(python3 *), Read`) plus `metadata:` block (author, original-author, source permalink, version: "0.1.0", last-updated, status: active, replaced-by: null, license, tags) per Constitution Principle I; body explains stdin-JSON invocation, `--logbook`, `--type`, `--acknowledge-sensitive`, `--project-root` flags
- [X] T016 [US1] Create `plugins/logbook/skills/logbook-push/scripts/push.py` — reads `meta.json` (exit 10 if missing); reads stdin as JSON payload; imports `_schemas.py` and calls the matching validator (exit 11 on schema error, exit 12 on type mismatch); scans for sensitive content via `SENSITIVE_PATTERNS` (exit 14 unless `--acknowledge-sensitive` passed); reads last line of `entries.jsonl` to compute next `id`; generates `ulid` using `time`+`uuid.uuid4`; adds `id`, `ulid`, `created_at` to payload; appends single JSON line; prints `{"ok":true,"id":N,"ulid":"...","logbook":"<slug>","path":"..."}` to stdout; exit 20 on I/O error, 99 on unexpected exception
- [X] T017 [US1] Create `plugins/logbook/skills/logbook-push/CHANGELOG.md` (v0.1.0 — initial release)
- [X] T018 [US1] Create `plugins/logbook/skills/logbook-format/SKILL.md` with frontmatter per `contracts/format-skill.md` (`name: logbook-format`, `model: haiku`, `effort: low`, `disable-model-invocation: true`, `allowed-tools: Bash(python3 *), Read`) plus `metadata:` block (author, original-author, source permalink, version: "0.1.0", last-updated, status: active, replaced-by: null, license, tags) per Constitution Principle I; body explains `--logbook`, `--project-root`, `--output` flags and idempotency guarantee
- [X] T019 [US1] Create `plugins/logbook/skills/logbook-format/scripts/format.py` — reads `meta.json` and all lines of `entries.jsonl`; skips and records corrupt lines (exit non-zero only if zero entries parsed, else exit 0 with `warnings`); groups entries by type within the logbook's `schema_type`; sorts newest-first per group; renders each entry as `### [#<id>] <title> — <date>`; renders amendment entries with a `> Amended by #N on <date>: <reason>` callout under the original entry header; writes `rendered.md`; prints `{"ok":true,"entries_rendered":N,"output":"..."}` to stdout; idempotent (same JSONL → same bytes in rendered.md)
- [X] T020 [US1] Create `plugins/logbook/skills/logbook-format/CHANGELOG.md` (v0.1.0 — initial release)
- [X] T021 [US1] Create `plugins/logbook/agents/logbook.md` — thin orchestrator subagent per `contracts/subagent-frontmatter.md`: YAML frontmatter with `name: logbook`, `description` (negative constraint first, trigger phrases `logbook`/`bitácora`/`bitacora`, explicit NOT-DO list), `model: sonnet`, `color: cyan`, `memory: project`, `background: true`, `effort: low`, `permissionMode: default`, `tools: Bash, Read, Skill, SlashCommand`, `skills: [logbook-schema, logbook-push, logbook-format, logbook-init, logbook-list, logbook-query]`; body implements all 8 system prompt responsibilities from the contract (identify target logbook, validate schema, preserve input language, never fabricate, sensitive-content gate, delegate to skills, amendment handling, report back id+path)
- [X] T021b [US1] Update `AGENTS.md` at repo root — add `logbook` entry under `## Subagents` section: one-paragraph description, trigger phrases (`logbook`, `bitácora`, `bitacora`), location (`plugins/logbook/agents/logbook.md`), install command (`/plugin install logbook@my-skills`). Required by Constitution Principle IV in the same change as adding the subagent.

**Checkpoint**: `pytest tests/logbook/test_init.py tests/logbook/test_push.py tests/logbook/test_format.py` all pass. Run quickstart.md Scenario 1 manually to confirm end-to-end.

---

## Phase 4: User Story 2 — Registrar proceso de co-creación con IA (Priority: P2)

**Goal**: User can initialize a `collaboration`-type logbook, dictate an AI/human session, get a structured entry with `ai_contribution`, `human_contribution`, `human_corrections`, and `milestone` fields. Amendments can correct any prior entry (tests or collaboration).

**Independent Test**: Push a `collaboration` entry via push.py and verify `ai_contribution`, `human_contribution`, `human_corrections`, `milestone` are stored. Push an `amendment` entry with valid `amends.{id,ulid}` and verify the format.py output shows backlink under original entry. Push an amendment with invalid `amends.id` and verify exit 13. `pytest tests/logbook/test_amendment.py tests/logbook/test_list.py` passes.

### Tests for User Story 2

- [X] T022 [P] [US2] Create `tests/logbook/test_amendment.py` — tests: valid amendment (matching `amends.id` and `amends.ulid`) appended successfully; amendment with non-existent `amends.id` exits 13; amendment with mismatched `amends.ulid` exits 13; format.py renders amendment backlink `> Amended by #N` under the original entry header; original entry line bytes unchanged after amendment push
- [X] T023 [P] [US2] Create `tests/logbook/test_list.py` — tests: empty `logbook/` dir returns `{"ok":true,"logbooks":[]}`; two logbooks listed with correct `slug`, `schema_type`, `entries` count, `last_entry_at`; non-logbook directories under `logbook/` (missing `meta.json`) are silently skipped; I/O error exits 20

### Implementation for User Story 2

- [X] T024 [US2] Create `plugins/logbook/skills/logbook-list/SKILL.md` with frontmatter per `contracts/init-list-skills.md` (`name: logbook-list`, `model: haiku`, `effort: low`, `disable-model-invocation: true`, `allowed-tools: Bash(python3 *), Read`) plus `metadata:` block (author, original-author, source permalink, version: "0.1.0", last-updated, status: active, replaced-by: null, license, tags) per Constitution Principle I; body explains `--project-root` flag and JSON output format
- [X] T025 [US2] Create `plugins/logbook/skills/logbook-list/scripts/list.py` — scans `logbook/` for subdirectories containing `meta.json`; for each: reads `slug`, `schema_type`, `created_at` from `meta.json`; counts non-empty lines in `entries.jsonl`; reads last line's `created_at` as `last_entry_at`; returns `{"ok":true,"logbooks":[...]}` sorted by `last_entry_at` descending; exits 20 on I/O error
- [X] T026 [US2] Create `plugins/logbook/skills/logbook-list/CHANGELOG.md` (v0.1.0 — initial release)

**Checkpoint**: `pytest tests/logbook/test_amendment.py tests/logbook/test_list.py` passes. Run quickstart.md Scenario 2 and Scenario 3 manually.

---

## Phase 5: User Story 3 — Consultar la bitácora (Priority: P3)

**Goal**: User can ask the `logbook` subagent to query entries by date, tag, or type. The skill returns only facts present in `entries.jsonl`, cited by entry `id`. Zero fabrication.

**Independent Test**: Create logbook with 5 entries (mixed dates and tags). Run `query.py --logbook <slug> --since <date>` → returns only entries after that date. Run with `--type tests` → only tests entries. Run with `--tag auth` → only tagged entries. Run with filters that match nothing → `{"ok":true,"count":0,"entries":[]}`. `pytest tests/logbook/test_query.py` passes.

### Tests for User Story 3

- [X] T027 [P] [US3] Create `tests/logbook/test_query.py` — tests: `--since` returns only entries with `created_at ≥ since`; `--until` upper-bound filter; `--type` filters by entry type; `--tag` filters by tag; `--limit N` returns at most N entries; zero-match returns `count:0, entries:[]` (not an error); corrupt line skipped with `warnings` list, exit 0 if others parse; logbook not found exits 10; results ordered newest-first

### Implementation for User Story 3

- [X] T028 [US3] Create `plugins/logbook/skills/logbook-query/SKILL.md` with frontmatter per `contracts/query-skill.md` (`name: logbook-query`, `model: sonnet`, `effort: medium`, `disable-model-invocation: true`, `allowed-tools: Bash(python3 *), Read`) plus `metadata:` block (author, original-author, source permalink, version: "0.1.0", last-updated, status: active, replaced-by: null, license, tags) per Constitution Principle I; skill body: parse user's natural-language query → `--since`/`--until`/`--type`/`--tag`/`--limit` flags → call `query.py` via Bash → if `count:0` respond "No entries match this query in `<slug>`" → otherwise summarize citing entry IDs, preserving input language, never introducing absent claims
- [X] T029 [US3] Create `plugins/logbook/skills/logbook-query/scripts/query.py` — reads all lines of `entries.jsonl` (skips+records corrupt lines); applies `--since` (ISO date, inclusive), `--until` (ISO date, inclusive), `--type`, `--tag` (substring match in `tags[]`), `--limit N` (newest-first cap) filters; prints `{"ok":true,"logbook":"<slug>","count":N,"entries":[...]}` newest-first; if corrupt lines present adds `"warnings":["line N: <error>"]`; exits 10 if logbook not found, 15 only if zero entries could be parsed (else exit 0), 20 on I/O error
- [X] T030 [US3] Create `plugins/logbook/skills/logbook-query/CHANGELOG.md` (v0.1.0 — initial release)

**Checkpoint**: `pytest tests/logbook/` — all 6 test files pass. Run quickstart.md Scenario 4 manually.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, repo integration, and validation of trigger behavior and quickstart scenarios.

- [X] T032 [P] Create `plugins/logbook/README.md` — sections: Overview, Install (two-command: `/plugin marketplace add` + `/plugin install logbook@my-skills`), Verify (three slash-command checks from quickstart.md), Usage (one paragraph per skill), Plugin layout diagram
- [X] T033 Create `plugins/logbook/CHANGELOG.md` — plugin-level CHANGELOG, v0.1.0 initial release listing all bundled components (subagent + 6 skills)
- [X] T034 Create `plugins/logbook/LICENSE` — single line referencing repo root LICENSE file
- [X] T035 Run quickstart.md Scenario 5 (false activation check): in a fresh context, verify the logbook subagent description does NOT trigger on the 10 negative prompts in `contracts/triggering.md`; document pass/fail for each case
- [X] T036 [P] Run full `pytest tests/logbook/` and verify all tests pass; fix any regressions before marking this phase complete

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (directories must exist) — **BLOCKS all user stories**
- **US1 (Phase 3)**: Depends on Phase 2 (`_schemas.py` and fixtures must exist)
- **US2 (Phase 4)**: Depends on Phase 3 (amendment tests require `push.py` to be complete)
- **US3 (Phase 5)**: Depends on Phase 2; does NOT depend on US2 — can start as soon as Phase 2 is done
- **Polish (Phase 6)**: Depends on all user story phases

### User Story Dependencies

- **US1 (P1)**: After Phase 2. No cross-story dependencies.
- **US2 (P2)**: After US1 — amendment tests call `push.py` (already built in US1); `list.py` is independent but logically grouped here because US2 introduces a second logbook type.
- **US3 (P3)**: After Phase 2. `query.py` only reads JSONL — no dependency on `push.py` internals beyond the fixture entries.

### Within Each User Story

- Write tests **before** implementation (TDD: tests must fail first)
- Tests and fixtures marked [P] can be written in parallel
- `SKILL.md` → `scripts/*.py` → `CHANGELOG.md` for each skill (SKILL.md first so scripts can reference it during review)
- `logbook.md` subagent last in US1 (needs all skill names confirmed); AGENTS.md update (T021b) immediately after subagent creation per Constitution IV

### Parallel Opportunities

Within Phase 2: T004–T008 all target different files — run in parallel.
Within Phase 3 tests: T009, T010, T011 target different test files — run in parallel.
Within Phase 3 implementation: T012+T015+T018 (SKILL.md files) can be written in parallel; T013 (init.py) and T016 (push.py) can be written in parallel (different files, T016 imports `_schemas.py` which is already complete).
Within Phase 4 tests: T022, T023 target different test files — run in parallel.
Within Phase 6: T031, T032, T035, T036 target different files — run in parallel.

---

## Parallel Example: Phase 3 (US1) Tests

```
# Write all US1 tests simultaneously (different files, same fixtures):
Task: "Create tests/logbook/test_init.py"     # T009
Task: "Create tests/logbook/test_push.py"     # T010
Task: "Create tests/logbook/test_format.py"   # T011

# Then implement all SKILL.md files simultaneously:
Task: "Create plugins/logbook/skills/logbook-init/SKILL.md"    # T012
Task: "Create plugins/logbook/skills/logbook-push/SKILL.md"    # T015
Task: "Create plugins/logbook/skills/logbook-format/SKILL.md"  # T018
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T003)
2. Complete Phase 2: Foundational (T004–T008) — CRITICAL
3. Complete Phase 3: User Story 1 (T009–T021)
4. **STOP and VALIDATE**: `pytest tests/logbook/test_init.py test_push.py test_format.py` + quickstart Scenario 1
5. Plugin is functional for the primary use case — ship if needed

### Incremental Delivery

1. Setup + Foundational → skeleton ready
2. **US1** → tests logbook end-to-end → MVP (record test outcomes)
3. **US2** → adds collaboration schema + amendment + list → richer authoring
4. **US3** → adds query → full read/write workflow
5. Polish → docs + trigger validation → production-ready

### Total Task Count

| Phase | Tasks | Parallel opportunities |
|---|---|---|
| Phase 1: Setup | 3 | T002, T003 (different files) |
| Phase 2: Foundational | 6 | T006, T006b, T007, T008 |
| Phase 3: US1 | 15 | T009–T011, T012/T015/T018, T021b |
| Phase 4: US2 | 5 | T022, T023 |
| Phase 5: US3 | 4 | T027 (test) with T028 (SKILL.md) |
| Phase 6: Polish | 5 | T032, T033, T034, T035, T036 |
| **Total** | **38** | |

---

## Notes

- `[P]` = different files, no shared state — safe to run in parallel
- `[Story]` label maps every task to its user story for traceability
- Each phase ends with an explicit **Checkpoint** — verify before advancing
- All scripts: `#!/usr/bin/env python3`, stdlib only, no `uv`/`venv`
- Data paths in scripts use `$CLAUDE_PROJECT_DIR` (or `--project-root` arg); script paths use `$CLAUDE_PLUGIN_ROOT`
- Entry `ulid` generation: combine `time.time_ns()` (48-bit timestamp) + `uuid.uuid4().bytes` (80-bit random) → encode as Crockford base-32 (26 chars). Or use a stdlib-compatible inline implementation — no third-party `python-ulid` package.
- Sensitive content regex patterns (from research R8): `AKIA[0-9A-Z]{16}`, `-----BEGIN .* PRIVATE KEY-----`, `[A-Za-z0-9_-]{40,}` adjacent to `token|key|secret` (case-insensitive), email addresses
