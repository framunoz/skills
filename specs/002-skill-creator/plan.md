# Implementation Plan: skill-creator

**Branch**: `002-skill-creator` | **Date**: 2026-04-23 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `/specs/002-skill-creator/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Create an OpenCode skill that guides users through authoring, validating, and improving other OpenCode skills. The skill follows a conversational workflow: capture intent → ask clarifying questions → generate a draft feature description for `/speckit.specify` → scaffold files via `init_skill.cjs` → validate via `validate_skill.cjs` → present a quality checklist and test prompts.

The skill reduces AGENTS.md bloat by migrating the detailed "Skills" section into self-contained reference files loaded on-demand. It is inspired by Claude and Gemini skill-creators but adapted to OpenCode's native `skill` tool, progressive disclosure model, and lack of subagent/evaluation infrastructure.

## Technical Context

**Language/Version**: Node.js 18+  
**Primary Dependencies**: `js-yaml` (peer dependency; scripts check for it and report install instructions if missing)  
**Storage**: N/A (filesystem only)  
**Testing**: Manual — test prompts + `validate_skill.cjs` + quality checklist (no automated test harness)  
**Target Platform**: OpenCode CLI (cross-platform via Node.js; macOS, Linux, Windows)  
**Project Type**: AI agent skill / CLI tooling  
**Performance Goals**: N/A (not performance-critical)  
**Constraints**: 
- Must work offline after Node.js + js-yaml are installed
- Scripts MUST exit with non-zero code on error (Constitution Additional Constraints)
- All content MUST be English-only (Constitution Principle V additional rule)
- Skill path is always user-provided; no default assumed
- Must integrate with speckit when `.specify/` exists; standalone when it does not

**Scale/Scope**: Single repository, project-local installation; intended for solo maintainer and occasional contributors

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Check | Status | Notes |
|-----------|-------|--------|-------|
| I. Provenance & Traceability | Metadata includes author, original-author, source permalink, version, last-updated, status | ✅ Compliant | Will embed in `metadata` frontmatter; adapted from Claude & Gemini skill-creators, so upstream attribution required |
| II. Semantic Versioning | `CHANGELOG.md` present; version bumped on every change | ✅ Compliant | Will include `CHANGELOG.md` in skill directory |
| III. Shareability & Portability | Self-contained, no personal paths, declared dependencies | ✅ Compliant | Scripts declare js-yaml dependency; no hard-coded credentials or paths |
| IV. License & Upstream Attribution | Upstream LICENSE preserved or referenced; original-author/source populated | ⚠️ NEEDS ACTION | Must preserve/reference Claude and Gemini upstream licenses; add `references/UPSTREAM_ATTRIBUTION.md` |
| V. Trigger Testability | Description is specific; Test Questions section present | ✅ Compliant | Will include 3+ test questions in SKILL.md |
| Additional: English-only | All content in English | ✅ Compliant | All skill content will be authored in English |
| Additional: Directory structure | Canonical top-level folder per AGENTS.md | ✅ Compliant | AGENTS.md defines `.opencode/skills/<name>/` as canonical OpenCode project-local path; constitution says "as defined in AGENTS.md" |
| Additional: Script testability | Scripts declare dependencies, exit non-zero on error, have dry-run or example invocation | ✅ Compliant | `validate_skill.cjs` supports `--dry-run`; `init_skill.cjs` prints usage on error |

**Post-design re-check required**: Yes — after SKILL.md body and references are drafted.

## Project Structure

### Documentation (this feature)

```text
specs/002-skill-creator/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
.opencode/skills/skill-creator/
├── SKILL.md                              # Skill definition (frontmatter + instructions)
├── CHANGELOG.md                          # Semver changelog per constitution
├── scripts/
│   ├── init_skill.cjs                    # Scaffold new skill directory + SKILL.md template
│   └── validate_skill.cjs                # Validate existing skill structure + content
├── references/
│   ├── skill-standards.md                # OpenCode skill spec: frontmatter rules, naming, layout
│   ├── skill-patterns.md                 # Progressive disclosure, domain org, conditional details
│   └── upstream-attribution.md           # License references for Claude & Gemini skill-creator sources
└── assets/
    └── skill-template.md                 # Template injected by init_skill.cjs into new SKILL.md
```

**Structure Decision**: Single skill directory under `.opencode/skills/skill-creator/`. OpenCode discovers project-local skills from `.opencode/skills/*/SKILL.md`. The skill is self-contained: all scripts, references, and assets live inside the directory. No separate `src/` or `tests/` directories — validation is performed by the bundled `validate_skill.cjs` script.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| No package.json / no dependency manager | The skill is a documentation + script bundle, not a Node project. js-yaml is a peer dependency checked at runtime. | Adding a package.json would create an unnecessary build artifact and complicate installation for a simple script bundle. |
| Dual metadata schemas (OpenCode string-to-string map vs Constitution rich provenance) | OpenCode `metadata` is defined as string-to-string; Constitution requires specific provenance keys. | Both schemas are satisfied by placing all keys in `metadata` as strings, which is valid per OpenCode spec and sufficient for Constitution audit. |

---

## Research Findings

See [research.md](research.md) for Phase 0 output.

## Design Artifacts

See [data-model.md](data-model.md), [quickstart.md](quickstart.md), and [contracts/](contracts/) for Phase 1 output.
