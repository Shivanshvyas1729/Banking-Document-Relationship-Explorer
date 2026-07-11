# Data Schema Definitions: BankDocLink

This document defines all objects and their schemas within the BankDocLink application.

---

## 1. Document Schema
Represents a document uploaded by the user, inheriting from LangChain's native `Document` model so that it can be seamlessly integrated with LangChain's vector databases, retrievers, and chain components.

```python
from langchain_core.documents import Document as LCDocument

class Document(LCDocument):
    """Custom Document inheriting from LangChain's Document to support custom attributes."""
    # id: Optional[str] = None (inherited natively from LCDocument)
    # page_content: str (inherited natively from LCDocument, holds parsed content)
    # metadata: dict (inherited natively from LCDocument, holds custom name, path, and parsed_entities)

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
```

---

## 2. Embedding Schema
Represents the numerical vector embedding generated from document segments, stored in the vector database.

```python
@dataclass
class Embedding:
    doc_id: str                     # Reference to the source Document ID
    vector: List[float]             # Numerical vector coordinates (e.g., length 384 for all-MiniLM-L6-v2)
    metadata: Dict[str, Any]        # Chunk metadata (e.g., chunk index, raw text, source filename)
```

---

## 3. Query Schema
Represents a natural language question submitted by the user.

```python
@dataclass
class Query:
    text: str                       # The raw question text inputted by the user
    filters: Optional[Dict[str, Any]] = None  # Optional metadata filters (e.g. to filter by doc_id)
```

---

## 4. RetrievalResult Schema
Represents a chunk retrieved from the vector store matching the query.

```python
@dataclass
class RetrievalResult:
    doc_id: str                     # ID of the source Document
    score: float                    # Distance/similarity score (lower is closer in FAISS L2)
    text: str                       # Raw text content of the retrieved chunk
```

---

## 5. Explanation Schema
Represents the AI-generated answer.

```python
@dataclass
class Explanation:
    query_id: str                   # Unique UUID generated for the audit trail
    original_query: str             # The user's original query text
    generated_text: str             # Synthesized response from the LLM
    related_docs: List[str]         # List of source document names cited in the response
    metadata: Dict[str, Any]        # Metadata including token counts or latency
```
