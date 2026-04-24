# Schema Contract: SKILL.md Frontmatter

**Feature**: skill-creator  
**Date**: 2026-04-23

---

## Overview

This contract defines the valid structure of the YAML frontmatter block in every `SKILL.md` file, as consumed by OpenCode and validated by `validate_skill.cjs`.

---

## Format

The frontmatter is a YAML block delimited by `---` at the start of the file:

```markdown
---
name: skill-name
description: What this skill does and when to use it.
license: MIT
compatibility: Designed for OpenCode
metadata:
  author: framunoz
  original-author: framunoz
  source: https://github.com/framunoz/skills/tree/<commit>/opencode/skills/skill-name
  version: "1.0.0"
  last-updated: "2026-04-23"
  status: active
  replaced-by: "null"
---
```

---

## Field Specifications

### `name` (required)

- **Type**: string
- **Constraints**:
  - 1-64 characters
  - Lowercase alphanumeric with single hyphen separators
  - Must not start or end with `-`
  - Must not contain consecutive `--`
  - Must match the directory name containing `SKILL.md`
- **Regex**: `^[a-z0-9]+(-[a-z0-9]+)*$`

### `description` (required)

- **Type**: string
- **Constraints**:
  - 1-1024 characters
  - Must be a single-line string in YAML (no unescaped newlines)
  - Must describe what the skill does AND when to use it
  - Should include trigger keywords

### `license` (optional)

- **Type**: string
- **Constraints**:
  - Non-empty if present
  - License name or reference to bundled license file

### `compatibility` (optional)

- **Type**: string
- **Constraints**:
  - 1-500 characters if present
  - Should describe environment requirements

### `metadata` (optional)

- **Type**: map<string, string>
- **Constraints**:
  - All keys must be strings
  - All values must be strings (no nested maps, arrays, or numbers)
- **Required keys per Constitution**:
  - `author`: Current maintainer handle or team name
  - `original-author`: Upstream creator for adapted work; equals `author` for original work
  - `source`: Permalink (commit-pinned URL) to canonical upstream
  - `version`: Semver string (e.g., `1.0.0`)
  - `last-updated`: ISO date `YYYY-MM-DD`
  - `status`: One of `active`, `deprecated`, `archived`
  - `replaced-by`: Required when status is `deprecated` or `archived`; successor name or `null`

---

## Validation Behavior

The `validate_skill.cjs` script must enforce this schema as follows:

1. Reject unknown top-level fields? **No** — OpenCode ignores unknown fields, so the validator should warn but not error on unknown top-level keys.
2. Reject nested values in metadata? **Yes** — if metadata contains non-string values, report an error.
3. Reject multiline description in YAML? **Yes** — if the YAML parser reads the description as a multiline string (containing literal newlines), report an error.

---

## Example: Minimal Valid Frontmatter

```yaml
---
name: git-release
description: Create consistent releases and changelogs. Use when preparing a tagged release.
metadata:
  author: framunoz
  original-author: framunoz
  source: https://github.com/framunoz/skills/tree/abc123/opencode/skills/git-release
  version: "1.0.0"
  last-updated: "2026-04-23"
  status: active
  replaced-by: "null"
---
```

## Example: Invalid Frontmatter (errors)

```yaml
---
name: GitRelease
description: |
  This is a multiline
  description.
---
```

Errors:
- `name` contains uppercase letters
- `description` is a multiline YAML string
