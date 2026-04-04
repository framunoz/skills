# Claude Code Hooks System

This directory contains specialized hooks for Claude Code to enhance security, maintain code quality, and provide robust execution tracing.

## 🛠 Hooks Catalog

| Hook Name | Event | Matcher | Description |
| :--- | :--- | :--- | :--- |
| **`block-env-read`** | `PreToolUse` | `Read` | **Security**: Prevents the agent from reading sensitive `.env` files while allowing access to template files like `.env.example`. |
| **`safe-git-commit`** | `PreToolUse` | `Bash` | **Security**: Automatically escapes backticks (`) in git commit messages to prevent accidental shell execution or errors. |
| **`py-format-silent`** | `PostToolUse` | `Write`, `Edit` | **Automation**: Automatically formats Python files using Ruff after every write/edit tool call. |
| **`py-quality-gate`** | `Stop` | `.*` | **Quality**: Runs scoped diagnostics (Ruff + Pyrefly) on directories specified by `CLAUDE_HOOKS_PY_QUALITY_DIRS`. Disabled when not set. Blocks with retry on errors (up to 3 attempts). |
| **`notification`** | `Notification` | `.*` | **User Experience**: Displays desktop notifications (macOS/Linux) when Claude Code needs user attention. |

## 📝 Logging System

All hooks use a centralized logging utility at `utils/logger.js`.

### Features
- **Shared Log File**: All activity is consolidated in `logs/hooks.log`.
- **Automatic Retries**: If `py-quality-gate` detects errors, it triggers up to **3 retries**, allowing the agent to self-correct before failing. Retry state is stored in `/tmp/` per session.
- **Automatic Rotation**: When `hooks.log` exceeds **1MB**, it is rotated to `hooks.old.log` (1 backup max).
- **Log Levels**: Supports `DEBUG`, `INFO`, `WARN`, and `ERROR`.
- **Full Audit Trail**: In `DEBUG` mode, hooks record the full JSON input and output.
- **Fail-Open Design**: Internal hook failures never block the user — they default to `{"decision": "allow"}`.

### Configuration
Control verbosity with the `CLAUDE_HOOKS_LOG_LEVEL` environment variable:

```bash
export CLAUDE_HOOKS_LOG_LEVEL=DEBUG  # Full JSON audit trails
export CLAUDE_HOOKS_LOG_LEVEL=ERROR  # Only critical failures
```

#### Environment Variables

| Variable | Scope | Description |
| :--- | :--- | :--- |
| `CLAUDE_HOOKS_LOG_LEVEL` | All | Controls logging verbosity (`DEBUG`, `INFO`, `WARN`, `ERROR`). |
| `CLAUDE_HOOKS_PY_QUALITY_DIRS` | Claude | Comma-separated list of directories to scan (e.g., `src,tests`). |
| `HOOKS_PY_QUALITY_DIRS` | Shared | Fallback list of directories for all agents. |

If `CLAUDE_HOOKS_PY_QUALITY_DIRS` or `HOOKS_PY_QUALITY_DIRS` is not set, the quality gate is **DISABLED** to prevent injecting excessive context. A one-time warning will be shown per session.

## 📂 File Structure

```text
hooks/
├── block-env-read.js     # Security: blocks .env reads
├── safe-git-commit.js    # Security: escapes backticks in git commits
├── py-format-silent.js   # Automation: auto-formats Python files
├── py-quality-gate.js    # Quality: Ruff + Pyrefly gate on Stop
├── notification.js       # UX: desktop notifications
├── pyproject.toml        # Ruff configuration (line-length, rules, etc.)
├── README.md             # This documentation
├── CLAUDE.md             # Agent instructions for working with hooks
├── AGENTS.md             # Additional agent guidelines
├── best-practices.md     # Best practices for hook development
├── logs/
│   └── hooks.log         # Active shared log file
├── tests/
│   ├── fixtures/
│   │   └── horrible.py   # Intentionally bad Python for manual testing
│   ├── test-block-env.sh
│   ├── test-py-format.sh
│   ├── test-py-quality.sh
│   ├── test-safe-git.sh
│   ├── test-safe-git.js
│   └── test-notification.sh
└── utils/
    └── logger.js         # Shared logging utility
```

## ⚙️ Configuration Example

Register hooks in your Claude Code `settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hooks/block-env-read.js",
            "statusMessage": "Checking .env access..."
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hooks/safe-git-commit.js",
            "statusMessage": "Checking git commit safety..."
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hooks/py-format-silent.js",
            "statusMessage": "Formatting Python file..."
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hooks/py-quality-gate.js",
            "statusMessage": "Running quality gate..."
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hooks/notification.js",
            "statusMessage": "Sending notification..."
          }
        ]
      }
    ]
  }
}
```

## 🔍 Debugging & Testing

### Independent Test Scripts

```bash
./tests/test-block-env.sh
./tests/test-py-format.sh
./tests/test-py-quality.sh
./tests/test-safe-git.sh
./tests/test-notification.sh
```

### Manual Hook Testing

Pipe a JSON payload directly to any hook:

```bash
echo '{"tool_name": "Read", "session_id": "test", "tool_input": {"file_path": ".env"}}' | ./block-env-read.js
```

## 📚 Additional Documentation

- **[CLAUDE.md](./CLAUDE.md)** - Agent instructions for working within the hooks directory
- **[AGENTS.md](./AGENTS.md)** - Additional agent guidelines
- **[best-practices.md](./best-practices.md)** - Best practices for hook development, security, and debugging