"""
core/vector_db_client.py
=========================
Class: VectorDBClient
Source: LLD Section 2 "Class/Interface Overview"

    Description: Interface to vector database
    Key Methods/Attributes: store_embedding(), search(query)

System Component (HLD Section 1 / LLD Section 1):
    "Vector DB Interface" -> "Manages storage/retrieval of embeddings in
    vector database" -> Key Responsibilities: Store, search, retrieve
    document vectors.

Technical Spec:
    FAISS, ChromaDB, Pinecone, or similar (PRD Section 7, HLD Section 4).

Data Model stored (LLD Section 3):
    Embedding: doc_id, vector, metadata

Security (HLD Section 5 / PRD NFR4):
    In-memory/session-based storage; no document retention post-session.

Error Handling (LLD Section 5):
    Scenario: Vector DB connection error -> Retry, show error if persistent
    Scenario: No relevant documents retrieved -> Inform user, suggest query refinement
"""

import config


class VectorDBClient:
    """Thin wrapper around the chosen vector database backend.

    Backend is selected via config.VECTOR_DB_BACKEND ("faiss" or "chromadb").
    Because config.VECTOR_DB_PERSIST_DIR is intentionally None, the index
    lives only for the duration of the Streamlit session (NFR4).
    """

    def __init__(self, backend: str = None):
        self.backend = backend or config.VECTOR_DB_BACKEND
        self._index = None  # underlying FAISS/Chroma index, created on first store

    def store_embedding(self, doc_id: str, vector: list, metadata: dict = None) -> None:
        """Persist (session-scoped) a document's embedding + metadata.

        metadata typically carries the entities/topics extracted by
        DocParser so search() results can be enriched without a second
        document lookup.

        On connection error: retry, and only surface an error to the user
        if retries are exhausted (LLD Section 5).
        """
        raise NotImplementedError(
            "Implement in Phase 3: add (doc_id, vector, metadata) to the "
            "FAISS/Chroma index, wrapping calls in a retry policy."
        )

    def search(self, query_vector: list, top_k: int = None):
        """Return the top_k most similar embeddings as RetrievalResult-shaped data.

        top_k defaults to config.RAG_TOP_K. If nothing relevant is found,
        the caller (RAGEngine) should inform the user and suggest query
        refinement rather than fabricating an answer (LLD Section 5).
        """
        raise NotImplementedError(
            "Implement in Phase 3: run a similarity search against the "
            "index and return [RetrievalResult(doc_id, score, snippet), ...]."
        )
