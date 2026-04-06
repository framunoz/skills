# OpenCode Configuration

> **Reference**: Based on [OpenCode Permissions Docs](https://opencode.ai/docs/permissions) and [OpenCode Tools Docs](https://opencode.ai/docs/tools/). See [AGENTS.md](../AGENTS.md) for the common standard across all clients.

This file documents OpenCode-specific configuration for agents and skills.

---

## Tools

Manage the tools an LLM can use.

### Configure

Use the `permission` field to control tool behavior. By default, all tools are enabled.

### Built-in Tools

| Tool | Description | Permission |
|------|-------------|-------------|
| bash | Execute shell commands | bash |
| edit | Modify files (covers edit, write, apply_patch, multiedit) | edit |
| read | Read file contents | read |
| grep | Regex content search | grep |
| glob | Find files by pattern | glob |
| list | List directory contents | list |
| lsp | LSP server interaction | lsp |
| skill | Load skills | skill |
| todowrite | Manage todo lists | todowrite |
| webfetch | Fetch web content | webfetch |
| websearch | Web search via Exa AI | websearch |
| question | Ask user questions | question |

#### Tool Details

**bash** - Execute shell commands (npm install, git status, etc.)

**edit/write** - File modification. The `write` tool is controlled by the `edit` permission.

**read** - Read file contents. Supports line ranges for large files.

**grep/glob/list** - Search tools using ripgrep under the hood. Respect `.gitignore` by default.

**lsp** - Requires `OPENCODE_EXPERIMENTAL_LSP_TOOL=true`. Provides goToDefinition, findReferences, hover, documentSymbol, workspaceSymbol, etc. See [LSP Servers](https://opencode.ai/docs/lsp/).

**skill** - Loads a SKILL.md file into the conversation.

**todowrite** - Creates and updates task lists. **Note: Disabled for subagents by default.**

**webfetch** - Fetch and read web pages.

**websearch** - Requires OpenCode provider or `OPENCODE_ENABLE_EXA=1`. Uses Exa AI for web search.

**question** - Allows LLM to ask user questions during execution.

### Custom Tools

Custom tools let you define your own functions that the LLM can call. See [Custom Tools](https://opencode.ai/docs/custom-tools/).

### MCP Servers

MCP (Model Context Protocol) servers integrate external tools and services. See [MCP Servers](https://opencode.ai/docs/mcp-servers/).

### Ignore Patterns

Create a `.ignore` file to include files normally ignored by `.gitignore`:

```
!node_modules/
!dist/
!build/
```

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

**Important**: Rule order matters! If you place `"*": "deny"` after specific allow rules, it will override them.

```yaml
# WRONG - all edits denied, even docs/prd-*.md
edit:
  "docs/prd-*.md": allow
  "docs/interviews/*.md": allow
  "*": deny  # This wins because it's last

# CORRECT - specific paths allowed, everything else denied
edit:
  "*": deny
  "docs/prd-*.md": allow
  "docs/interviews/*.md": allow
```

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