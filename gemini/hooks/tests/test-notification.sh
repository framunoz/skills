#!/bin/bash

# Simple test runner for gemini/hooks/notification.js
HOOK_PATH="$(dirname "$0")/../notification.js"

echo "🧪 Running Tests for Gemini notification.js (Synchronized Spec)..."

# Test Case 1: Standard notification payload (Official Spec)
echo "  [Test 1] Official Spec (notification_type)..."
RESULT=$(echo '{"notification_type": "ToolPermission", "message": "Allow ls tool?"}' | "$HOOK_PATH")

if [[ $RESULT == *"allow"* ]]; then
    echo "    ✅ Passed (JSON Output: $RESULT)"
else
    echo "    ❌ Failed: Expected 'allow', got '$RESULT'"
    exit 1
fi

echo "✨ Gemini notification.js verified with official schema!"
