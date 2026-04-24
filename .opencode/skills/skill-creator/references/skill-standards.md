# Skill Standards

Reference guide for authoring OpenCode skills. Covers frontmatter rules, naming conventions, length limits, and directory layout.

---

## File Structure

A skill is a directory containing, at minimum, a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

---

## SKILL.md Format

Each `SKILL.md` must start with YAML frontmatter, followed by markdown content.

### Frontmatter Fields

| Field           | Required | Constraints                                                                         |
| --------------- | -------- | ----------------------------------------------------------------------------------- |
| `name`          | Yes      | 1-64 chars. Lowercase letters, numbers, hyphens only. Cannot start/end with hyphen. |
| `description`   | Yes      | 1-1024 chars. Describes what the skill does and when to use it.                     |
| `license`       | No       | License name or reference to a bundled license file.                                |
| `compatibility` | No       | 1-500 chars. Environment requirements (product, packages, network access, etc.).    |
| `metadata`      | No       | Arbitrary key-value mapping for additional metadata.                                |

#### Name Validation

The `name` must:

- Be 1–64 characters
- Be lowercase alphanumeric with single hyphen separators
- Not start or end with `-`
- Not contain consecutive `--`
- Match the directory name

Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`

#### Description

Must be 1-1024 characters. Should describe both what the skill does and when to use it. Include specific keywords that help agents identify relevant tasks.

#### Compatibility

The optional `compatibility` field:

- Must be 1-500 characters if provided
- Should only be included if the skill has specific environment requirements
- Can indicate intended product, required system packages, network access needs, etc.

Examples:

```yaml
compatibility: Designed for OpenCode
compatibility: Claude Code compatible
compatibility: Requires git, docker, jq, and access to the internet
```

#### Metadata

The optional `metadata` field is a map from string keys to string values. Clients can use this to store additional properties.

**Recommended keys for team collaboration:**

```yaml
metadata:
  author: your-username or team-name
  co-author: collaborator-username (optional)
  source: URL or reference to original skill
  version: "1.0.0"
  last-updated: "2026-04-05"
  tags: comma-separated-tags
  related-with:
    skills:
      - skill-name
    agents:
      - agent-name
    commands:
      - command-name
```

- `author`: Who created the skill
- `co-author`: Additional contributors (optional)
- `source`: Original source URL or reference (useful when adapting skills from others)
- `version`: Track version for changes
- `last-updated`: Last modification date
- `tags`: Optional tags for categorization
- `related-with`: Related skills, agents, and commands

---

## Optional Directories

### `scripts/`

Contains executable code that agents can run. Scripts should:

- Be self-contained or clearly document dependencies
- Include helpful error messages
- Handle edge cases gracefully

### `references/`

Contains additional documentation:

- `REFERENCE.md` - Detailed technical reference
- `FORMS.md` - Form templates
- Domain-specific files

### `assets/`

Contains static resources:

- Templates
- Images
- Data files

---

## Writing the Skill Instructions

The content below the frontmatter in `SKILL.md` becomes the skill's instructions. When an agent activates a skill, it reads this content to understand how to perform the task.

When writing this section, you must include:

1. **Context & Goal**: Explain why this skill exists and what it aims to achieve.
2. **Step-by-Step Procedure**: Provide clear, sequential instructions on how the agent should execute the task.
3. **Usage of Resources**: If the skill includes scripts, references, or assets in the subdirectories, explicitly tell the agent how and when to use them (e.g., "Run the `scripts/validate.py` script to check the output").
4. **Constraints & Rules**: Explicitly list what the agent MUST NOT do while executing this skill.
5. **Expected Output**: Define how the agent should conclude the task and present the results to the user.
