#!/bin/bash

# Simple test runner for py-format-silent hook
HOOK_PATH="$(dirname "$0")/../py-format-silent.js"
SESSION_ID="test_session_$(date +%s)"
TMP_DIR="/Users/franciscomunoz/Codes/Personal/my-skills/tmp/hooks"
STATE_FILE="$TMP_DIR/state_$SESSION_ID.json"

echo "🧪 Running Tests for py-format-silent.js..."

# Ensure we start clean
mkdir -p "$TMP_DIR"
rm -f "$STATE_FILE"
touch mock.py

# Test Case 1: Trigger on a mock .py file
echo "  [Test 1] Triggering on mock.py..."
RESULT=$(echo "{\"tool_name\": \"Write\", \"session_id\": \"$SESSION_ID\", \"tool_input\": {\"file_path\": \"mock.py\"}}" | "$HOOK_PATH")

if [[ $RESULT == "{}" ]]; then
    echo "    ✅ Valid JSON output"
else
    echo "    ❌ Failed: Expected '{}', got '$RESULT'"
    rm mock.py
    exit 1
fi

if [[ -f "$STATE_FILE" ]]; then
    echo "    ✅ State file created"
    if grep -q "mock.py" "$STATE_FILE"; then
        echo "    ✅ mock.py recorded in JSON state"
    else
        echo "    ❌ Failed: mock.py not found in $STATE_FILE"
        rm mock.py
        exit 1
    fi
else
    echo "    ❌ Failed: $STATE_FILE was not created"
    rm mock.py
    exit 1
fi

# Clean up
rm -f "$STATE_FILE"
rm mock.py

echo "✨ All tests for py-format-silent.js passed!"
