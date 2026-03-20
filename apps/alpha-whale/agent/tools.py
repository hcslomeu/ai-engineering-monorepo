"""Finance tools for the AlphaWhale agent backed by Supabase."""

import os

from langchain_core.tools import tool
from supabase import Client, create_client

from agent.models import TradeSignal
from py_core import extract, get_logger

logger = get_logger("agent.tools")

# Maps user-friendly ticker symbols to Polygon.io format stored in Supabase
TICKER_MAP: dict[str, str] = {
    "BTC": "X:BTCUSD",
    "ETH": "X:ETHUSD",
    "SOL": "X:SOLUSD",
}

_MAX_DAYS = 30
_MAX_TICKERS = 5

_client: Client | None = None


def _get_supabase() -> Client:
    """Return a cached synchronous Supabase client.

    Lazily initialised on first call so that tests can patch os.environ
    before the client is created.
    """
    global _client  # noqa: PLW0603
    if _client is None:
        _client = create_client(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_KEY"],
        )
    return _client


def _validate_days(days: int) -> dict[str, str] | None:
    if not 1 <= days <= _MAX_DAYS:
        return {"error": f"days must be between 1 and {_MAX_DAYS}"}
    return None


def _resolve_ticker(ticker: str) -> str:
    """Normalise a ticker to its Supabase-stored format (uppercase, crypto mapped)."""
    upper = ticker.upper()
    return TICKER_MAP.get(upper, upper)


@tool
def get_stock_price(ticker: str, days: int = 7) -> dict:
    """Fetch recent daily OHLCV price data for a stock or crypto asset.

    Returns the latest N days of open, high, low, close, and volume data.

    Supported tickers: AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, BTC, ETH, SOL.

    Args:
        ticker: Asset symbol (e.g. "AAPL", "BTC").
        days: Number of recent trading days to return. Default is 7.
    """
    if error := _validate_days(days):
        return error
    resolved = _resolve_ticker(ticker)
    result = (
        _get_supabase()
        .table("market_data_daily")
        .select("ticker, date, open, high, low, close, volume")
        .eq("ticker", resolved)
        .order("date", desc=True)
        .limit(days)
        .execute()
    )

    if not result.data:
        return {"error": f"No price data found for {ticker}"}

    return {"ticker": ticker.upper(), "rows": result.data}


@tool
def get_technical_indicators(ticker: str, days: int = 7) -> dict:
    """Fetch recent daily technical indicators for a stock or crypto asset.

    Returns EMA (8, 80), SMA (200), MACD (value, signal, histogram),
    RSI (14), and Stochastic (K, D) for the latest N days.

    Supported tickers: AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, BTC, ETH, SOL.

    Args:
        ticker: Asset symbol (e.g. "NVDA", "ETH").
        days: Number of recent trading days to return. Default is 7.
    """
    if error := _validate_days(days):
        return error
    resolved = _resolve_ticker(ticker)
    result = (
        _get_supabase()
        .table("technical_indicators_daily")
        .select(
            "ticker, date, ema_8, ema_80, sma_200, "
            "macd_value, macd_signal, macd_histogram, "
            "rsi_14, stoch_k, stoch_d"
        )
        .eq("ticker", resolved)
        .order("date", desc=True)
        .limit(days)
        .execute()
    )

    if not result.data:
        return {"error": f"No indicator data found for {ticker}"}

    return {"ticker": ticker.upper(), "rows": result.data}


@tool
def compare_assets(tickers: list[str], metric: str = "close", days: int = 7) -> dict:
    """Compare a metric across multiple assets for recent trading days.

    Returns side-by-side values for each ticker, useful for questions like
    "Compare NVDA vs TSLA volume last 7 days".

    Supported tickers: AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, BTC, ETH, SOL.
    Supported metrics: open, high, low, close, volume.

    Args:
        tickers: List of asset symbols to compare (e.g. ["NVDA", "TSLA"]).
        metric: OHLCV field to compare. Default is "close".
        days: Number of recent trading days to return. Default is 7.
    """
    if error := _validate_days(days):
        return error
    if not 1 <= len(tickers) <= _MAX_TICKERS:
        return {"error": f"Choose between 1 and {_MAX_TICKERS} tickers"}
    valid_metrics = {"open", "high", "low", "close", "volume"}
    if metric not in valid_metrics:
        return {"error": f"Invalid metric '{metric}'. Choose from: {sorted(valid_metrics)}"}

    comparison: dict[str, list] = {}
    for ticker in tickers:
        resolved = _resolve_ticker(ticker)
        result = (
            _get_supabase()
            .table("market_data_daily")
            .select(f"date, {metric}")
            .eq("ticker", resolved)
            .order("date", desc=True)
            .limit(days)
            .execute()
        )
        comparison[ticker.upper()] = result.data if result.data else []

    return {"metric": metric, "days": days, "data": comparison}


@tool
def generate_trade_signal(ticker: str, analysis_context: str) -> dict:
    """Generate a structured trade signal from market analysis.

    Uses LLM extraction to produce a TradeSignal with direction (bullish/bearish/neutral),
    confidence score, reasoning, and indicators used.

    Args:
        ticker: Asset symbol (e.g. "NVDA", "BTC").
        analysis_context: Market analysis text to extract the signal from.
    """
    prompt = f"Based on this analysis for {ticker}, extract a trade signal:\n\n{analysis_context}"
    signal = extract(prompt, TradeSignal)
    payload = signal.model_dump()
    if payload["ticker"].upper() != ticker.upper():
        logger.warning(
            "trade_signal_ticker_mismatch",
            requested_ticker=ticker.upper(),
            extracted_ticker=payload["ticker"],
        )
    payload["ticker"] = ticker.upper()
    return payload
