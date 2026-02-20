"""Configuration for AlphaWhale API service."""

from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """Environment-based settings for the FastAPI service.

    All fields map to environment variables with the ``API_`` prefix.
    Example: ``API_DEBUG=true`` sets ``debug``.
    """

    app_name: str = "AlphaWhale API"
    debug: bool = False
    cors_origins: list[str] = ["http://localhost:3000"]
    market_data_base_url: str = "https://www.alphavantage.co/query"

    model_config = {"env_prefix": "API_"}
