"""
tests/test_vector_db_client.py
==============================

Unit tests for the VectorDBClient class.
"""

import os
import sys
from unittest.mock import patch
import pytest

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.vector_db_client import VectorDBClient
from models.schemas import RetrievalResult
from utils.error_handling import VectorDBError


def test_init():
    """Test database initialization and config settings."""
    with patch("core.vector_db_client.OpenAIEmbeddings") as MockEmbeddings:
        client = VectorDBClient(backend="faiss")
        assert client.backend == "faiss"
        MockEmbeddings.assert_called_once()


def test_faiss_store_and_search():
    """Test storing and searching embeddings using FAISS backend."""
    with patch("core.vector_db_client.OpenAIEmbeddings"):
        client = VectorDBClient(backend="faiss")
        vector = [0.1, 0.2, 0.3]
        metadata = {"text": "hello faiss chunk", "name": "doc1.txt", "doc_id": "uuid-1"}

        # Store vector
        client.store_embedding(doc_id="uuid-1", vector=vector, metadata=metadata)
        assert client._index is not None

        # Search vector
        results = client.search(query_vector=[0.1, 0.2, 0.29], top_k=1)
        assert len(results) == 1
        res = results[0]
        assert isinstance(res, RetrievalResult)
        assert res.doc_id == "uuid-1"
        assert res.text == "hello faiss chunk"
        assert res.score >= 0.0


def test_chroma_store_and_search():
    """Test storing and searching embeddings using ChromaDB backend."""
    with patch("core.vector_db_client.OpenAIEmbeddings"):
        client = VectorDBClient(backend="chromadb")
        vector = [0.1, 0.2, 0.3]
        metadata = {"text": "hello chroma chunk", "name": "doc2.txt", "doc_id": "uuid-2"}

        # Store vector
        client.store_embedding(doc_id="uuid-2", vector=vector, metadata=metadata)
        assert client._index is not None

        # Search vector
        results = client.search(query_vector=[0.1, 0.2, 0.29], top_k=1)
        assert len(results) == 1
        res = results[0]
        assert isinstance(res, RetrievalResult)
        assert res.doc_id == "uuid-2"
        assert res.text == "hello chroma chunk"
        assert res.score >= 0.0


def test_store_embedding_retry_failure():
    """Test that a persistent failure triggers the retry attempts and raises VectorDBError."""
    with patch("core.vector_db_client.OpenAIEmbeddings"):
        client = VectorDBClient(backend="faiss")

        # Mock FAISS to fail
        with patch("core.vector_db_client.FAISS.from_embeddings", side_effect=Exception("Connection refused")):
            with pytest.raises(VectorDBError) as exc_info:
                client.store_embedding(
                    doc_id="uuid-3",
                    vector=[1.0, 2.0],
                    metadata={"text": "fail text"}
                )
            assert "Failed to persist embedding after 3 attempts" in str(exc_info.value)


# ---------------------------------------------------------------------------
# store_embeddings_batch tests
# ---------------------------------------------------------------------------

def _make_items(n: int, backend_prefix: str = "id") -> list:
    """Helper: build n (doc_id, vector, metadata) tuples."""
    return [
        (f"{backend_prefix}-{i}", [float(i), float(i) + 0.1], {"text": f"chunk {i}", "chunk_index": i})
        for i in range(n)
    ]


def test_batch_faiss_store_and_search():
    """Batch insert via FAISS creates the index and results are searchable."""
    with patch("core.vector_db_client.OpenAIEmbeddings"):
        client = VectorDBClient(backend="faiss")
        items = _make_items(3, "faiss-batch")

        client.store_embeddings_batch(items)
        assert client._index is not None

        # Verify a similarity search returns results
        results = client.search(query_vector=[0.0, 0.1], top_k=2)
        assert len(results) <= 3
        for r in results:
            assert isinstance(r, RetrievalResult)
            assert r.score >= 0.0


def test_batch_chroma_store_and_search():
    """Batch insert via Chroma creates the collection and results are searchable."""
    with patch("core.vector_db_client.OpenAIEmbeddings"):
        client = VectorDBClient(backend="chromadb")
        items = _make_items(3, "chroma-batch")

        client.store_embeddings_batch(items)
        assert client._index is not None

        results = client.search(query_vector=[0.0, 0.1], top_k=2)
        assert len(results) <= 3
        for r in results:
            assert isinstance(r, RetrievalResult)


def test_batch_empty_input_is_noop():
    """store_embeddings_batch with an empty list must not touch the index."""
    with patch("core.vector_db_client.OpenAIEmbeddings"):
        client = VectorDBClient(backend="faiss")
        client.store_embeddings_batch([])   # should not raise
        assert client._index is None        # index never created


def test_batch_retry_failure():
    """Persistent failure during batch insert raises VectorDBError after 3 attempts."""
    with patch("core.vector_db_client.OpenAIEmbeddings"):
        client = VectorDBClient(backend="faiss")

        with patch("core.vector_db_client.FAISS.from_embeddings", side_effect=Exception("Disk full")):
            with pytest.raises(VectorDBError) as exc_info:
                client.store_embeddings_batch(_make_items(2))
            assert "Batch insert failed after 3 attempts" in str(exc_info.value)
            assert "Disk full" in str(exc_info.value)
