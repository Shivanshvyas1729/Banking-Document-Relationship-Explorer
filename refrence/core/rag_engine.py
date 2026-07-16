"""
core/rag_engine.py
===================
Class: RAGEngine
Source: LLD Section 2 "Class/Interface Overview"

    Description: Orchestrates retrieval and generation
    Key Methods/Attributes: retrieve(query), generate_answer()

Relationship (LLD Section 2): "RAGEngine uses VectorDBClient and AIGenerator"

System Component (HLD Section 1):
    "RAG Engine" -> "Retrieves related content and generates explanations
    using generative AI."

Architecture Flow this class implements (HLD Section 1 Architecture Flow,
steps 4-6):
    4. User submits a query about document relationships.
    5. Query Handler retrieves relevant content using RAG.
    6. Generative AI produces explanations, displayed in the UI.

Functional Requirements covered:
    FR5 - Users can input queries; system uses RAG to retrieve and generate
          explanations. (High)

Full pipeline (LLD Section 4 "Query & Relationship Exploration"):

    def answer_query(query):
        query_vec = Embedder.embed(query)
        results = VectorDBClient.search(query_vec)
        context = [r.snippet for r in results]
        explanation = AIGenerator.explain_relationships(context)
        return explanation
"""

from core.embedder import Embedder
from core.vector_db_client import VectorDBClient
from core.ai_generator import AIGenerator
from models.schemas import Query, RetrievalResult, Explanation


class RAGEngine:
    """Orchestrates the retrieval-augmented generation pipeline:
    Embedder -> VectorDBClient -> AIGenerator.
    """

    def __init__(self, embedder: Embedder, vector_db: VectorDBClient, ai_generator: AIGenerator):
        self.embedder = embedder
        self.vector_db = vector_db
        self.ai_generator = ai_generator

    def retrieve(self, query: Query) -> list[RetrievalResult]:
        """Embed the query and fetch the most relevant document snippets.

        Corresponds to `query_vec = Embedder.embed(query)` +
        `results = VectorDBClient.search(query_vec)` in LLD Section 4.
        """
        raise NotImplementedError(
            "Implement in Phase 4: query_vec = self.embedder.embed(query.query_text); "
            "return self.vector_db.search(query_vec)"
        )

    def generate_answer(self, query: Query) -> Explanation:
        """Full RAG pipeline: retrieve context, then generate an explanation.

        Corresponds to `answer_query(query)` in LLD Section 4. If retrieve()
        returns no results, inform the user and suggest query refinement
        rather than calling the AI Generator with empty context (LLD
        Section 5 error handling table).
        """
        raise NotImplementedError(
            "Implement in Phase 4: results = self.retrieve(query); "
            "if not results: return Explanation with a 'no relevant "
            "documents found, try refining your query' message; "
            "else context = [r.snippet for r in results]; "
            "generated_text = self.ai_generator.explain_relationships(context); "
            "return Explanation(query.query_text, [r.doc_id for r in results], generated_text)"
        )
