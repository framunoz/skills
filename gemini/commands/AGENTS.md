# Gemini CLI Custom Commands Configuration

> **Reference**: See [AGENTS.md](../../AGENTS.md) for the common standard.

This file provides critical instructions for any AI agent tasked with creating or modifying a Gemini CLI Custom Command. Follow these constraints strictly.

---

## File Format & Metadata

A custom command file MUST be written in **TOML** format with a `.toml` extension. It does NOT use Markdown or YAML frontmatter.

### Required & Optional Fields

| Field         | Type   | Required | Description                                                                                    |
| :------------ | :----- | :------- | :--------------------------------------------------------------------------------------------- |
| `prompt`      | String | **Yes**  | The exact instruction sent to the model. Can be a multi-line string.                           |
| `description` | String | No       | A short summary displayed in the `/help` menu. If omitted, one is generated from the filename. |

### Example Command (`.gemini/commands/review.toml`)

```toml
description = "Reviews code for security vulnerabilities"

prompt = """
You are a senior security engineer. Review the following code for potential vulnerabilities.
Focus on SQLi, XSS, and proper error handling.

Here is the context:
@{src/auth.py}
"""
```

---

## Writing the Prompt: Dynamic Injections

When writing the `prompt` string for the TOML file, you must leverage Gemini CLI's built-in dynamic injection syntaxes to make the command useful:

1. **Argument Injection (`{{args}}`)**:
   - Use the `{{args}}` placeholder exactly where user input should appear in the prompt.
   - If `{{args}}` is omitted, any user-provided arguments will simply be appended to the end of the prompt separated by two newlines.

2. **Shell Command Execution (`!{...}`)**:
   - You can execute shell commands and inject their output directly into the prompt using `!{command}`.
   - **Security Note:** If you use `{{args}}` _inside_ a shell execution block (e.g., `!{git log {{args}}}`), the CLI automatically shell-escapes the input for security. Outside of `!{}`, `{{args}}` injects raw text.

3. **File/Directory Injection (`@{...}`)**:
   - You can embed the exact content of a file or a listing of a directory by using `@{path/to/file}`.
   - This is highly effective for commands that require specific context without manual copy-pasting by the user.

---

## Reloading

If you are modifying a command while the user has an active Gemini CLI session, instruct the user to run `/commands reload` in their CLI so the changes take effect without needing to restart the application.
