"""
models/schemas.py
==================
Data model definitions.

Source: LLD Section 3 "Data Structure Overview"

    Data Model      | Fields/Schema
    -----------------|--------------------------------------------
    Document         | id, filename, raw_text, parsed_entities
    Embedding        | doc_id, vector, metadata
    Query            | query_text, filters
    RetrievalResult  | doc_id, score, snippet
    Explanation      | query, related_docs, generated_text

These are implemented as dataclasses so they can be passed between
DocumentUploader -> DocParser -> Embedder -> VectorDBClient -> RAGEngine ->
AIGenerator (see LLD Section 2 "Relationships") without ambiguity about
shape or required fields.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Document:
    """A single uploaded banking document.

    id: unique identifier assigned on upload (e.g., uuid4 hex)
    filename: original filename as uploaded by the user
    raw_text: full extracted text (populated by DocParser.parse)
  
    """
    id: str
    filename: str
    raw_text: str = ""
    


@dataclass
class Embedding:
    """Vector representation of a Document (or a chunk of one).

    doc_id: foreign key back to Document.id
    vector: the embedding vector (list[float])
    metadata: arbitrary metadata stored alongside the vector in the vector DB,
        e.g. entities/topics so VectorDBClient.search() can return rich context
        without a second lookup (see LLD Section 4 Document Upload & Indexing).
    """
    doc_id: str
    vector: list
    metadata: dict = field(default_factory=dict)


@dataclass
class Query:
    """A user-submitted question about document relationships.

    query_text: the raw natural-language question typed by the user
    filters: optional constraints (e.g., restrict to a subset of doc_ids)
    """
    query_text: str
    filters: Optional[dict] = None


@dataclass
class RetrievalResult:
    """A single relevant hit returned by VectorDBClient.search().

    doc_id: which Document this result came from
    score: similarity score (higher = more relevant, or distance depending on backend)
    snippet: the retrieved text chunk used as RAG context
    """
    doc_id: str
    score: float
    snippet: str


@dataclass
class Explanation:
    """The final AI-generated answer returned to the UI.

    query: the original Query object (or text) this explanation answers
    related_docs: list of doc_ids that contributed to the answer
    generated_text: the natural-language explanation from AIGenerator
    """
    query: str
    related_docs: list
    generated_text: str
