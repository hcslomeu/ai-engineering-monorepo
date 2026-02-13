"""BigQuery Bronze layer writer for raw market data."""

from typing import Any

from google.cloud import bigquery
from google.cloud.bigquery import LoadJobConfig, SourceFormat, WriteDisposition

from ingestion.config import IngestionSettings
from ingestion.schemas import CRYPTO_DAILY_SCHEMA


def ensure_dataset(client: bigquery.Client, dataset_id: str) -> None:
    """Create the dataset if it does not exist."""
    dataset_ref = bigquery.DatasetReference(client.project, dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    client.create_dataset(dataset, exists_ok=True)


def ensure_table(client: bigquery.Client, table_id: str) -> None:
    """Create the table with the Bronze schema if it does not exist."""
    table = bigquery.Table(table_id, schema=CRYPTO_DAILY_SCHEMA)
    client.create_table(table, exists_ok=True)


def load_rows(
    client: bigquery.Client,
    table_id: str,
    rows: list[dict[str, Any]],
) -> int:
    """Batch-load rows into a BigQuery table.

    Args:
        client: Authenticated BigQuery client.
        table_id: Fully qualified table ID (project.dataset.table).
        rows: List of dicts matching the table schema.

    Returns:
        Number of rows loaded.
    """
    if not rows:
        return 0

    job_config = LoadJobConfig(
        schema=CRYPTO_DAILY_SCHEMA,
        source_format=SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=WriteDisposition.WRITE_APPEND,
    )
    load_job = client.load_table_from_json(rows, table_id, job_config=job_config)
    load_job.result()  # blocks until the job completes
    return load_job.output_rows if load_job.output_rows is not None else len(rows)


def ingest(symbol: str, settings: IngestionSettings) -> int:
    """Run the full Bronze ingestion pipeline for a cryptocurrency.

    Fetches data from Alpha Vantage and writes raw rows to BigQuery.

    Args:
        symbol: Cryptocurrency symbol (e.g. "BTC").
        settings: Ingestion pipeline configuration.

    Returns:
        Number of rows ingested.
    """
    from ingestion.alpha_vantage import fetch_crypto_daily

    client = bigquery.Client(project=settings.gcp_project_id)
    table_id = f"{settings.gcp_project_id}.{settings.bq_dataset}.{settings.bq_table}"

    ensure_dataset(client, settings.bq_dataset)
    ensure_table(client, table_id)

    rows = fetch_crypto_daily(symbol, settings)
    return load_rows(client, table_id, rows)
