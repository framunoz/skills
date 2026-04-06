# Gemini CLI Agent Configuration

> **Reference**: See [AGENTS.md](../../AGENTS.md) for the common standard.

This file documents Gemini CLI-specific behavior for creating custom subagents. For the general specification, recommended metadata, and best practices for writing the system prompt, refer to the common `AGENTS.md`.

---

## Enabling Subagents

To use custom subagents in Gemini CLI, ensure the experimental feature is enabled in your `settings.json` (or `.gemini/settings.json`):

```json
{
  "experimental": {
    "enableAgents": true
  }
}
```

---

## Locations

Save agent definition files in one of the following locations:

| Location                   | Path                         |
| -------------------------- | ---------------------------- |
| Project config             | `.gemini/agents/<name>.md`   |
| Global config              | `~/.gemini/agents/<name>.md` |
| Agent-compatible (project) | `.agents/<name>.md`          |
| Agent-compatible (global)  | `~/.agents/<name>.md`        |

The filename (excluding `.md`) typically matches the `name` field in the frontmatter.

---

## Frontmatter Options

The file must begin with a YAML frontmatter block, followed by the Markdown body which serves as the **System Prompt** for the subagent.

```yaml
---
name: security-auditor
description: Specialized in finding security vulnerabilities like SQLi and XSS.
kind: local
tools:
  - read_file
  - grep_search
model: inherit
temperature: 0.2
max_turns: 10
timeout_mins: 5
metadata:
  author: your-username
  version: "1.0.0"
---
```

### Options Reference

| Field          | Type   | Required | Description                                                                   |
| :------------- | :----- | :------- | :---------------------------------------------------------------------------- |
| `name`         | string | **Yes**  | Unique slug used as the tool name (lowercase, numbers, hyphens/underscores).  |
| `description`  | string | **Yes**  | Visible to the main agent to help it decide when to delegate a task.          |
| `kind`         | string | No       | `local` (default) or `remote`.                                                |
| `tools`        | array  | No       | List of allowed tool names. Supports wildcards: `*`, `mcp_*`, `mcp_server_*`. |
| `model`        | string | No       | Specific model ID or `inherit` (default).                                     |
| `temperature`  | number | No       | Model temperature (0.0 - 2.0). Defaults to `1`.                               |
| `max_turns`    | number | No       | Max conversation turns before returning. Defaults to `30`.                    |
| `timeout_mins` | number | No       | Max execution time in minutes. Defaults to `10`.                              |

_Note: You should also include standard metadata fields (like `metadata`, `compatibility`) as defined in the common [AGENTS.md](../../AGENTS.md)._

---

## Configuration & Overrides

While definition files handle the persona, you can use your Gemini `settings.json` for persistent overrides (e.g., disabling an agent or changing its limits):

```json
{
  "agents": {
    "overrides": {
      "security-auditor": {
        "enabled": true,
        "runConfig": {
          "maxTurns": 20
        }
      }
    }
  }
}
```

---

## Usage

- **Automatic:** The main agent will call your subagent if the task matches its `description`. Make sure the description is highly specific about the expected inputs and task.
- **Explicit:** Use the `@` syntax in the CLI prompt: `@security-auditor Check my auth.py for leaks`.
- **Management:** Use the `/agents` command inside the CLI to list, enable, or disable agents interactively.

---

## Writing the System Prompt

The content below the frontmatter becomes the agent's system prompt. Write clear instructions about:

1. **Role**: What the agent is and does.
2. **Focus areas**: What to prioritize (security, performance, etc.).
3. **Constraints**: What the agent should NOT do.
4. **Output format**: How results should be structured and presented.
5. **Report obstacles**: Instruct the agent to document workarounds, quirks, or problems found so the main thread doesn't have to rediscover them.
