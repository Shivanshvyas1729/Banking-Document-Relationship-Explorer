"""
Tests for core.document_uploader.DocumentUploader

Covers:
    FR1 - upload, view, remove multiple documents
    NFR3 - support for at least 10 documents/session
    LLD Section 5 - Invalid/unsupported file upload -> show error, skip file
"""

import pytest
from core.document_uploader import DocumentUploader


def test_upload_files_accepts_supported_types():
    """TODO (Phase 1): uploading a .pdf/.docx/.txt file should register a Document."""
    raise NotImplementedError


def test_upload_files_rejects_unsupported_type():
    """TODO (Phase 1): an unsupported extension should be skipped with an error, not crash."""
    raise NotImplementedError


def test_max_documents_per_session_enforced():
    """TODO (Phase 1): uploading more than config.MAX_DOCUMENTS_PER_SESSION should be capped."""
    raise NotImplementedError


def test_remove_file():
    """TODO (Phase 1): remove_file(doc_id) removes the doc and returns True; unknown id returns False."""
    raise NotImplementedError
