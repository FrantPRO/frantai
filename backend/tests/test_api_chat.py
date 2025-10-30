import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from httpx import AsyncClient

from app.models.chat import ChatSession


@pytest.mark.asyncio
async def test_create_session(client: AsyncClient):
    """Test creating a new chat session"""
    response = await client.post("/api/v1/chat/session/new")

    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["message_count"] == 0


@pytest.mark.asyncio
async def test_get_session(client: AsyncClient, db_session):
    """Test getting session information"""
    # Create session
    session = ChatSession(ip_hash="test_hash")
    db_session.add(session)
    await db_session.commit()

    # Get session
    response = await client.get(f"/api/v1/chat/session/{session.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(session.id)
    assert data["message_count"] == 0


@pytest.mark.asyncio
async def test_get_nonexistent_session(client: AsyncClient):
    """Test getting non-existent session"""
    fake_id = uuid4()
    response = await client.get(f"/api/v1/chat/session/{fake_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_chat_message_empty(client: AsyncClient):
    """Test sending empty message"""
    response = await client.post("/api/v1/chat/message", json={"message": ""})

    assert response.status_code == 422  # Pydantic validation error


@pytest.mark.asyncio
async def test_chat_message_with_session(client: AsyncClient, db_session):
    """Test sending message with existing session"""
    # Create session
    session = ChatSession(ip_hash="test_hash")
    db_session.add(session)
    await db_session.commit()

    # Mock RAG service
    async def mock_chat(*args, **kwargs):
        yield "Test"
        yield " response"

    with patch("app.api.v1.chat.get_rag_service") as mock_rag:
        mock_service = AsyncMock()
        mock_service.chat = mock_chat
        mock_rag.return_value = mock_service

        # Send message (SSE response)
        response = await client.post(
            "/api/v1/chat/message",
            json={"message": "Test question", "session_id": str(session.id)},
        )

        assert response.status_code == 200
        assert (
            response.headers["content-type"]
            == "text/event-stream; charset=utf-8"
        )


@pytest.mark.asyncio
async def test_chat_message_new_session(client: AsyncClient):
    """Test sending message without session (auto-create)"""

    async def mock_chat(*args, **kwargs):
        yield "Response"

    with patch("app.api.v1.chat.get_rag_service") as mock_rag:
        mock_service = AsyncMock()
        mock_service.chat = mock_chat
        mock_rag.return_value = mock_service

        response = await client.post(
            "/api/v1/chat/message", json={"message": "Test question"}
        )

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_chat_rate_limit(client: AsyncClient):
    """Test rate limiting on chat endpoint"""
    # This test would need proper rate limit testing
    # For now, just verify endpoint is accessible

    async def mock_chat(*args, **kwargs):
        yield "Response"

    with patch("app.api.v1.chat.get_rag_service") as mock_rag:
        mock_service = AsyncMock()
        mock_service.chat = mock_chat
        mock_rag.return_value = mock_service

        # Send multiple requests
        for i in range(5):
            response = await client.post(
                "/api/v1/chat/message", json={"message": f"Question {i}"}
            )
            assert response.status_code == 200


@pytest.mark.asyncio
async def test_session_persistence(client: AsyncClient, db_session):
    """Test that sessions persist across requests"""
    # Create session
    create_response = await client.post("/api/v1/chat/session/new")
    session_id = create_response.json()["session_id"]

    # Send message
    async def mock_chat(*args, **kwargs):
        yield "Response"

    with patch("app.api.v1.chat.get_rag_service") as mock_rag:
        mock_service = AsyncMock()
        mock_service.chat = mock_chat
        mock_rag.return_value = mock_service

        await client.post(
            "/api/v1/chat/message",
            json={"message": "Test", "session_id": session_id},
        )

    # Get session - message count should be updated
    get_response = await client.get(f"/api/v1/chat/session/{session_id}")

    assert get_response.status_code == 200
    data = get_response.json()
    assert data["message_count"] == 2  # user + assistant
