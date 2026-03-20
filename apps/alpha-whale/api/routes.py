"""API route handlers for AlphaWhale."""

import json
import uuid
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Query
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from sse_starlette import EventSourceResponse

from api.dependencies import GraphDep, RedisClientDep, SupabaseDep
from api.models import (
    ApprovalRequest,
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
    thread_id: str,
) -> AsyncGenerator[dict[str, str], None]:
    """Yield SSE-formatted dicts from the LangGraph agent stream."""
    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

    yield {
        "event": "metadata",
        "data": json.dumps({"thread_id": thread_id}),
    }

    try:
        async for event in graph.astream_events(
            {"messages": [HumanMessage(content=message)]},
            config=config,
            version="v2",
        ):
            if event["event"] == "on_chat_model_stream" and event["data"]["chunk"].content:
                yield {
                    "event": "message",
                    "data": json.dumps({"token": event["data"]["chunk"].content}),
                }

        # Check if the graph paused at an interrupt
        state = await graph.aget_state(config)
        interrupted_task = next(
            (t for t in (state.tasks or []) if hasattr(t, "interrupts") and t.interrupts),
            None,
        )
        if interrupted_task:
            interrupt_value = interrupted_task.interrupts[0].value
            yield {
                "event": "approval_request",
                "data": json.dumps(interrupt_value),
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
    thread_id = body.thread_id or str(uuid.uuid4())
    return EventSourceResponse(_stream_agent(graph, body.message, thread_id))


@router.post("/chat/approve")
async def chat_approve(body: ApprovalRequest, graph: GraphDep) -> EventSourceResponse:
    """Resume a paused conversation after human approval/rejection."""
    thread_id = body.thread_id

    async def _stream_resume() -> AsyncGenerator[dict[str, str], None]:
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        try:
            async for event in graph.astream_events(
                Command(resume=body.approved),
                config=config,
                version="v2",
            ):
                if event["event"] == "on_chat_model_stream" and event["data"]["chunk"].content:
                    yield {
                        "event": "message",
                        "data": json.dumps({"token": event["data"]["chunk"].content}),
                    }
        except Exception as exc:
            logger.error("approval_stream_error", error=str(exc), thread_id=thread_id)
            yield {
                "event": "error",
                "data": json.dumps({"error": str(exc)}),
            }
        finally:
            yield {"event": "message", "data": "[DONE]"}

    return EventSourceResponse(_stream_resume())


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
