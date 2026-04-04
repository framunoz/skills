# Agent Instructions: Gemini CLI Hooks System

This file provides critical context and operational mandates for any AI agent working within the `hooks/` directory.

## ⚖️ Core Mandates

1.  **Strict JSON Rule**: `stdout` is reserved EXCLUSIVELY for valid JSON decisions. All logs, warnings, and errors MUST be redirected to `stderr` or the centralized logger.
2.  **Centralized Logging**: All hooks MUST use `utils/logger.js`. Direct `console.log` is forbidden. Mirroring to `stderr` is handled by the logger for visibility in the Debug Drawer (F12).
3.  **Path Portability**: Use `__dirname` or absolute paths for all file operations. Never rely on the CWD.
4.  **Fail-Open Policy**: Internal hook failures (logging, state cleanup) MUST NOT block the user. Catch all errors and default to `{"decision": "allow"}` unless it's a critical security/quality block.
5.  **Exit Codes**: Use Exit Code `0` for success and `2` for critical blocks or to trigger automatic retries in `AfterAgent` hooks.
6.  **Robust JSON Parsing**: Parse JSON with proper libraries (e.g., `jq` in bash, `JSON.parse` in JS). Never use fragile regex or text processing for JSON input.

## 🔒 Security & Performance

- **Input Validation**: ALWAYS validate the JSON input from `stdin` before processing. Check for required fields like `session_id` or `tool_input`.
- **Timeouts**: Any hook spawning subprocesses MUST implement a strict timeout (e.g., 10s-30s) to prevent hanging the agent loop.
- **Selective Matchers**: Register hooks with the most specific matcher possible in `settings.json`. Avoid `*` if possible to minimize overhead.
- **Caching & Parallelism**: Cache expensive operations (e.g., in `.gemini/hook-cache.json`). Use parallel operations (`Promise.all` or concurrent bash processes) to keep hooks fast.
- **Environment Redaction**: Ensure sensitive keys (like `GEMINI_API_KEY`) are redacted in `settings.json`'s `security` block.
- **Privacy**: Hooks can return `{"suppressOutput": true}` to hide metadata from persistent logs and telemetry while still providing feedback via `systemMessage`.

## 🏗 Architectural Integrity

- **State Management**: All cross-hook state (e.g., tracking modified files) MUST be handled by `utils/state-manager.js`.
- **Session Isolation**: State MUST be isolated by `session_id` and stored in the project's temporary directory (`~/.gemini/tmp/hooks/`) to support concurrent sessions.
- **Atomic Refactoring**: Changes to the shared utilities (`logger.js`, `state-manager.js`) MUST be applied to all dependent hooks simultaneously.

## ✅ Verification Workflow

- **Mandatory Testing**: After modifying any hook or utility, run the corresponding test script:
    - `./tests/test-block-env.sh`
    - `./tests/test-py-format.sh`
    - `./tests/test-py-quality.sh`
- **Independent Validation**: Test hooks manually with sample JSON files before deployment to verify behavior and exit codes.
- **Diagnostics**: Use the `/hooks panel` command inside the CLI to monitor execution status, timing, and errors.
- **Auto-Retry Validation**: For quality hooks, verify that `AfterAgent` correctly triggers retries upon detection of fixable errors.

## 📝 Documentation Standards

- **Headers**: Maintain JSDoc headers at the top of each script (`@hook`, `@event`, `@matcher`, `@description`, `@performance`, etc.).
- **Descriptions**: Always provide a meaningful `description` field in `settings.json`. This text is displayed in the `/hooks panel` UI for diagnostics.
- **README**: Keep `README.md` updated with any changes to the hook catalog, state logic, or features.
