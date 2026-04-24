# CLI Contract: skill-creator Scripts

**Feature**: skill-creator  
**Date**: 2026-04-23

---

## Command: `init_skill.cjs`

### Synopsis

```bash
node init_skill.cjs <skill-name> --path <output-directory>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `skill-name` | Yes | The skill identifier. Must match `^[a-z0-9]+(-[a-z0-9]+)*$`. Max 64 chars. |
| `--path <output-directory>` | Yes | The parent directory where the skill folder will be created. The skill folder name will equal `skill-name`. |

### Behavior

1. Validate `skill-name` against the regex. If invalid, print error and exit with code 1.
2. Resolve `<output-directory>/<skill-name>`. If the directory already exists, print error and exit with code 1.
3. Create the directory structure:
   - `<skill-name>/SKILL.md`
   - `<skill-name>/CHANGELOG.md`
   - `<skill-name>/scripts/example_script.cjs`
   - `<skill-name>/references/example_reference.md`
   - `<skill-name>/assets/example_asset.txt`
4. Populate `SKILL.md` from a template with frontmatter placeholders and TODO markers.
5. Populate `CHANGELOG.md` with a stub entry for version `0.1.0`.
6. Print success message with the absolute path to the created directory.

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid name, directory exists, missing js-yaml, filesystem error) |

### Error Messages

- Invalid name: `ERROR: Skill name must match ^[a-z0-9]+(-[a-z0-9]+)*$ and be 1-64 characters.`
- Directory exists: `ERROR: Directory <path> already exists. Choose a different name or remove the existing directory.`
- Missing js-yaml: `ERROR: js-yaml is required. Install with: npm install js-yaml`

---

## Command: `validate_skill.cjs`

### Synopsis

```bash
node validate_skill.cjs <path-to-skill-directory> [--strict]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `path-to-skill-directory` | Yes | Absolute or relative path to the skill directory to validate. |
| `--strict` | No | If present, warnings (e.g., TODO markers) are treated as errors. |

### Behavior

1. Check that the directory exists and contains `SKILL.md`.
2. Read `SKILL.md` and extract YAML frontmatter between `---` delimiters.
3. Parse frontmatter with js-yaml.
4. Validate fields per the OpenCode spec and project constitution.
5. Recursively scan all files under the skill directory for `TODO:` markers (case-insensitive).
6. Print a structured report to stdout.

### Output Format

```
Skill: <name>
Status: <valid | valid_with_warnings | invalid>

Errors:
- <error message>

Warnings:
- <warning message>
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Valid (or valid with warnings, unless `--strict`) |
| 1 | Invalid (errors found, or warnings in strict mode) |

### Validation Rules

| Rule ID | Check | Severity |
|---------|-------|----------|
| VR-001 | `SKILL.md` exists | Error |
| VR-002 | Frontmatter delimiters present | Error |
| VR-003 | Frontmatter parseable by js-yaml | Error |
| VR-004 | `name` present, matches regex, 1-64 chars, equals directory name | Error |
| VR-005 | `description` present, 1-1024 chars, single-line | Error |
| VR-006 | `license` if present is non-empty string | Error |
| VR-007 | `compatibility` if present is 1-500 chars | Error |
| VR-008 | `metadata` if present is string-to-string map | Error |
| VR-009 | No `TODO:` markers in any file | Warning (Error in strict mode) |

---

## Dependencies

Both scripts require:
- Node.js 18 or higher
- `js-yaml` package (peer dependency)

The scripts must check for `js-yaml` at runtime and emit a clear install instruction if missing.
