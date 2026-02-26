# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Before Starting Any Task

Always read these files first to understand current progress and context:
```bash
cat PROGRESS.md
cat .claude/learning-progress.md
cat .claude/learning-context.md
```

**Check learning mode**: Read the `Learning Mode` section in `.claude/learning-context.md`.

- If set to `LEARNING`:
  - ALWAYS use the file writing tool (`write_file`, `edit_file`) to create or modify files
  - NEVER paste full file contents or code blocks into the chat — the diff view handles code display
  - After writing each file (which triggers the VS Code diff view), provide a `## Code Walkthrough` in chat explaining purpose, key functions, idioms, and gotchas
  - Use analogies for abstract concepts
  - Wait for user confirmation before proceeding to the next file

- If set to `PRODUCTION`: generate code efficiently without walkthroughs

---

## Project Overview

**ai-engineering-monorepo** is an enterprise-grade AI Engineering Monorepo designed for hands-on learning and production-ready implementations. It combines Python (AI/ML, Data Engineering) and TypeScript (React frontends) in a hybrid workspace orchestrated by Nx.

### The Three Projects

| Project | Domain | Key Technologies |
|---------|--------|------------------|
| **AlphaWhale** | Finance | BigQuery, Airflow, Databricks, LangGraph, WhatsApp (Evolution API) |
| **MediGuard** | Healthcare | FHIR APIs, Hugging Face (PII masking), AWS S3/Lambda, LlamaIndex |
| **RailSense** | Transportation | Kafka (Darwin feeds), PyTorch LSTM, Supabase, CrewAI |

---

## Architecture Principles

### Medallion Architecture (Data)

All data pipelines follow Bronze → Silver → Gold:

| Layer | Purpose | Example |
|-------|---------|---------|
| **Bronze** | Raw ingestion, no transformation | Raw API responses, Kafka messages |
| **Silver** | Cleaned, conformed, deduplicated | Validated schemas, standardised timestamps |
| **Gold** | Feature-ready, vector-ready | Aggregations, embeddings, ML features |

### Agentic Reliability

- Use **LangGraph** for stateful control and human-in-the-loop gates
- All workflows must be traced via **LangSmith**
- Implement proper error handling and retry logic

### Data Contracts

- **Source of truth:** JSON Schema in `libs/schemas/definitions/`
- **Python:** Generated Pydantic models in `libs/schemas/generated/python/`
- **TypeScript:** Generated Zod schemas in `libs/schemas/generated/typescript/`

---

## Development Workflow

### Phase Approach (for non-trivial WPs)

Follow three phases with `/clear` between each to manage context:

**Phase 1 — Research** (read-only)
- Explore codebase to understand what exists today
- Use `tools/gemini-analyze.sh` or targeted Read calls
- Document findings, don't suggest improvements
- Output: write findings to `.claude/specs/WP-XXX-research.md`
- Run `/clear` when done

**Phase 2 — Plan** (interactive)
- Read the research file from Phase 1
- Write implementation plan with phased approach
- Each phase must have success criteria (automated + manual)
- Include a "What We're NOT Doing" section to prevent scope creep
- Resolve ALL open questions before proceeding — if uncertain, ask
- Get user confirmation before moving to implementation
- Output: write plan to `.claude/specs/WP-XXX-plan.md`
- Run `/clear` when done

**Phase 3 — Implement** (code + verify)
- Read the plan file from Phase 2
- In LEARNING mode: ALWAYS USE DIFF VIEW and explain BLOCKS of code for each file before creating it, referencing by line numbers, wait for user confirmation before continue
- Follow the plan phase by phase
- Run tests after each phase — don't proceed if tests fail
- If reality doesn't match the plan, STOP and communicate:
  "Expected: X. Found: Y. How should I proceed?"
- AVOID to print large files in the chat, only print shorter bits of code, like functions

<!-- For trivial tasks (typo, single-file fix, config change): skip directly to implement. -->

### Phase Output Files

Each WP's research and plans are saved to `.claude/specs/`:
- `.claude/specs/WP-XXX-research.md` — Research findings (Phase 1 output)
- `.claude/specs/WP-XXX-plan.md` — Implementation plan (Phase 2 output)

These files persist between `/clear` calls and across sessions.

### Before Committing

Always run the quality checks:
```bash
# Python quality checks
poetry run ruff check .                    # Linting
poetry run ruff format --check .           # Format check
poetry run mypy libs apps pipelines        # Type checking
poetry run bandit -r libs apps pipelines   # Security scan
poetry run pytest                          # Tests

# TypeScript quality checks (when applicable)
pnpm nx run-many -t lint
pnpm nx run-many -t test
```

### Creating a New Python Library

1. Create the folder structure:
```bash
   mkdir -p libs/py-newlib/src/py_newlib
   mkdir -p libs/py-newlib/tests
```

2. Create `libs/py-newlib/pyproject.toml`

3. Create `libs/py-newlib/project.json` for Nx integration

4. Add path dependency to root if needed

### Creating a New TypeScript Package
```bash
pnpm nx g @nx/js:lib libs/<package-name> --publishable --importPath=@ai-engineering-monorepo/<package-name>
```

### Engineering Principles

These four principles guide all code decisions in this project:

| Principle | Rule | In Practice |
|-----------|------|-------------|
| **DRY** | Don't Repeat Yourself | Search codebase for existing functions before creating new ones. Extract shared logic into `libs/` |
| **KISS** | Keep It Simple | Prefer the simplest solution that works. Three similar lines > premature abstraction |
| **YAGNI** | You Aren't Gonna Need It | Only build what's requested. Don't design for hypothetical future requirements |
| **SoC** | Separation of Concerns | One module, one purpose. Keep data, logic, and presentation in distinct layers |

### Security-First Engineering

Security is a design constraint, not an afterthought. Apply these rules during code generation:

**Zero-Trust Logic:**
- Never trust client-side data. Re-validate prices, quantities, permissions on the backend (FastAPI endpoint level)
- Authorization must check resource ownership (`user_id`), not just authentication status
- Use parameterized queries for all database operations (SQLAlchemy/BigQuery). Never interpolate user input into queries
- Sanitize frontend inputs with appropriate escaping (DOMPurify for HTML, Zod schemas for form data)

**Secret Management:**
- Never hardcode API keys, tokens, or credentials. Use `SecretStr` (Pydantic) and environment variables
- Verify `.env`, `.pem`, credentials files are in `.gitignore` before committing
- If generated code contains a hardcoded secret, stop and refactor to use env vars immediately

**Secure Defaults:**
- CORS: use explicit origin allowlists, never wildcard `*` in production configs
- Use HTTPS URLs for all external API calls
- Implement rate limiting on public-facing endpoints

**Dependency Hygiene:**
- Before adding a new library, verify it exists on PyPI/npm and check its maintenance status
- Prefer established libraries with security track records (e.g., argon2-cffi over hashlib for passwords)
- Pin dependency versions in lockfiles

**Frontend & Design System Protection:**
- Enforce security headers in Next.js config (`next.config.ts`): `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`
- Implement Content Security Policy (CSP) using nonce-based script allowlisting — never `unsafe-inline` or `unsafe-eval`
- Protect design system assets: use Subresource Integrity (SRI) hashes for any CDN-loaded fonts, icons, or scripts
- Prevent CSS injection: never interpolate user input into `style` attributes or CSS custom properties
- Disable source maps in production builds (`productionBrowserSourceMaps: false` in Next.js config)
- Protect against clickjacking: use `X-Frame-Options` and CSP `frame-ancestors` to block embedding in unauthorized origins

**Post-Generation Security Review:**
- After writing auth, payment, or data-handling code, perform a "Bug Hunter" pass: "How would a malicious user bypass this or access another user's data?"
- Ensure structured logs (structlog) never include raw secrets, tokens, or PII — use redaction

### Anti-Patterns to Avoid

- **Violating DRY**: Check for existing libraries/utilities before building from scratch
- **Violating KISS**: Don't add features, refactor code, or make "improvements" beyond what was asked. Don't create helpers or abstractions for one-time operations
- **Violating YAGNI**: If it's not in the plan, don't build it. Add it to a future WP instead
- **Violating SoC**: Don't add unrelated code to a file. Don't mix data access with business logic
- **Knowledge gaps**: Use context7/langchain MCP for current docs. Don't guess at APIs
- **Security shortcuts**: Don't disable CORS, skip input validation, or use `verify=False` on HTTP requests to "make it work"

### Verification

- After implementing any code change, run the relevant test suite to verify
- If no tests exist for the changed code, write them
- Separate success criteria into automated (commands) and manual (human testing)

### Context Hygiene

- Run `/clear` between phases and between unrelated tasks
- When compacting, preserve: modified file paths, current WP number, test commands
- Discard exploration output and MCP lookup results during compaction

---

## Git Workflow

```bash
# Create feature branch (use WP-XXX prefix)
git checkout -b feature/WP-XXX-short-description

# Commit with conventional commits
git commit -m "feat(scope): description"
git commit -m "fix(scope): description"
git commit -m "chore(scope): description"

# Create PR linking to issue
gh pr create --title "feat: WP-XXX description" --body "Closes #XX"
```

### Git Commit Guidelines

When committing, staging, or pushing is necessary:

- **Provide git commands as text** for the user to copy and run, rather than executing them directly. This saves tokens and gives the user control.
- **No co-authorship**: Do not add `Co-Authored-By` lines to commit messages. The developer is the sole author.
- **Conventional commits**: Always use the format `type(scope): description` as shown above.
- Avoid line breakers on git add commands because this affects the format after pasting on terminal and fails when executed
- Subject line under 72 characters, imperative mood.
- Reference WP numbers when applicable.

---

## GitHub Project

Issues are tracked at: https://github.com/hcslomeu/ai-engineering-monorepo/issues

Work packages follow the pattern: `WP-XXX: Title`

- **WP-001 to WP-006**: Foundation phase
- **WP-101 to WP-108**: AlphaWhale
- **WP-201 to WP-208**: MediGuard
- **WP-301 to WP-309**: RailSense

### Work Package Completion Checklist

When a work package is marked as completed:

1. Update `PROGRESS.md` with completion date and notes
2. Update `.claude/learning-progress.md` with new skills learned
3. Generate a LinkedIn post using the skill in `.claude/skills/generate-linkedin-post.md`
4. Save the post to `.claude/linkedin-posts/WP-XXX-short-title.md`
5. Suggest: "Consider generating a prompt for a diagram for this post using Gemini Banana (this will save Claude tokens)"

---

## Testing Strategy

| Test Type | Location | Purpose |
|-----------|----------|---------|
| **Unit tests** | `libs/*/tests/`, `apps/*/tests/` | Test individual functions/classes |
| **Integration tests** | `tests/integration/` | Test component interactions |
| **E2E tests** | `tests/e2e/` | Test full workflows |

Run specific test categories:
```bash
# Unit tests only
poetry run pytest libs apps pipelines

# Integration tests only
poetry run pytest tests/integration

# All tests with coverage
poetry run pytest --cov=libs --cov=apps --cov-report=html
```

---

## Claude Code Configuration

This project uses a `.claude/` folder for Claude Code configuration:

```
.claude/
├── commands/             # Lightweight prompt templates → /project:name (committed)
├── skills/               # Complex workflow skills (committed)
├── specs/                # WP research and plan files (committed)
├── linkedin-posts/       # Generated LinkedIn posts (committed)
├── learning-context.md   # Session preferences (gitignored)
└── learning-progress.md  # Skills development tracker (gitignored)
```

**Commands vs Skills**: Commands in `.claude/commands/` are simple prompt templates (invokable as `/project:name`). When a command grows into a multi-step workflow, promote it to a full skill in `.claude/skills/`.

Private files in `.claude/` are gitignored and contain personal learning context.

### MCP Servers

The following MCP servers are configured and should be used in these scenarios:

| Server | When to Use | Status |
|--------|-------------|--------|
| **context7** | Fetch up-to-date library docs (LangChain, FastAPI, pytest, etc.) | Active |
| **langchain (Docs by LangChain)** | LangChain/LangGraph-specific API reference and patterns | Active |
| **ide** | VS Code diagnostics (`getDiagnostics`) and Jupyter kernel execution | Active |
| **railway-mcp-server** | Railway deployment, logs, environment management | Active |
| **doc-gen** | Documentation structure generation | Deprecated (will be archived) |

**Prefer MCP lookups over pasting docs** — use context7 or langchain to fetch reference material instead of copying documentation into the conversation. This keeps context clean and ensures up-to-date information.

### Custom Skills

Skills in `.claude/skills/` automate repeated workflows:

| Skill | Purpose | Invoke |
|-------|---------|--------|
| **generate-linkedin-post** | LinkedIn post after WP completion | `/generate-linkedin-post` |
| **claude-code-practices** | Review advanced Claude Code feature adoption | `/claude-code-practices` |
| **gemini-analysis** | Delegate codebase analysis to Gemini CLI | `/gemini-analysis` |
| **review-pr** | Fetch and summarize AI reviewer comments on PRs | `/review-pr [number]` |
| **landing-page-copy-optimizer** | Analyze landing page copy using April Dunford methodology | `/landing-page-copy-optimizer` |
| **landing-page-prompt-generator** | Generate Replit Design Mode prompts for landing pages | `/landing-page-prompt-generator` |
| **scaffold-py-lib** | Scaffold new Python library with standard structure | `/scaffold-py-lib <name>` |
| **agent-development** | LangGraph agent patterns reference (langgraph ^1.0) | `/agent-development` |

### Sub-Agent and Context Management Rules

Claude Code sub-agents (Task tool) consume significant context. Follow these rules strictly:

**When to use sub-agents:**
- First time exploring an unknown module with 5+ files
- Truly parallel, independent research tasks (e.g., two unrelated API lookups)

**When NOT to use sub-agents:**
- File paths are already known from the session handoff — use Read tool directly
- Only 1-3 files need reading — Read them directly
- Plan can be written from existing knowledge — do not launch Plan agents redundantly
- File creation or writing is needed — sub-agents get write permissions denied

**Context hygiene rules:**
- NEVER read raw sub-agent JSON transcripts — only check the final result message
- Before fetching MCP docs, confirm the current WP actually needs them (do not pre-fetch for future WPs)
- Prefer `tools/gemini-analyze.sh` via Bash for pre-WP research before deploying Explore sub-agents
- When Gemini is unavailable (429 errors), fall back to targeted Read tool calls, not broad Explore agents

---

## Code Generation Standards

### Portfolio-Ready Code

All generated code must be production-quality and suitable for a professional portfolio. Follow these rules:

#### DO:
- Write concise, professional docstrings that explain WHAT the code does
- Use clear variable and function names that are self-documenting
- Include type hints for all function parameters and return values
- Follow PEP 8 and project linting rules (ruff)
- Add inline comments only when the logic is genuinely complex
- Explore basic to hard concepts and conventions outside of the code

#### DO NOT:
- Include pedagogical or teaching comments (e.g., "This is called encapsulation...")
- Explain basic programming concepts in docstrings or comments
- Add comments that reveal AI-assisted generation
- Include step-by-step explanations of standard patterns
- Over-comment obvious code

#### Example

```python
# BAD - Teaching comment
class GitHubCLI:
    """
    Wrapper class for the GitHub CLI (`gh`) tool.

    This is the ENCAPSULATION principle - hiding complexity behind
    a simple interface.
    """

# GOOD - Professional docstring
class GitHubCLI:
    """Wrapper for GitHub CLI operations."""
```

### Docstring Format

Use Google-style docstrings, kept minimal:

```python
def create_issue(self, title: str, body: str) -> dict:
    """Create a new GitHub issue.

    Args:
        title: Issue title
        body: Issue body in Markdown

    Returns:
        Dictionary with 'number' and 'url' of created issue
    """
```

### When Comments ARE Appropriate

- Explaining non-obvious business logic
- Documenting workarounds for known issues
- TODO/FIXME markers with ticket references
- Complex algorithms that genuinely need explanation