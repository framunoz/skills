# Gemini CLI Hooks System

This directory contains specialized hooks for the Gemini CLI to enhance security, maintain code quality, and provide robust execution tracing.

## 🛠 Hooks Catalog

| Hook Name | Event | Description |
| :--- | :--- | :--- |
| **`block-env-read`** | `BeforeTool` | **Security**: Prevents the agent from reading sensitive `.env` files while allowing access to template files like `.env.example`. |
| **`py-format-silent`** | `AfterTool` | **Automation**: Automatically formats Python files using `black` and `ruff` after every successful tool change. |
| **`py-quality-gate`** | `AfterAgent` | **Quality**: Runs global project diagnostics (Ruff, Pyrefly) before allowing a turn to finish if Python files were modified. |

## 📝 Logging System

All hooks utilize a centralized logging utility located in `utils/logger.js`.

### Features
- **Shared Log File**: All activity is consolidated in `logs/hooks.log`.
- **Session Isolation**: Each agent session uses its own temporary state file in `~/.gemini/tmp/hooks/` to track modified files.
- **Automatic Retries**: If `py-quality-gate` detects errors, it will automatically trigger up to **3 retries**, allowing the agent to self-correct.
- **Automatic Rotation**: When `hooks.log` exceeds **1MB**, it is automatically rotated to `hooks.old.log` (keeping only 1 backup to save space).
- **Log Levels**: Supports `DEBUG`, `INFO`, `WARN`, and `ERROR`.
- **Full Audit Trail**: In `DEBUG` mode, hooks record the full JSON input (tool name, arguments) and final JSON output (decision).
- **Fail-Open Design**: If logging fails (e.g., disk full), the hook will gracefully continue to avoid blocking the workflow.
- **Real-time Monitoring**: All logs are mirrored to `stderr`, making them visible in the **Gemini CLI Debug Drawer (F12)**.

### Configuration
You can control the verbosity of the logs using the `GEMINI_HOOKS_LOG_LEVEL` environment variable:

```bash
# Set to DEBUG for full JSON audit trails
export GEMINI_HOOKS_LOG_LEVEL=DEBUG

# Set to ERROR to see only critical failures
export GEMINI_HOOKS_LOG_LEVEL=ERROR
```

## 📂 File Structure

```text
.gemini/hooks/
├── block-env-read.js    # Security interception logic
├── py-format-silent.js  # Formatting logic
├── py-quality-gate.js   # Global quality gate logic
├── README.md            # This documentation
├── logs/
│   └── hooks.log        # Active shared log file
└── utils/
    ├── logger.js        # Shared logging utility
    └── state-manager.js # Session-specific state management
```

## ⚙️ Configuration Example

To activate these hooks, add the following to your `~/.gemini/settings.json` file:

```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "(read_file|run_shell_command)",
        "hooks": [
          {
            "name": "block-env-read",
            "description": "Prevents reading sensitive .env files unless they are example files.",
            "type": "command",
            "command": "~/.gemini/hooks/block-env-read.js"
          }
        ]
      }
    ],
    "AfterTool": [
      {
        "matcher": "(write_file|replace)",
        "hooks": [
          {
            "name": "py-format-silent",
            "description": "Automatically formats Python files using black and ruff after each tool change.",
            "type": "command",
            "command": "~/.gemini/hooks/py-format-silent.js"
          }
        ]
      }
    ],
    "AfterAgent": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "name": "py-quality-gate",
            "description": "Validates code standards and typing (Ruff/Pyrefly) before allowing the agent to complete the turn.",
            "type": "command",
            "command": "~/.gemini/hooks/py-quality-gate.js"
          }
        ]
      }
    ]
  }
}
```

## 🔍 Debugging & Testing

### 1. Debug Drawer
Press `F12` in the Gemini CLI to see live hook logs and stderr output.

### 2. Independent Testing
Following best practices, each hook has a standalone test script to verify its logic without needing the full CLI environment.

To run the tests:
```bash
# Run all tests
./tests/test-block-env.sh
./tests/test-py-format.sh
./tests/test-py-quality.sh
```

### 3. Manual Test
You can also test any hook manually by piping a JSON payload to the script:
```bash
echo '{"tool_name": "read_file", "tool_input": {"file_path": ".env"}}' | ./block-env-read.js
```

### 4. Configuration Tips
Always ensure hooks are registered with absolute paths (or using `~`) in `~/.gemini/settings.json` to avoid `MODULE_NOT_FOUND` errors when working in subdirectories.
