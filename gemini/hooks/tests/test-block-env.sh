#!/bin/bash

# Simple test runner for block-env-read hook
HOOK_PATH="$(dirname "$0")/../block-env-read.js"

echo "🧪 Running Tests for block-env-read.js..."

# Test Case 1: Block .env read
echo "  [Test 1] Blocking .env read..."
RESULT=$(echo '{"tool_name": "read_file", "tool_input": {"file_path": ".env"}}' | "$HOOK_PATH")
if [[ $RESULT == *"deny"* ]] && echo "$RESULT" | node "$(dirname "$0")/utils/schema-validator.js"; then
    echo "    ✅ Passed"
else
    echo "    ❌ Failed: Expected 'deny', got '$RESULT' or schema is invalid."
    exit 1
fi

# Test Case 2: Allow .env.example read
echo "  [Test 2] Allowing .env.example read..."
RESULT=$(echo '{"tool_name": "read_file", "tool_input": {"file_path": ".env.example"}}' | "$HOOK_PATH")
if [[ $RESULT == *"allow"* ]] && echo "$RESULT" | node "$(dirname "$0")/utils/schema-validator.js"; then
    echo "    ✅ Passed"
else
    echo "    ❌ Failed: Expected 'allow', got '$RESULT' or schema is invalid."
    exit 1
fi

# Test Case 3: Block cat .env shell command
echo "  [Test 3] Blocking cat .env shell command..."
RESULT=$(echo '{"tool_name": "run_shell_command", "tool_input": {"command": "cat .env"}}' | "$HOOK_PATH")
if [[ $RESULT == *"deny"* ]] && echo "$RESULT" | node "$(dirname "$0")/utils/schema-validator.js"; then
    echo "    ✅ Passed"
else
    echo "    ❌ Failed: Expected 'deny', got '$RESULT' or schema is invalid."
    exit 1
fi

echo "✨ All tests for block-env-read.js passed!"
