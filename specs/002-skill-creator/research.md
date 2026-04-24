# Research: skill-creator

**Feature**: skill-creator  
**Date**: 2026-04-23  
**Sources**: OpenCode skills docs, Claude skill-creator SKILL.md, Gemini skill-creator SKILL.md, project constitution, AGENTS.md

---

## Unknowns Resolved

### 1. OpenCode Skill Standard vs Constitution Metadata Requirements

**Decision**: Place all Constitution-required provenance keys inside OpenCode's `metadata` frontmatter field as strings.

**Rationale**: OpenCode defines `metadata` as an optional string-to-string map. The Constitution requires `author`, `original-author`, `source`, `version`, `last-updated`, `status`, and `replaced-by`. These are all representable as strings, so placing them in `metadata` satisfies both standards without conflict.

**Alternatives considered**:
- Custom frontmatter fields (rejected: OpenCode ignores unknown fields, making them invisible to agents)
- Separate `provenance.yml` file (rejected: adds indirection; Constitution expects metadata in definition file)

### 2. Path Selection for New Skills

**Decision**: The skill-creator MUST ask the user for an output path every time. No default path is assumed.

**Rationale**: User clarified explicitly that the skill-creator always asks the user where to save the skill and never assumes a default path. This prevents accidental overwrites and supports both project-local and global installations, as well as arbitrary paths for testing or redistribution.

### 3. Evaluation Infrastructure

**Decision**: No automated evaluation harness. Use manual test prompts + validation script + quality checklist.

**Rationale**: OpenCode does not provide subagents or benchmark runners like Claude Code does. The Gemini CLI has `package_skill.cjs` which validates but does not benchmark. The correct adaptation is to:
1. Provide 2-3 realistic test prompts in SKILL.md
2. Bundle `validate_skill.cjs` for structural/content validation
3. Present a manual quality checklist at the end of creation

**Alternatives considered**:
- Spawn OpenCode subagents for A/B testing (rejected: OpenCode does not support subagents)
- Build a custom benchmark runner (rejected: over-engineered for scope; manual review is sufficient for a solo-maintainer project)

### 4. Speckit Integration Strategy

**Decision**: Hybrid adaptive — detect `.specify/` and use speckit flow; otherwise generate files directly.

**Rationale**: The project uses speckit, but users may want to create skills in other projects or standalone. The skill-creator must:
- Detect `.specify/` presence (FR-004)
- If present: generate a draft feature description for `/speckit.specify` and instruct the user to paste it; then assist in generating SKILL.md, scripts, references during `/speckit.implement`
- If absent: generate files directly using write/edit tools

### 5. js-yaml Dependency Management

**Decision**: Treat js-yaml as a peer dependency. Both scripts check for it at runtime and emit clear install instructions if missing.

**Rationale**: The project has no `package.json`. Adding one just for js-yaml would be overkill. Node.js 18+ includes sufficient APIs; only js-yaml is needed for robust YAML parsing. The scripts will use a try/catch block to detect missing js-yaml and exit with a clear error message.

### 6. Upstream Attribution for Adapted Work

**Decision**: Create `references/upstream-attribution.md` referencing both Claude and Gemini skill-creator sources, and include `original-author` and `source` in metadata.

**Rationale**: Constitution Principle IV requires license/upstream attribution when adapting external sources. The Claude skill-creator is from Anthropic's marketplace; the Gemini skill-creator is bundled with Gemini CLI. Both are third-party work. We must note that the skill is inspired by these sources, preserve any license-required notices, and use permalinks in the `source` metadata field.

### 7. AGENTS.md Reduction Strategy

**Decision**: Migrate the Skills section (lines 9-157, ~148 lines) from AGENTS.md into:
- `references/skill-standards.md` (frontmatter rules, naming, lengths, directory layout)
- `references/skill-patterns.md` (progressive disclosure, domain organization, file references)

AGENTS.md will be reduced to a brief paragraph + link to the skill-creator.

**Rationale**: SC-001 requires reducing AGENTS.md by at least 100 lines. The Skills section is ~148 lines. Moving it to reference files loaded on-demand reduces startup context while preserving discoverability.

---

## Technology Choices

| Technology | Role | Rationale |
|------------|------|-----------|
| Node.js 18+ | Script runtime | Already assumed by spec; cross-platform; no compilation step |
| js-yaml | YAML parsing | Robust parsing of frontmatter with error messages; handles quoted strings, multiline, and metadata maps correctly. Regex alternative rejected due to fragility with edge cases. |
| CommonJS (.cjs) | Module format | Avoids ESM/CJS friction in Node.js scripts; explicit and compatible |
| Markdown | Documentation | Native format for skills; no transformation needed |

---

## Integration Patterns

### Pattern: Progressive Disclosure in SKILL.md Body

Inspired by Gemini skill-creator. The SKILL.md body will:
1. Start with a brief summary (~100 words)
2. Load detailed standards from `references/skill-standards.md` only when needed
3. Load patterns from `references/skill-patterns.md` only when needed
4. Keep the body under 500 lines

### Pattern: Speckit Hybrid Flow

The skill-creator will:
1. Capture intent (name, description, resources)
2. Ask up to 3 clarifying questions if needed
3. Generate draft feature description
4. If `.specify/` exists: present draft for `/speckit.specify` and guide through speckit workflow
5. If `.specify/` absent: run init_skill.cjs with user-provided path, then edit generated files
6. Run validate_skill.cjs
7. Present checklist + test prompts

### Pattern: Validation Script Design

The validate script checks:
1. Directory exists and contains SKILL.md
2. SKILL.md has YAML frontmatter between --- delimiters
3. Frontmatter parseable by js-yaml
4. name: present, matches regex, 1-64 chars, matches directory name
5. description: present, 1-1024 chars, single-line
6. license: if present, non-empty string
7. compatibility: if present, 1-500 chars
8. metadata: if present, string-to-string map
9. No TODO markers in any file under the skill directory (warning)
10. No auxiliary docs inside subdirectories

Exit codes: 0 for valid (warnings allowed), 1 for errors.

### Pattern: Init Script Design

The init script:
1. Validates skill-name against regex
2. Ensures output-dir/skill-name does not exist
3. Creates directory structure with SKILL.md, CHANGELOG.md, and example subdirs
4. Generates SKILL.md from template with TODO placeholders
