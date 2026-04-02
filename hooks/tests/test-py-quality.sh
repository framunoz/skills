#!/bin/bash

# Simple test runner for py-quality-gate hook
HOOK_PATH="$(dirname "$0")/../py-quality-gate.js"
SESSION_ID="test_session_$(date +%s)"
TMP_DIR="/Users/franciscomunoz/Codes/Personal/my-skills/tmp/hooks"
STATE_FILE="$TMP_DIR/state_$SESSION_ID.json"

echo "🧪 Running Tests for py-quality-gate.js..."

# Ensure we start clean
mkdir -p "$TMP_DIR"
rm -f "$STATE_FILE"

# Test Case 1: Allow when no files touched
echo "  [Test 1] Allowing when no files touched..."
rm -f "$STATE_FILE"
RESULT=$(echo "{\"session_id\": \"$SESSION_ID\", \"hook_event_name\": \"Stop\"}" | "$HOOK_PATH")
if [[ $RESULT == *"allow"* ]]; then
    echo "    ✅ Passed"
else
    echo "    ❌ Failed: Expected 'allow', got '$RESULT'"
    exit 1
fi

# Test Case 2: Process when files ARE touched
echo "  [Test 2] Triggering diagnostics when files touched..."
# Use a simple timestamp for mock
TS=$(date +%s000)
echo "{\"files\": [\"mock.py\"], \"retryCount\": 0, \"lastModified\": $TS}" > "$STATE_FILE"
# Capture both output and exit code
RESULT=$(echo "{\"session_id\": \"$SESSION_ID\", \"hook_event_name\": \"Stop\"}" | "$HOOK_PATH")
EXIT_CODE=$?

if [[ -f "$STATE_FILE" ]]; then
    echo "    ✅ State file exists (correct for retry 1)"
    if grep -q "\"retryCount\": 1" "$STATE_FILE"; then
        echo "    ✅ retryCount was incremented to 1"
    else
        echo "    ❌ Failed: retryCount not incremented in $STATE_FILE"
        cat "$STATE_FILE"
        exit 1
    fi
else
    echo "    ❌ Failed: $STATE_FILE was deleted too early"
    exit 1
fi

if [[ $EXIT_CODE -eq 0 ]]; then
    echo "    ✅ Exit code 0 confirmed"
else
    echo "    ❌ Failed: Expected exit code 0, got $EXIT_CODE"
    exit 1
fi

if [[ $RESULT == *"block"* ]]; then
    echo "    ✅ Output contains 'block' decision"
else
    echo "    ❌ Failed: Expected 'block' in output, got '$RESULT'"
    exit 1
fi

# Clean up
rm -f "$STATE_FILE"

echo "✨ All tests for py-quality-gate.js passed!"
