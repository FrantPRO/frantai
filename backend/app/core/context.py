"""
Context management utilities for RAG system.
Handles context window, chunk selection, and formatting.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class RetrievedChunk:
    """Represents a chunk retrieved from vector search"""

    id: int
    text: str
    similarity: float
    source_table: str
    source_id: int
    metadata: dict[str, Any]


def format_chunks_for_context(
    chunks: list[RetrievedChunk], max_tokens: int = 2000
) -> str:
    """
    Format retrieved chunks into context string.

    Args:
        chunks: List of retrieved chunks (sorted by similarity)
        max_tokens: Maximum tokens for context

    Returns:
        Formatted context string
    """
    from app.services.text_utils import estimate_tokens

    context_parts = []
    total_tokens = 0

    for i, chunk in enumerate(chunks, 1):
        # Format chunk with source info
        chunk_text = f"[Source {i}]\n{chunk.text}\n"
        chunk_tokens = estimate_tokens(chunk_text)

        # Check if adding this chunk would exceed limit
        if total_tokens + chunk_tokens > max_tokens:
            break

        context_parts.append(chunk_text)
        total_tokens += chunk_tokens

    if not context_parts:
        return "No relevant information found."

    return "\n---\n\n".join(context_parts)


def rank_chunks_by_relevance(
    chunks: list[RetrievedChunk], query: str
) -> list[RetrievedChunk]:
    """
    Re-rank chunks by relevance to query.
    Currently just sorts by similarity, but can be enhanced
    with additional ranking algorithms.

    Args:
        chunks: Retrieved chunks
        query: User query

    Returns:
        Sorted chunks by relevance
    """
    # Simple ranking by similarity score
    return sorted(chunks, key=lambda c: c.similarity, reverse=True)


def deduplicate_chunks(
    chunks: list[RetrievedChunk],
) -> list[RetrievedChunk]:
    """
    Remove duplicate or highly similar chunks.

    Args:
        chunks: List of chunks

    Returns:
        Deduplicated chunks
    """
    seen_texts = set()
    unique_chunks = []

    for chunk in chunks:
        # Simple deduplication by exact text match
        text_lower = chunk.text.lower().strip()
        if text_lower not in seen_texts:
            seen_texts.add(text_lower)
            unique_chunks.append(chunk)

    return unique_chunks
