"""
utils/error_handling.py
========================
Centralized error handling policy, implementing LLD Section 5 verbatim:

    Scenario                          | Handling Approach
    -----------------------------------|--------------------------------------
    Invalid/unsupported file upload    | Show error message, skip file
    Embedding/model failure            | Log error, notify user, skip document
    Vector DB connection error         | Retry, show error if persistent
    No relevant documents retrieved    | Inform user, suggest query refinement
    AI generation timeout/failure      | Return fallback message, log for review

Each scenario below gets a small helper so `core/` modules and `ui/` pages
apply the policy consistently instead of re-implementing it ad hoc.
"""

from utils.logger import get_logger

logger = get_logger(__name__)


class UnsupportedFileError(Exception):
    """Raised by DocParser/DocumentUploader for invalid/unsupported files."""


class EmbeddingGenerationError(Exception):
    """Raised by Embedder on model failure."""


class VectorDBConnectionError(Exception):
    """Raised by VectorDBClient after retries are exhausted."""


class AIGenerationError(Exception):
    """Raised by AIGenerator on timeout/failure."""


def handle_invalid_file(filename: str) -> str:
    """Invalid/unsupported file upload -> show error message, skip file."""
    message = f"'{filename}' is not a supported file type and was skipped."
    logger.warning(message)
    return message


def handle_embedding_failure(doc_id: str, error: Exception) -> str:
    """Embedding/model failure -> log error, notify user, skip document."""
    logger.error(f"Embedding failed for doc_id={doc_id}: {error}")
    return f"Could not process document {doc_id}; it was skipped."


def handle_vector_db_error(error: Exception, retries_exhausted: bool) -> str | None:
    """Vector DB connection error -> retry, show error if persistent."""
    if retries_exhausted:
        logger.error(f"Vector DB connection error (retries exhausted): {error}")
        return "We're having trouble reaching the document index. Please try again shortly."
    logger.warning(f"Vector DB connection error, retrying: {error}")
    return None


def handle_no_results(query_text: str) -> str:
    """No relevant documents retrieved -> inform user, suggest query refinement."""
    logger.info(f"No relevant documents found for query: {query_text!r}")
    return "No relevant documents were found. Try rephrasing or narrowing your question."


def handle_ai_generation_failure(error: Exception) -> str:
    """AI generation timeout/failure -> return fallback message, log for review."""
    logger.error(f"AI generation failed: {error}")
    return "The explanation could not be generated right now. Please try again."
