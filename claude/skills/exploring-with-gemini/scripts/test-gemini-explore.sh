#!/usr/bin/env bash
# Tests for gemini-explore.sh
# Mocks external dependencies to test validation, error handling, and parsing logic.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$SCRIPT_DIR/gemini-explore.sh"
POLICY="$SCRIPT_DIR/../policies/read-only-explorer.toml"
PASSED=0
FAILED=0
MOCK_DIR=$(mktemp -d /tmp/gemini-test-mocks.XXXXXX)

cleanup() { rm -rf "$MOCK_DIR"; }
trap cleanup EXIT

# --- Helpers ---

pass() { ((PASSED++)); echo "  PASS: $1"; }
fail() { ((FAILED++)); echo "  FAIL: $1 — $2"; }

run_script() {
  PATH="$MOCK_DIR:$PATH" "$SCRIPT" "$@" 2>/dev/null
}

run_script_stderr() {
  PATH="$MOCK_DIR:$PATH" "$SCRIPT" "$@" 2>&1
}

create_mock() {
  local name="$1"
  local content="$2"
  cat > "$MOCK_DIR/$name" <<MOCKSCRIPT
#!/usr/bin/env bash
$content
MOCKSCRIPT
  chmod +x "$MOCK_DIR/$name"
}

# =============================================================================
echo "=== Test: No prompt provided ==="
# =============================================================================

create_mock "gemini" "exit 0"
create_mock "jq" "exit 0"

set +e
PATH="$MOCK_DIR:$PATH" "$SCRIPT" 2>/dev/null
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -eq 1 ]]; then
  pass "exits with code 1 when no prompt"
else
  fail "exits with code 1 when no prompt" "got exit code $EXIT_CODE"
fi

OUTPUT=$(run_script_stderr || true)
if [[ "$OUTPUT" == *"No prompt provided"* ]]; then
  pass "shows usage message when no prompt"
else
  fail "shows usage message when no prompt" "got: $OUTPUT"
fi

# =============================================================================
echo "=== Test: Missing gemini CLI ==="
# =============================================================================

rm -f "$MOCK_DIR/gemini"

set +e
PATH="$MOCK_DIR:/usr/bin:/bin" "$SCRIPT" "test prompt" 2>/dev/null
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -eq 3 ]]; then
  pass "exits with code 3 when gemini not found"
else
  fail "exits with code 3 when gemini not found" "got exit code $EXIT_CODE"
fi

OUTPUT=$(PATH="$MOCK_DIR:/usr/bin:/bin" "$SCRIPT" "test prompt" 2>&1 || true)
if [[ "$OUTPUT" == *"gemini CLI is not installed"* ]]; then
  pass "shows gemini not found message"
else
  fail "shows gemini not found message" "got: $OUTPUT"
fi

# =============================================================================
echo "=== Test: Missing jq ==="
# =============================================================================

create_mock "gemini" "exit 0"
rm -f "$MOCK_DIR/jq"

SAFE_BIN="$MOCK_DIR/safe-bin"
mkdir -p "$SAFE_BIN"
for cmd in bash env cat rm mktemp command; do
  src=$(command -v "$cmd" 2>/dev/null) && ln -sf "$src" "$SAFE_BIN/" 2>/dev/null || true
done

set +e
PATH="$MOCK_DIR:$SAFE_BIN" "$SCRIPT" "test prompt" 2>/dev/null
EXIT_CODE=$?
set -e

rm -rf "$SAFE_BIN"

if [[ $EXIT_CODE -eq 3 ]]; then
  pass "exits with code 3 when jq not found"
else
  fail "exits with code 3 when jq not found" "got exit code $EXIT_CODE"
fi

# =============================================================================
echo "=== Test: Missing policy file ==="
# =============================================================================

create_mock "gemini" "exit 0"
create_mock "jq" "exit 0"

# Temporarily hide the policy file
mv "$POLICY" "$POLICY.bak"

set +e
PATH="$MOCK_DIR:$PATH" "$SCRIPT" "test prompt" 2>/dev/null
EXIT_CODE=$?
set -e

mv "$POLICY.bak" "$POLICY"

if [[ $EXIT_CODE -eq 3 ]]; then
  pass "exits with code 3 when policy file missing"
else
  fail "exits with code 3 when policy file missing" "got exit code $EXIT_CODE"
fi

# =============================================================================
echo "=== Test: Gemini CLI failure ==="
# =============================================================================

create_mock "gemini" "echo 'API error' >&2; exit 1"
create_mock "jq" 'cat'

set +e
PATH="$MOCK_DIR:$PATH" "$SCRIPT" "test prompt" 2>/dev/null
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -eq 1 ]]; then
  pass "exits with code 1 when gemini fails"
else
  fail "exits with code 1 when gemini fails" "got exit code $EXIT_CODE"
fi

OUTPUT=$(PATH="$MOCK_DIR:$PATH" "$SCRIPT" "test prompt" 2>&1 || true)
if [[ "$OUTPUT" == *"Gemini CLI failed"* ]]; then
  pass "shows failure message with details"
else
  fail "shows failure message with details" "got: $OUTPUT"
fi

# =============================================================================
echo "=== Test: Empty/null response ==="
# =============================================================================

create_mock "gemini" 'echo "{\"session_id\": \"abc\", \"response\": null}"'
create_mock "jq" "$(which jq) \"\$@\""

set +e
PATH="$MOCK_DIR:$PATH" "$SCRIPT" "test prompt" 2>/dev/null
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -eq 2 ]]; then
  pass "exits with code 2 when response is null"
else
  fail "exits with code 2 when response is null" "got exit code $EXIT_CODE"
fi

# =============================================================================
echo "=== Test: Successful response ==="
# =============================================================================

create_mock "gemini" 'echo "{\"session_id\": \"abc\", \"response\": \"Found 3 files matching the pattern.\"}"'

set +e
OUTPUT=$(PATH="$MOCK_DIR:$PATH" "$SCRIPT" "test prompt" 2>/dev/null)
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -eq 0 ]]; then
  pass "exits with code 0 on success"
else
  fail "exits with code 0 on success" "got exit code $EXIT_CODE"
fi

if [[ "$OUTPUT" == "Found 3 files matching the pattern." ]]; then
  pass "outputs only the response text"
else
  fail "outputs only the response text" "got: $OUTPUT"
fi

# =============================================================================
echo "=== Test: Custom model via env var ==="
# =============================================================================

create_mock "gemini" '
while [[ $# -gt 0 ]]; do
  case "$1" in
    -m) echo "{\"session_id\": \"abc\", \"response\": \"model=$2\"}"; exit 0 ;;
  esac
  shift
done
'

set +e
OUTPUT=$(GEMINI_EXPLORE_MODEL="gemini-3-flash" PATH="$MOCK_DIR:$PATH" "$SCRIPT" "test" 2>/dev/null)
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -eq 0 && "$OUTPUT" == "model=gemini-3-flash" ]]; then
  pass "respects GEMINI_EXPLORE_MODEL env var"
else
  fail "respects GEMINI_EXPLORE_MODEL env var" "got exit=$EXIT_CODE output=$OUTPUT"
fi

# =============================================================================
echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[[ $FAILED -eq 0 ]] && exit 0 || exit 1
