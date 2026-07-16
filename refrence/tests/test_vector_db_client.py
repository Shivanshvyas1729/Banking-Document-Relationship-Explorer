"""
Tests for core.vector_db_client.VectorDBClient

Covers:
    FR2 - stores embeddings
    FR5 - search retrieves relevant content for RAG
    LLD Section 5 - Vector DB connection error -> retry, show error if persistent
    LLD Section 5 - No relevant documents retrieved -> inform user, suggest refinement
"""

import pytest
from core.vector_db_client import VectorDBClient


def test_store_and_search_round_trip():
    """TODO (Phase 3): storing an embedding then searching with the same vector returns it as top hit."""
    raise NotImplementedError


def test_search_returns_empty_when_no_matches():
    """TODO (Phase 3): searching an empty/unrelated index returns an empty list, not an error."""
    raise NotImplementedError


def test_connection_error_retries_then_raises():
    """TODO (Phase 3): a persistent connection failure should raise VectorDBConnectionError after retries."""
    raise NotImplementedError
