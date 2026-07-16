"""
tests/test_doc_parser.py
========================

Unit tests for the DocParser class.
"""

import os
import sys
import tempfile
from pathlib import Path
import pytest

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.doc_parser import DocParser


@pytest.fixture(scope="module")
def parser():
    """Module-level fixture to load DocParser and spaCy only once."""
    return DocParser()


def test_parse_txt(parser):
    """Test that a plain text file is parsed correctly."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w", encoding="utf-8") as f:
        f.write("Hello, this is a test text file for parsing.")
        temp_path = f.name

    try:
        content = parser.parse(temp_path)
        assert "parsing" in content
        assert "Hello" in content
    finally:
        os.unlink(temp_path)


def test_parse_unsupported(parser):
    """Test that an unsupported file format raises a RuntimeError containing ValueError."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        temp_path = f.name

    try:
        with pytest.raises(RuntimeError) as exc_info:
            parser.parse(temp_path)
        assert "Unsupported file type" in str(exc_info.value.__cause__ or exc_info.value)
    finally:
        os.unlink(temp_path)


def test_parse_missing_file(parser):
    """Test that a missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parser.parse("non_existent_file_12345.txt")


def test_extract_entities(parser):
    """Test that named entities, topics, and key terms are extracted in the correct structure."""
    text = (
        "John Doe visited the Federal Reserve in Washington, D.C. on January 15, 2026. "
        "They discussed monetary policies and the inflation rate, which affected banking transactions."
    )
    result = parser.extract_entities(text)

    # Check structure
    assert "entities" in result
    assert "topics" in result
    assert "key_terms" in result

    assert isinstance(result["entities"], list)
    assert isinstance(result["topics"], list)
    assert isinstance(result["key_terms"], list)

    # Verify that items were extracted
    assert len(result["entities"]) > 0 or len(result["topics"]) > 0 or len(result["key_terms"]) > 0


def test_extract_entities_empty(parser):
    """Test extracting entities from empty text returns an empty structure."""
    result = parser.extract_entities("")
    assert result == {"entities": [], "topics": [], "key_terms": []}
