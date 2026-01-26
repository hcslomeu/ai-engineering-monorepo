# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
| `SKILLS.md` | Learning progress tracker |
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

## Learning Context

This repository is being built as a learning project. The developer:

- Is proficient with Python data stacks (Pandas/NumPy)
- Is a **novice at Python Classes** (needs practice)
- Has **zero experience with TypeScript/JavaScript**
- Has **zero experience with Monorepo patterns**
- Learns best through hands-on implementation

When assisting, provide:
- Syntax refreshers for Docker/Git/SQL
- Explanations of the "why" behind architectural decisions
- Small, digestible work packages
- Theory before implementation for new frameworks