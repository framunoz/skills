# OpenCode Agent Skills

> **Reference**: See [AGENTS.md](../../AGENTS.md) for the common standard.

This file documents OpenCode-specific behavior for skills. For the general specification, frontmatter fields, and recommended metadata, refer to the common AGENTS.md.

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