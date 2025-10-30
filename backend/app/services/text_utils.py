import logging
import re

from langdetect import LangDetectException, detect

logger = logging.getLogger(__name__)


def detect_language(text: str) -> str:
    """
    Detect language of text.
    Returns ISO 639-1 language code (e.g., 'en', 'ru', 'de')
    Falls back to 'en' if detection fails.
    """
    if not text or len(text.strip()) < 3:
        return "en"

    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        logger.warning(f"Language detection failed for text: {text[:50]}...")
        return "en"


def estimate_tokens(text: str) -> int:
    """
    Estimate number of tokens in text.
    Rough approximation: 1 token ≈ 4 characters for English
    """
    # Simple heuristic: split by whitespace and punctuation
    words = re.findall(r"\b\w+\b", text)
    return len(words)


def chunk_text(
    text: str,
    max_tokens: int = 800,
    overlap: int = 150,
    min_chunk_size: int = 100,
) -> list[str]:
    """
    Split text into chunks with overlap.

    Args:
        text: Text to split
        max_tokens: Maximum tokens per chunk
        overlap: Number of tokens to overlap between chunks
        min_chunk_size: Minimum chunk size (discard smaller chunks)

    Returns:
        List of text chunks
    """
    if not text or not text.strip():
        return []

    # Estimate tokens
    estimated_tokens = estimate_tokens(text)

    # If text is short enough, return as single chunk
    if estimated_tokens <= max_tokens:
        return [text.strip()]

    # Split by sentences
    sentences = split_into_sentences(text)

    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = estimate_tokens(sentence)

        # If single sentence exceeds max_tokens, split it further
        if sentence_tokens > max_tokens:
            # Split by punctuation
            sub_parts = re.split(r"[,;:]", sentence)
            for part in sub_parts:
                part = part.strip()
                if not part:
                    continue

                part_tokens = estimate_tokens(part)

                if current_tokens + part_tokens > max_tokens:
                    # Save current chunk
                    if current_chunk and current_tokens >= min_chunk_size:
                        chunks.append(" ".join(current_chunk))

                    # Start new chunk with overlap
                    overlap_sentences = get_overlap_sentences(
                        current_chunk, overlap
                    )
                    current_chunk = overlap_sentences + [part]
                    current_tokens = sum(
                        estimate_tokens(s) for s in current_chunk
                    )
                else:
                    current_chunk.append(part)
                    current_tokens += part_tokens
        # Normal sentence processing
        elif current_tokens + sentence_tokens > max_tokens:
            # Save current chunk
            if current_chunk and current_tokens >= min_chunk_size:
                chunks.append(" ".join(current_chunk))

            # Start new chunk with overlap
            overlap_sentences = get_overlap_sentences(
                current_chunk, overlap
            )
            current_chunk = overlap_sentences + [sentence]
            current_tokens = sum(estimate_tokens(s) for s in current_chunk)
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

    # Add last chunk
    if current_chunk and current_tokens >= min_chunk_size:
        chunks.append(" ".join(current_chunk))

    return chunks


def split_into_sentences(text: str) -> list[str]:
    """
    Split text into sentences.
    Handles common abbreviations and edge cases.
    """
    # Replace common abbreviations to avoid false splits
    text = text.replace("Dr.", "Dr<DOT>")
    text = text.replace("Mr.", "Mr<DOT>")
    text = text.replace("Mrs.", "Mrs<DOT>")
    text = text.replace("Ms.", "Ms<DOT>")
    text = text.replace("Jr.", "Jr<DOT>")
    text = text.replace("Sr.", "Sr<DOT>")
    text = text.replace("e.g.", "e<DOT>g<DOT>")
    text = text.replace("i.e.", "i<DOT>e<DOT>")

    # Split by sentence endings
    sentences = re.split(r"(?<=[.!?])\s+", text)

    # Restore abbreviations
    sentences = [s.replace("<DOT>", ".") for s in sentences]

    # Filter out empty sentences
    return [s.strip() for s in sentences if s.strip()]


def get_overlap_sentences(
    sentences: list[str], overlap_tokens: int
) -> list[str]:
    """
    Get sentences from the end that fit within overlap_tokens.
    """
    if not sentences:
        return []

    overlap = []
    tokens = 0

    for sentence in reversed(sentences):
        sentence_tokens = estimate_tokens(sentence)
        if tokens + sentence_tokens > overlap_tokens:
            break
        overlap.insert(0, sentence)
        tokens += sentence_tokens

    return overlap
