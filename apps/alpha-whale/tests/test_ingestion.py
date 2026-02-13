"""Tests for AlphaWhale Bronze layer ingestion pipeline."""

from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from ingestion.config import IngestionSettings
from ingestion.schemas import CRYPTO_DAILY_SCHEMA

# --- Fixtures ---

SAMPLE_API_RESPONSE = {
    "Meta Data": {
        "1. Information": "Daily Prices (Digital Currency)",
        "2. Digital Currency Code": "BTC",
    },
    "Time Series (Digital Currency Daily)": {
        "2026-02-11": {
            "1. open": "97234.56",
            "2. high": "98100.00",
            "3. low": "96500.00",
            "4. close": "97800.00",
            "5. volume": "12345.67",
        },
        "2026-02-10": {
            "1. open": "96000.00",
            "2. high": "97500.00",
            "3. low": "95800.00",
            "4. close": "97234.56",
            "5. volume": "11234.56",
        },
    },
}


@pytest.fixture()
def settings(monkeypatch: pytest.MonkeyPatch) -> IngestionSettings:
    monkeypatch.setenv("INGESTION_GCP_PROJECT_ID", "test-project")
    monkeypatch.setenv("INGESTION_ALPHA_VANTAGE_API_KEY", "test-key")
    return IngestionSettings()


# --- IngestionSettings ---


class TestIngestionSettings:
    def test_loads_from_env(self, settings: IngestionSettings) -> None:
        assert settings.gcp_project_id == "test-project"
        assert settings.alpha_vantage_api_key == "test-key"

    def test_default_values(self, settings: IngestionSettings) -> None:
        assert settings.bq_dataset == "alpha_whale_bronze"
        assert settings.bq_table == "crypto_daily"

    def test_missing_required_field_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("INGESTION_GCP_PROJECT_ID", raising=False)
        monkeypatch.delenv("INGESTION_ALPHA_VANTAGE_API_KEY", raising=False)
        with pytest.raises(ValidationError):
            IngestionSettings()


# --- CRYPTO_DAILY_SCHEMA ---


class TestCryptoDailySchema:
    def test_has_expected_columns(self) -> None:
        names = [field.name for field in CRYPTO_DAILY_SCHEMA]
        assert "symbol" in names
        assert "date" in names
        assert "open" in names
        assert "close" in names
        assert "raw_response" in names
        assert "ingested_at" in names
        assert "source" in names

    def test_all_fields_required(self) -> None:
        for field in CRYPTO_DAILY_SCHEMA:
            assert field.mode == "REQUIRED", f"{field.name} should be REQUIRED"

    def test_field_types(self) -> None:
        type_map = {f.name: f.field_type for f in CRYPTO_DAILY_SCHEMA}
        assert type_map["symbol"] == "STRING"
        assert type_map["date"] == "DATE"
        assert type_map["open"] == "FLOAT"
        assert type_map["ingested_at"] == "TIMESTAMP"


# --- fetch_crypto_daily ---


class TestFetchCryptoDaily:
    @patch("ingestion.alpha_vantage.requests.get")
    def test_returns_rows_for_each_day(
        self, mock_get: MagicMock, settings: IngestionSettings
    ) -> None:
        mock_get.return_value.json.return_value = SAMPLE_API_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()

        from ingestion.alpha_vantage import fetch_crypto_daily

        rows = fetch_crypto_daily("BTC", settings)
        assert len(rows) == 2

    @patch("ingestion.alpha_vantage.requests.get")
    def test_row_has_expected_keys(self, mock_get: MagicMock, settings: IngestionSettings) -> None:
        mock_get.return_value.json.return_value = SAMPLE_API_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()

        from ingestion.alpha_vantage import fetch_crypto_daily

        rows = fetch_crypto_daily("BTC", settings)
        expected_keys = {
            "symbol",
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "raw_response",
            "ingested_at",
            "source",
        }
        assert set(rows[0].keys()) == expected_keys

    @patch("ingestion.alpha_vantage.requests.get")
    def test_numeric_fields_are_floats(
        self, mock_get: MagicMock, settings: IngestionSettings
    ) -> None:
        mock_get.return_value.json.return_value = SAMPLE_API_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()

        from ingestion.alpha_vantage import fetch_crypto_daily

        row = fetch_crypto_daily("BTC", settings)[0]
        assert isinstance(row["open"], float)
        assert isinstance(row["close"], float)
        assert isinstance(row["volume"], float)

    @patch("ingestion.alpha_vantage.requests.get")
    def test_source_is_alpha_vantage(
        self, mock_get: MagicMock, settings: IngestionSettings
    ) -> None:
        mock_get.return_value.json.return_value = SAMPLE_API_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()

        from ingestion.alpha_vantage import fetch_crypto_daily

        row = fetch_crypto_daily("BTC", settings)[0]
        assert row["source"] == "alpha_vantage"

    @patch("ingestion.alpha_vantage.requests.get")
    def test_raises_on_missing_time_series(
        self, mock_get: MagicMock, settings: IngestionSettings
    ) -> None:
        mock_get.return_value.json.return_value = {"Note": "Rate limit exceeded"}
        mock_get.return_value.raise_for_status = MagicMock()

        from ingestion.alpha_vantage import fetch_crypto_daily

        with pytest.raises(ValueError, match="missing"):
            fetch_crypto_daily("BTC", settings)

    @patch("ingestion.alpha_vantage.requests.get")
    def test_passes_api_key_in_params(
        self, mock_get: MagicMock, settings: IngestionSettings
    ) -> None:
        mock_get.return_value.json.return_value = SAMPLE_API_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()

        from ingestion.alpha_vantage import fetch_crypto_daily

        fetch_crypto_daily("BTC", settings)
        call_kwargs = mock_get.call_args
        assert call_kwargs.kwargs["params"]["apikey"] == "test-key"


# --- Bronze writer ---


class TestBronzeWriter:
    @patch("ingestion.bronze.bigquery.Client")
    def test_ensure_dataset_calls_create(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value
        mock_client.project = "test-project"

        from ingestion.bronze import ensure_dataset

        ensure_dataset(mock_client, "alpha_whale_bronze")
        mock_client.create_dataset.assert_called_once()
        call_kwargs = mock_client.create_dataset.call_args
        assert call_kwargs.kwargs.get("exists_ok") is True

    @patch("ingestion.bronze.bigquery.Client")
    def test_ensure_table_calls_create(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value

        from ingestion.bronze import ensure_table

        ensure_table(mock_client, "test-project.alpha_whale_bronze.crypto_daily")
        mock_client.create_table.assert_called_once()
        call_kwargs = mock_client.create_table.call_args
        assert call_kwargs.kwargs.get("exists_ok") is True

    @patch("ingestion.bronze.bigquery.Client")
    def test_load_rows_returns_row_count(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value
        mock_job = MagicMock()
        mock_job.output_rows = 5
        mock_client.load_table_from_json.return_value = mock_job

        from ingestion.bronze import load_rows

        count = load_rows(mock_client, "project.dataset.table", [{"a": 1}] * 5)
        assert count == 5
        mock_client.load_table_from_json.assert_called_once()
