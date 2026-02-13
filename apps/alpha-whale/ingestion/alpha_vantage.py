"""Alpha Vantage API client for crypto market data."""

import json
from datetime import UTC, datetime
from typing import Any

import requests

from ingestion.config import IngestionSettings

TIME_SERIES_KEY = "Time Series (Digital Currency Daily)"
KEY_OPEN = "1. open"
KEY_HIGH = "2. high"
KEY_LOW = "3. low"
KEY_CLOSE = "4. close"
KEY_VOLUME = "5. volume"


def fetch_crypto_daily(
    symbol: str,
    settings: IngestionSettings,
    market: str = "USD",
) -> list[dict[str, Any]]:
    """Fetch daily crypto OHLCV data and return Bronze-ready rows.

    Args:
        symbol: Cryptocurrency symbol (e.g. "BTC", "ETH").
        settings: Ingestion configuration with API key and base URL.
        market: Fiat currency market. Defaults to "USD".

    Returns:
        List of dicts ready for BigQuery insertion, one per trading day.

    Raises:
        requests.HTTPError: On non-2xx response from Alpha Vantage.
        ValueError: When response is missing expected time series data.
    """
    params = {
        "function": "DIGITAL_CURRENCY_DAILY",
        "symbol": symbol,
        "market": market,
        "apikey": settings.alpha_vantage_api_key.get_secret_value(),
    }
    response = requests.get(settings.alpha_vantage_base_url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if "Error Message" in data:
        raise ValueError(f"Alpha Vantage API error: {data['Error Message']}")
    if "Note" in data:
        raise ValueError(f"Alpha Vantage rate limit: {data['Note']}")

    if TIME_SERIES_KEY not in data:
        raise ValueError(
            f"Unexpected API response: missing '{TIME_SERIES_KEY}'. "
            f"Keys received: {list(data.keys())}"
        )

    time_series = data[TIME_SERIES_KEY]
    now = datetime.now(tz=UTC).isoformat()

    rows: list[dict[str, Any]] = []
    for date_str, daily_data in time_series.items():
        rows.append(
            {
                "symbol": symbol,
                "date": date_str,
                "open": float(daily_data[KEY_OPEN]),
                "high": float(daily_data[KEY_HIGH]),
                "low": float(daily_data[KEY_LOW]),
                "close": float(daily_data[KEY_CLOSE]),
                "volume": float(daily_data[KEY_VOLUME]),
                "raw_response": json.dumps(daily_data),
                "ingested_at": now,
                "source": "alpha_vantage",
            }
        )

    return rows
