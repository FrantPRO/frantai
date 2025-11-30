"""
RAG (Retrieval-Augmented Generation) service.
Combines vector search with LLM generation.
"""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.context import (
    RetrievedChunk,
    deduplicate_chunks,
    format_chunks_for_context,
    rank_chunks_by_relevance,
)
from app.core.prompts import get_system_prompt
from app.services.embeddings import get_embedding_service
from app.services.llm import get_ollama_service
from app.services.text_utils import detect_language

logger = logging.getLogger(__name__)


class RAGService:
    """Service for RAG pipeline"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.embedding_service = get_embedding_service()
        self.llm_service = get_ollama_service()

    async def vector_search(
        self,
        query: str,
        top_k: int = 3,
        similarity_threshold: float = 0.5,
    ) -> list[RetrievedChunk]:
        """
        Perform vector similarity search.

        Args:
            query: Search query
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score

        Returns:
            List of retrieved chunks
        """
        # Create query embedding
        query_embedding = self.embedding_service.create_query_embedding(
            query
        )

        # Convert to pgvector format
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

        # Vector search query using cosine similarity
        query_sql = text(
            """
            SELECT
                id,
                chunk_text,
                source_table,
                source_id,
                chunk_metadata,
                1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
            FROM knowledge_chunks
            WHERE 1 - (embedding <=> CAST(:embedding AS vector)) > :threshold
            ORDER BY similarity DESC
            LIMIT :limit
        """
        )

        result = await self.db.execute(
            query_sql,
            {
                "embedding": embedding_str,
                "threshold": similarity_threshold,
                "limit": top_k,
            },
        )

        rows = result.fetchall()

        chunks = [
            RetrievedChunk(
                id=row[0],
                text=row[1],
                source_table=row[2],
                source_id=row[3],
                metadata=row[4] or {},
                similarity=float(row[5]),
            )
            for row in rows
        ]

        logger.info(
            f"Vector search for '{query[:50]}...': "
            f"found {len(chunks)} chunks"
        )

        return chunks

    async def generate_response(
        self,
        question: str,
        context: str,
        language: str = "en",
        stream: bool = True,
    ) -> AsyncGenerator[str, None]:
        """
        Generate response using LLM.

        Args:
            question: User question
            context: Retrieved context
            language: Language for response
            stream: Whether to stream response

        Yields:
            Response tokens
        """
        # Get system prompt
        prompt = get_system_prompt(language, context, question)

        logger.info(f"Generating response for question: {question[:50]}...")

        if stream:
            async for token in self.llm_service.generate_stream(
                prompt=prompt, temperature=0.7
            ):
                yield token
        else:
            response = await self.llm_service.generate(
                prompt=prompt, temperature=0.7
            )
            yield response

    async def chat(
        self, question: str, top_k: int = 3, stream: bool = True
    ) -> AsyncGenerator[str, None]:
        """
        Complete RAG pipeline: retrieve + generate.

        Args:
            question: User question
            top_k: Number of chunks to retrieve
            stream: Whether to stream response

        Yields:
            Response tokens
        """
        # Detect language
        language = detect_language(question)
        logger.info(f"Detected language: {language}")

        # Vector search
        chunks = await self.vector_search(query=question, top_k=top_k)

        if not chunks:
            # No relevant information found
            no_info_msg = self._get_no_info_message(language)
            yield no_info_msg
            return

        # Deduplicate and rank
        chunks = deduplicate_chunks(chunks)
        chunks = rank_chunks_by_relevance(chunks, question)

        # Format context
        context = format_chunks_for_context(chunks)

        # Generate response
        async for token in self.generate_response(
            question=question, context=context, language=language, stream=stream
        ):
            yield token

    def _get_no_info_message(self, language: str) -> str:
        """Get 'no information found' message in user's language"""
        messages = {
            "en": (
                "I don't have specific information about that in my "
                "knowledge base. Could you try rephrasing your question "
                "or ask about Stan's professional experience, skills, "
                "or projects?"
            ),
            "ru": (
                "У меня нет конкретной информации об этом в базе знаний. "
                "Попробуйте переформулировать вопрос или спросите о "
                "профессиональном опыте, навыках или проектах Стана."
            ),
            "de": (
                "Ich habe keine spezifischen Informationen darüber in "
                "meiner Wissensdatenbank. Könnten Sie Ihre Frage anders "
                "formulieren oder nach Stans beruflicher Erfahrung, "
                "Fähigkeiten oder Projekten fragen?"
            ),
        }
        return messages.get(language, messages["en"])


# Global instance
_rag_service: RAGService | None = None


async def get_rag_service(db: AsyncSession) -> RAGService:
    """Get RAG service instance (not singleton, needs db session)"""
    return RAGService(db)
