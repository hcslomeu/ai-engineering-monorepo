# Development Workflow

## Quality Checks

Run these before every commit to match what CI enforces:

```bash
# Run all tests with coverage
poetry run pytest --cov=libs --cov-report=term-missing

# Lint (catches style issues, import ordering, common bugs)
poetry run ruff check .

# Format check (verifies code style without modifying files)
poetry run ruff format --check .

# Type checking
poetry run mypy libs

# Security scan
poetry run bandit -r libs -ll
```

!!! tip "Auto-fix linting issues"
    Run `poetry run ruff check --fix .` to auto-fix what ruff can handle (import sorting, unused imports, etc.). Then run `poetry run ruff format .` to apply formatting.

## Nx Targets

Nx orchestrates tasks across the monorepo. Each project defines its own targets in `project.json`.

### Run a target on a specific project

```bash
# Run tests for py-core only
pnpm nx test py-core

# Lint py-core only
pnpm nx lint py-core

# Type check py-core only
pnpm nx typecheck py-core
```

### Run targets across all projects

```bash
# Test all projects
pnpm nx run-many -t test

# Lint all projects
pnpm nx run-many -t lint

# Only run affected projects (based on git diff)
pnpm nx affected -t test
```

### Useful Nx commands

```bash
# List all registered projects
pnpm nx show projects

# Visualise the dependency graph in a browser
pnpm nx graph

# Clear Nx cache (when things seem stale)
pnpm nx reset
```

## Serving Docs Locally

Preview the documentation site during development:

```bash
poetry run mkdocs serve
```

This starts a local server at `http://127.0.0.1:8000` with **live reload** — edit any markdown file in `docs/` and the browser refreshes automatically.

To build the static site (what CI does for deployment):

```bash
poetry run mkdocs build --strict
```

The `--strict` flag treats warnings as errors, catching broken links and missing pages before they reach production.

## Git Workflow

```bash
# Create a feature branch (always use WP prefix)
git checkout -b feature/WP-XXX-short-description

# Commit using conventional commits
git commit -m "feat(scope): description"
git commit -m "fix(scope): description"
git commit -m "chore(scope): description"

# Create a PR linking to the GitHub issue
gh pr create --title "feat: WP-XXX description" --body "Closes #XX"
```

## CI Pipeline

The GitHub Actions pipeline (`.github/workflows/ci-python.yaml`) runs **four parallel jobs** on every push and pull request:

| Job | Command | What it catches |
|-----|---------|-----------------|
| **Test** | `pytest --cov=libs` | Broken logic, regressions |
| **Lint** | `ruff check` + `ruff format --check` | Style violations, import issues |
| **Security** | `bandit -r libs -ll` | Common security vulnerabilities |
| **Type Check** | `mypy libs` | Type errors, missing annotations |

All four jobs must pass before a PR can be merged.