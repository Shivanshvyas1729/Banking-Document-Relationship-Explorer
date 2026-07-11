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