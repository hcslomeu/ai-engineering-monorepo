"""Configuration for AlphaWhale ingestion pipeline."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class IngestionSettings(BaseSettings):
    """Environment-based settings for the Massive API + Supabase pipeline.

    All fields map to environment variables with the ``INGESTION_`` prefix.
    Example: ``INGESTION_SUPABASE_URL=https://xxx.supabase.co`` sets ``supabase_url``.
    """

    supabase_url: str
    supabase_key: SecretStr
    massive_api_key: SecretStr
    massive_base_url: str = "https://api.polygon.io"

    model_config = {"env_prefix": "INGESTION_"}
