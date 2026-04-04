#!/bin/bash

# Simple test runner for block-env-read hook
HOOK_PATH="$(dirname "$0")/../block-env-read.js"
VALIDATOR_PATH="node $(dirname "$0")/utils/schema-validator.js"
EVENT="PreToolUse"

echo "🧪 Running Tests for block-env-read.js..."

# Test Case 1: Block .env read
echo "  [Test 1] Blocking .env read..."
INPUT='{"hook_event_name": "'$EVENT'", "session_id": "test", "cwd": "test", "tool_name": "Read", "tool_input": {"file_path": ".env"}}'
$VALIDATOR_PATH input $EVENT "$INPUT" || exit 1
RESULT=$(echo "$INPUT" | "$HOOK_PATH")
$VALIDATOR_PATH output $EVENT "$RESULT" || exit 1

if [[ $RESULT == *"block"* ]]; then
    echo "    ✅ Passed"
else
    echo "    ❌ Failed: Expected 'block', got '$RESULT'"
    exit 1
fi

# Test Case 2: Allow .env.example read
echo "  [Test 2] Allowing .env.example read..."
INPUT='{"hook_event_name": "'$EVENT'", "session_id": "test", "cwd": "test", "tool_name": "Read", "tool_input": {"file_path": ".env.example"}}'
$VALIDATOR_PATH input $EVENT "$INPUT" || exit 1
RESULT=$(echo "$INPUT" | "$HOOK_PATH")

# This next line is expected to FAIL in TDD RED phase because result is likely {"decision":"allow"}
$VALIDATOR_PATH output $EVENT "$RESULT"
if [[ $? -ne 0 ]]; then
    echo "    ❌ SCHEMA FAILURE: Hook output is invalid for event $EVENT"
    echo "    (TDD RED: Expected failure until hook is refactored to return {})"
    # We continue to expose other errors if any
else
    if [[ $RESULT == "{}" ]]; then
        echo "    ✅ Passed"
    else
        echo "    ❌ Failed: Expected '{}', got '$RESULT'"
        exit 1
    fi
fi

# Test Case 3: Block cat .env shell command
echo "  [Test 3] Blocking cat .env shell command..."
INPUT='{"hook_event_name": "'$EVENT'", "session_id": "test", "cwd": "test", "tool_name": "Bash", "tool_input": {"command": "cat .env"}}'
$VALIDATOR_PATH input $EVENT "$INPUT" || exit 1
RESULT=$(echo "$INPUT" | "$HOOK_PATH")
$VALIDATOR_PATH output $EVENT "$RESULT" || exit 1

if [[ $RESULT == *"block"* ]]; then
    echo "    ✅ Passed"
else
    echo "    ❌ Failed: Expected 'block', got '$RESULT'"
    exit 1
fi

echo "🧪 Done with block-env-read.js tests."
