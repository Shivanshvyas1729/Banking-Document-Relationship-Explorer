"""
Tests for core.doc_parser.DocParser

Covers:
    FR2 - parses documents, extracts text
    FR3 - key terms/entities/topics extracted per document
    NFR2 - processing time < 30 seconds/file
"""

import pytest
from core.doc_parser import DocParser


def test_parse_pdf_extracts_text():
    """TODO (Phase 2): parsing a sample PDF returns non-empty text."""
    raise NotImplementedError


def test_parse_docx_extracts_text():
    """TODO (Phase 2): parsing a sample DOCX returns non-empty text."""
    raise NotImplementedError


def test_parse_txt_extracts_text():
    """TODO (Phase 2): parsing a sample TXT returns the exact file contents."""
    raise NotImplementedError


def test_extract_entities_returns_expected_shape():
    """TODO (Phase 2): extract_entities() returns dict with entities/topics/key_terms keys."""
    raise NotImplementedError
