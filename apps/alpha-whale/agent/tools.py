"""Finance tools for the AlphaWhale agent.

Each function decorated with @tool becomes discoverable by the LLM.
The LLM uses the function name, docstring, and type hints to decide
when and how to call each tool.
"""

import random

from langchain_core.tools import tool


@tool
def fetch_btc_price() -> dict:
    """Fetch the current Bitcoin (BTC) price in USD.

    Returns the latest price, 24h change percentage, and 24h volume.
    Use this tool when the user asks about Bitcoin's current price or market data.
    """
    price = round(random.uniform(40_000, 70_000), 2)
    change = round(random.uniform(-5.0, 5.0), 2)
    volume = round(random.uniform(15e9, 40e9), 0)

    return {
        "symbol": "BTC",
        "price_usd": price,
        "change_24h_pct": change,
        "volume_24h_usd": volume,
    }


@tool
def calculate_rsi(prices: list[float], period: int = 14) -> dict:
    """Calculate the Relative Strength Index (RSI) for a list of prices.

    RSI measures momentum on a scale of 0-100:
    - Above 70: overbought (potential sell signal)
    - Below 30: oversold (potential buy signal)
    - Between 30-70: neutral

    Args:
        prices: Historical closing prices (most recent last). Minimum length: period + 1.
        period: RSI lookback period. Default is 14.
    """
    if len(prices) < period + 1:
        return {"error": f"Need at least {period + 1} prices, got {len(prices)}"}

    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    recent = deltas[-period:]

    gains = [d for d in recent if d > 0]
    losses = [-d for d in recent if d < 0]

    avg_gain = sum(gains) / period if gains else 0.0
    avg_loss = sum(losses) / period if losses else 0.0

    if avg_gain == 0 and avg_loss == 0:
        rsi = 50.0
    elif avg_loss == 0:
        rsi = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))

    return {
        "rsi": round(rsi, 2),
        "period": period,
        "signal": "overbought" if rsi > 70 else "oversold" if rsi < 30 else "neutral",
    }


@tool
def get_market_summary() -> dict:
    """Get a summary of the current cryptocurrency market conditions.

    Returns overall market sentiment, total market cap, BTC dominance,
    and top movers. Use this when the user asks about general market conditions
    or wants a broad overview.
    """
    sentiments = ["bullish", "bearish", "neutral"]
    top_movers = [
        {"symbol": "BTC", "change_pct": round(random.uniform(-5, 5), 2)},
        {"symbol": "ETH", "change_pct": round(random.uniform(-8, 8), 2)},
        {"symbol": "SOL", "change_pct": round(random.uniform(-12, 12), 2)},
    ]

    return {
        "sentiment": random.choice(sentiments),
        "total_market_cap_usd": round(random.uniform(1.5e12, 3.0e12), 0),
        "btc_dominance_pct": round(random.uniform(40, 60), 1),
        "top_movers": top_movers,
    }
