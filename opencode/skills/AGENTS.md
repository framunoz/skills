# OpenCode Agent Skills

> **Reference**: See [AGENTS.md](../../AGENTS.md) for the common standard.

This file documents OpenCode-specific behavior for skills. For the general specification, frontmatter fields, and recommended metadata, refer to the common AGENTS.md.

---

## Locations

OpenCode searches these locations for skills:

| Location | Path |
|----------|------|
| Project config | `.opencode/skills/<name>/SKILL.md` |
| Global config | `~/.config/opencode/skills/<name>/SKILL.md` |
| Claude-compatible (project) | `.claude/skills/<name>/SKILL.md` |
| Claude-compatible (global) | `~/.claude/skills/<name>/SKILL.md` |
| Agent-compatible (project) | `.agents/skills/<name>/SKILL.md` |
| Agent-compatible (global) | `~/.agents/skills/<name>/SKILL.md` |

### Discovery

For project-local paths, OpenCode walks up from your current working directory until it reaches the git worktree. It loads any matching `skills/*/SKILL.md` in `.opencode/` and any matching `.claude/skills/*/SKILL.md` or `.agents/skills/*/SKILL.md` along the way.

Global definitions are loaded from `~/.config/opencode/skills/*/SKILL.md`, `~/.claude/skills/*/SKILL.md`, and `~/.agents/skills/*/SKILL.md`.

---

## How OpenCode Uses Skills

OpenCode lists available skills in the `skill` tool description:

```
<available_skills>
  <skill>
    <name>git-release</name>
    <description>Create consistent releases and changelogs</description>
  </skill>
</available_skills>
```

The agent loads a skill by calling:

```
skill({ name: "git-release" })
```

---

## Permissions

For detailed information about available permissions, wildcards, defaults, and configuration options, see [opencode/AGENTS.md](../AGENTS.md#permissions).

Quick reference for skill-specific permissions:

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

| Permission | Behavior |
|------------|-----------|
| `allow` | Skill loads immediately |
| `deny` | Skill hidden from agent |
| `ask` | User prompted for approval |

### Override Per Agent

**For custom agents** (in agent frontmatter):

```yaml
---
permission:
  skill:
    "documents-*": "allow"
---
```

**For built-in agents** (in `opencode.json`):

```json
{
  "agent": {
    "plan": {
      "permission": {
        "skill": {
          "internal-*": "allow"
        }
      }
    }
  }
}
```

### Disable the Skill Tool

**For custom agents**:

```yaml
---
tools:
  skill: false
---
```

**For built-in agents**:

```json
{
  "agent": {
    "plan": {
      "tools": {
        "skill": false
      }
    }
  }
}
```

---

## Troubleshooting

If a skill does not show up:

1. Verify `SKILL.md` is spelled in all caps
2. Check that frontmatter includes `name` and `description`
3. Ensure skill names are unique across all locations
4. Check permissions—skills with `deny` are hidden from agents