#!/bin/bash

# Base directory for scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if at least one file is provided
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 [FILES]..."
    exit 1
fi

# Execute modular scripts passing all arguments correctly
"$SCRIPT_DIR/black.sh" "$@"
"$SCRIPT_DIR/ruff.sh" "$@"
"$SCRIPT_DIR/pyrefly.sh" "$@"

# Check if any .ipynb files are in the list
HAS_NOTEBOOK=false
for file in "$@"; do
    if [[ "$file" == *.ipynb ]]; then
        HAS_NOTEBOOK=true
        break
    fi
done

if [ "$HAS_NOTEBOOK" = true ]; then
    echo -e "\n--- Found Jupyter Notebook ---"
    echo "INFO: Use '$SCRIPT_DIR/nbstripout.sh [FILES]...' if you want to strip outputs."
fi
