# ---- Stage 1: Dependencies ----
FROM python:3.11-slim AS deps

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.2.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app

# Copy dependency manifests and path dependencies
# Path dependencies (libs/*) need full source for Poetry to install them
COPY pyproject.toml poetry.lock ./
COPY libs/py-core/ libs/py-core/
# Future libs: uncomment as they are created
# COPY libs/py-agents/ libs/py-agents/
# COPY libs/py-retrieval/ libs/py-retrieval/
# COPY libs/py-streaming/ libs/py-streaming/

# Install dependencies only (--no-root skips installing the workspace itself)
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    --mount=type=cache,target=/root/.cache/pip \
    poetry install --no-root --only main


# ---- Stage 2: Runtime ----
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy the virtualenv from the deps stage
COPY --from=deps /app/.venv .venv

# Copy application source code
COPY libs/ libs/
COPY pyproject.toml ./

# Non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --no-create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "py_core"]
