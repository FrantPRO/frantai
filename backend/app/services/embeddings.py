from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings using multilingual-e5-base"""

    def __init__(self, model_name: str = "intfloat/multilingual-e5-base"):
        self.model_name = model_name
        self._model: Optional[SentenceTransformer] = None

    @property
    def model(self) -> SentenceTransformer:
        """Lazy load model on first use"""
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded successfully")
        return self._model

    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for a single text.
        For E5 models, queries should be prefixed with 'query: '
        and passages with 'passage: '
        """
        # For search queries, prefix with 'query: '
        # For documents being indexed, prefix with 'passage: '
        # We'll add this in the calling code
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts (batch processing)"""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def create_query_embedding(self, query: str) -> List[float]:
        """Create embedding for a search query (with query prefix)"""
        prefixed_query = f"query: {query}"
        return self.create_embedding(prefixed_query)

    def create_passage_embedding(self, passage: str) -> List[float]:
        """Create embedding for a document passage (with passage prefix)"""
        prefixed_passage = f"passage: {passage}"
        return self.create_embedding(prefixed_passage)

    @property
    def embedding_dimension(self) -> int:
        """Get the dimension of embeddings (768 for multilingual-e5-base)"""
        return self.model.get_sentence_embedding_dimension()

    @staticmethod
    def cosine_similarity(
        embedding1: List[float], embedding2: List[float]
    ) -> float:
        """Calculate cosine similarity between two embeddings"""
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))


# Global instance (singleton pattern)
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get or create global embedding service instance"""
    global _embedding_service
    if _embedding_service is None:
        from app.config import settings

        _embedding_service = EmbeddingService(settings.embedding_model)
    return _embedding_service
