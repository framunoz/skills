#!/bin/bash

# Simple test runner for block-env-read hook
HOOK_PATH="$(dirname "$0")/../block-env-read.js"

echo "🧪 Running Tests for block-env-read.js..."

# Test Case 1: Block .env read
echo "  [Test 1] Blocking .env read..."
RESULT=$(echo '{"tool_name": "Read", "tool_input": {"file_path": ".env"}}' | "$HOOK_PATH")
if [[ $RESULT == *"block"* ]]; then
    echo "    ✅ Passed"
else
    echo "    ❌ Failed: Expected 'block', got '$RESULT'"
    exit 1
fi

# Test Case 2: Allow .env.example read
echo "  [Test 2] Allowing .env.example read..."
RESULT=$(echo '{"tool_name": "Read", "tool_input": {"file_path": ".env.example"}}' | "$HOOK_PATH")
if [[ $RESULT == *"allow"* ]]; then
    echo "    ✅ Passed"
else
    echo "    ❌ Failed: Expected 'allow', got '$RESULT'"
    exit 1
fi

# Test Case 3: Block cat .env shell command
echo "  [Test 3] Blocking cat .env shell command..."
RESULT=$(echo '{"tool_name": "Bash", "tool_input": {"command": "cat .env"}}' | "$HOOK_PATH")
if [[ $RESULT == *"block"* ]]; then
    echo "    ✅ Passed"
else
    echo "    ❌ Failed: Expected 'block', got '$RESULT'"
    exit 1
fi

echo "✨ All tests for block-env-read.js passed!"
