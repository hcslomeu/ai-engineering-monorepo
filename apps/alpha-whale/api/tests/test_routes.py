"""Integration tests for AlphaWhale API routes."""

from httpx import AsyncClient

# --- /health endpoint ---


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


async def test_health_includes_dependency_checks(client: AsyncClient) -> None:
    response = await client.get("/health")
    data = response.json()
    assert "redis" in data["checks"]
    assert "pinecone" in data["checks"]


async def test_health_checks_are_stubs(client: AsyncClient) -> None:
    response = await client.get("/health")
    data = response.json()
    for name, check in data["checks"].items():
        assert check["status"] == "ok", f"{name} check should be ok"
        assert check["detail"] == "stub", f"{name} should be a stub"


# --- /market/{asset} endpoint ---


async def test_market_returns_ohlcv_data(client: AsyncClient, mock_http_client: None) -> None:
    response = await client.get("/market/BTC")
    assert response.status_code == 200
    data = response.json()
    assert data["asset"] == "BTC"
    assert data["date"] == "2026-02-19"
    assert data["close"] == 50000.0
    assert data["volume"] == 12345.67
    assert data["source"] == "alpha_vantage"


async def test_market_uppercases_asset(client: AsyncClient, mock_http_client: None) -> None:
    response = await client.get("/market/btc")
    data = response.json()
    assert data["asset"] == "BTC"


async def test_market_returns_latest_date(client: AsyncClient, mock_http_client: None) -> None:
    response = await client.get("/market/BTC")
    data = response.json()
    assert data["date"] == "2026-02-19"  # First key = most recent


async def test_market_returns_502_on_upstream_error(
    client: AsyncClient, mock_http_client_error: None
) -> None:
    response = await client.get("/market/INVALID")
    assert response.status_code == 502
    data = response.json()
    assert "detail" in data


# --- /chat/stream endpoint ---


async def test_chat_stream_returns_event_stream(client: AsyncClient, mock_graph: None) -> None:
    response = await client.post(
        "/chat/stream",
        json={"message": "What is Bitcoin?"},
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]


async def test_chat_stream_contains_tokens(client: AsyncClient, mock_graph: None) -> None:
    response = await client.post(
        "/chat/stream",
        json={"message": "What is Bitcoin?"},
    )
    body = response.text
    assert '"token"' in body
    assert "Hello" in body
    assert "Whale" in body


async def test_chat_stream_ends_with_done_sentinel(client: AsyncClient, mock_graph: None) -> None:
    response = await client.post(
        "/chat/stream",
        json={"message": "What is Bitcoin?"},
    )
    assert "[DONE]" in response.text


async def test_chat_stream_empty_message_returns_422(client: AsyncClient) -> None:
    response = await client.post(
        "/chat/stream",
        json={"message": ""},
    )
    assert response.status_code == 422


async def test_chat_stream_missing_message_returns_422(client: AsyncClient) -> None:
    response = await client.post(
        "/chat/stream",
        json={},
    )
    assert response.status_code == 422


async def test_chat_stream_no_body_returns_422(client: AsyncClient) -> None:
    response = await client.post("/chat/stream")
    assert response.status_code == 422
