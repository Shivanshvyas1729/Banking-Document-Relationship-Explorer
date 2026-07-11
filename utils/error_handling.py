"""
utils/error_handling.py
=======================

Centralized error handling and custom exceptions for BankDocLink.
"""

import logging

logger = logging.getLogger("bankdoclink.error_handling")


class InvalidFileError(ValueError):
    """Raised when an uploaded file is invalid (e.g., wrong type or limit exceeded)."""
    pass


def handle_invalid_file(filename: str, reason: str) -> None:
    """Logs the validation failure and raises an InvalidFileError."""
    message = f"Invalid file '{filename}': {reason}"
    logger.warning(message)
    raise InvalidFileError(message)
