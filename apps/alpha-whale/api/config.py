"""Configuration for AlphaWhale API service."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """Environment-based settings for the FastAPI service.

    All fields map to environment variables with the ``API_`` prefix.
    Example: ``API_DEBUG=true`` sets ``debug``.
    """

    app_name: str = "AlphaWhale API"
    debug: bool = False
    cors_origins: list[str] = ["http://localhost:3000"]
    supabase_url: str = ""
    supabase_key: SecretStr = SecretStr("")

    model_config = {"env_prefix": "API_"}