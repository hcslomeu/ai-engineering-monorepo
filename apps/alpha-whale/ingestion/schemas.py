"""BigQuery table schema definitions for the Bronze layer."""

from google.cloud.bigquery import SchemaField

CRYPTO_DAILY_SCHEMA: list[SchemaField] = [
    SchemaField("symbol", "STRING", mode="REQUIRED"),
    SchemaField("date", "DATE", mode="REQUIRED"),
    SchemaField("open", "FLOAT", mode="REQUIRED"),
    SchemaField("high", "FLOAT", mode="REQUIRED"),
    SchemaField("low", "FLOAT", mode="REQUIRED"),
    SchemaField("close", "FLOAT", mode="REQUIRED"),
    SchemaField("volume", "FLOAT", mode="REQUIRED"),
    SchemaField("raw_response", "STRING", mode="REQUIRED"),
    SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
    SchemaField("source", "STRING", mode="REQUIRED"),
]
