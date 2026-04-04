#!/bin/bash

# Ported test runner for gemini/hooks/py-format-silent.js
# Synchronized with Claude's refined architecture (Stateless Formatter)

HOOK_PATH="$(dirname "$0")/../py-format-silent.js"
SESSION_ID="test_session_$(date +%s)"

echo "🧪 Running Tests for gemini py-format-silent.js..."

# Ensure we start clean
touch mock.py

# Test Case 1: Trigger on a mock .py file
echo "  [Test 1] Triggering on mock.py..."
RESULT=$(echo "{\"tool_name\": \"write_file\", \"session_id\": \"$SESSION_ID\", \"tool_input\": {\"file_path\": \"mock.py\"}}" | "$HOOK_PATH")

if [[ $RESULT == *"allow"* ]] && echo "$RESULT" | node "$(dirname "$0")/utils/schema-validator.js"; then
    echo "    ✅ Valid JSON output with 'allow' decision"
else
    echo "    ❌ Failed: Expected 'allow' and valid schema, got '$RESULT'"
    rm mock.py
    exit 1
fi

# Clean up
rm mock.py

echo "✨ Gemini py-format-silent.js verified (Stateless)!"
