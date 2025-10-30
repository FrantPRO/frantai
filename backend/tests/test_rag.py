import pytest
from unittest.mock import AsyncMock, Mock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.rag import RAGService


@pytest.mark.unit
@pytest.mark.asyncio
async def test_rag_service_init():
    """Test RAGService initialization"""
    mock_db = AsyncMock(spec=AsyncSession)

    with (
        patch("app.services.rag.get_embedding_service"),
        patch("app.services.rag.get_ollama_service"),
    ):
        service = RAGService(mock_db)
        assert service.db == mock_db


@pytest.mark.unit
@pytest.mark.asyncio
async def test_vector_search():
    """Test vector search"""
    mock_db = AsyncMock(spec=AsyncSession)
    mock_embedding_service = Mock()
    mock_embedding_service.create_query_embedding.return_value = [
        0.1,
        0.2,
        0.3,
    ]

    # Mock database query result
    mock_result = Mock()
    mock_result.fetchall.return_value = [
        (1, "Test chunk", "work_experience", 1, {}, 0.9),
        (2, "Another chunk", "projects", 2, {}, 0.85),
    ]
    mock_db.execute.return_value = mock_result

    with (
        patch(
            "app.services.rag.get_embedding_service",
            return_value=mock_embedding_service,
        ),
        patch("app.services.rag.get_ollama_service"),
    ):
        service = RAGService(mock_db)
        chunks = await service.vector_search("test query", top_k=2)

        assert len(chunks) == 2
        assert chunks[0].similarity == 0.9
        assert chunks[1].similarity == 0.85


@pytest.mark.unit
@pytest.mark.asyncio
async def test_generate_response_streaming():
    """Test response generation with streaming"""
    mock_db = AsyncMock(spec=AsyncSession)
    mock_llm = Mock()

    async def mock_stream(*args, **kwargs):
        for token in ["Hello", " ", "world"]:
            yield token

    mock_llm.generate_stream = mock_stream

    with (
        patch("app.services.rag.get_embedding_service"),
        patch("app.services.rag.get_ollama_service", return_value=mock_llm),
    ):
        service = RAGService(mock_db)

        tokens = []
        async for token in service.generate_response(
            question="Test?", context="Context", language="en", stream=True
        ):
            tokens.append(token)

        assert "".join(tokens) == "Hello world"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_chat_no_results():
    """Test chat when no chunks found"""
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock empty search result
    mock_result = Mock()
    mock_result.fetchall.return_value = []
    mock_db.execute.return_value = mock_result

    mock_embedding = Mock()
    mock_embedding.create_query_embedding.return_value = [0.1, 0.2]

    with (
        patch(
            "app.services.rag.get_embedding_service",
            return_value=mock_embedding,
        ),
        patch("app.services.rag.get_ollama_service"),
    ):
        service = RAGService(mock_db)

        response_parts = []
        async for part in service.chat("random question"):
            response_parts.append(part)

        response = "".join(response_parts)
        assert "don't have specific information" in response.lower()


@pytest.mark.unit
def test_no_info_messages():
    """Test no-info messages in different languages"""
    mock_db = AsyncMock(spec=AsyncSession)

    with (
        patch("app.services.rag.get_embedding_service"),
        patch("app.services.rag.get_ollama_service"),
    ):
        service = RAGService(mock_db)

        # English
        msg_en = service._get_no_info_message("en")
        assert "don't have" in msg_en.lower()
        assert "Stan" in msg_en

        # Russian
        msg_ru = service._get_no_info_message("ru")
        assert "нет" in msg_ru.lower()
        assert "Стана" in msg_ru

        # German
        msg_de = service._get_no_info_message("de")
        assert "keine" in msg_de.lower()
        assert "Stans" in msg_de
