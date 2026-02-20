"""API route handlers for AlphaWhale."""

import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from sse_starlette import EventSourceResponse

from api.dependencies import GraphDep, HTTPClientDep, SettingsDep
from api.models import ChatRequest, HealthCheck, HealthResponse, MarketDataResponse
from py_core import HTTPClientError, get_logger

logger = get_logger("api.routes")

router = APIRouter()

TIME_SERIES_KEY = "Time Series (Digital Currency Daily)"


async def _stream_agent(
    graph: GraphDep,
    message: str,
) -> AsyncGenerator[dict[str, str], None]:
    """Yield SSE-formatted dicts from the LangGraph agent stream."""
    try:
        async for event in graph.astream_events(
            {"messages": [HumanMessage(content=message)]},
            version="v2",
        ):
            if event["event"] == "on_chat_model_stream" and event["data"]["chunk"].content:
                yield {
                    "event": "message",
                    "data": json.dumps({"token": event["data"]["chunk"].content}),
                }
    except Exception as exc:
        logger.error("stream_error", error=str(exc))
        yield {
            "event": "error",
            "data": json.dumps({"error": str(exc)}),
        }
    finally:
        yield {"event": "message", "data": "[DONE]"}


@router.post("/chat/stream")
async def chat_stream(body: ChatRequest, graph: GraphDep) -> EventSourceResponse:
    """Stream agent responses as Server-Sent Events."""
    return EventSourceResponse(_stream_agent(graph, body.message))


@router.get("/market/{asset}", response_model=MarketDataResponse)
async def get_market_data(
    asset: str, client: HTTPClientDep, settings: SettingsDep
) -> MarketDataResponse:
    """Fetch most recent daily OHLCV data for a crypto asset."""
    try:
        response = await client.get(
            "",
            params={
                "function": "DIGITAL_CURRENCY_DAILY",
                "symbol": asset.upper(),
                "market": "USD",
                "apikey": settings.market_data_api_key,
            },
        )
        data = response.json()

        if "Error Message" in data:
            raise ValueError(data["Error Message"])
        if "Note" in data:
            raise ValueError(data["Note"])

        time_series = data.get(TIME_SERIES_KEY, {})
        if not time_series:
            raise ValueError(f"No time series data for {asset}")

        latest_date = next(iter(time_series))
        day = time_series[latest_date]

        return MarketDataResponse(
            asset=asset.upper(),
            date=latest_date,
            open=float(day.get("1. open", 0.0)),
            high=float(day.get("2. high", 0.0)),
            low=float(day.get("3. low", 0.0)),
            close=float(day.get("4. close", 0.0)),
            volume=float(day.get("5. volume", 0.0)),
        )
    except (HTTPClientError, KeyError, ValueError) as exc:
        logger.error("market_data_error", asset=asset, error=str(exc))
        raise HTTPException(
            status_code=502,
            detail=f"Market data unavailable for {asset.upper()}",
        ) from exc


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Service health check with dependency stubs."""
    return HealthResponse(
        status="ok",
        checks={
            "redis": HealthCheck(status="ok", detail="stub"),  # TODO: WP-119
            "pinecone": HealthCheck(status="ok", detail="stub"),  # TODO: WP-205
        },
    )
