"""
ui/main_page.py
================
UI Page: Main Page
Source: PRD Section 8 "UI/UX Overview"

    Main Page: Upload/manage documents, view document list.

Wires together:
    - core.document_uploader.DocumentUploader.upload_files()
    - core.document_uploader.DocumentUploader.get_file_list()
    - core.document_uploader.DocumentUploader.remove_file()

Functional Requirements covered:
    FR1 - Users can upload, view, and remove multiple documents.

Non-Functional Requirements covered:
    NFR1 - Responsive and intuitive UI
    NFR3 - Support for at least 10 documents/session
"""

import streamlit as st
from core.document_uploader import DocumentUploader
import config


def render(uploader: DocumentUploader) -> None:
    """Render the Main Page: file uploader widget + current document list
    with per-document remove buttons.
    """
    st.header("📁 Document Manager")
    st.caption(
        f"Upload up to {config.MAX_DOCUMENTS_PER_SESSION} banking documents "
        f"({', '.join(config.SUPPORTED_FILE_TYPES).upper()})."
    )

    raise NotImplementedError(
        "Implement in Phase 5: st.file_uploader(accept_multiple_files=True) "
        "-> uploader.upload_files(files); then st.write a table/list from "
        "uploader.get_file_list() with a remove button per row calling "
        "uploader.remove_file(doc_id)."
    )
