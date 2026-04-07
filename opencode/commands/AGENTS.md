# OpenCode Custom Commands Configuration

> **Reference**: See [AGENTS.md](../../AGENTS.md) for the common standard.

This file provides critical instructions for any AI agent tasked with creating or modifying an OpenCode Custom Command. Follow these constraints strictly.

---

## File Format & Metadata

OpenCode commands are defined as **Markdown** files with `.md` extension. They use a YAML frontmatter block for configuration, followed by the instruction prompt in the body.

### Locations
- **Project Scope**: `.opencode/commands/<name>.md`
- **Global Scope**: `~/.config/opencode/commands/<name>.md`

The filename (excluding the extension) becomes the command name (e.g., `review.md` -> `/review`).

### Required & Optional Frontmatter Fields

| Field         | Type   | Required | Description                                                                                    |
| :------------ | :----- | :------- | :--------------------------------------------------------------------------------------------- |
| `description` | String | **Yes**  | A short summary displayed in the `/help` menu.                                                 |
| `agent`       | String | No       | Optional subagent or primary agent to handle the command.                                      |
| `model`       | String | No       | Specific model override (e.g., `anthropic/claude-3-5-sonnet-20240620`).                         |
| `subtask`     | Bool   | No       | If `true`, the command runs in a separate subtask context.                                     |

### Example Command (`.opencode/commands/test.md`)

```markdown
---
description: Run tests and summarize results
model: anthropic/claude-3-5-sonnet-20240620
---
You are a test engineer. Analyze the output of the following tests:

!{npm test}

If there are failures, suggest fixes based on:
@{src/main.js}
```

---

## Writing the Prompt: Dynamic Injections

OpenCode commands support powerful dynamic injections to make prompts interactive and context-aware:

1. **User Arguments (`$ARGUMENTS` or `$1`, `$2`)**:
   - Use `$ARGUMENTS` to inject the entire string of arguments provided by the user.
   - Use `$1`, `$2`, etc., for specific positional arguments.

2. **Shell Command Execution (`!{...}`)**:
   - Embed the output of any shell command using `!{command}` (e.g., `!{ls -la}`, `!{git status}`).

3. **File/Directory Injection (`@{...}`)**:
   - Embed the content of a specific file or a directory listing using `@{path/to/file}`.
   - Use `@@{path/to/dir}` to list files in a directory.

---

## Verification

After creating or modifying a command, ensure it works by typing `/` followed by the command name in the OpenCode TUI. If the command was created globally, it may require a restart of the application to be detected.
