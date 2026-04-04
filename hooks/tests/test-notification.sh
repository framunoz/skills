#!/bin/bash

# Simple test runner for notification hook
HOOK_PATH="$(dirname "$0")/../notification.js"
VALIDATOR_PATH="node $(dirname "$0")/utils/schema-validator.js"
EVENT="Notification"

echo "🧪 Running Tests for notification.js..."

# Test Case 1: Basic notification
echo "  [Test 1] Basic notification..."
# This is how the hook currently expects it (WRONG per official docs)
INPUT='{"hook_event_name": "'$EVENT'", "session_id": "test", "cwd": "test", "title": "Test", "message": "Hello from Claude Code", "notification_type": "permission_prompt"}'

# The validator should FAIL here because we provided "notification" object instead of root "title"/"message"
$VALIDATOR_PATH input $EVENT "$INPUT"
if [[ $? -ne 0 ]]; then
    echo "    ❌ SCHEMA FAILURE: Hook input mock is invalid for event $EVENT"
    echo "    (TDD RED: Mock follows current buggy implementation, not the official spec)"
fi

RESULT=$(echo "$INPUT" | "$HOOK_PATH")
$VALIDATOR_PATH output $EVENT "$RESULT" || exit 1

if [[ $RESULT == *"{}"* ]] || [[ $RESULT == *"allow"* ]]; then
    echo "    ✅ Execution Passed"
else
    echo "    ❌ Failed: Expected allow/empty, got '$RESULT'"
    exit 1
fi

echo "🧪 Done with notification.js tests."