"""
ui/relationship_explorer.py
============================
UI Page: Relationship Explorer
Source: PRD Section 8 "UI/UX Overview"

    Relationship Explorer: Interactive graph/network of cross-document
    relationships.

Functional Requirements covered:
    FR4 - Relationships between terms/entities/topics across documents are
          visualized (e.g., graph view).

Technical approach (HLD Section 4 Visualization):
    Streamlit components (e.g., network/graph visualization libraries)
    -> networkx to build the graph, pyvis (or streamlit-agraph) to render it.

Success Metric this page supports:
    Relationship accuracy > 85% (manual eval)
"""

import streamlit as st
from models.schemas import Document


def build_relationship_graph(documents: list[Document]):
    """Build a graph where nodes are documents + shared entities/topics, and
    edges connect documents that share a key term/entity/topic.

    Returns a networkx.Graph (or compatible structure) ready to be rendered.
    """
    raise NotImplementedError(
        "Implement in Phase 6: use networkx.Graph(); add a node per document "
        "(doc.id, label=doc.filename) and a node per shared entity/topic; "
        "add edges document<->entity for each entity in doc.parsed_entities."
    )


def render(documents: list[Document]) -> None:
    """Render the interactive relationship graph in the Streamlit page."""
    st.header("🕸️ Relationship Explorer")

    if len(documents) < 2:
        st.info("Upload at least 2 documents to explore relationships between them.")
        return

    raise NotImplementedError(
        "Implement in Phase 6: graph = build_relationship_graph(documents); "
        "render with pyvis.network.Network(...).from_nx(graph) embedded via "
        "st.components.v1.html(), or streamlit-agraph as an alternative."
    )
