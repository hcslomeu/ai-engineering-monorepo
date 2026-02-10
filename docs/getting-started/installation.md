# Installation

## Prerequisites

| Tool | Required Version | Purpose |
|------|-----------------|---------|
| **Python** | 3.11+ | AI/ML libraries, data pipelines, API backends |
| **Poetry** | 2.x | Python dependency management |
| **Node.js** | 18+ | Nx orchestration, TypeScript frontend |
| **pnpm** | 10+ | Node package management (via Corepack) |
| **Docker Desktop** | Latest | Container builds and local services |

!!! tip "Version managers"
    Use [pyenv](https://github.com/pyenv/pyenv) for Python and [nvm](https://github.com/nvm-sh/nvm) for Node.js to manage multiple versions without conflicts.

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:hcslomeu/ai-engineering-monorepo.git
cd ai-engineering-monorepo
```

### 2. Enable Corepack (for pnpm)

```bash
corepack enable
```

Corepack ships with Node.js and manages pnpm versions automatically using the `packageManager` field in `package.json`.

### 3. Install TypeScript dependencies

```bash
pnpm install
```

### 4. Install Python dependencies

```bash
poetry install
```

This installs all root dependencies plus path-linked libraries (like `py-core`) in development mode.

### 5. Verify the setup

```bash
# Nx should list all projects
pnpm nx show projects

# Python tools should be available
poetry run pytest --version
poetry run ruff --version
poetry run mkdocs --version

# Docker should be running
docker info --format '{{.ServerVersion}}'
```

## What gets installed

The root `pyproject.toml` installs:

- **Runtime:** `py-core` (shared library, linked via path dependency)
- **Dev — Testing:** pytest, pytest-cov, pytest-asyncio
- **Dev — Quality:** ruff (linting + formatting), mypy (type checking), bandit (security)
- **Dev — Docs:** mkdocs-material (this documentation site)

The root `package.json` installs:

- **Nx** and its plugins for monorepo orchestration
- **TypeScript** toolchain (added when frontend work begins)