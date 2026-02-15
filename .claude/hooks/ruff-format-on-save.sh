#!/bin/bash
# Hook: Auto-format Python files after Claude edits/writes them.
# Triggered by PostToolUse on Edit|Write events.
# Receives JSON on stdin with tool_input.file_path.

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only format Python files
if [[ "$FILE_PATH" == *.py ]]; then
  poetry run ruff format "$FILE_PATH" 2>/dev/null
fi

exit 0