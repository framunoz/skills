#!/bin/bash
# test-safe-git.sh - Entry point for safe-git-commit hook tests

# Ensure the script directory is the working directory
cd "$(dirname "$0")"

# Check if node is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required to run these tests."
    exit 1
fi

# Run the robust Node.js test suite
node test-safe-git.js
exit $?
