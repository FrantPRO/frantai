import pytest
from unittest.mock import Mock, patch
from app.services.embeddings import EmbeddingService
import numpy as np

@pytest.mark.unit
def test_embedding_service_lazy_loading():
    """Test that model is loaded lazily"""
    service = EmbeddingService()
    assert service._model is None

    # Access model property triggers loading
    with patch('app.services.embeddings.SentenceTransformer') as mock_st:
        mock_st.return_value = Mock()
        _ = service.model
        mock_st.assert_called_once()

@pytest.mark.unit
def test_create_embedding():
    """Test creating single embedding"""
    service = EmbeddingService()

    # Mock the model
    mock_model = Mock()
    mock_model.encode.return_value = np.array([0.1, 0.2, 0.3])
    service._model = mock_model

    embedding = service.create_embedding("test text")

    assert isinstance(embedding, list)
    assert len(embedding) == 3
    assert embedding == [0.1, 0.2, 0.3]

@pytest.mark.unit
def test_create_embeddings_batch():
    """Test creating multiple embeddings"""
    service = EmbeddingService()

    mock_model = Mock()
    mock_model.encode.return_value = np.array([[0.1, 0.2], [0.3, 0.4]])
    service._model = mock_model

    embeddings = service.create_embeddings(["text1", "text2"])

    assert len(embeddings) == 2
    assert embeddings[0] == [0.1, 0.2]
    assert embeddings[1] == [0.3, 0.4]

@pytest.mark.unit
def test_query_passage_prefixes():
    """Test that query and passage embeddings use correct prefixes"""
    service = EmbeddingService()

    mock_model = Mock()
    mock_model.encode.return_value = np.array([0.1, 0.2])
    service._model = mock_model

    # Test query prefix
    service.create_query_embedding("test query")
    mock_model.encode.assert_called_with("query: test query", convert_to_numpy=True)

    # Test passage prefix
    service.create_passage_embedding("test passage")
    mock_model.encode.assert_called_with("passage: test passage", convert_to_numpy=True)

@pytest.mark.unit
def test_cosine_similarity():
    """Test cosine similarity calculation"""
    emb1 = [1.0, 0.0, 0.0]
    emb2 = [1.0, 0.0, 0.0]
    emb3 = [0.0, 1.0, 0.0]

    # Identical vectors
    sim1 = EmbeddingService.cosine_similarity(emb1, emb2)
    assert abs(sim1 - 1.0) < 0.001

    # Orthogonal vectors
    sim2 = EmbeddingService.cosine_similarity(emb1, emb3)
    assert abs(sim2) < 0.001
