---
name: claude-code-practices
description: Review and suggest advanced Claude Code features for the current workflow, including skills, MCP servers, hooks, and tool optimization
user-invocable: true
---

# Skill: Claude Code Best Practices

Proactively identify opportunities to use advanced Claude Code features during development. The goal is to help the developer learn and adopt these capabilities naturally as part of the workflow.

## When to Use

- **Periodically during development**: After completing a task or work package, review if any advanced features could improve the workflow
- **When the user asks**: Explicitly requested review of Claude Code usage
- **When patterns emerge**: If a task is repetitive or could be automated, suggest the right feature

## Features to Watch For

### 1. Custom Skills (.claude/skills/)

**What**: Reusable markdown instructions for repeatable tasks.

**Identify opportunities when:**
- A task follows a consistent pattern (e.g., creating a new library, setting up a new app)
- The user asks for the same kind of output more than twice
- A workflow has multiple steps that should always happen together

**Suggest creating a skill for:**
- New work package setup (branch, issue link, PR template)
- Code review checklists
- New library/app scaffolding
- Documentation generation patterns

### 2. MCP Servers

**What**: External tool integrations that extend Claude Code capabilities.

**Identify opportunities when:**
- The workflow involves external APIs or services
- Data needs to be fetched from third-party sources
- IDE integration could improve the experience

**Currently configured MCP servers:**
- `doc-gen` - Documentation generation
- `context7` - Library documentation lookup
- `ide` - VS Code diagnostics and code execution
- `claude.ai langchain` - LangChain docs search

**Suggest new MCP servers when:**
- A new external service is introduced (database, API, cloud provider)
- A community MCP server exists for a tool being used

### 3. Programmatic Tool Calling (PTC)

**What**: Chaining multiple tool calls autonomously for complex multi-step tasks.

**Identify opportunities when:**
- A task requires reading multiple files, analyzing them, and producing output
- Multi-step operations could be batched (e.g., "check all quality tools at once")
- Research tasks need multiple searches combined

**Best practices:**
- Let Claude chain: read files -> analyze -> generate output in one flow
- Use Task tool with subagents for independent parallel research
- Batch file reads when multiple files are needed for context

### 4. Tool Search

**What**: Discovering the right MCP tool from a large set of available tools.

**Identify opportunities when:**
- New MCP servers are added with many tools
- The user isn't sure which tool to use for a task
- A task could be done multiple ways with different tools

**Best practices:**
- Use descriptive tool names when configuring MCP servers
- Check available MCP tools before writing custom bash scripts

### 5. Hooks

**What**: Shell commands that execute automatically in response to Claude Code events.

**Identify opportunities when:**
- Quality checks should run automatically before commits
- Notifications should trigger after certain actions
- Pre-flight validation is needed before destructive operations

**Suggested hooks for this project:**
- Pre-commit: `poetry run ruff format . && poetry run ruff check .`
- Post-WP-completion: LinkedIn post generation reminder
- Verify size of context window from time to time and suggest /`compact` or `/clear` commands to improve performance

## Periodic Review Checklist

When reviewing Claude Code usage, check:

- [ ] Are there repetitive tasks that should be skills?
- [ ] Are all relevant MCP servers configured?
- [ ] Could any manual bash commands be replaced with MCP tools?
- [ ] Are there workflows that could benefit from hooks?
- [ ] Is the learning-context.md up to date with current mode and preferences?
- [ ] Are there new Claude Code features or Anthropic blog posts worth checking?

## Staying Updated

Periodically search for:
- Anthropic blog posts about Claude Code updates
- New MCP servers on the community registry
- Claude Code changelog and release notes
- Best practices shared by the developer community

**Search queries to use:**
- "Claude Code new features 2026"
- "Anthropic blog Claude Code"
- "MCP servers registry"
- "Claude Code hooks examples"