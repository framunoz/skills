# OpenCode Agent Configuration

> **Reference**: See [AGENTS.md](../AGENTS.md) for the common standard.

This file documents OpenCode-specific behavior for creating agents. For the general specification, frontmatter fields, and recommended metadata, refer to the common AGENTS.md.

---

## Locations

Save agent definition files in:

| Location | Path |
|----------|------|
| Project config | `.opencode/agents/<name>.md` |
| Global config | `~/.config/opencode/agents/<name>.md` |
| Claude-compatible (project) | `.claude/agents/<name>.md` |
| Claude-compatible (global) | `~/.claude/agents/<name>.md` |
| Agent-compatible (project) | `.agents/<name>.md` |
| Agent-compatible (global) | `~/.agents/<name>.md` |

The filename becomes the agent name (e.g., `review.md` creates `@review`).

---

## Frontmatter Options

```yaml
---
description: Brief description of what the agent does and when to use it
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
steps: 10
permission:
  edit: deny
  bash: ask
  webfetch: allow
hidden: false
color: "#FF5733"
---
```

### Options Reference

| Option | Description |
|--------|-------------|
| `description` | What the agent does. Used for @ mention autocomplete. **Required** |
| `mode` | `primary`, `subagent`, or `all` (default). Controls how the agent can be used. |
| `model` | Override the model (format: `provider/model-id`) |
| `temperature` | 0.0-1.0, controls creativity (default: model-specific) |
| `steps` | Max agentic iterations before forced to respond with text |
| `disable` | Set to `true` to disable the agent |
| `permission` | Control tool access: `allow`, `ask`, or `deny` |
| `hidden` | Hide from @ autocomplete (for internal agents) |
| `color` | Hex color or theme color for UI |
| `top_p` | Alternative to temperature for response diversity |
| `prompt` | External prompt file (use with `{file:./path}`) |

---

## Mode

The `mode` option determines how the agent can be used:

| Mode | Description |
|------|-------------|
| `primary` | Main agent that handles your conversation. Switch using **Tab**. Only one primary agent active at a time. |
| `subagent` | Specialized assistant invoked by primary agents or via `@mention`. Used for specific tasks. |
| `all` | Can function as both (default if not specified). |

- **Primary agents**: Handle the main conversation.
- **Subagents**: Invoked for specific tasks.

---

## Permissions Syntax

For detailed information about permissions, wildcards, defaults, and configuration options, see [opencode/AGENTS.md](../AGENTS.md#permissions).

Quick reference:

```yaml
permission:
  edit: deny                    # Deny all edits
  bash: ask                     # Ask before running bash
  webfetch: allow               # Allow all web requests
  bash:                         # Per-command permissions
    "*": ask                    # Default: ask
    "git status *": allow       # Allow specific commands
    "git push": deny            # Deny specific commands
```

### Task Permissions

Control which subagents this agent can invoke:

```yaml
permission:
  task:
    "*": deny                   # Default: deny all
    "explorer": allow           # Allow specific subagents
    "code-*": ask               # Allow glob patterns
```

---

## Writing the System Prompt

The content below the frontmatter becomes the agent's system prompt. Write clear instructions about:

1. **Role**: What the agent is and does
2. **Focus areas**: What to prioritize (security, performance, etc.)
3. **Constraints**: What the agent should NOT do
4. **Output format**: How results should be presented

### Prompt Best Practices

- Be specific about the agent's purpose
- Define clear boundaries (e.g., "do not make direct changes")
- List specific things to look for or check
- Specify when to use other tools or agents

---

## Testing Your Agent

1. Restart OpenCode to load the new agent
2. Invoke with `@agent-name` in a message
3. Check the agent responds according to your prompt
4. Adjust permissions or prompt as needed