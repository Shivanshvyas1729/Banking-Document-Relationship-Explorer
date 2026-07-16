"""
Tests for core.rag_engine.RAGEngine

Covers:
    FR5 - Users can input queries; system uses RAG to retrieve and generate explanations.
    Success Metric: Query response time < 10 seconds.
    LLD Section 5 - AI generation timeout/failure -> fallback message, log for review
"""

import pytest
from core.rag_engine import RAGEngine


def test_retrieve_embeds_query_and_searches_vector_db():
    """TODO (Phase 4): retrieve() calls embedder.embed then vector_db.search with that vector."""
    raise NotImplementedError


def test_generate_answer_full_pipeline():
    """TODO (Phase 4): generate_answer() returns an Explanation built from retrieved snippets."""
    raise NotImplementedError


def test_generate_answer_no_results_message():
    """TODO (Phase 4): when retrieve() returns [], generate_answer() returns a refinement-suggestion message."""
    raise NotImplementedError


def test_generate_answer_ai_failure_fallback():
    """TODO (Phase 4): when AIGenerator raises, generate_answer() returns the fallback message."""
    raise NotImplementedError
