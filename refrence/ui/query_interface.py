"""
ui/query_interface.py
======================
UI Page: Query Interface
Source: PRD Section 8 "UI/UX Overview"

    Query Interface: Input questions, view AI-generated answers with
    supporting document snippets.

Wires together:
    - core.rag_engine.RAGEngine.generate_answer()

Functional Requirements covered:
    FR5 - Users can input queries; system uses RAG to retrieve and generate
          explanations.

Success Metrics this page supports:
    Query response time < 10 seconds
    User satisfaction (survey) > 80% positive
"""

import streamlit as st
from core.rag_engine import RAGEngine
from models.schemas import Query


def render(rag_engine: RAGEngine) -> None:
    """Render a text input for the user's question, a submit button, and
    the resulting Explanation (generated_text + supporting snippets from
    related_docs).
    """
    st.header("💬 Ask About Document Relationships")

    raise NotImplementedError(
        "Implement in Phase 6: query_text = st.text_input(...); on submit, "
        "with st.spinner('Generating explanation...'): "
        "explanation = rag_engine.generate_answer(Query(query_text)); "
        "st.write(explanation.generated_text); "
        "st.caption('Sources: ' + ', '.join(explanation.related_docs))"
    )
