#!/bin/bash

# Simple test runner for py-format-silent hook
HOOK_PATH="$(dirname "$0")/../py-format-silent.js"
SESSION_ID="test_session_$(date +%s)"

echo "🧪 Running Tests for py-format-silent.js..."

# Create a temporary Python file with bad formatting
MOCK_FILE="$(pwd)/test_format_mock.py"
echo "x=1;y=2;z=3" > "$MOCK_FILE"

# Test Case 1: Trigger on a .py file - should return {} and format
echo "  [Test 1] Triggering on test_format_mock.py..."
RESULT=$(echo "{\"tool_name\": \"Write\", \"session_id\": \"$SESSION_ID\", \"tool_input\": {\"file_path\": \"$MOCK_FILE\"}}" | "$HOOK_PATH")

if [[ $RESULT == "{}" ]]; then
    echo "    ✅ Valid JSON output"
else
    echo "    ❌ Failed: Expected '{}', got '$RESULT'"
    rm -f "$MOCK_FILE"
    exit 1
fi

# Test Case 2: Non-Python file should be ignored
echo "  [Test 2] Ignoring non-Python file..."
RESULT=$(echo "{\"tool_name\": \"Write\", \"session_id\": \"$SESSION_ID\", \"tool_input\": {\"file_path\": \"test.js\"}}" | "$HOOK_PATH")

if [[ $RESULT == "{}" ]]; then
    echo "    ✅ Non-Python file ignored correctly"
else
    echo "    ❌ Failed: Expected '{}', got '$RESULT'"
    rm -f "$MOCK_FILE"
    exit 1
fi

# Test Case 3: Excluded path should be ignored
echo "  [Test 3] Ignoring excluded path (.venv)..."
RESULT=$(echo "{\"tool_name\": \"Write\", \"session_id\": \"$SESSION_ID\", \"tool_input\": {\"file_path\": \"/project/.venv/lib/site.py\"}}" | "$HOOK_PATH")

if [[ $RESULT == "{}" ]]; then
    echo "    ✅ Excluded path ignored correctly"
else
    echo "    ❌ Failed: Expected '{}', got '$RESULT'"
    rm -f "$MOCK_FILE"
    exit 1
fi

# Clean up
rm -f "$MOCK_FILE"

echo "✨ All tests for py-format-silent.js passed!"
