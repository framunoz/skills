#!/usr/bin/env bash
# gemini-explore.sh — Wrapper for invoking Gemini CLI in read-only exploration mode.
# Used by the exploring-with-gemini skill.
#
# Usage: gemini-explore.sh "<prompt>"
# Exit codes: 0 = success, 1 = gemini error, 2 = empty response, 3 = missing dependency

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
POLICY="$BASE_DIR/policies/read-only-explorer.toml"
MODEL="${GEMINI_EXPLORE_MODEL:-gemini-2.5-flash}"
STDERR_LOG=$(mktemp /tmp/gemini-stderr.XXXXXX)

cleanup() { rm -f "$STDERR_LOG"; }
trap cleanup EXIT

# --- Validate dependencies ---
if ! command -v gemini &>/dev/null; then
  echo "ERROR: gemini CLI is not installed or not in PATH" >&2
  exit 3
fi

if ! command -v jq &>/dev/null; then
  echo "ERROR: jq is not installed or not in PATH" >&2
  exit 3
fi

if [[ ! -f "$POLICY" ]]; then
  echo "ERROR: Policy file not found at $POLICY" >&2
  exit 3
fi

# --- Validate input ---
PROMPT="${1:-}"
if [[ -z "$PROMPT" ]]; then
  echo "ERROR: No prompt provided. Usage: gemini-explore.sh \"<prompt>\"" >&2
  exit 1
fi

# --- Execute ---
OUTPUT=$(gemini -m "$MODEL" --policy "$POLICY" -p "$PROMPT" -o json 2>"$STDERR_LOG") || {
  EXIT_CODE=$?
  echo "ERROR: Gemini CLI failed (exit code $EXIT_CODE):" >&2
  cat "$STDERR_LOG" >&2
  exit 1
}

# --- Parse response ---
RESPONSE=$(echo "$OUTPUT" | jq -r '.response // empty')

if [[ -z "$RESPONSE" ]]; then
  echo "ERROR: Gemini returned no response (null or empty)" >&2
  echo "Raw output: $OUTPUT" >&2
  exit 2
fi

echo "$RESPONSE"
