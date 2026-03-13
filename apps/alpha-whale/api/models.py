"""Request and response schemas for the AlphaWhale API."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """POST body for /chat/stream."""

    message: str = Field(..., min_length=1, max_length=2000)


class ChatStreamEvent(BaseModel):
    """Shape of a single SSE event (for documentation/typing)."""

    event: str = "message"
    data: str


class MarketDataResponse(BaseModel):
    """Daily OHLCV data for a ticker (stock or crypto)."""

    ticker: str
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class HealthCheck(BaseModel):
    """Individual service check result."""

    status: str
    detail: str = ""


class HealthResponse(BaseModel):
    """Response from /health."""

    status: str = "ok"
    checks: dict[str, HealthCheck] = {}
