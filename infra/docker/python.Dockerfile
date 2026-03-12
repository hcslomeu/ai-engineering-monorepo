# ---- Stage 1: Dependencies ----
FROM python:3.12-slim AS deps

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /uvx /bin/

WORKDIR /app

# Copy dependency manifests and workspace members
COPY pyproject.toml uv.lock ./
COPY libs/py-core/ libs/py-core/
# Future libs: uncomment as they are created
# COPY libs/py-agents/ libs/py-agents/
# COPY libs/py-retrieval/ libs/py-retrieval/
# COPY libs/py-streaming/ libs/py-streaming/

# Install dependencies and workspace packages
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --all-packages --frozen

# ---- Stage 2: Runtime ----
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy the virtualenv from the deps stage
COPY --from=deps /app/.venv .venv

# Copy application source code
COPY libs/ libs/
COPY pyproject.toml uv.lock ./

# Non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --no-create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "py_core"]