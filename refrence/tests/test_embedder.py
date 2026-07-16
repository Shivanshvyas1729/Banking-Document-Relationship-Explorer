"""
Tests for core.embedder.Embedder

Covers:
    FR2 - generates vector embeddings
    LLD Section 5 - Embedding/model failure -> log error, notify user, skip document
"""

import pytest
from core.embedder import Embedder


def test_embed_returns_vector_of_expected_dimension():
    """TODO (Phase 2): embed(text) returns a list[float] of the model's known dimension."""
    raise NotImplementedError


def test_embed_handles_model_failure_gracefully():
    """TODO (Phase 2): a model failure should raise EmbeddingGenerationError, not crash silently."""
    raise NotImplementedError
