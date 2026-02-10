# Architecture Overview

## Hybrid Workspace

This monorepo manages two ecosystems side by side:

| Ecosystem | Package Manager | Scope |
|-----------|----------------|-------|
| **Python** | Poetry | AI/ML libraries, data pipelines, API backends |
| **TypeScript** | pnpm | React frontends (unified Next.js app) |

**Nx** sits above both as the orchestrator. It doesn't install packages or compile code — it runs tasks (`test`, `lint`, `typecheck`) on the right projects in the right order, regardless of language.

```
                    ┌──────────┐
                    │    Nx    │  ← Orchestration (task runner)
                    └────┬─────┘
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         ┌────────┐ ┌────────┐ ┌────────┐
         │ Poetry │ │  pnpm  │ │ Docker │
         └────┬───┘ └────┬───┘ └────┬───┘
              ▼          ▼          ▼
          Python      TypeScript  Containers
          libs/       apps/*/web  infra/docker/
          apps/*/     libs/shared-
          pipelines/  schemas
```

### Why not just one package manager?

Python and TypeScript have incompatible dependency models. Poetry resolves Python packages from PyPI; pnpm resolves Node packages from npm. Trying to force both into one system creates more problems than it solves. Instead, each ecosystem uses its native tooling, and Nx coordinates across both.

## Shared Libraries

The `libs/` directory contains reusable code that multiple applications depend on:

| Library | Purpose | Used By |
|---------|---------|---------|
| **py-core** | Config (Pydantic), logging (structlog), exceptions | All Python apps |
| **py-agents** | LangChain/LangGraph base classes | AlphaWhale, MediGuard |
| **py-retrieval** | LlamaIndex + Pinecone abstractions | MediGuard |
| **py-streaming** | Kafka producers/consumers | RailSense |
| **shared-schemas** | Zod schemas (generated from JSON Schema) | All frontends |

Libraries are linked as **path dependencies** in Poetry:

```toml
# Root pyproject.toml
[tool.poetry.dependencies]
py-core = { path = "libs/py-core", develop = true }
```

The `develop = true` flag means changes to `py-core` are immediately available to all consumers without reinstalling — like a live symlink.

## Project Structure

Each of the three application projects follows the same internal layout:

```
apps/<project>/
├── agent/     # AI agent (LangGraph workflow)
├── api/       # FastAPI backend
└── web/       # Next.js frontend (in unified app)
```

This consistency means patterns learned in one project transfer directly to the others.

## Nx Task Graph

Each project defines its tasks in a `project.json` file. Nx builds a dependency graph and runs tasks in the correct order.

Example from `libs/py-core/project.json`:

```json
{
  "name": "py-core",
  "targets": {
    "test": {
      "executor": "nx:run-commands",
      "options": {
        "command": "poetry run pytest libs/py-core/tests -v"
      }
    },
    "lint": {
      "executor": "nx:run-commands",
      "options": {
        "command": "poetry run ruff check libs/py-core/src"
      }
    },
    "typecheck": {
      "executor": "nx:run-commands",
      "options": {
        "command": "poetry run mypy libs/py-core/src"
      }
    }
  }
}
```

When you run `pnpm nx run-many -t test`, Nx discovers every project with a `test` target and runs them — respecting dependencies so that shared libraries are tested before the apps that use them.
