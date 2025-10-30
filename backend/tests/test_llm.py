import pytest
from unittest.mock import AsyncMock, patch, Mock
from app.services.llm import OllamaService
import httpx

@pytest.mark.unit
@pytest.mark.asyncio
async def test_ollama_health_check_success():
    """Test successful health check"""
    service = OllamaService()

    with patch('httpx.AsyncClient') as mock_client:
        mock_response = Mock()
        mock_response.status_code = 200

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )

        result = await service.check_health()
        assert result is True

@pytest.mark.unit
@pytest.mark.asyncio
async def test_ollama_health_check_failure():
    """Test failed health check"""
    service = OllamaService()

    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            side_effect=httpx.ConnectError("Connection failed")
        )

        result = await service.check_health()
        assert result is False

@pytest.mark.unit
@pytest.mark.asyncio
async def test_ollama_generate():
    """Test non-streaming generation"""
    service = OllamaService()

    with patch('httpx.AsyncClient') as mock_client:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Generated text"}

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        result = await service.generate("test prompt")
        assert result == "Generated text"

@pytest.mark.unit
@pytest.mark.asyncio
async def test_ollama_generate_with_system():
    """Test generation with system prompt"""
    service = OllamaService()

    with patch('httpx.AsyncClient') as mock_client:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Response"}

        post_mock = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value.post = post_mock

        await service.generate("prompt", system="system prompt")

        # Verify system was included in payload
        call_args = post_mock.call_args
        payload = call_args.kwargs['json']
        assert payload['system'] == "system prompt"
