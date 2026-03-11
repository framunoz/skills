#!/bin/bash
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 [FILES]..."
    exit 1
fi
echo "--- Running nbstripout ---"
uvx nbstripout@latest --drop-empty-cells "$@"
