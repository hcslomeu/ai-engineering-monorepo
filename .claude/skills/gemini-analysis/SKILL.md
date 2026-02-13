---
name: gemini-analysis
description: Delegate large codebase analysis tasks to Google Gemini CLI to preserve Claude context and tokens
user-invocable: true
---

# Skill: Gemini Codebase Analysis

Delegate large-scale codebase analysis, cross-module inspection, and session context building to Google Gemini CLI (`gemini`). This preserves Claude's context window for code generation, file editing, and git operations.

## When to Use

- When the user invokes `/gemini-analysis` with a task description
- When Claude identifies that a task would consume excessive context (3+ files of analysis)
- When the user needs a session briefing or architecture overview

## Decision Criteria: Gemini vs Claude

### Delegate to Gemini

| Scenario | Why Gemini |
|----------|-----------|
| Cross-module analysis (3+ files) | Avoids loading large context into Claude |
| Session startup summarization | Builds context without consuming Claude tokens |
| Pattern verification across codebase | Bulk file scanning is cheaper on Gemini |
| Pre-WP research | Explores existing patterns before Claude generates code |
| Large diff review | PR diffs can be huge; offload the read |
| Architecture overview | Reads all modules at once |
| Codebase audit (type hints, docstrings, TODOs) | Repetitive file-by-file checks |

### Keep in Claude

| Scenario | Why Claude |
|----------|-----------|
| Code generation and file writing | Claude has Write/Edit tools |
| Single file analysis | Fits in context easily |
| Git operations (commit, branch, PR) | Claude has Bash and gh access |
| Anything requiring action | Gemini is read-only analysis |
| Test execution and debugging | Claude can run commands |
| MCP server interactions | Only Claude has MCP access |

## Prerequisites

- Gemini CLI installed (`gemini --version` to verify)
- Gemini Pro account authenticated
- Wrapper script at `tools/gemini-analyze.sh` (provides token tracking)

## Command Templates

All commands use the wrapper script `tools/gemini-analyze.sh` for token tracking. The wrapper accepts a category label and a prompt string (with `@` file references).

### Session Startup / Handoff

Build context for a new Claude session without consuming Claude tokens.

```bash
tools/gemini-analyze.sh "session-startup" "@PROGRESS.md @CLAUDE.md @apps/alpha-whale/ @libs/py-core/ Provide a concise summary of: current project state, completed work packages, active modules and their purpose, and key patterns used. Format as a briefing for an AI coding assistant starting a new session."
```

### Pre-WP Research

Explore existing patterns before starting implementation.

```bash
tools/gemini-analyze.sh "pre-wp-research" "@apps/alpha-whale/ @libs/py-core/ I'm about to implement [FEATURE]. What existing patterns, utilities, and conventions should I follow? List relevant files and functions."
```

### Cross-Module Pattern Check

Verify code quality standards across the entire codebase.

```bash
tools/gemini-analyze.sh "pattern-check" "@apps/ @libs/ Check if all Python functions have type hints, all classes have docstrings, and error handling is consistent. Report any gaps."
```

### Architecture Overview

Generate a high-level architecture description.

```bash
tools/gemini-analyze.sh "architecture" "@apps/ @libs/ @infra/ Describe the architecture: what modules exist, how they depend on each other, what patterns are used (Medallion, tool-calling, etc). Include a dependency map."
```

### Post-Implementation Verification

Audit a module after completing implementation.

```bash
tools/gemini-analyze.sh "post-impl-verify" "@apps/alpha-whale/ Verify: all functions type-hinted, docstrings present, no TODO/FIXME left, error handling consistent, test coverage for public functions."
```

### PR Diff Analysis

Analyze a PR diff for quality issues.

```bash
git diff main...HEAD > /tmp/pr-diff.txt
tools/gemini-analyze.sh "pr-review" "@/tmp/pr-diff.txt Review this PR diff for: code quality, potential bugs, missing tests, security concerns, and adherence to conventional commit standards."
```

### Dependency / Import Analysis

Map internal dependencies across the monorepo.

```bash
tools/gemini-analyze.sh "dependency-map" "@apps/ @libs/ Map all internal imports between apps and libs. Identify circular dependencies, unused imports, and missing __init__.py exports."
```

### Documentation Gap Analysis

Find undocumented or under-documented modules.

```bash
tools/gemini-analyze.sh "doc-gaps" "@apps/ @libs/ @docs/ Compare actual code modules against MkDocs pages. Identify modules that are missing documentation or have outdated docs."
```

## Token Tracking

The wrapper script automatically tracks usage. Every invocation logs to `.claude/gemini-usage.log`.

### View Usage Summary

```bash
tools/gemini-analyze.sh --summary
```

### Log Format

Each entry in `.claude/gemini-usage.log`:

```
2026-02-13T14:30:00Z | session-startup | input_tokens_est: 12500 | output_tokens_est: 800 | files: apps/alpha-whale/,libs/py-core/ | duration_sec: 4.2
```

## Workflow Integration

When Claude identifies a task matching the "Delegate to Gemini" criteria:

1. **Suggest the command** to the user, with placeholders filled in
2. **User runs the command** in their terminal (or Claude runs via Bash)
3. **Output is used** to inform Claude's next action — code generation, planning, etc.

This keeps Gemini as the "reader" and Claude as the "writer."