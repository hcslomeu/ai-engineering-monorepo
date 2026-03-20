"""Tests for AlphaWhale API routes.

Tests use httpx AsyncClient with FastAPI dependency overrides.
"""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from api.dependencies import get_graph
from api.main import create_app


@pytest.fixture
def mock_graph():
    """Create a mock compiled graph."""
    graph = AsyncMock()
    graph.astream_events = _make_async_iter([])
    graph.aget_state = AsyncMock(return_value=MagicMock(tasks=[]))
    return graph


@pytest.fixture
def app(mock_graph):
    """Create a test app with mocked dependencies."""
    test_app = create_app()
    test_app.state.supabase = AsyncMock()
    test_app.state.redis_client = None
    test_app.dependency_overrides[get_graph] = lambda: mock_graph
    return test_app


@pytest.fixture
async def client(app):
    """Async test client that bypasses lifespan."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


def _make_async_iter(items):
    """Return a callable that produces a fresh async iterator each time."""

    async def _iter(*_args, **_kwargs):
        for item in items:
            yield item

    return _iter


def _parse_sse_data_lines(text: str, *, exclude_done: bool = True) -> list[str]:
    """Extract data: lines from SSE response text."""
    lines = []
    for line in text.strip().split("\n"):
        stripped = line.strip()
        if stripped.startswith("data:"):
            if exclude_done and "[DONE]" in stripped:
                continue
            lines.append(stripped.removeprefix("data:").strip())
    return lines


class TestChatStream:
    async def test_stream_includes_thread_id_in_metadata(
        self, client: AsyncClient, mock_graph: AsyncMock
    ):
        """First SSE event should contain the thread_id."""
        response = await client.post(
            "/chat/stream",
            json={"message": "Hello", "thread_id": "test-thread-123"},
        )
        assert response.status_code == 200

        data_lines = _parse_sse_data_lines(response.text)
        metadata = json.loads(data_lines[0])
        assert metadata["thread_id"] == "test-thread-123"

    async def test_stream_generates_thread_id_when_missing(
        self, client: AsyncClient, mock_graph: AsyncMock
    ):
        """Should auto-generate a UUID thread_id when not provided."""
        response = await client.post(
            "/chat/stream",
            json={"message": "Hello"},
        )
        assert response.status_code == 200

        data_lines = _parse_sse_data_lines(response.text)
        metadata = json.loads(data_lines[0])
        assert "thread_id" in metadata
        assert len(metadata["thread_id"]) == 36  # UUID format


class TestChatApprove:
    async def test_approve_resumes_graph(self, client: AsyncClient, mock_graph: AsyncMock):
        """POST /chat/approve should resume the graph and stream tokens."""
        token_event = {
            "event": "on_chat_model_stream",
            "data": {"chunk": MagicMock(content="Signal approved!")},
        }
        mock_graph.astream_events = _make_async_iter([token_event])

        response = await client.post(
            "/chat/approve",
            json={"thread_id": "test-thread-123", "approved": True},
        )
        assert response.status_code == 200

        data_lines = _parse_sse_data_lines(response.text)
        assert len(data_lines) >= 1
        token_data = json.loads(data_lines[0])
        assert token_data["token"] == "Signal approved!"

    async def test_reject_resumes_graph(self, client: AsyncClient, mock_graph: AsyncMock):
        """POST /chat/approve with approved=false should resume with rejection."""
        token_event = {
            "event": "on_chat_model_stream",
            "data": {"chunk": MagicMock(content="Signal rejected.")},
        }
        mock_graph.astream_events = _make_async_iter([token_event])

        response = await client.post(
            "/chat/approve",
            json={"thread_id": "test-thread-123", "approved": False},
        )
        assert response.status_code == 200

        data_lines = _parse_sse_data_lines(response.text)
        token_data = json.loads(data_lines[0])
        assert token_data["token"] == "Signal rejected."


class TestApprovalRequestValidation:
    async def test_rejects_missing_thread_id(self, client: AsyncClient):
        """Should return 422 when thread_id is missing."""
        response = await client.post(
            "/chat/approve",
            json={"approved": True},
        )
        assert response.status_code == 422

    async def test_rejects_missing_approved(self, client: AsyncClient):
        """Should return 422 when approved field is missing."""
        response = await client.post(
            "/chat/approve",
            json={"thread_id": "some-thread"},
        )
        assert response.status_code == 422
