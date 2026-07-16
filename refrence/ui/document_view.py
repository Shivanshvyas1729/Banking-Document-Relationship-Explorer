"""
ui/document_view.py
====================
UI Page: Document View
Source: PRD Section 8 "UI/UX Overview"

    Document View: See extracted terms/entities/topics.

Wires together:
    - core.doc_parser.DocParser.extract_entities() (already run at upload time,
      results stored on Document.parsed_entities)

Functional Requirements covered:
    FR3 - Key terms, entities, and topics are extracted and displayed per document.
"""

import streamlit as st
from models.schemas import Document


def render(documents: list[Document]) -> None:
    """Render a per-document breakdown of extracted key terms, entities,
    and topics (Document.parsed_entities), e.g. as an expander per document
    with three columns/tag-lists: entities, topics, key_terms.
    """
    st.header("🔍 Document Insights")

    if not documents:
        st.info("Upload documents on the Main Page to see extracted insights here.")
        return

    raise NotImplementedError(
        "Implement in Phase 5: for doc in documents: st.expander(doc.filename) "
        "showing doc.parsed_entities['entities'], ['topics'], ['key_terms'] "
        "as tag chips or bullet lists."
    )
