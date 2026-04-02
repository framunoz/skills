# Agent Instructions: Claude Code Hooks System

This file provides critical context and operational mandates for any AI agent working within the `hooks/` directory.

## ⚖️ Core Mandates

1.  **Strict JSON Rule**: `stdout` is reserved EXCLUSIVELY for valid JSON decisions. All logs, warnings, and errors MUST be redirected to `stderr` or the centralized logger.
2.  **Centralized Logging**: All hooks MUST use `utils/logger.js`. Direct `console.log` is forbidden except for the final JSON output.
3.  **Path Portability**: Use `__dirname` or absolute paths for all file operations. Never rely on the CWD.
4.  **Fail-Open Policy**: Internal hook failures (logging, state cleanup) MUST NOT block the user. Catch all errors and default to `{"decision": "allow"}` unless it's a critical security/quality block.
5.  **Exit Codes**: Use Exit Code `0` for success. For Stop hooks, use `{"decision": "block", "reason": "..."}` to prevent the agent from stopping (triggers retry).
6.  **Robust JSON Parsing**: Parse JSON with `JSON.parse`. Never use fragile regex or text processing for JSON input.

## 🔧 Claude Code Hook Events

| Event         | Trigger                          | Can block? |
|---------------|----------------------------------|------------|
| `PreToolUse`  | Before any tool call             | Yes — `{"decision": "block", "reason": "..."}` |
| `PostToolUse` | After any tool call              | No         |
| `Stop`        | When agent finishes a turn       | Yes — `{"decision": "block", "reason": "..."}` |
| `Notification`| On agent notifications           | No         |

## 🔧 Claude Code Tool Names

Use these exact names in hook matchers:
- `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`, `Agent`, `WebSearch`, `WebFetch`

## 🔧 Hook Output Schemas

**PreToolUse — allow:**
```json
{"decision": "allow"}
```

**PreToolUse — block:**
```json
{"decision": "block", "reason": "Explanation shown to the model."}
```

**PreToolUse — modify tool input:**
```json
{"tool_input": {"key": "new_value"}}
```

**Stop — block (triggers retry):**
```json
{"decision": "block", "reason": "Issues found, please fix."}
```

## 🔒 Security & Performance

- **Input Validation**: ALWAYS validate the JSON input from `stdin` before processing.
- **Timeouts**: Any hook spawning subprocesses MUST implement a strict timeout (10s–30s).
- **Selective Matchers**: Register hooks with the most specific matcher possible in `settings.json`.

## 🏗 Architectural Integrity

- **State Management**: All cross-hook state MUST be handled by `utils/state-manager.js`.
- **Session Isolation**: State is isolated by `session_id` and stored in `tmp/hooks/` relative to the project root.
- **Atomic Refactoring**: Changes to shared utilities (`logger.js`, `state-manager.js`) MUST be applied to all dependent hooks simultaneously.

## ✅ Verification Workflow

After modifying any hook or utility, run the corresponding test script:
- `./tests/test-block-env.sh`
- `./tests/test-py-format.sh`
- `./tests/test-py-quality.sh`

## 📝 Documentation Standards

- **Headers**: Maintain JSDoc headers at the top of each script (`@hook`, `@event`, `@matcher`, `@description`, `@performance`, etc.).
- **README**: Keep `README.md` updated with any changes to the hook catalog, state logic, or features.
- **Log level**: Controlled by `CLAUDE_HOOKS_LOG_LEVEL` env var (DEBUG/INFO/WARN/ERROR, default INFO).
