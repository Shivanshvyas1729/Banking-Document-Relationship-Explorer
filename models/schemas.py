"""
models/schemas.py
=================

Data models and schemas used throughout the BankDocLink application.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document as LCDocument


class Document(LCDocument):
    """Custom Document inheriting from LangChain's Document to support custom attributes."""

    @property
    def name(self) -> str:
        return self.metadata.get("name", "")

    @property
    def path(self) -> str:
        return self.metadata.get("path", "")

    @property
    def parsed_entities(self) -> dict:
        if "parsed_entities" not in self.metadata:
            self.metadata["parsed_entities"] = {
                "entities": [],
                "topics": [],
                "key_terms": []
            }
        return self.metadata["parsed_entities"]

    @parsed_entities.setter
    def parsed_entities(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("parsed_entities must be a dictionary")
        self.metadata["parsed_entities"] = value

    @property
    def content(self) -> str:
        return self.page_content

    @content.setter
    def content(self, value: str):
        self.page_content = value


@dataclass
class Embedding:
    """Represents a generated document or passage embedding."""
    doc_id: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Query:
    """Represents a user query."""
    text: str
    filters: Optional[Dict[str, Any]] = None


@dataclass
class RetrievalResult:
    """Represents a chunk retrieved from the vector database."""
    doc_id: str
    score: float
    text: str


@dataclass
class Explanation:
    """Represents an AI-generated explanation response with an audit trail."""
    query_id: str
    original_query: str
    generated_text: str
    related_docs: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
