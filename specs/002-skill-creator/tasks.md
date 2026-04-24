# Tasks: skill-creator

**Input**: Design documents from `/specs/002-skill-creator/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT included — the feature specification does not explicitly request automated tests. Manual verification tasks are included as implementation tasks where appropriate.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Environment & Directory Structure)

**Purpose**: Verify runtime dependencies and create the skill-creator directory structure

- [x] T001 Verify Node.js 18+ is installed and install js-yaml if missing (`npm install js-yaml`)
- [x] T002 Create `.opencode/skills/skill-creator/` directory structure with `scripts/`, `references/`, and `assets/` subdirectories

---

## Phase 2: Foundational (Reference Docs, Template, and Core Scripts)

**Purpose**: Core artifacts that MUST be complete before ANY user story can be fully implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 [P] Create `.opencode/skills/skill-creator/references/upstream-attribution.md` with Claude and Gemini skill-creator attribution per Constitution Principle IV
- [ ] T004 [P] Create `.opencode/skills/skill-creator/references/skill-standards.md` with frontmatter rules, naming conventions, length limits, and directory layout per OpenCode spec and AGENTS.md
- [ ] T005 [P] Create `.opencode/skills/skill-creator/references/skill-patterns.md` with progressive disclosure, domain organization, conditional details, and output patterns
- [ ] T006 [P] Create `.opencode/skills/skill-creator/assets/skill-template.md` with frontmatter placeholders, TODO markers, and boilerplate sections for new skills
- [ ] T007 Create `.opencode/skills/skill-creator/CHANGELOG.md` with initial version `0.1.0` entry per Constitution Principle II
- [ ] T008 [P] Implement `.opencode/skills/skill-creator/scripts/init_skill.cjs` with skill-name regex validation, directory scaffolding, `SKILL.md` template injection, and `CHANGELOG.md` stub generation
- [ ] T009 [P] Implement `.opencode/skills/skill-creator/scripts/validate_skill.cjs` with frontmatter parsing (js-yaml), field validation (name, description, license, compatibility, metadata), recursive TODO scanning, and structured report output

**Checkpoint**: Foundation ready — reference docs, template, changelog, init script, and validate script are all in place. User story implementation can now begin.

---

## Phase 3: User Story 1 - Crear una skill nueva desde cero (Priority: P1) 🎯 MVP

**Goal**: A user can say "I want to create a skill for X" and the skill-creator guides them from intent capture through clarifying questions, draft generation, file scaffolding, and validation to a quality-checked skill.

**Independent Test**: Tell OpenCode: "I want to create a skill for generating changelogs." Verify that the skill-creator infers a name, asks at most 3 clarifying questions if needed, generates a draft feature description, scaffolds files in a user-provided path, and the resulting skill passes `validate_skill.cjs` with exit code 0.

### Implementation for User Story 1

- [ ] T010 [US1] Create `.opencode/skills/skill-creator/SKILL.md` frontmatter with `name: skill-creator`, description, license, compatibility, and Constitution-required metadata (author, original-author, source, version, last-updated, status, replaced-by)
- [ ] T011 [US1] Add Context & Goal and Step-by-Step Procedure for creation workflow to `.opencode/skills/skill-creator/SKILL.md` (intent capture → clarifying questions → draft generation → path selection → file scaffolding)
- [ ] T012 [US1] Add speckit integration instructions to `.opencode/skills/skill-creator/SKILL.md` (detect `.specify/`, generate draft for `/speckit.specify`, hybrid adaptive flow when speckit is absent)
- [ ] T013 [US1] Add Usage of Resources, Constraints & Rules, and Expected Output sections to `.opencode/skills/skill-creator/SKILL.md`
- [ ] T014 [US1] Add quality checklist and 2-3 test prompts with expected results to `.opencode/skills/skill-creator/SKILL.md`
- [ ] T015 [US1] Run `.opencode/skills/skill-creator/scripts/validate_skill.cjs` on the skill-creator directory itself and fix any reported errors or warnings

**Checkpoint**: At this point, User Story 1 should be fully functional. A user can create a new skill from scratch using the skill-creator.

---

## Phase 4: User Story 2 - Editar o mejorar una skill existente (Priority: P2)

**Goal**: A user can improve an existing skill by having the skill-creator read it, present a gap diagnosis, propose changes, apply them with confirmation, and re-validate.

**Independent Test**: Tell OpenCode: "I want to improve the skill efectivo-functions." Verify that the skill-creator reads the existing `.opencode/skills/efectivo-functions/SKILL.md`, presents relevant gaps (e.g., missing metadata, unclear description, no scripts), proposes specific changes, and after application the skill passes validation.

### Implementation for User Story 2

- [ ] T016 [US2] Add edit/improve workflow section to `.opencode/skills/skill-creator/SKILL.md` (read existing SKILL.md → present diagnosis → user confirms scope of changes)
- [ ] T017 [US2] Add gap analysis and guided change application instructions to `.opencode/skills/skill-creator/SKILL.md` (identify missing metadata, weak description, absent scripts/references/assets, progressive disclosure gaps)
- [ ] T018 [US2] Test edit workflow by invoking skill-creator with "improve [an-existing-skill-name]" and verify the proposed changes are relevant and the updated skill passes validation

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. A user can create a new skill or improve an existing one.

---

## Phase 5: User Story 3 - Validar una skill creada manualmente (Priority: P3)

**Goal**: A user who created skill files by hand can run `validate_skill.cjs` and receive a clear report: valid (exit 0), valid with warnings (exit 0), or invalid (exit 1 with specific errors).

**Independent Test**: Create a temporary directory with a hand-written `SKILL.md` and run `node .opencode/skills/skill-creator/scripts/validate_skill.cjs <path>`. Verify it reports `valid` for correct skills, lists specific field errors for invalid frontmatter, and reports TODO warnings with file paths and line numbers.

### Implementation for User Story 3

- [ ] T019 [US3] Verify `.opencode/skills/skill-creator/scripts/validate_skill.cjs` reports `valid` with exit code 0 for a correctly structured manually created skill
- [ ] T020 [US3] Verify `.opencode/skills/skill-creator/scripts/validate_skill.cjs` reports specific field errors (e.g., invalid name regex, multiline description, missing required fields) with exit code 1 for invalid frontmatter
- [ ] T021 [US3] Verify `.opencode/skills/skill-creator/scripts/validate_skill.cjs` reports TODO warnings with exact file paths and line numbers, and that `--strict` mode promotes warnings to errors

**Checkpoint**: All user stories should now be independently functional. The validate script works correctly for skills created manually, by init_skill.cjs, or edited via the skill-creator.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Reduce AGENTS.md bloat, verify success criteria, and ensure consistency across all deliverables

- [ ] T022 [P] Reduce the "Skills" section in `AGENTS.md` to a brief paragraph with a reference to the skill-creator, migrating detailed rules to `.opencode/skills/skill-creator/references/skill-standards.md`
- [ ] T023 Count lines in `AGENTS.md` before and after reduction to verify SC-001 (reduction of at least 100 lines)
- [ ] T024 Update `specs/002-skill-creator/quickstart.md` if any implementation details diverged from the original plan
- [ ] T025 Run `.opencode/skills/skill-creator/scripts/validate_skill.cjs --strict` on the skill-creator directory and fix any remaining warnings or errors

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
  - Reference docs (T003–T005), template (T006), changelog (T007), init script (T008), and validate script (T009) can be developed in parallel where marked [P]
- **User Stories (Phase 3–5)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3)
  - US1 (P1) is the MVP and should be completed first
  - US2 (P2) and US3 (P3) can start in parallel after US1 if team capacity allows
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2). No dependencies on other stories. This is the MVP.
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) and ideally after US1 is complete (shares SKILL.md file). US2 adds edit workflow instructions to the same SKILL.md created in US1.
- **User Story 3 (P3)**: Can start after Foundational (Phase 2). US3 verifies the validate script created in Phase 2 against manual skills. No code dependency on US1 or US2.

### Within Each User Story

- US1: Frontmatter (T010) → Creation workflow body (T011–T014) → Self-validation (T015)
- US2: Edit workflow section (T016) → Gap analysis section (T017) → Live test (T018)
- US3: Valid skill test (T019) → Invalid skill test (T020) → TODO warning test (T021)

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T001–T002)
- All Foundational tasks marked [P] can run in parallel (T003–T006, T008–T009)
- T007 (CHANGELOG.md) is sequential but quick
- Once Foundational phase completes:
  - US1, US2, and US3 can theoretically start in parallel (if different team members work on them)
  - However, US2 edits the same SKILL.md created in US1, so sequential ordering (US1 → US2) is recommended for a single developer
  - US3 is fully independent and can run in parallel with US1 and US2

---

## Parallel Example: User Story 1

```bash
# Create SKILL.md frontmatter and body sections in parallel (different parts of same file, but sequential editing recommended):
Task: "Create .opencode/skills/skill-creator/SKILL.md frontmatter with Constitution-required metadata"
Task: "Add Context & Goal and Step-by-Step Procedure for creation workflow to SKILL.md"
Task: "Add speckit integration instructions to SKILL.md"
Task: "Add Usage of Resources, Constraints & Rules, and Expected Output sections to SKILL.md"
Task: "Add quality checklist and 2-3 test prompts to SKILL.md"

# After SKILL.md is complete:
Task: "Run validate_skill.cjs on skill-creator directory and fix any reported issues"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (verify Node.js, install js-yaml, create directory structure)
2. Complete Phase 2: Foundational (reference docs, template, changelog, init script, validate script)
3. Complete Phase 3: User Story 1 (SKILL.md with creation workflow, self-validation)
4. **STOP and VALIDATE**: Test User Story 1 independently by creating a sample skill
5. The skill-creator is now usable for its primary use case

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test by creating a skill → Validate → MVP complete
3. Add User Story 2 → Test by improving an existing skill → Validate
4. Add User Story 3 → Test validate script against manual skills → Validate
5. Complete Polish phase → Reduce AGENTS.md → Verify SC-001 → Final validation
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (SKILL.md creation workflow)
   - Developer B: User Story 2 (edit workflow additions to SKILL.md — coordinate with A on file merges)
   - Developer C: User Story 3 (validate script verification against manual skills)
3. Stories complete and integrate independently
4. Team converges on Polish phase together

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate the story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- The skill-creator is project-local; all paths are relative to repository root unless noted
