# Docker

## Overview

The monorepo provides two multi-stage Dockerfiles (Python and Node) plus a Docker Compose file for orchestration. Both images are designed for production use with small footprints and non-root users.

**Location:** `infra/docker/`

## Python Image

**File:** `infra/docker/python.Dockerfile`

Two-stage build: install dependencies in one stage, run application in another.

```
Stage 1: deps       Stage 2: runtime
┌─────────────┐     ┌─────────────────┐
│ python:3.11  │     │ python:3.11-slim│
│ + Poetry     │     │ + .venv (copied)│
│ + poetry.lock│────▶│ + app source    │
│ + libs/      │     │ + appuser (1000)│
└─────────────┘     └─────────────────┘
```

### Key design decisions

- **`python:3.11-slim`** as the runtime base — much smaller than the full image, excludes compilers and dev headers
- **Cache mounts** (`--mount=type=cache`) on Poetry and pip caches — speeds up rebuilds by reusing downloaded packages across builds
- **`POETRY_VIRTUALENVS_IN_PROJECT=true`** — puts `.venv` inside `/app` so it can be copied to the runtime stage with a simple `COPY --from=deps`
- **`--no-root --only main`** — installs dependencies only, not the workspace root package or dev dependencies
- **Non-root user** (`appuser`, UID 1000) — containers run without root privileges
- **Path dependencies** — `libs/py-core/` is fully copied (source + README + pyproject.toml) because Poetry needs the complete package to resolve path dependencies

## Node Image

**File:** `infra/docker/node.Dockerfile`

Three-stage build: install dependencies, build application, run with minimal runtime.

```
Stage 1: deps       Stage 2: builder     Stage 3: runtime
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ node:22-slim │     │ (from deps) │     │ node:22-slim│
│ + pnpm       │     │ + source    │     │ + built app │
│ + node_modules│───▶│ + nx build  │────▶│ + node user │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Key design decisions

- **Corepack** activates pnpm — no global npm install needed, version is pinned to `10.28.1`
- **`--frozen-lockfile`** — ensures deterministic installs (fails if `pnpm-lock.yaml` is out of date)
- **Three stages** — deps, builder (compiles TypeScript/Next.js), and runtime (only the built output)
- **Built-in `node` user** — `node:22-slim` already includes a non-root user with UID/GID 1000, no need to create one
- **`--chown=node:node` on COPY** — files are owned by the non-root user from the start (not copied as root then chowned)
- **Specific COPYs** — copies `nx.json`, `tsconfig.base.json`, `libs/`, `apps/` individually instead of `COPY . .` to prevent `.env` leakage

!!! info "Build steps are scaffolded"
    The builder stage and runtime CMD are placeholders until the frontend is built (WP-004). The image currently verifies the Node.js version.

## Docker Compose

**File:** `infra/docker-compose.yml`

Orchestrates both services with a shared build context (the repo root):

```bash
# Build both images
docker compose -f infra/docker-compose.yml build

# Run both services
docker compose -f infra/docker-compose.yml up
```

| Service | Image | Container Name |
|---------|-------|----------------|
| `python` | `python.Dockerfile` → `runtime` stage | `ai-mono-python` |
| `node` | `node.Dockerfile` → `runtime` stage | `ai-mono-node` |

Both services use `required: false` for the `.env` file, so they start even without environment variables configured.

### Future services

The Compose file is ready to expand with:

- **Postgres** — application database
- **Redis** — caching and message broker
- **Kafka** — event streaming (RailSense)

## .dockerignore

**File:** `.dockerignore`

Controls what gets sent to the Docker daemon as build context. Excludes:

- `.git/` — version history (large, not needed in images)
- `node_modules/` — reinstalled inside the container
- `.venv/` — rebuilt by Poetry in the deps stage
- `.env` — secrets must not be baked into images
- IDE files (`.vscode/`, `.idea/`)