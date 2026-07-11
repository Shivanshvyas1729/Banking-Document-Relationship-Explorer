"""
config.py
=========

Centralized configuration for BankDocLink.
"""

import os
from dotenv import load_dotenv

load_dotenv()


# -----------------------------------------------------------------------
# API Configuration
# -----------------------------------------------------------------------

BASE_URL: str = os.getenv("BASE_URL", "")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")


# -----------------------------------------------------------------------
# Document Upload
# -----------------------------------------------------------------------

SUPPORTED_FILE_TYPES: list[str] = ["pdf", "docx", "txt"]

MAX_DOCUMENTS_PER_SESSION: int = int(
    os.getenv("MAX_DOCUMENTS_PER_SESSION", 10)
)

MAX_FILE_PROCESSING_SECONDS: int = int(
    os.getenv("MAX_FILE_PROCESSING_SECONDS", 30)
)


# -----------------------------------------------------------------------
# Embedding Configuration
# -----------------------------------------------------------------------

EMBEDDING_PROVIDER: str = os.getenv(
    "EMBEDDING_PROVIDER",
    "sentence-transformers"
)

EMBEDDING_MODEL_NAME: str = os.getenv(
    "EMBEDDING_MODEL_NAME",
    "all-MiniLM-L6-v2"
)


# -----------------------------------------------------------------------
# Vector Database
# -----------------------------------------------------------------------

VECTOR_DB_BACKEND: str = os.getenv(
    "VECTOR_DB_BACKEND",
    "faiss"
)

VECTOR_DB_PATH: str = os.getenv(
    "VECTOR_DB_PATH",
    ""
)

VECTOR_DB_PERSIST_DIR: str | None = None


# -----------------------------------------------------------------------
# LLM Configuration
# -----------------------------------------------------------------------

LLM_PROVIDER: str = os.getenv(
    "LLM_PROVIDER",
    "openai"
)

LLM_MODEL_NAME: str = os.getenv(
    "LLM_MODEL_NAME",
    "gpt-4.1-mini"
)

RAG_TOP_K: int = int(
    os.getenv("RAG_TOP_K", 5)
)

QUERY_RESPONSE_TIMEOUT_SECONDS: int = int(
    os.getenv("QUERY_RESPONSE_TIMEOUT_SECONDS", 10)
)


# -----------------------------------------------------------------------
# Security
# -----------------------------------------------------------------------

SESSION_ONLY_STORAGE: bool = True

RETAIN_DOCUMENTS_AFTER_SESSION: bool = False


# -----------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------

LOG_LEVEL: str = os.getenv(
    "LOG_LEVEL",
    "INFO"
)