# py-core

Core utilities for the AI Engineering Monorepo.

## Modules

- **config** - Environment variable management with Pydantic BaseSettings
- **logging** - Structured JSON logging with structlog
- **exceptions** - Custom exception hierarchy for consistent error handling

## Usage

```python
from py_core import Settings, get_logger, configure_logging

# Load settings from environment
settings = Settings()

# Configure logging
configure_logging(level=settings.log_level, format=settings.log_format)

# Get a logger
logger = get_logger(__name__)
logger.info("Application started", environment=settings.environment)
```