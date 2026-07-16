"""
core/ai_generator.py
=====================
Class: AIGenerator
Source: LLD Section 2 "Class/Interface Overview"

    Description: Generates explanations
    Key Methods/Attributes: explain_relationships(context)

System Component (HLD/LLD Section 1):
    "AI Generator" -> "Generative AI for explanations and relationship
    summaries" -> Key Responsibilities: Generate natural language outputs.

Technical Spec:
    RAG Pipeline - Generation: LLM (e.g., GPT-3.5/4 via API) (PRD Section 7).
    RAG & Generative AI: OpenAI API, HuggingFace Transformers, or similar
    (HLD Section 4).

Used in LLD Section 4 "Query & Relationship Exploration":

    def answer_query(query):
        query_vec = Embedder.embed(query)
        results = VectorDBClient.search(query_vec)
        context = [r.snippet for r in results]
        explanation = AIGenerator.explain_relationships(context)
        return explanation

Error Handling (LLD Section 5):
    Scenario: AI generation timeout/failure -> Return fallback message, log for review
"""

import config


class AIGenerator:
    """Wraps the configured LLM provider to turn retrieved context into a
    natural-language explanation of cross-document relationships.
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.LLM_MODEL_NAME

    def explain_relationships(self, context: list[str]) -> str:
        """Generate an explanation of how the documents/snippets in
        `context` relate to the user's query.

        Must respect config.QUERY_RESPONSE_TIMEOUT_SECONDS (Success Metric:
        query response time < 10 seconds). On timeout/failure: return a
        fallback message and log the failure for review (LLD Section 5) -
        never raise an unhandled exception up to the UI.
        """
        raise NotImplementedError(
            "Implement in Phase 4: call config.LLM_PROVIDER (OpenAI or "
            "HuggingFace) with a prompt built from `context`, enforce a "
            "timeout, and catch/log failures with a graceful fallback "
            "string, e.g. 'Unable to generate an explanation right now.'"
        )
