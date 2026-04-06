# Agent Configuration (Common Standard)

> **Reference**: Based on [Agent Skills Specification](https://agentskills.io/specification)

This file defines the common standard for agents and skills across all AI client implementations (OpenCode, Claude, Gemini, etc.).

---

## Skills

Skills are reusable behavior definitions discovered from your repo or home directory. They are loaded on-demand via the native `skill` tool.

### File Structure

A skill is a directory containing, at minimum, a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/      # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

### SKILL.md Format

Each `SKILL.md` must start with YAML frontmatter, followed by markdown content.

#### Frontmatter Fields

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | 1-64 chars. Lowercase letters, numbers, hyphens only. Cannot start/end with hyphen. |
| `description` | Yes | 1-1024 chars. Describes what the skill does and when to use it. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | 1-500 chars. Environment requirements (product, packages, network access, etc.). |
| `metadata` | No | Arbitrary key-value mapping for additional metadata. |

##### Name Validation

The `name` must:
- Be 1–64 characters
- Be lowercase alphanumeric with single hyphen separators
- Not start or end with `-`
- Not contain consecutive `--`
- Match the directory name

Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`

##### Description

Must be 1-1024 characters. Should describe both what the skill does and when to use it. Include specific keywords that help agents identify relevant tasks.

##### Compatibility

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

##### Metadata

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
```

- `author`: Who created the skill
- `co-author`: Additional contributors (optional)
- `source`: Original source URL or reference (useful when adapting skills from others)
- `version`: Track version for changes
- `last-updated`: Last modification date
- `tags`: Optional tags for categorization

##### Allowed Tools (Experimental)

```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

### Optional Directories

#### `scripts/`

Contains executable code that agents can run. Scripts should:
- Be self-contained or clearly document dependencies
- Include helpful error messages
- Handle edge cases gracefully

#### `references/`

Contains additional documentation:
- `REFERENCE.md` - Detailed technical reference
- `FORMS.md` - Form templates
- Domain-specific files

#### `assets/`

Contains static resources:
- Templates
- Images
- Data files

### Progressive Disclosure

1. **Metadata** (~100 tokens): `name` and `description` loaded at startup
2. **Instructions** (< 5000 tokens): Full `SKILL.md` body when activated
3. **Resources** (as needed): Files in `scripts/`, `references/`, `assets/` loaded on demand

### File References

Use relative paths from skill root:

```markdown
See [the reference guide](references/REFERENCE.md) for details.
scripts/extract.py
```

---

## Subagents

Subagents are specialized assistants that can be invoked for specific tasks. They are defined using markdown files.

### File Structure

```
agent-name.md
```

Or:

```
agent-name/
└── AGENT.md
```

### AGENT.md Format

```yaml
---
description: Brief description of what the agent does
compatibility: Compatible platforms (optional)
metadata:
  author: creator-username
  co-author: collaborator-username (optional)
  source: URL or reference to original agent
  version: "1.0.0"
  last-updated: "2026-04-05"
  tags: comma-separated-tags
---

You are a specialized assistant. Focus on:
- Specific task 1
- Specific task 2
```

**Recommendation**: Include the same metadata keys for consistency:

- `author`: Who created the agent
- `co-author`: Additional contributors (optional)
- `source`: Original source URL (if adapted from another agent)
- `version`: Track version for changes
- `last-updated`: Last modification date
- `tags`: Optional tags for categorization

---

## Locations

### Skills

| Client | Project Path | Global Path |
|--------|--------------|-------------|
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` |
| Claude | `.claude/skills/` | `~/.claude/skills/` |
| Gemini | `.gemini/skills/` | `~/.gemini/skills/` |
| Agent-compatible | `.agents/skills/` | `~/.agents/skills/` |

### Agents

| Client | Project Path | Global Path |
|--------|--------------|-------------|
| OpenCode | `.opencode/agents/` | `~/.config/opencode/agents/` |
| Claude | `.claude/agents/` | `~/.claude/agents/` |
| Agent-compatible | `.agents/` | `~/.agents/` |

> **Note**: For OpenCode-specific configuration (permissions, tools, discovery), see [opencode/AGENTS.md](opencode/AGENTS.md).

---

## Examples

### Skill Example

```markdown
---
name: git-release
description: Create consistent releases and changelogs from merged PRs
license: MIT
compatibility: OpenCode, Claude Code
metadata:
  author: your-team
  version: "1.0.0"
  last-updated: "2026-04-05"
  source: https://github.com/example/skills/git-release
---

## What I do
- Draft release notes from merged PRs
- Propose a version bump

## When to use me
Use when preparing a tagged release.
```

### Subagent Example

```markdown
---
description: Reviews code for quality and best practices
compatibility: OpenCode, Claude Code
metadata:
  author: your-team
  co-author: collaborator
  source: https://github.com/example/agents/code-reviewer
  version: "1.0.0"
  last-updated: "2026-04-05"
---

You are a code reviewer. Focus on:
- Code quality and best practices
- Security considerations

Provide feedback without making direct changes.
```