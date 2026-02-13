#!/usr/bin/env bash
# gemini-analyze.sh — Wrapper around Gemini CLI with token tracking
# Usage: tools/gemini-analyze.sh <category> "<prompt with @file refs>"
#        tools/gemini-analyze.sh --summary

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_FILE="${REPO_ROOT}/.claude/gemini-usage.log"

# ─── Summary mode ───────────────────────────────────────────────────
if [[ "${1:-}" == "--summary" ]]; then
    if [[ ! -f "$LOG_FILE" ]]; then
        echo "No usage data yet. Run some analyses first."
        exit 0
    fi

    total_calls=$(wc -l < "$LOG_FILE" | tr -d ' ')
    total_input=$(awk -F'|' '{gsub(/[^0-9]/,"",$3); sum+=$3} END{print sum}' "$LOG_FILE")
    total_output=$(awk -F'|' '{gsub(/[^0-9]/,"",$4); sum+=$3} END{print sum}' "$LOG_FILE")
    total_duration=$(awk -F'|' '{gsub(/[^0-9.]/,"",$6); sum+=$6} END{printf "%.1f", sum}' "$LOG_FILE")

    echo ""
    echo "Gemini CLI Usage Summary"
    echo "========================"
    echo "Total invocations:            ${total_calls}"
    printf "Total est. input tokens:      %'d\n" "$total_input"
    printf "Total est. output tokens:     %'d\n" "$total_output"
    echo "Total duration:               ${total_duration}s"
    echo ""
    echo "By category:"
    awk -F'|' '{
        cat = $2; gsub(/^ +| +$/, "", cat)
        gsub(/[^0-9]/, "", $3)
        counts[cat]++; tokens[cat]+=$3
    } END {
        for (c in counts) printf "  %-22s: %d calls, ~%d input tokens\n", c, counts[c], tokens[c]
    }' "$LOG_FILE" | sort
    echo ""
    exit 0
fi

# ─── Analysis mode ──────────────────────────────────────────────────
if [[ $# -lt 2 ]]; then
    echo "Usage: tools/gemini-analyze.sh <category> \"<prompt with @file refs>\""
    echo "       tools/gemini-analyze.sh --summary"
    echo ""
    echo "Categories: session-startup, pre-wp-research, pattern-check,"
    echo "            architecture, post-impl-verify, pr-review,"
    echo "            dependency-map, doc-gaps, custom"
    exit 1
fi

CATEGORY="$1"
PROMPT="$2"

# ─── Estimate input tokens from @-referenced files ──────────────────
estimate_input_tokens() {
    local prompt="$1"
    local total_chars=0

    # Extract @-referenced paths from the prompt
    local files
    files=$(echo "$prompt" | grep -oE '@[^ "]+' | sed 's/^@//' || true)

    for ref in $files; do
        local full_path="${REPO_ROOT}/${ref}"
        if [[ -d "$full_path" ]]; then
            # Directory: sum all text files
            local dir_chars
            dir_chars=$(find "$full_path" -type f \( -name "*.py" -o -name "*.toml" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.md" -o -name "*.txt" -o -name "*.cfg" \) -exec wc -c {} + 2>/dev/null | tail -1 | awk '{print $1}')
            total_chars=$((total_chars + ${dir_chars:-0}))
        elif [[ -f "$full_path" ]]; then
            # Single file
            local file_chars
            file_chars=$(wc -c < "$full_path" 2>/dev/null || echo 0)
            total_chars=$((total_chars + file_chars))
        fi
    done

    # Add prompt text itself
    local prompt_chars=${#prompt}
    total_chars=$((total_chars + prompt_chars))

    # Rough estimate: 1 token ≈ 4 characters
    echo $(( total_chars / 4 ))
}

# ─── Extract referenced file paths for logging ──────────────────────
extract_file_refs() {
    echo "$1" | grep -oE '@[^ "]+' | sed 's/^@//' | paste -sd',' - || echo "none"
}

# ─── Run Gemini ─────────────────────────────────────────────────────
input_est=$(estimate_input_tokens "$PROMPT")
file_refs=$(extract_file_refs "$PROMPT")

start_time=$(date +%s.%N 2>/dev/null || date +%s)

# Capture output while still printing it
output_file=$(mktemp)
trap 'rm -f "$output_file"' EXIT

# Run gemini with the prompt (cd to repo root so @ paths resolve correctly)
cd "$REPO_ROOT"
gemini -p "$PROMPT" 2>/dev/null | tee "$output_file"

end_time=$(date +%s.%N 2>/dev/null || date +%s)
duration=$(echo "$end_time - $start_time" | bc 2>/dev/null || echo "0")

# Estimate output tokens
output_chars=$(wc -c < "$output_file" | tr -d ' ')
output_est=$(( output_chars / 4 ))

# ─── Log the usage ──────────────────────────────────────────────────
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "${timestamp} | ${CATEGORY} | input_tokens_est: ${input_est} | output_tokens_est: ${output_est} | files: ${file_refs} | duration_sec: ${duration}" >> "$LOG_FILE"

# Print tracking info to stderr (doesn't pollute output)
>&2 echo ""
>&2 echo "--- Gemini Analysis Complete ---"
>&2 echo "Category:     ${CATEGORY}"
>&2 echo "Input est:    ~${input_est} tokens"
>&2 echo "Output est:   ~${output_est} tokens"
>&2 echo "Duration:     ${duration}s"
>&2 echo "Logged to:    .claude/gemini-usage.log"