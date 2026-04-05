# OpenCode Configuration

> **Reference**: Based on [OpenCode Permissions Docs](https://opencode.ai/docs/permissions). See [AGENTS.md](../AGENTS.md) for the common standard across all clients.

This file documents OpenCode-specific configuration for agents and skills.

---

## Permissions

Control which actions require approval to run. OpenCode uses the `permission` config to decide whether an action should run automatically, prompt, or be blocked.

### Available Permissions

| Permission | Description |
|------------|-------------|
| `read` | Reading a file (matches the file path) |
| `edit` | All file modifications (covers `edit`, `write`, `patch`, `multiedit`) |
| `glob` | File globbing (matches the glob pattern) |
| `grep` | Content search (matches the regex pattern) |
| `list` | Listing files in a directory (matches the directory path) |
| `bash` | Running shell commands (matches parsed commands like `git status --porcelain`) |
| `task` | Launching subagents (matches the subagent type) |
| `skill` | Loading a skill (matches the skill name) |
| `lsp` | Running LSP queries |
| `question` | Asking the user questions during execution |
| `webfetch` | Fetching a URL (matches the URL) |
| `websearch` | Web search (matches the query) |
| `codesearch` | Code search (matches the query) |
| `external_directory` | Triggered when a tool touches paths outside the project working directory |
| `doom_loop` | Triggered when the same tool call repeats 3 times with identical input |

### Actions

Each permission resolves to one of:
- `"allow"` — run without approval
- `"ask"` — prompt for approval
- `"deny"` — block the action

### Basic Configuration

```json
{
  "permission": {
    "*": "ask",
    "bash": "allow",
    "edit": "deny"
  }
}
```

You can also set all permissions at once:
```json
{ "permission": "allow" }
```

### Granular Rules (Object Syntax)

For most permissions, use an object to apply different actions based on tool input:

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow",
      "rm *": "deny",
      "grep *": "allow"
    },
    "edit": {
      "*": "deny",
      "packages/web/src/content/docs/*.mdx": "allow"
    }
  }
}
```

#### Wildcards

Permission patterns use simple wildcard matching:
- `*` matches zero or more of any character
- `?` matches exactly one character
- All other characters match literally

#### Home Directory Expansion

Use `~` or `$HOME` at the start of a pattern:
- `~/projects/*` -> `/Users/username/projects/*`
- `$HOME/projects/*` -> `/Users/username/projects/*`

#### External Directories

Allow tool calls that touch paths outside the working directory:

```json
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow"
    }
  }
}
```

Since `read` defaults to `allow`, reads are also allowed for entries under `external_directory` unless overridden:

```json
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow"
    },
    "edit": {
      "~/projects/personal/**": "deny"
    }
  }
}
```

### Rule Evaluation

Rules are evaluated by pattern match, with **the last matching rule winning**. A common pattern is to put the catch-all `"*"` rule first, and more specific rules after it.

### Defaults

If you don't specify anything, OpenCode starts from permissive defaults:

| Permission | Default |
|------------|---------|
| Most permissions | `allow` |
| `doom_loop` | `ask` |
| `external_directory` | `ask` |
| `read` | `allow` |
| `*.env` | `deny` |
| `*.env.*` | `deny` |
| `*.env.example` | `allow` |

### What "Ask" Does

When OpenCode prompts for approval, the UI offers:
- `once` — approve just this request
- `always` — approve future requests matching suggested patterns
- `reject` — deny the request

### doom_loop

Triggered when the same tool call repeats 3 times with identical input. Useful to prevent infinite loops.

---

## Tools vs Permission

> **Note**: The legacy `tools` boolean config is deprecated. Use `permission` instead.

Old format (deprecated):
```json
{ "tools": { "write": true, "bash": false } }
```

New format:
```json
{ "permission": { "edit": "allow", "bash": "deny" } }
```

---

## Agent-Specific Permissions

Agent permissions are merged with the global config, and agent rules take precedence.

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git push *": "deny"
    }
  },
  "agent": {
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git push *": "ask"
        }
      }
    }
  }
}
```

For more details, see:
- [opencode/agents/AGENTS.md](agents/AGENTS.md)
- [opencode/skills/AGENTS.md](skills/AGENTS.md)