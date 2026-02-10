# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Before Starting Any Task

Always read these files first to understand current progress and context:

```bash
cat PROGRESS.md                    # Current work package status
cat .claude/learning-progress.md   # Skills development tracker (private)
cat .claude/learning-context.md    # Session preferences (private)
```

**Check learning mode**: Read the `Learning Mode` section in `.claude/learning-context.md`. If set to `LEARNING`, follow all pacing rules and explain before/after code generation. If set to `PRODUCTION`, generate code efficiently.

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

## Repository Structure
```
ai-engineering-monorepo/
├── libs/                    # Shared libraries
│   ├── schemas/             # JSON Schema source of truth
│   ├── py-core/             # Python: Core utilities, logging, config
│   ├── py-agents/           # Python: LangChain/LangGraph base classes
│   ├── py-retrieval/        # Python: LlamaIndex + Pinecone abstractions
│   ├── py-streaming/        # Python: Kafka producers/consumers
│   └── shared-schemas/      # TypeScript: Zod schemas (generated)
│
├── pipelines/               # Data Engineering
│   ├── airflow-dags/        # Airflow DAG definitions
│   └── databricks-jobs/     # Databricks notebooks + Delta jobs
│
├── apps/                    # Applications
│   ├── alpha-whale/         # Finance: agent/, api/, web/
│   ├── medi-guard/          # Healthcare: agent/, api/, web/
│   └── rail-sense/          # Transportation: agent/, predictor/, api/, web/
│
├── tests/                   # Integration & E2E tests
├── docs/                    # MkDocs Material documentation
├── infra/                   # Terraform + Docker
└── tools/                   # Scripts + Nx generators
```

---

## Commands

### Nx (Monorepo Orchestration)
```bash
# Run a task on a specific project
pnpm nx <target> <project-name>

# Run tasks on all affected projects
pnpm nx affected -t <target>

# Run tasks on all projects
pnpm nx run-many -t <target>

# Visualise dependency graph
pnpm nx graph

# List all projects
pnpm nx show projects
```

### Poetry (Python)
```bash
# Install all dependencies (from root)
poetry install

# Run a command in the virtual environment
poetry run <command>

# Add a dependency to a specific package
cd libs/py-core && poetry add <package>

# Run tests
poetry run pytest

# Run linting
poetry run ruff check .

# Run security scan
poetry run bandit -r libs apps pipelines

# Run type checking
poetry run mypy libs apps pipelines
```

### pnpm (TypeScript)
```bash
# Install all dependencies
pnpm install

# Add a dependency to a specific package
pnpm --filter <package-name> add <dependency>

# Run a script in a specific package
pnpm --filter <package-name> run <script>
```

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

### Git Workflow

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

## Key Files

| File | Purpose |
|------|---------|
| `nx.json` | Nx workspace configuration |
| `pnpm-workspace.yaml` | pnpm workspace packages |
| `pyproject.toml` | Root Poetry configuration + tool settings |
| `tsconfig.base.json` | Base TypeScript configuration |
| `.claude/learning-progress.md` | Skills development tracker (private) |
| `PROGRESS.md` | Work package completion log |

---

## Environment Setup

### Prerequisites

- Node.js 18+ (recommend using nvm)
- pnpm 8+ (via Corepack: `corepack enable`)
- Python 3.11+ (recommend using pyenv)
- Poetry 1.7+
- Docker Desktop

### Initial Setup
```bash
# Clone the repository
git clone <repo-url>
cd ai-engineering-monorepo

# Install TypeScript dependencies
pnpm install

# Install Python dependencies
poetry install

# Verify setup
pnpm nx graph
poetry run pytest --version
```

---

## CI/CD

GitHub Actions workflows in `.github/workflows/`:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci-python.yaml` | Push/PR | pytest, ruff, bandit, mypy |
| `ci-typescript.yaml` | Push/PR | ESLint, Vitest |
| `deploy-docs.yaml` | Push to main | Build & deploy MkDocs |

---

## Troubleshooting

### Poetry "No file/folder found for package"

Ensure `package-mode = false` is set in the root `pyproject.toml`.

### Nx can't find a project

Run `pnpm nx reset` to clear the cache, then `pnpm nx graph` to verify.

### pnpm workspace issues

Check that `pnpm-workspace.yaml` includes the correct paths.

---

## Claude Code Configuration

This project uses a `.claude/` folder for Claude Code configuration:

```
.claude/
├── skills/               # Project-specific skills (committed)
├── learning-context.md   # Session preferences (gitignored)
└── learning-progress.md  # Skills development tracker (gitignored)
```

Private files in `.claude/` are gitignored and contain personal learning context.

### MCP Servers

The following MCP servers are configured and should be used in these scenarios:

| Server | When to Use |
|--------|-------------|
| **context7** | Fetch up-to-date library docs (LangChain, FastAPI, pytest, MkDocs, etc.) before writing code that depends on external libraries |
| **doc-gen** | Generate documentation structure for new libraries or complex modules |
| **langchain (Docs by LangChain)** | LangChain/LangGraph-specific API reference and patterns when building agents in `libs/py-agents/` or `apps/*/agent/` |

**Prefer MCP lookups over pasting docs** — use context7 or langchain to fetch reference material instead of copying documentation into the conversation. This keeps context clean and ensures up-to-date information.

### Custom Skills

Skills in `.claude/skills/` automate repeated workflows:

- **`generate-linkedin-post`**: Generate LinkedIn post after WP completion. Invoke with `/generate-linkedin-post`.
- **`claude-code-practices`**: Review advanced Claude Code feature adoption. Invoke with `/claude-code-practices`.

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

#### Examples

```python
# ❌ BAD - Teaching comment
class GitHubCLI:
    """
    Wrapper class for the GitHub CLI (`gh`) tool.
    
    This is the ENCAPSULATION principle - hiding complexity behind
    a simple interface.
    """

# ✅ GOOD - Professional docstring
class GitHubCLI:
    """Wrapper for GitHub CLI operations."""
```

```python
# ❌ BAD - Explaining basic concepts
# The underscore prefix (_run) is a Python convention meaning
# "this is an internal method, not part of the public API".
def _run(self, args: list[str]) -> CommandResult:

# ✅ GOOD - No comment needed, convention is self-evident
def _run(self, args: list[str]) -> CommandResult:
```

```python
# ❌ BAD - Over-explaining
# Using a set here because sets automatically remove duplicates.
# If WP-002 has ["python", "library"] and WP-003 has ["python", "testing"],
# the set will contain {"python", "library", "testing"}.
labels = set()

# ✅ GOOD - Simple and clear
labels: set[str] = set()
```

### Docstring Format

Use Google-style docstrings, kept minimal:

```python
def create_issue(self, title: str, body: str) -> dict:
    """
    Create a new GitHub issue.

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