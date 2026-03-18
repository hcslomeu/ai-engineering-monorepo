"""API route handlers for AlphaWhale."""

import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Query
from langchain_core.messages import HumanMessage
from sse_starlette import EventSourceResponse

from api.dependencies import GraphDep, RedisClientDep, SupabaseDep
from api.models import (
    ChatRequest,
    HealthCheck,
    HealthResponse,
    IndicatorDataResponse,
    MarketDataResponse,
)
from py_core import get_logger

logger = get_logger("api.routes")

router = APIRouter()


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


@router.get("/market/{asset}", response_model=list[MarketDataResponse])
async def get_market_data(
    asset: str,
    supabase: SupabaseDep,
    redis: RedisClientDep,
    days: int = Query(default=30, ge=1, le=3650),
) -> list[MarketDataResponse]:
    """Return recent daily OHLCV data for a ticker from Supabase."""
    ticker = asset.upper()
    cache_key = f"market:{ticker}:{days}"

    if redis is not None:
        cached = await redis.get(cache_key)
        if cached is not None:
            try:
                logger.info("cache_hit", key=cache_key)
                return [MarketDataResponse(**row) for row in json.loads(cached)]
            except (json.JSONDecodeError, TypeError, KeyError) as exc:
                logger.warning("cache_deserialize_failed", key=cache_key, error=str(exc))

    result = (
        await supabase.table("market_data_daily")
        .select("ticker, date, open, high, low, close, volume")
        .eq("ticker", ticker)
        .order("date", desc=True)
        .limit(days)
        .execute()
    )

    if not result.data:
        return []

    if redis is not None:
        await redis.set(cache_key, json.dumps(result.data))

    return [MarketDataResponse(**row) for row in result.data]  # type: ignore[arg-type]


@router.get("/market/{asset}/indicators", response_model=list[IndicatorDataResponse])
async def get_indicator_data(
    asset: str,
    supabase: SupabaseDep,
    redis: RedisClientDep,
    days: int = Query(default=30, ge=1, le=3650),
) -> list[IndicatorDataResponse]:
    """Return recent daily technical indicators for a ticker from Supabase."""
    ticker = asset.upper()
    cache_key = f"indicators:{ticker}:{days}"

    if redis is not None:
        cached = await redis.get(cache_key)
        if cached is not None:
            try:
                logger.info("cache_hit", key=cache_key)
                return [IndicatorDataResponse(**row) for row in json.loads(cached)]
            except (json.JSONDecodeError, TypeError, KeyError) as exc:
                logger.warning("cache_deserialize_failed", key=cache_key, error=str(exc))

    result = (
        await supabase.table("technical_indicators_daily")
        .select(
            "ticker, date, ema_8, ema_80, sma_200, "
            "macd_value, macd_signal, macd_histogram, "
            "rsi_14, stoch_k, stoch_d"
        )
        .eq("ticker", ticker)
        .order("date", desc=True)
        .limit(days)
        .execute()
    )

    if not result.data:
        return []

    if redis is not None:
        await redis.set(cache_key, json.dumps(result.data))

    return [IndicatorDataResponse(**row) for row in result.data]  # type: ignore[arg-type]


@router.get("/health", response_model=HealthResponse)
async def health_check(redis: RedisClientDep) -> HealthResponse:
    """Service health check with dependency status."""
    if redis is not None:
        redis_ok = await redis.health_check()
        redis_check = HealthCheck(
            status="ok" if redis_ok else "degraded",
            detail="connected" if redis_ok else "unreachable",
        )
    else:
        redis_check = HealthCheck(status="ok", detail="disabled")

    return HealthResponse(
        status="ok",
        checks={
            "redis": redis_check,
            "pinecone": HealthCheck(status="ok", detail="stub"),  # TODO: WP-205
        },
    )
