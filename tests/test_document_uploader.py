"""
tests/test_document_uploader.py
================================

Unit tests for the DocumentUploader class.
"""

import os
import sys
# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch
import shutil
import tempfile
from pathlib import Path
import pytest

import config
from core.document_uploader import DocumentUploader
from utils.error_handling import InvalidFileError


@pytest.fixture(autouse=True)
def mock_pipeline_dependencies():
    """Automatically mock parser, embedder, and vector DB client to prevent live API calls and parsing failures in uploader tests."""
    with patch("core.embedder.OpenAIEmbeddings") as MockEmbeddings, \
         patch("core.doc_parser.DocParser") as MockParser, \
         patch("core.vector_db_client.VectorDBClient") as MockVectorDB:

        # Setup mock parser return values
        mock_parser_instance = MockParser.return_value
        mock_parser_instance.parse.return_value = "Mocked parsed content"
        mock_parser_instance.extract_entities.return_value = {
            "entities": [],
            "topics": [],
            "key_terms": []
        }

        # Setup mock embedder — both single and batch methods
        mock_emb_instance = MockEmbeddings.return_value
        mock_emb_instance.embed_query.return_value = [0.1, 0.2, 0.3]
        mock_emb_instance.embed_documents.return_value = [[0.1, 0.2, 0.3]]

        yield


class MockUploadedFile:
    """Mock class simulating Streamlit's UploadedFile / file-like objects."""

    def __init__(self, name: str, content: bytes):
        self.name = name
        self.content = content
        self.size = len(content)

    def read(self) -> bytes:
        return self.content

    def seek(self, offset: int, whence: int = 0) -> None:
        pass


@pytest.fixture
def temp_upload_dir():
    """Fixture that creates and tears down a temporary upload directory."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


def test_upload_valid_files(temp_upload_dir):
    """Test that valid file types (.txt, .pdf, .docx) upload successfully."""
    uploader = DocumentUploader(upload_dir=temp_upload_dir)

    file1 = MockUploadedFile("test1.txt", b"Hello text file")
    file2 = MockUploadedFile("test2.pdf", b"%PDF-1.4 dummy pdf content")
    file3 = MockUploadedFile("test3.docx", b"dummy word content")

    uploaded = uploader.upload_files([file1, file2, file3])

    assert len(uploaded) == 3
    assert len(uploader.get_file_list()) == 3

    # Check files on disk
    for doc in uploaded:
        assert Path(doc.path).exists()
        assert Path(doc.path).parent == temp_upload_dir


def test_upload_invalid_extension(temp_upload_dir):
    """Test that files with unsupported extensions are rejected."""
    uploader = DocumentUploader(upload_dir=temp_upload_dir)

    file_invalid = MockUploadedFile("image.png", b"dummy png content")

    with pytest.raises(InvalidFileError) as exc_info:
        uploader.upload_files([file_invalid])

    assert "Unsupported file type" in str(exc_info.value)
    assert len(uploader.get_file_list()) == 0


def test_upload_limit_exceeded(temp_upload_dir, monkeypatch):
    """Test that uploading beyond the maximum session limit raises an error."""
    # Temporarily set max documents to 2
    monkeypatch.setattr(config, "MAX_DOCUMENTS_PER_SESSION", 2)

    uploader = DocumentUploader(upload_dir=temp_upload_dir)

    file1 = MockUploadedFile("test1.txt", b"content1")
    file2 = MockUploadedFile("test2.docx", b"content2")
    file3 = MockUploadedFile("test3.pdf", b"content3")

    # Upload first two
    uploader.upload_files([file1, file2])
    assert len(uploader.get_file_list()) == 2

    # Third upload should exceed limit
    with pytest.raises(InvalidFileError) as exc_info:
        uploader.upload_files([file3])

    assert "Maximum document limit" in str(exc_info.value)
    assert len(uploader.get_file_list()) == 2


def test_remove_file(temp_upload_dir):
    """Test removing an uploaded file deletes it from disk and uploader state."""
    uploader = DocumentUploader(upload_dir=temp_upload_dir)

    file1 = MockUploadedFile("test1.txt", b"content1")
    uploaded = uploader.upload_files([file1])
    doc = uploaded[0]
    doc_id = doc.id
    file_path = Path(doc.path)

    assert file_path.exists()
    assert len(uploader.get_file_list()) == 1

    # Remove document
    success = uploader.remove_file(doc_id)
    assert success is True
    assert len(uploader.get_file_list()) == 0
    assert not file_path.exists()

    # Attempting to remove non-existent file returns False
    success_non_existent = uploader.remove_file("non-existent-id")
    assert success_non_existent is False


def test_document_schema_properties(temp_upload_dir):
    """Test custom properties and getters/setters on Document schema."""
    uploader = DocumentUploader(upload_dir=temp_upload_dir)
    file1 = MockUploadedFile("test1.txt", b"content1")
    uploaded = uploader.upload_files([file1])
    doc = uploaded[0]
    
    # Verify default parsed_entities structure
    assert doc.parsed_entities == {"entities": [], "topics": [], "key_terms": []}
    
    # Verify explicit setter persists back to metadata
    doc.parsed_entities = {
        "entities": ["Bank"],
        "topics": ["Finance"],
        "key_terms": ["Account"]
    }
    assert doc.metadata["parsed_entities"]["entities"] == ["Bank"]
    
    # Verify mutating nested lists persists back to metadata
    doc.parsed_entities["entities"].append("Branch")
    assert doc.metadata["parsed_entities"]["entities"] == ["Bank", "Branch"]
    
    # Verify content property links to page_content (get/set)
    assert doc.content == "Mocked parsed content"
    doc.content = "New text content"
    assert doc.page_content == "New text content"
    assert doc.content == "New text content"

