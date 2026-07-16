"""
tests/test_embedder.py
======================

Unit tests for the Embedder class, mocking OpenAI API interactions.
"""

import os
import sys
from unittest.mock import patch
import pytest

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.embedder import Embedder
from utils.error_handling import EmbeddingFailureError


def test_embed_success():
    """Test generating embeddings successfully with a mocked OpenAIEmbeddings client."""
    with patch("core.embedder.OpenAIEmbeddings") as MockOpenAIEmbeddings:
        mock_instance = MockOpenAIEmbeddings.return_value
        mock_instance.embed_query.return_value = [0.1, 0.2, 0.3, 0.4]

        embedder = Embedder()
        vector = embedder.embed("Hello world test text")

        assert vector == [0.1, 0.2, 0.3, 0.4]
        mock_instance.embed_query.assert_called_once_with("Hello world test text")


def test_embed_empty():
    """Test embedding an empty or whitespace-only string returns an empty list."""
    with patch("core.embedder.OpenAIEmbeddings") as MockOpenAIEmbeddings:
        embedder = Embedder()
        assert embedder.embed("") == []
        assert embedder.embed("   ") == []


def test_embed_failure():
    """Test that an embedding exception from the OpenAI client is captured and raises EmbeddingFailureError."""
    with patch("core.embedder.OpenAIEmbeddings") as MockOpenAIEmbeddings:
        mock_instance = MockOpenAIEmbeddings.return_value
        mock_instance.embed_query.side_effect = Exception("API connection timeout error")

        embedder = Embedder()
        with pytest.raises(EmbeddingFailureError) as exc_info:
            embedder.embed("Test query that fails")

        assert "Failed to generate embedding" in str(exc_info.value)
        assert "API connection timeout error" in str(exc_info.value)


def test_embedder_init_failure():
    """Test that initialization failures in OpenAIEmbeddings raise EmbeddingFailureError."""
    with patch("core.embedder.OpenAIEmbeddings", side_effect=ValueError("Invalid OpenAI API Key")):
        with pytest.raises(EmbeddingFailureError) as exc_info:
            Embedder()

        assert "Could not initialize OpenAIEmbeddings" in str(exc_info.value)
        assert "Invalid OpenAI API Key" in str(exc_info.value)


# ---------------------------------------------------------------------------
# embed_batch tests
# ---------------------------------------------------------------------------

def test_embed_batch_success():
    """Batch of 3 texts returns 3 vectors in the correct order."""
    with patch("core.embedder.OpenAIEmbeddings") as MockEmbeddings:
        mock_instance = MockEmbeddings.return_value
        mock_instance.embed_documents.return_value = [
            [0.1, 0.2],
            [0.3, 0.4],
            [0.5, 0.6],
        ]

        embedder = Embedder()
        results = embedder.embed_batch(["text A", "text B", "text C"])

        assert len(results) == 3
        assert results[0] == [0.1, 0.2]
        assert results[1] == [0.3, 0.4]
        assert results[2] == [0.5, 0.6]
        mock_instance.embed_documents.assert_called_once_with(["text A", "text B", "text C"])


def test_embed_batch_empty_input():
    """Empty list returns empty list without calling the API."""
    with patch("core.embedder.OpenAIEmbeddings") as MockEmbeddings:
        mock_instance = MockEmbeddings.return_value
        embedder = Embedder()
        assert embedder.embed_batch([]) == []
        mock_instance.embed_documents.assert_not_called()


def test_embed_batch_blank_slot_preservation():
    """Blank/whitespace strings get [] slots; non-blank strings are embedded."""
    with patch("core.embedder.OpenAIEmbeddings") as MockEmbeddings:
        mock_instance = MockEmbeddings.return_value
        mock_instance.embed_documents.return_value = [[1.0, 2.0], [3.0, 4.0]]

        embedder = Embedder()
        results = embedder.embed_batch(["hello", "", "world", "   "])

        assert results[0] == [1.0, 2.0]   # "hello"
        assert results[1] == []            # blank → empty slot
        assert results[2] == [3.0, 4.0]   # "world"
        assert results[3] == []            # whitespace → empty slot
        # Only 2 valid texts were sent to the API
        mock_instance.embed_documents.assert_called_once_with(["hello", "world"])


def test_embed_batch_chunking_over_limit():
    """More than 2048 texts are split into sub-batches of ≤2048."""
    with patch("core.embedder.OpenAIEmbeddings") as MockEmbeddings:
        mock_instance = MockEmbeddings.return_value
        # Return a flat vector for each text
        mock_instance.embed_documents.side_effect = lambda batch: [[0.0, 0.0]] * len(batch)

        embedder = Embedder()
        texts = [f"text_{i}" for i in range(3000)]
        results = embedder.embed_batch(texts)

        assert len(results) == 3000
        # Should have been called twice: first 2048, then 952
        assert mock_instance.embed_documents.call_count == 2
        first_call_len = len(mock_instance.embed_documents.call_args_list[0][0][0])
        second_call_len = len(mock_instance.embed_documents.call_args_list[1][0][0])
        assert first_call_len == 2048
        assert second_call_len == 952


def test_embed_batch_api_failure():
    """API failure during embed_batch propagates as EmbeddingFailureError."""
    with patch("core.embedder.OpenAIEmbeddings") as MockEmbeddings:
        mock_instance = MockEmbeddings.return_value
        mock_instance.embed_documents.side_effect = Exception("Rate limit exceeded")

        embedder = Embedder()
        with pytest.raises(EmbeddingFailureError) as exc_info:
            embedder.embed_batch(["some text"])

        assert "embed_batch" in str(exc_info.value)
        assert "Rate limit exceeded" in str(exc_info.value)
