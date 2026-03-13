"""Shared test fixtures for the AlphaWhale API."""

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.dependencies import get_graph, get_supabase
from api.main import create_app

SAMPLE_MARKET_ROWS = [
    {
        "ticker": "AAPL",
        "date": "2026-03-12",
        "open": 178.50,
        "high": 180.25,
        "low": 177.80,
        "close": 179.90,
        "volume": 52_000_000,
    },
    {
        "ticker": "AAPL",
        "date": "2026-03-11",
        "open": 176.00,
        "high": 179.10,
        "low": 175.50,
        "close": 178.50,
        "volume": 48_000_000,
    },
]


def _build_supabase_mock(rows: list[dict[str, Any]]) -> MagicMock:
    """Build a mock Supabase client that returns given rows for any query."""
    result = MagicMock()
    result.data = rows

    builder = MagicMock()
    builder.select.return_value = builder
    builder.eq.return_value = builder
    builder.order.return_value = builder
    builder.limit.return_value = builder
    builder.execute = AsyncMock(return_value=result)

    client = MagicMock()
    client.table.return_value = builder
    return client


async def _fake_stream_events(
    input_data: dict[str, Any],
    *,
    version: str = "v2",
    **kwargs: Any,
) -> AsyncGenerator[dict[str, Any], None]:
    """Fake LangGraph astream_events that yields token-like events."""
    tokens = ["Hello", " from", " Alpha", "Whale", "!"]
    for token in tokens:
        chunk = MagicMock()
        chunk.content = token
        yield {
            "event": "on_chat_model_stream",
            "data": {"chunk": chunk},
        }


@pytest.fixture
def app() -> FastAPI:
    """Create a fresh FastAPI app for each test."""
    return create_app()


@pytest.fixture
async def client(app: Any) -> AsyncGenerator[AsyncClient, None]:
    """Async test client using httpx ASGITransport."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_graph(app: Any) -> None:
    """Override graph dependency with a fake streaming graph."""
    mock = MagicMock()
    mock.astream_events = _fake_stream_events
    app.dependency_overrides[get_graph] = lambda: mock


@pytest.fixture
def mock_supabase(app: Any) -> MagicMock:
    """Override Supabase dependency with a mock returning sample data."""
    mock = _build_supabase_mock(SAMPLE_MARKET_ROWS)
    app.dependency_overrides[get_supabase] = lambda: mock
    return mock


@pytest.fixture
def mock_supabase_empty(app: Any) -> MagicMock:
    """Override Supabase dependency with a mock returning no data."""
    mock = _build_supabase_mock([])
    app.dependency_overrides[get_supabase] = lambda: mock
    return mock
