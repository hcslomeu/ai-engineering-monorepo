"""Shared test fixtures for the AlphaWhale API."""

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from httpx import ASGITransport, AsyncClient

from api.dependencies import get_graph, get_http_client
from api.main import create_app

FAKE_ALPHA_VANTAGE_RESPONSE: dict[str, Any] = {
    "Meta Data": {"1. Information": "Daily Prices (Digital Currency)"},
    "Time Series (Digital Currency Daily)": {
        "2026-02-19": {
            "1. open": "48000.00",
            "2. high": "51000.00",
            "3. low": "47500.00",
            "4. close": "50000.00",
            "5. volume": "12345.67",
        },
        "2026-02-18": {
            "1. open": "47000.00",
            "2. high": "49000.00",
            "3. low": "46500.00",
            "4. close": "48000.00",
            "5. volume": "11234.56",
        },
    },
}

FAKE_ALPHA_VANTAGE_ERROR: dict[str, str] = {
    "Error Message": "Invalid API call. Please check the symbol.",
}


def _make_mock_response(data: dict[str, Any], status_code: int = 200) -> httpx.Response:
    """Build a fake httpx.Response with JSON body."""
    return httpx.Response(
        status_code=status_code,
        json=data,
        request=httpx.Request("GET", "http://test"),
    )


def _build_mock_http_client(response_data: dict[str, Any]) -> AsyncMock:
    """Create a mock AsyncHTTPClient that returns pre-canned data."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=_make_mock_response(response_data))
    return mock_client


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
def app():
    """Create a fresh FastAPI app for each test."""
    return create_app()


@pytest.fixture
async def client(app: Any) -> AsyncGenerator[AsyncClient, None]:
    """Async test client using httpx ASGITransport."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_http_client(app: Any) -> None:
    """Override HTTP client dependency with a fake Alpha Vantage success response."""
    mock = _build_mock_http_client(FAKE_ALPHA_VANTAGE_RESPONSE)
    app.dependency_overrides[get_http_client] = lambda: mock


@pytest.fixture
def mock_http_client_error(app: Any) -> None:
    """Override HTTP client dependency with a fake Alpha Vantage error response."""
    mock = _build_mock_http_client(FAKE_ALPHA_VANTAGE_ERROR)
    app.dependency_overrides[get_http_client] = lambda: mock


@pytest.fixture
def mock_graph(app: Any) -> None:
    """Override graph dependency with a fake streaming graph."""
    mock = MagicMock()
    mock.astream_events = _fake_stream_events
    app.dependency_overrides[get_graph] = lambda: mock
