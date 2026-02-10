# py-core

Core utilities shared across all Python applications in the monorepo. Provides configuration management, structured logging, and base exception classes.

- **Location:** `libs/py-core/`
- **Package:** `py_core`
- **Dependencies:** pydantic ^2.0, pydantic-settings ^2.0, structlog ^24.0

## Public API

All exports are available from the top-level package:

```python
from py_core import Settings, configure_logging, get_logger
from py_core import PyCorError, ConfigurationError, ValidationError
```

## Configuration

The `Settings` class uses Pydantic BaseSettings to load configuration from environment variables with sensible defaults.

```python
from py_core import Settings

settings = Settings()
print(settings.app_name)      # "ai-engineering-monorepo"
print(settings.environment)   # "development"
print(settings.log_level)     # "INFO"
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `app_name` | `str` | `ai-engineering-monorepo` | Application identifier |
| `environment` | `development` \| `staging` \| `production` | `development` | Deployment environment |
| `debug` | `bool` | `False` | Debug mode flag |
| `log_level` | `DEBUG` \| `INFO` \| `WARNING` \| `ERROR` \| `CRITICAL` | `INFO` | Minimum log level |
| `log_format` | `json` \| `console` | `json` | Log output format |

Settings are loaded from environment variables and `.env` files. Use `get_settings()` for a cached singleton instance:

```python
from py_core import Settings

# Direct instantiation (new instance each time)
settings = Settings()

# Cached singleton (recommended)
from py_core.config import get_settings
settings = get_settings()
```

Override values via environment variables:

```bash
export APP_NAME=alpha-whale
export ENVIRONMENT=production
export LOG_LEVEL=DEBUG
```

## Logging

Structured logging powered by structlog. Supports JSON output (production) and coloured console output (development).

```python
from py_core import configure_logging, get_logger

# Configure once at startup
configure_logging(level="INFO", log_format="console")

# Get a logger instance
logger = get_logger(__name__, service="alpha-whale")
logger.info("Agent started", model="claude-opus-4.6")
```

**JSON format** (default, for production):

```json
{"event": "Agent started", "model": "claude-opus-4.6", "service": "alpha-whale", "level": "info", "timestamp": "2026-02-10T12:00:00Z"}
```

**Console format** (for development):

```
2026-02-10T12:00:00Z [info] Agent started  model=claude-opus-4.6 service=alpha-whale
```

## Exceptions

Base exception hierarchy for consistent error handling across all projects.

```python
from py_core import PyCorError, ConfigurationError, ValidationError

# All exceptions carry a message and optional details dict
try:
    raise ConfigurationError(
        "Missing API key",
        details={"variable": "OPENAI_API_KEY"}
    )
except PyCorError as e:
    print(e.message)   # "Missing API key"
    print(e.details)   # {"variable": "OPENAI_API_KEY"}
```

| Exception | Purpose |
|-----------|---------|
| `PyCorError` | Base class — catch all py-core errors |
| `ConfigurationError` | Invalid or missing configuration |
| `ValidationError` | Data validation failures |

## Tests

14 unit tests covering all three modules:

```bash
# Run py-core tests only
poetry run pytest libs/py-core/tests -v

# Via Nx
pnpm nx test py-core
```

| Test file | Count | Covers |
|-----------|-------|--------|
| `test_config.py` | 5 | Defaults, env overrides, validation, caching |
| `test_logging.py` | 4 | Logger interface, context binding, JSON output, level filtering |
| `test_exceptions.py` | 5 | Message storage, details dict, exception hierarchy |