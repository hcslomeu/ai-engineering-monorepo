# CI/CD Pipeline

## Overview

The Python CI pipeline runs on every push to `main` or `feature/*` branches and on all pull requests to `main`. It executes **four parallel jobs** to validate code quality before merging.

**Workflow file:** `.github/workflows/ci-python.yaml`

```
┌──────────────────────────────────────────────────────┐
│                  Push / Pull Request                  │
└──────────┬──────────┬──────────┬──────────┬──────────┘
           ▼          ▼          ▼          ▼
      ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
      │  Test  │ │  Lint  │ │Security│ │TypeCheck │
      │(pytest)│ │ (ruff) │ │(bandit)│ │ (mypy)   │
      └────────┘ └────────┘ └────────┘ └──────────┘
```

All four must pass for a PR to be mergeable.

## Jobs

### Test (pytest)

Runs the full test suite with coverage reporting.

```bash
poetry run pytest --cov=libs --cov-report=term-missing
```

Coverage is currently scoped to `libs/` and will expand to include `apps/` and `pipelines/` as those directories are created.

### Lint (ruff)

Two checks — linting rules and formatting consistency:

```bash
poetry run ruff check .           # Lint rules (import order, unused vars, etc.)
poetry run ruff format --check .  # Formatting (without modifying files)
```

Ruff configuration is in the root `pyproject.toml`:

- **Line length:** 100 characters
- **Target version:** Python 3.11
- **Enabled rule sets:** E (pycodestyle), W (warnings), F (Pyflakes), I (isort), B (bugbear), C4 (comprehensions), UP (pyupgrade)

### Security (bandit)

Scans for common security vulnerabilities in Python code:

```bash
poetry run bandit -r libs -ll
```

The `-ll` flag sets the severity threshold to low. Configuration in `pyproject.toml` excludes test directories and allows `assert` statements (B101) in tests.

### Type Check (mypy)

Enforces type annotations across the codebase:

```bash
poetry run mypy libs
```

mypy is configured in strict mode:

- `disallow_untyped_defs = true` — all functions must have type annotations
- `warn_return_any = true` — warns when returning `Any`
- `warn_unused_ignores = true` — catches stale `# type: ignore` comments

## Shared Setup

All four jobs share the same environment setup:

| Component | Version | Notes |
|-----------|---------|-------|
| **Runner** | `ubuntu-latest` | GitHub-hosted |
| **Python** | 3.12 | Via `actions/setup-python@v5` |
| **Poetry** | 2.2.1 (pinned) | Installed via official installer |
| **Cache** | `actions/cache@v4` | Keyed by `poetry.lock` hash |

Poetry is configured with `virtualenvs.in-project = true` so the `.venv` directory can be cached between runs.

## Triggers

| Event | Branches | Jobs Run |
|-------|----------|----------|
| `push` | `main`, `feature/*` | All 4 |
| `pull_request` | `main` | All 4 |

## Future Additions

- **CI for TypeScript** (`ci-typescript.yaml`) — ESLint + Vitest, added when frontend work begins
- **CD for docs** (`deploy-docs.yaml`) — MkDocs build + GitHub Pages deploy, added in this work package
- **CD for apps** — deployment workflows, added when there's something to deploy