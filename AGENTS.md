# AGENTS.md

This repository uses [CLAUDE.md](/Users/humbertolomeu/ai-engineering-monorepo/CLAUDE.md) as the canonical instruction file for all coding agents, including Codex.

## Startup Order

Before starting any non-trivial task, read these files in order:

```bash
cat CLAUDE.md
cat PROGRESS.md
cat .claude/coordination/README.md
```

If they exist and are relevant to the current task, also read:

```bash
cat .claude/learning-progress.md
cat .claude/learning-context.md
```

## Source of Truth

- [CLAUDE.md](/Users/humbertolomeu/ai-engineering-monorepo/CLAUDE.md) contains the main repository instructions
- [PROGRESS.md](/Users/humbertolomeu/ai-engineering-monorepo/PROGRESS.md) contains project status, planning context, and WP history
- `.claude/skills/` and `.claude/commands/` contain reusable workflows and should be treated as reference material for repeated tasks

## Codex Translation Notes

Some instructions in `CLAUDE.md` are Claude-specific. In Codex, follow the intent of those rules using native Codex workflows:

- `Read` / `Write` / `Edit` tool references map to shell reads plus `apply_patch`
- Claude sub-agents map to Codex delegated agents only when the work is truly parallel and independent
- Claude slash commands in `.claude/commands/` are not executable in Codex, but the markdown files still define the intended workflow
- Claude skills in `.claude/skills/` remain useful repository knowledge and should be consulted when relevant

## Parallel Work With Claude Code

When Claude Code and Codex are active at the same time:

- Follow `.claude/coordination/README.md`
- Treat `CLAUDE.md` and `PROGRESS.md` as shared, high-signal files and edit them carefully
- Prefer splitting work by module or file ownership
- Do not overwrite another agent's in-progress changes; inspect `git status` and diffs first
- Use separate ignored local notes under `.claude/coordination/` for active scope claims and handoffs
