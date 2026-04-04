#!/bin/bash

# Ported test runner for gemini/hooks/py-quality-gate.js
# Synchronized with Claude's refined architecture (Scoped Directories + Opt-in)

HOOK_PATH="$(dirname "$0")/../py-quality-gate.js"
VALIDATOR_PATH="node $(dirname "$0")/utils/schema-validator.js"
SESSION_ID="gemini_test_$(date +%s)"
RETRY_PREFIX="py-quality-retry-"
SKIP_PREFIX="py-quality-skip-"
TMP_DIR="/tmp"

RETRY_FILE="$TMP_DIR/$RETRY_PREFIX$SESSION_ID"
SKIP_FILE="$TMP_DIR/$SKIP_PREFIX$SESSION_ID"

export GEMINI_HOOKS_LOG_LEVEL=DEBUG

echo "🧪 Running Synchronized Tests for Gemini py-quality-gate.js..."

# Ensure we start clean
rm -f "$RETRY_FILE" "$SKIP_FILE"

# --- Test Case A: No environment variable set (Opt-in behavior) ---
INPUT_DEFAULT="{\"session_id\": \"$SESSION_ID\", \"hook_event_name\": \"AfterAgent\", \"cwd\": \"$(pwd)\"}"

echo "  [Test A1] No env var - should skip with warning and block on first run..."
# Unset both possible var names
RESULT_A1=$(echo "$INPUT_DEFAULT" | env -u GEMINI_HOOKS_PY_QUALITY_DIRS -u HOOKS_PY_QUALITY_DIRS "$HOOK_PATH" 2>&1)

if [[ $RESULT_A1 == *"py-quality-gate is DISABLED"* ]] && [[ $RESULT_A1 == *"deny"* ]]; then
    echo "    ✅ Output has 'deny' decision and Warning found"
else
    echo "    ❌ Failed: Expected warning and 'deny' decision, got: '$RESULT_A1'"
    exit 1
fi

if [[ -f "$SKIP_FILE" ]]; then
    echo "    ✅ Skip sentinel file created"
else
    echo "    ❌ Failed: Skip sentinel file not created at $SKIP_FILE"
    exit 1
fi

echo "  [Test A2] No env var - should skip SILENTLY on second run..."
RESULT_A2=$(echo "$INPUT_DEFAULT" | env -u GEMINI_HOOKS_PY_QUALITY_DIRS -u HOOKS_PY_QUALITY_DIRS "$HOOK_PATH" 2>&1)

if [[ $RESULT_A2 == *"py-quality-gate is DISABLED"* ]]; then
    echo "    ❌ Failed: Warning message should NOT appear on second run"
    exit 1
else
    echo "    ✅ No warning message on second run (silent skip)"
fi

# Clean up skip file for next tests
rm -f "$SKIP_FILE"

# --- Test Case B: Invalid paths ---
echo "  [Test B] Invalid path - should warn and block..."
RESULT_B=$(echo "$INPUT_DEFAULT" | GEMINI_HOOKS_PY_QUALITY_DIRS="nonexistent_dir_xyz" "$HOOK_PATH" 2>&1)

if [[ $RESULT_B == *"deny"* ]] && [[ $RESULT_B == *"Path does not exist"* ]]; then
    echo "    ✅ Correctly warned about invalid path and blocked for recommendation"
else
    echo "    ❌ Failed: Expected warning and 'deny' decision, got: '$RESULT_B'"
    exit 1
fi

# --- Test Case C: Valid scoped path (Retry logic test) ---
# We use the current directory as fixture if nothing else works
FIXTURES_DIR="."

echo "  [Test C] Valid path ($FIXTURES_DIR) - should run diagnostics..."
rm -f "$RETRY_FILE"

# Test C1: First run with errors
echo "    [C1] First run - simulating detection..."
# We create a temporary bad file in a subdir to avoid polluting the workspace too much
TEST_SCOPE="/tmp/gemini-quality-scope-$$"
mkdir -p "$TEST_SCOPE"
echo "print(undefined_var)" > "$TEST_SCOPE/bad.py"

RESULT_C1=$(echo "$INPUT_DEFAULT" | GEMINI_HOOKS_PY_QUALITY_DIRS="$TEST_SCOPE" "$HOOK_PATH" 2>&1)
EXIT_CODE_C1=$?

if [[ $RESULT_C1 == *"deny"* ]] && [[ $EXIT_CODE_C1 -eq 2 ]]; then
    echo "      ✅ Output contains 'deny' decision and Exit 2 (Issues detected)"
    
    if [[ -f "$RETRY_FILE" ]]; then
        RETRY_COUNT=$(cat "$RETRY_FILE")
        echo "      ✅ Retry count file created: $RETRY_COUNT"
    else
        echo "      ❌ Failed: Retry count file not created"
        exit 1
    fi

    # Test C2: Second run (increment)
    echo "    [C2] Second run - incrementing retry..."
    RESULT_C2=$(echo "$INPUT_DEFAULT" | GEMINI_HOOKS_PY_QUALITY_DIRS="$TEST_SCOPE" "$HOOK_PATH" 2>&1)
    RETRY_COUNT_2=$(cat "$RETRY_FILE")
    if [[ $RETRY_COUNT_2 -eq 2 ]]; then
        echo "      ✅ Retry count incremented to 2"
    else
        echo "      ❌ Failed: Retry count expected 2, got $RETRY_COUNT_2"
        exit 1
    fi
else
    echo "      ❌ Failed: Expected 'deny' and Exit 2, got '$RESULT_C1' (Exit $EXIT_CODE_C1)"
    exit 1
fi

# --- Test Case D: Context limit truncation ---
echo "  [Test D] Truncation - generating 15 errors..."
# Generate 15 undefined variable errors (not auto-fixable by ruff check --fix)
for i in {1..15}; do
    echo "print(undefined_var_$i)" >> "$TEST_SCOPE/bad.py"
done
# Run with a limit of 5 lines
RESULT_D=$(echo "$INPUT_DEFAULT" | GEMINI_HOOKS_PY_QUALITY_DIRS="$TEST_SCOPE" GEMINI_HOOKS_PY_QUALITY_LIMIT=5 "$HOOK_PATH" 2>&1)

if [[ $RESULT_D == *"[AND "* ]] && [[ $RESULT_D == *"MORE LINES HIDDEN TO SAVE CONTEXT]"* ]]; then
    echo "    ✅ Correctly truncated output and found hidden lines warning"
else
    echo "    ❌ Failed: Expected truncation text not found in output."
    exit 1
fi

# Clean up
rm -rf "$TEST_SCOPE"
rm -f "$RETRY_FILE" "$SKIP_FILE"

echo "✨ Gemini py-quality-gate logic verified against Claude Ground Truth!"
