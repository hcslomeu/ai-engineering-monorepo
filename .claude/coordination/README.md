# Cross-Agent Coordination

This file defines how Claude Code and Codex should collaborate in this repository without stepping on each other.

## Shared Sources of Truth

- `CLAUDE.md` is the main instruction file for all agents
- `PROGRESS.md` is the main planning and project-status file
- This document defines the parallel-work protocol

## Core Rule

Split work by ownership first, not by speed.

Good splits:
- one agent implements backend code while the other updates tests or docs in different files
- one agent researches and writes a plan while the other stays read-only
- one agent reviews a diff while the other implements

Bad splits:
- both agents editing the same file at the same time
- both agents refactoring the same module independently
- both agents updating `PROGRESS.md` during the same task unless one change is clearly coordinated

## Scope Claim Protocol

Before making edits:

1. Read `git status --short`
2. Check whether another agent already has in-flight changes in the same files
3. Create or update your own ignored coordination note:
   - `.claude/coordination/claude.local.md`
   - `.claude/coordination/codex.local.md`
4. Record:
   - current task or WP
   - files you own
   - files you may read but will not edit
   - handoff notes or blockers

Never edit the other agent's `*.local.md` file.

## Handoff Format

Use this lightweight template in your own local note:

```md
# Agent: codex
- Task: WP-XXX short description
- Editing: path/a.py, path/b.ts
- Read-only: path/c.md
- Status: in_progress | blocked | done
- Notes: anything the other agent must know before touching these files
```

## Conflict Avoidance

- If another agent has modified a file you planned to edit, re-read that file before touching it
- If ownership becomes ambiguous, stop and re-split the work before editing
- For shared instruction files (`CLAUDE.md`, `PROGRESS.md`, `.gitignore`), prefer a single designated editor per task
- Keep changes narrow and atomic so rebasing or manual merge resolution stays cheap

## Completion

When your part is finished:

- update your local coordination note with `Status: done`
- include any follow-up steps or validation still needed
- if you touched project-planning state, make sure `PROGRESS.md` still matches reality
