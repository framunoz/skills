#!/bin/bash

# Simple test runner for py-quality-gate hook
HOOK_PATH="$(dirname "$0")/../py-quality-gate.js"
SESSION_ID="test_session_$(date +%s)"
RETRY_FILE="/tmp/py-quality-retry-$SESSION_ID"
SKIP_FILE="/tmp/py-quality-skip-$SESSION_ID"
TIMEOUT_SEC=30
export CLAUDE_HOOKS_LOG_LEVEL=DEBUG

echo "🧪 Running Tests for py-quality-gate.js..."

# Ensure we start clean
rm -f "$RETRY_FILE" "$SKIP_FILE"

# Helper to run a command with timeout and capture output
# Usage: run_test "Test Name" "EnvVar=Value" "InputJSON"
run_test_cmd() {
    local test_name="$1"
    local env_vars="$2"
    local input_json="$3"
    
    echo "  [$test_name] Running..."
    
    # Run with timeout if available, otherwise just run
    # (Mac timeout might not be present, so we use a subshell if needed)
    if command -v timeout >/dev/null 2>&1; then
        VAL=$(echo "$input_json" | env $env_vars timeout $TIMEOUT_SEC "$HOOK_PATH" 2>&1)
    else
        # Basic subshell timeout for Mac
        VAL=$(echo "$input_json" | env $env_vars "$HOOK_PATH" 2>&1 &
             PID=$!; (sleep $TIMEOUT_SEC && kill -9 $PID >/dev/null 2>&1) &
             WATCHER=$!; wait $PID 2>/dev/null; kill $WATCHER >/dev/null 2>&1)
        # Re-run to capture output properly if didn't timeout (a bit hacky but works for bash)
        VAL=$(echo "$input_json" | env $env_vars "$HOOK_PATH" 2>&1)
    fi
    echo "$VAL"
}

# --- Test Case A: No environment variable set (Opt-in behavior) ---
INPUT_DEFAULT="{\"session_id\": \"$SESSION_ID\", \"hook_event_name\": \"Stop\", \"cwd\": \"$(pwd)\"}"

echo "  [Test A1] No env var - should skip with warning on first run..."
RESULT_A1=$(echo "$INPUT_DEFAULT" | env -u CLAUDE_HOOKS_PY_QUALITY_DIRS -u HOOKS_PY_QUALITY_DIRS "$HOOK_PATH" 2>&1)

if [[ $RESULT_A1 == *"py-quality-gate is DISABLED"* ]] && [[ $RESULT_A1 == *"block"* ]]; then
    echo "    ✅ Output has 'block' decision and Warning found"
else
    echo "    ❌ Failed: Expected warning and 'block' decision, got: '$RESULT_A1'"
    exit 1
fi

if [[ -f "$SKIP_FILE" ]]; then
    echo "    ✅ Skip sentinel file created"
else
    echo "    ❌ Failed: Skip sentinel file not created"
    exit 1
fi

echo "  [Test A2] No env var - should skip SILENTLY on second run..."
RESULT_A2=$(echo "$INPUT_DEFAULT" | env -u CLAUDE_HOOKS_PY_QUALITY_DIRS -u HOOKS_PY_QUALITY_DIRS "$HOOK_PATH" 2>&1)

if [[ $RESULT_A2 == *"py-quality-gate is DISABLED"* ]]; then
    echo "    ❌ Failed: Warning message should NOT appear on second run"
    exit 1
else
    echo "    ✅ No warning message on second run (silent skip)"
fi

# Clean up skip file for next tests
rm -f "$SKIP_FILE"

# --- Test Case B: Invalid paths ---
echo "  [Test B] Invalid path - should warn and skip..."
RESULT_B=$(echo "$INPUT_DEFAULT" | CLAUDE_HOOKS_PY_QUALITY_DIRS="nonexistent_dir_xyz" "$HOOK_PATH" 2>&1)

if [[ $RESULT_B == *"block"* ]] && [[ $RESULT_B == *"Path does not exist"* ]]; then
    echo "    ✅ Correctly warned about invalid path and blocked for recommendation"
else
    echo "    ❌ Failed: Expected warning and 'block' decision, got: '$RESULT_B'"
    exit 1
fi

# --- Test Case C: Valid scoped path (Retry logic test) ---
FIXTURES_DIR="hooks/tests/fixtures"
if [[ ! -d "$FIXTURES_DIR" ]]; then
    FIXTURES_DIR="."
fi

echo "  [Test C] Valid path ($FIXTURES_DIR) - should run diagnostics..."
# Ensure we start clean for retry tests
rm -f "$RETRY_FILE"

# First run: should detect errors if any and block
echo "    [C1] First run - detecting..."
RESULT_C1=$(echo "$INPUT_DEFAULT" | CLAUDE_HOOKS_PY_QUALITY_DIRS="$FIXTURES_DIR" "$HOOK_PATH" 2>&1)

if [[ $RESULT_C1 == *"block"* ]]; then
    echo "      ✅ Output contains 'block' decision (Issues detected as expected)"
    
    if [[ -f "$RETRY_FILE" ]]; then
        RETRY_COUNT=$(cat "$RETRY_FILE")
        echo "      ✅ Retry file created with count: $RETRY_COUNT"
    else
        echo "      ❌ Failed: Retry file not created at $RETRY_FILE"
        exit 1
    fi

    # Second run
    echo "    [C2] Second run - simulating retry..."
    RESULT_C2=$(echo "$INPUT_DEFAULT" | CLAUDE_HOOKS_PY_QUALITY_DIRS="$FIXTURES_DIR" "$HOOK_PATH" 2>&1)
    if [[ $RESULT_C2 == *"block"* ]]; then
        RETRY_COUNT=$(cat "$RETRY_FILE")
        echo "      ✅ Still blocking, retry count: $RETRY_COUNT"
    else
        echo "      ❌ Failed: Expected 'block', got '$RESULT_C2'"
        exit 1
    fi
else
    if [[ $RESULT_C1 == *"{}"* ]]; then
        echo "      ✅ No errors found in $FIXTURES_DIR (clean scope, allow confirmed)"
    else
        echo "      ❌ Failed: Unexpected result: '$RESULT_C1'"
        exit 1
    fi
fi

# Clean up
rm -f "$RETRY_FILE" "$SKIP_FILE"

echo "✨ All tests for py-quality-gate.js passed!"
