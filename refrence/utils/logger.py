"""
utils/logger.py
================
Simple logging utility used across core/, ui/, and utils/ modules.

Supports LLD Section 5 error-handling requirements that call for logging
(e.g. "Log error, notify user, skip document" and "Return fallback message,
log for review").
"""

import logging
import config


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))
    return logger
