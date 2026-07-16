"""
utils/error_handling.py
=======================

Centralized error handling and custom exceptions for BankDocLink.
"""


from utils.logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

class InvalidFileError(ValueError):
    """Raised when an uploaded file is invalid (e.g., wrong type or limit exceeded)."""
    def __init__(self, message: str, code: str = "ERR_FILE_VALIDATION"):
        self.code = code
        super().__init__(f"[{code}] {message}")

def handle_invalid_file(filename: str, reason: str) -> None:
    """Logs the validation failure and raises an InvalidFileError."""
    message = f"Invalid file '{filename}': {reason}"
    
    # Log the warning for audit trail purposes
    logger.warning(message)
    
    # Raise the exception to be caught by the UI layer
    raise InvalidFileError(message)


class EmbeddingFailureError(RuntimeError):
    """Raised when document embedding generation fails."""
    def __init__(self, message: str, code: str = "ERR_EMBEDDING_FAILURE"):
        self.code = code
        super().__init__(f"[{code}] {message}")


def handle_embedding_failure(identifier: str, reason: str) -> None:
    """Logs the embedding failure and raises an EmbeddingFailureError."""
    message = f"Failed to generate embedding for '{identifier}': {reason}"
    logger.error(message)
    raise EmbeddingFailureError(message)


class VectorDBError(RuntimeError):
    """Raised when a vector database operation (store or search) fails."""
    def __init__(self, message: str, code: str = "ERR_VECTOR_DB_FAILURE"):
        self.code = code
        super().__init__(f"[{code}] {message}")


def handle_vector_db_error(identifier: str, reason: str) -> None:
    """Logs the vector database error and raises a VectorDBError."""
    message = f"Vector DB error on operation '{identifier}': {reason}"
    logger.error(message)
    raise VectorDBError(message)