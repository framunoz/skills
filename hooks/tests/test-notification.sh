#!/bin/bash
# test-notification.sh - Test script for notification hook

# Ensure the script directory is the working directory
cd "$(dirname "$0")"

# Check if node is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required to run these tests."
    exit 1
fi

echo "🧪 Testing notification hook..."
echo ""

# Test 1: Basic notification
echo "Test 1: Basic notification"
echo '{"notification": {"title": "Test", "message": "Hello from Claude Code"}}' | node ../notification.js
if [ $? -eq 0 ]; then
    echo "✅ Pass: Basic notification processed"
else
    echo "❌ Fail: Basic notification failed"
fi
echo ""

# Test 2: Notification with subtitle
echo "Test 2: Notification with subtitle"
echo '{"notification": {"title": "Test Title", "message": "Main message", "subtitle": "Subtitle here"}}' | node ../notification.js
if [ $? -eq 0 ]; then
    echo "✅ Pass: Notification with subtitle processed"
else
    echo "❌ Fail: Notification with subtitle failed"
fi
echo ""

# Test 3: Empty notification (uses defaults)
echo "Test 3: Empty notification (defaults)"
echo '{}' | node ../notification.js
if [ $? -eq 0 ]; then
    echo "✅ Pass: Default notification processed"
else
    echo "❌ Fail: Default notification failed"
fi
echo ""

# Test 4: Special characters in message
echo "Test 4: Special characters in message"
echo '{"notification": {"title": "Test `backticks`", "message": "Message with \"quotes\" and '\''apostrophes'\''"}}' | node ../notification.js
if [ $? -eq 0 ]; then
    echo "✅ Pass: Special characters handled"
else
    echo "❌ Fail: Special characters failed"
fi
echo ""

echo "🎉 All tests completed!"