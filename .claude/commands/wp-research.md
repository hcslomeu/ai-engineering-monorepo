Perform Phase 1 (Research) for work package: $ARGUMENTS

## Instructions

1. Read `PROGRESS.md` to understand current project state and completed WPs
2. Fetch the GitHub issue for this WP: `gh issue view <number>`
3. Explore the codebase areas relevant to this WP using targeted Read calls
4. If the WP builds on an existing module (e.g., `apps/alpha-whale/agent/`), read key files there
5. If the WP introduces a new library or framework, use context7 or langchain MCP to fetch current docs
6. Check `.claude/specs/` for any prior research on related WPs

## Output

Write findings to `.claude/specs/<WP-number>-research.md` with:
- **What exists today**: Relevant files, patterns, dependencies
- **What the WP requires**: Based on the issue description
- **Key decisions to make**: Open questions for Phase 2 planning
- **Dependencies**: Libraries needed, config changes, etc.

## Rules

- Read-only phase: do NOT suggest code changes or improvements
- Do NOT launch Explore sub-agents if file paths are known — use Read directly
- Prefer `tools/gemini-analyze.sh` for broad codebase scans (3+ files)
- When done, suggest running `/clear` before Phase 2
