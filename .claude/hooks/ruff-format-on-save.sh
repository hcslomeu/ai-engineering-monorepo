#!/bin/bash
set -euo pipefail

# Hook: Auto-lint and format Python files after Claude edits/writes them.
# Triggered by PostToolUse on Edit|Write events.
# Receives JSON on stdin with tool_input.file_path.
# Runs both ruff check (lint fixes like import sorting) and ruff format.

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only process non-empty paths pointing to Python files
if [[ -n "$FILE_PATH" && "$FILE_PATH" == *.py ]]; then
  poetry run ruff check --fix "$FILE_PATH" 2>/dev/null || true
  poetry run ruff format "$FILE_PATH"
fi

exit 0
