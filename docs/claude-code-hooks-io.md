# Claude Code Hooks I/O Specification

This document defines the input and output JSON schemas for Claude Code hooks, based on the official Anthropic documentation.

## Common Input Fields

All hook events receive a JSON object with these common fields:

| Field | Type | Description |
| :--- | :--- | :--- |
| `session_id` | string | Unique identifier for the current Claude session. |
| `cwd` | string | Absolute path to the current working directory. |
| `hook_event_name` | string | The name of the event triggering the hook (e.g., `PreToolUse`, `Notification`). |
| `transcript_path` | string | Absolute path to the session's JSONL transcript file. |
| `permission_mode` | string | Current permission mode (`default`, `plan`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`). |

---

## Event-Specific Inputs

### PreToolUse
Triggered before a tool is executed.

- **`tool_name`**: The name of the tool (e.g., `Bash`, `Read`, `Write`).
- **`tool_input`**: The arguments passed to the tool (varies by tool).
  - *Bash*: `{ "command": "...", "description": "..." }`
  - *Read*: `{ "file_path": "..." }`
  - *Write*: `{ "file_path": "...", "content": "..." }`

### PostToolUse
Triggered after a tool has successfully completed.

- **`tool_name`**: The name of the tool.
- **`tool_input`**: The arguments passed to the tool.
- **`tool_response`**: The output of the tool.
- **`tool_use_id`**: Unique ID of the tool call.

### Stop
Triggered when the agent completes its turn.

- No specific additional fields beyond the common ones.

### Notification
Triggered when Claude needs to notify the user.

- **`title`**: The notification title.
- **`message`**: The notification body message.
- **`notification_type`**: Type of notification (e.g., `permission_prompt`, `idle_prompt`).

---

## Output Schemas (Stdout)

Hooks must communicate their decision by writing a JSON object to `stdout`.

### Decision Control (Universal)

To allow execution or continue normally:
- Return an empty object: `{}`
- Or: `{"continue": true}`

To block execution (PreToolUse, Stop):
- `{"decision": "block", "reason": "Explanation shown to Claude"}`

### HookSpecificOutput

For richer control, use `hookSpecificOutput` with `hookEventName`.

#### PreToolUse (Modified Decision)
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Not allowed by policy"
  }
}
```

#### Notification
Actually, notifications are generally non-blocking but should return `{}`.

---

## Best Practices

- **Stderr for Logs**: All logs, warnings, and non-JSON output MUST go to `stderr`.
- **Exit Codes**: 
  - `0`: Success (proceed).
  - `2`: Signal a blocking error (different from a regular error, often used to prevent retries or indicate specific policy violations).
- **Fail-Open**: If a hook fails internally, it should default to `{}` to avoid blocking the user experience.
