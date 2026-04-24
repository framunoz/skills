# Data Model: skill-creator

**Feature**: skill-creator  
**Date**: 2026-04-23

---

## Entity: Skill

A modular, self-contained package that extends OpenCode with specialized knowledge, workflows, or tools.

| Field | Type | Constraints | Source |
|-------|------|-------------|--------|
| name | string | Required. 1-64 chars. Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`. Must match directory name. | OpenCode spec + Constitution |
| description | string | Required. 1-1024 chars. Single-line. Must state what the skill does AND when to use it. | OpenCode spec + Constitution |
| license | string | Optional. Non-empty if present. | OpenCode spec |
| compatibility | string | Optional. 1-500 chars if present. | OpenCode spec |
| metadata | map<string,string> | Optional. String-to-string keys only. | OpenCode spec |
| metadata.author | string | Required by Constitution. Current maintainer handle. | Constitution Principle I |
| metadata.original-author | string | Required by Constitution. Equals author for original work; upstream creator for adapted work. | Constitution Principle I |
| metadata.source | string | Required by Constitution. Permalink (commit-pinned URL) to canonical upstream. | Constitution Principle I |
| metadata.version | string | Required by Constitution. Semver string. | Constitution Principle II |
| metadata.last-updated | string | Required by Constitution. ISO date `YYYY-MM-DD`. | Constitution Principle I |
| metadata.status | string | Required by Constitution. One of: `active`, `deprecated`, `archived`. | Constitution Principle I |
| metadata.replaced-by | string | Required when status is `deprecated` or `archived`. Successor tool name or `null`. | Constitution Principle I |
| body | markdown | Required. Instructions for the agent. Must include: Context & Goal, Step-by-Step Procedure, Usage of Resources, Constraints & Rules, Expected Output. | AGENTS.md + OpenCode spec |
| scripts | directory | Optional. Executable code. Must be testable, declare dependencies, exit non-zero on error. | AGENTS.md |
| references | directory | Optional. Documentation loaded on demand. | AGENTS.md |
| assets | directory | Optional. Static resources (templates, images, data files). | AGENTS.md |
| changelog | file | Required by Constitution. `CHANGELOG.md` at skill root. Documents every version bump. | Constitution Principle II |

---

## Entity: Validation Report

Output produced by `validate_skill.cjs`.

| Field | Type | Constraints |
|-------|------|-------------|
| status | string | `valid`, `valid_with_warnings`, or `invalid` |
| errors | array<string> | Empty if status is valid. One message per error. |
| warnings | array<string> | Empty if no warnings. One message per warning. |
| exit_code | integer | 0 for valid/valid_with_warnings, 1 for invalid |

---

## Relationships

```
Skill 1--* Script
Skill 1--* Reference
Skill 1--* Asset
Skill 1--1 Changelog
ValidationReport 1--1 Skill (evaluates)
```

---

## State Transitions

A skill progresses through these conceptual states during creation:

```
[Intent Captured] -> [Clarified] -> [Draft Generated] -> [Files Scaffolded] -> [Content Filled] -> [Validated] -> [Quality Checked]
```

| State | Entry Condition | Exit Condition |
|-------|-----------------|----------------|
| Intent Captured | User expresses desire to create a skill | Name, description, and resource types are inferred or provided |
| Clarified | Ambiguity detected | At most 3 question turns completed |
| Draft Generated | Information is complete | Draft feature description is presented |
| Files Scaffolded | User confirms path and name | init_skill.cjs creates directory structure |
| Content Filled | Agent edits scaffolded files | SKILL.md body, scripts, references are authored |
| Validated | validate_skill.cjs reports valid | No errors; warnings may exist |
| Quality Checked | Checklist presented and reviewed | User confirms or requests iteration |
```

---

## Validation Rules

Derived from FR-006 and spec requirements:

1. **VR-001**: SKILL.md must exist in the skill directory.
2. **VR-002**: SKILL.md must start with `---` followed by valid YAML frontmatter, closed by `---`.
3. **VR-003**: Frontmatter must be parseable by js-yaml without errors.
4. **VR-004**: `name` must be present, match `^[a-z0-9]+(-[a-z0-9]+)*$`, be 1-64 chars, and equal the directory basename.
5. **VR-005**: `description` must be present, 1-1024 chars, and not contain unescaped newlines within the YAML value.
6. **VR-006**: `license` if present must be a non-empty string.
7. **VR-007**: `compatibility` if present must be 1-500 chars.
8. **VR-008**: `metadata` if present must be a map where all keys and values are strings.
9. **VR-009**: No `TODO:` markers (case-insensitive) in any file under the skill directory. Violation is a warning, not an error.
10. **VR-010**: Scripts in `scripts/` must have executable permissions or a shebang, and must not be empty.
