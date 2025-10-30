import pytest
from app.services.text_utils import (
    detect_language,
    estimate_tokens,
    chunk_text,
    split_into_sentences
)

@pytest.mark.unit
def test_detect_language_english():
    """Test English language detection"""
    text = "This is a test in English language."
    lang = detect_language(text)
    assert lang == "en"

@pytest.mark.unit
def test_detect_language_short_text():
    """Test detection with very short text (fallback to en)"""
    text = "Hi"
    lang = detect_language(text)
    assert lang == "en"

@pytest.mark.unit
def test_estimate_tokens():
    """Test token estimation"""
    text = "This is a test sentence with multiple words."
    tokens = estimate_tokens(text)
    assert tokens == 8  # 8 words

@pytest.mark.unit
def test_chunk_text_short():
    """Test chunking with text shorter than max_tokens"""
    text = "Short text"
    chunks = chunk_text(text, max_tokens=100)
    assert len(chunks) == 1
    assert chunks[0] == "Short text"

@pytest.mark.unit
def test_chunk_text_long():
    """Test chunking with long text"""
    # Create text with many sentences
    sentences = ["This is sentence number {}.".format(i) for i in range(100)]
    text = " ".join(sentences)

    chunks = chunk_text(text, max_tokens=50, overlap=10, min_chunk_size=20)

    # Should create multiple chunks
    assert len(chunks) > 1

    # Each chunk should be reasonably sized
    for chunk in chunks:
        tokens = estimate_tokens(chunk)
        assert tokens <= 60  # Allow some tolerance

@pytest.mark.unit
def test_split_into_sentences():
    """Test sentence splitting"""
    text = "First sentence. Second sentence! Third sentence?"
    sentences = split_into_sentences(text)
    assert len(sentences) == 3
    assert sentences[0] == "First sentence."
    assert sentences[1] == "Second sentence!"
    assert sentences[2] == "Third sentence?"

@pytest.mark.unit
def test_split_with_abbreviations():
    """Test that abbreviations don't cause false splits"""
    text = "Dr. Smith works at the company. He is great."
    sentences = split_into_sentences(text)
    assert len(sentences) == 2
    assert "Dr. Smith" in sentences[0]

@pytest.mark.unit
def test_chunk_text_empty():
    """Test chunking empty text"""
    chunks = chunk_text("")
    assert chunks == []

    chunks = chunk_text("   ")
    assert chunks == []
