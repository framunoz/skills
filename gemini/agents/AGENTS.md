# Gemini CLI Agent Configuration

> **Reference**: See [AGENTS.md](../../AGENTS.md) for the common standard.

This file provides critical instructions for any AI agent tasked with creating or modifying a Gemini CLI subagent. Follow these constraints strictly.

---

## File Format & Frontmatter

A subagent file MUST begin with a YAML frontmatter block containing its configuration, followed by the Markdown body which acts as its **System Prompt**.

```yaml
---
name: specialized-subagent
description: Detailed explanation of what this agent does, when to use it, and what inputs it requires.
kind: local
tools:
  - read_file
  - grep_search
model: inherit
temperature: 0.2
max_turns: 15
timeout_mins: 10
metadata:
  author: creator-name
  version: "1.0.0"
---
```

### Required & Optional Fields

| Field          | Type   | Required | Description                                                                                                            |
| :------------- | :----- | :------- | :--------------------------------------------------------------------------------------------------------------------- |
| `name`         | string | **Yes**  | Unique slug. Lowercase, numbers, hyphens/underscores only. Max 64 chars.                                               |
| `description`  | string | **Yes**  | **CRITICAL:** This is how the main agent knows when to delegate. Be explicit about its expertise and required inputs.  |
| `kind`         | string | No       | `local` (default) or `remote`.                                                                                         |
| `tools`        | array  | No       | List of allowed tool names (e.g., `read_file`, `run_shell_command`). Supports wildcards: `*`, `mcp_*`, `mcp_server_*`. |
| `model`        | string | No       | Specific model ID (e.g., `gemini-2.5-flash`) or `inherit` (default).                                                   |
| `temperature`  | number | No       | Model temperature (0.0 - 2.0). Defaults to `1`.                                                                        |
| `max_turns`    | number | No       | Max conversation turns before returning. Defaults to `30`.                                                             |
| `timeout_mins` | number | No       | Max execution time in minutes. Defaults to `10`.                                                                       |

**Note on Metadata:** Always include standard collaboration metadata (author, version, tags) as defined in the common [AGENTS.md](../../AGENTS.md).

---

## Writing the System Prompt

The content below the frontmatter becomes the agent's system prompt. When writing this section, you must include:

1. **Role Definition**: Clearly state who the agent is and what its primary objective is.
2. **Specific Inputs & Outputs**: Define exactly what format the subagent expects to receive and what structured format it must return (e.g., "Return a JSON object...", "Output a structured Markdown report..."). This provides a natural stopping point.
3. **Constraints**: Explicitly list what the agent MUST NOT do (e.g., "Do not modify files directly", "Do not write tests").
4. **Tool Utilization**: If you provided specific tools in the frontmatter, instruct the agent on _when_ and _how_ to use them effectively.
5. **Obstacle Reporting**: Instruct the agent to document any workarounds, quirks, or problems found in its output so the main thread doesn't have to rediscover them.

### Effective Delegation Design

Vague descriptions lead to poor delegation. The `description` field in the frontmatter and the instructions in the System Prompt must align to ensure the subagent receives a highly focused, bounded task.
