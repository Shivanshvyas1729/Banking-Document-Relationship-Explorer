"""
core/embedder.py
=================
Class: Embedder
Source: LLD Section 2 "Class/Interface Overview"

    Description: Generates vector embeddings
    Key Methods/Attributes: embed(text), model

Technical Spec (PRD Section 7 / HLD Section 4):
    Embedding Model: OpenAI, HuggingFace Transformers, or similar
    (HLD specifically calls out "Pre-trained embedding models e.g. Sentence Transformers")

Used by both:
    - Document indexing (LLD Section 4 Document Upload & Indexing)
    - Query embedding (LLD Section 4 Query & Relationship Exploration):
        query_vec = Embedder.embed(query)

Error Handling (LLD Section 5):
    Scenario: Embedding/model failure -> Log error, notify user, skip document
"""

import config


class Embedder:
    """Wraps whichever embedding backend is configured (config.EMBEDDING_PROVIDER).

    Kept as a thin, swappable interface so DocumentUploader/RAGEngine never
    need to know whether embeddings come from OpenAI, HuggingFace, or
    Sentence Transformers (HLD Section 4 Technology Stack).
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.EMBEDDING_MODEL_NAME
        self.model = None  # lazily-loaded underlying embedding model/client

    def embed(self, text: str) -> list:
        """Generate a vector embedding for `text`.

        On failure: log the error, notify the user (surface via UI layer),
        and skip the offending document rather than crashing the whole
        upload batch (LLD Section 5 error handling table).
        """
        raise NotImplementedError(
            "Implement in Phase 2: load config.EMBEDDING_MODEL_NAME via "
            "sentence-transformers (or OpenAI embeddings API) and return "
            "model.encode(text)."
        )
