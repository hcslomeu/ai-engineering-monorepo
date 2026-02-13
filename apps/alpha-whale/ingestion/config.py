"""Configuration for AlphaWhale ingestion pipeline."""

from pydantic_settings import BaseSettings


class IngestionSettings(BaseSettings):
    """Environment-based settings for BigQuery ingestion.

    All fields map to environment variables with the given prefix.
    Example: ``INGESTION_GCP_PROJECT_ID=my-project`` sets ``gcp_project_id``.
    """

    gcp_project_id: str
    bq_dataset: str = "alpha_whale_bronze"
    bq_table: str = "crypto_daily"
    alpha_vantage_api_key: str
    alpha_vantage_base_url: str = "https://www.alphavantage.co/query"

    model_config = {"env_prefix": "INGESTION_"}
