# Claude Code Commands

Lightweight prompt templates that become slash commands via `/project:<name>`.

## How It Works

Each `.md` file in this folder is invokable as `/project:filename` (without the `.md` extension).
Use `$ARGUMENTS` as a placeholder for dynamic input passed after the command.

**Example**: `/project:wp-research WP-106 LangSmith Observability`

## Promotion to Skills

Commands are the testing ground for prompts. When a command:
- Needs supporting files (templates, examples, scripts)
- Requires multi-step validation or state tracking
- Has grown beyond a single markdown file

...promote it to a full skill in `.claude/skills/`.

## Current Commands

| Command | Invoke | Purpose |
|---------|--------|---------|
| `wp-research` | `/project:wp-research <WP-number> <title>` | Phase 1 research for a new work package |
| `quick-review` | `/project:quick-review <file-or-module>` | Quick code quality review of a file or module |