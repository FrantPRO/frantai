import pytest

from app.core.context import (
    RetrievedChunk,
    deduplicate_chunks,
    format_chunks_for_context,
    rank_chunks_by_relevance,
)


@pytest.mark.unit
def test_format_chunks_for_context():
    """Test formatting chunks into context string"""
    chunks = [
        RetrievedChunk(
            id=1,
            text="First chunk about Python",
            similarity=0.9,
            source_table="work_experience",
            source_id=1,
            metadata={},
        ),
        RetrievedChunk(
            id=2,
            text="Second chunk about Go",
            similarity=0.85,
            source_table="projects",
            source_id=2,
            metadata={},
        ),
    ]

    context = format_chunks_for_context(chunks)

    assert "[Source 1]" in context
    assert "[Source 2]" in context
    assert "Python" in context
    assert "Go" in context
    assert "---" in context


@pytest.mark.unit
def test_format_chunks_empty():
    """Test formatting with no chunks"""
    context = format_chunks_for_context([])
    assert context == "No relevant information found."


@pytest.mark.unit
def test_rank_chunks_by_relevance():
    """Test ranking chunks by similarity"""
    chunks = [
        RetrievedChunk(
            id=1,
            text="A",
            similarity=0.7,
            source_table="t",
            source_id=1,
            metadata={},
        ),
        RetrievedChunk(
            id=2,
            text="B",
            similarity=0.9,
            source_table="t",
            source_id=2,
            metadata={},
        ),
        RetrievedChunk(
            id=3,
            text="C",
            similarity=0.8,
            source_table="t",
            source_id=3,
            metadata={},
        ),
    ]

    ranked = rank_chunks_by_relevance(chunks, "query")

    assert ranked[0].similarity == 0.9
    assert ranked[1].similarity == 0.8
    assert ranked[2].similarity == 0.7


@pytest.mark.unit
def test_deduplicate_chunks():
    """Test removing duplicate chunks"""
    chunks = [
        RetrievedChunk(
            id=1,
            text="Same text",
            similarity=0.9,
            source_table="t",
            source_id=1,
            metadata={},
        ),
        RetrievedChunk(
            id=2,
            text="Same text",
            similarity=0.85,
            source_table="t",
            source_id=2,
            metadata={},
        ),
        RetrievedChunk(
            id=3,
            text="Different text",
            similarity=0.8,
            source_table="t",
            source_id=3,
            metadata={},
        ),
    ]

    unique = deduplicate_chunks(chunks)

    assert len(unique) == 2
    assert unique[0].text == "Same text"
    assert unique[1].text == "Different text"
