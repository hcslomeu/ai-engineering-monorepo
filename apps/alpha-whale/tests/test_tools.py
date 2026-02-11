"""Tests for AlphaWhale finance tools.

These tests verify both the tool logic and the auto-generated schemas
that LangChain creates from type hints and docstrings.
"""

from agent.tools import calculate_rsi, fetch_btc_price, get_market_summary

# --- fetch_btc_price ---


class TestFetchBtcPrice:
    def test_returns_expected_keys(self):
        result = fetch_btc_price.invoke({})
        assert set(result.keys()) == {
            "symbol",
            "price_usd",
            "change_24h_pct",
            "volume_24h_usd",
        }

    def test_symbol_is_btc(self):
        result = fetch_btc_price.invoke({})
        assert result["symbol"] == "BTC"

    def test_price_is_positive(self):
        result = fetch_btc_price.invoke({})
        assert result["price_usd"] > 0

    def test_tool_metadata(self):
        assert fetch_btc_price.name == "fetch_btc_price"
        assert "Bitcoin" in fetch_btc_price.description


# --- calculate_rsi ---


class TestCalculateRsi:
    def test_returns_rsi_and_signal(self):
        prices = [44 + i for i in range(20)]  # steadily rising
        result = calculate_rsi.invoke({"prices": prices})
        assert "rsi" in result
        assert "signal" in result
        assert "period" in result

    def test_rsi_range(self):
        prices = [44 + i * 0.5 for i in range(20)]
        result = calculate_rsi.invoke({"prices": prices})
        assert 0 <= result["rsi"] <= 100

    def test_rising_prices_high_rsi(self):
        prices = [100 + i * 10 for i in range(20)]  # strong uptrend
        result = calculate_rsi.invoke({"prices": prices})
        assert result["rsi"] > 70
        assert result["signal"] == "overbought"

    def test_falling_prices_low_rsi(self):
        prices = [200 - i * 10 for i in range(20)]  # strong downtrend
        result = calculate_rsi.invoke({"prices": prices})
        assert result["rsi"] < 30
        assert result["signal"] == "oversold"

    def test_insufficient_data_returns_error(self):
        result = calculate_rsi.invoke({"prices": [1, 2, 3]})
        assert "error" in result

    def test_custom_period(self):
        prices = list(range(50))
        result = calculate_rsi.invoke({"prices": prices, "period": 7})
        assert result["period"] == 7

    def test_tool_metadata(self):
        assert calculate_rsi.name == "calculate_rsi"
        assert "RSI" in calculate_rsi.description
        schema = calculate_rsi.args_schema.model_json_schema()
        assert "prices" in schema["properties"]
        assert "period" in schema["properties"]


# --- get_market_summary ---


class TestGetMarketSummary:
    def test_returns_expected_keys(self):
        result = get_market_summary.invoke({})
        assert set(result.keys()) == {
            "sentiment",
            "total_market_cap_usd",
            "btc_dominance_pct",
            "top_movers",
        }

    def test_sentiment_is_valid(self):
        result = get_market_summary.invoke({})
        assert result["sentiment"] in {"bullish", "bearish", "neutral"}

    def test_top_movers_is_list(self):
        result = get_market_summary.invoke({})
        assert isinstance(result["top_movers"], list)
        assert len(result["top_movers"]) == 3

    def test_tool_metadata(self):
        assert get_market_summary.name == "get_market_summary"
        assert "market" in get_market_summary.description.lower()
