# Gemini CLI Hooks I/O Schemas

This document outlines the standard Input/Output formats expected by the Gemini CLI hook system natively. Adherence is mandatory to prevent the agent's workflow from silently crashing or ignoring the hook.

## 📖 "The Golden Rule"
Hooks must output **ONLY** a single valid JSON object to `stdout`.
If any text strings, stack traces, or console warnings are sent to `stdout` before the final JSON payload, Gemini CLI's parser will fail. Redirect all other output to `stderr`.

## 📩 Input Parameters (`stdin`)

When a hook is triggered, it receives a JSON payload through standard input (`stdin`). The fields depend on the phase of execution, but typically include:

```json
{
  "hook_event": "BeforeTool",
  "session_id": "gemini-sess-9283f",
  "tool_name": "run_shell_command",
  "tool_input": {
    "command": "ls -la"
  },
  "cwd": "/Users/user/project"
}
```

*Note: For `AfterAgent` loops, tool fields may be empty or omitted.*

## 📤 Output Schemas (`stdout`)

### 1. Allowance (Success)
Use this to let the Agent proceed seamlessly without interruptions.
```json
{"decision": "allow"}
```

### 2. Denial (Block/Reject)
Use this to stop the tool from running (BeforeTool) or the turn from ending (AfterAgent).
```json
{
  "decision": "deny",
  "reason": "Security: Cannot read sensitive .env files. Ask the user instead.",
  "systemMessage": "🔒 Security Hook intervention."
}
```
*Note: The CLI might convert a `decision: deny` to an Exit Code 2 automatically depending on the event phase.*

### 3. Tool Mutation (BeforeTool)
Modify the incoming tool request dynamically.
```json
{
  "tool_input": {
    "command": "ls -la --color=always"
  }
}
```

## Privacidad / Privacy Flags
Gemini enforces strict privacy boundaries. By adding `"suppressOutput": true` to any schema, Gemini will keep the hook interventions hidden from persistent audit trails while still showing the `systemMessage` to the user in real-time.
