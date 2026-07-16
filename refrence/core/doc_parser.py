"""
core/doc_parser.py
===================
Class: DocParser
Source: LLD Section 2 "Class/Interface Overview"

    Description: Parses and preprocesses documents
    Key Methods/Attributes: parse(file), extract_entities()

Used in LLD Section 4 "Document Upload & Indexing" algorithm:

    for file in uploaded_files:
        text = DocParser.parse(file)
        entities = DocParser.extract_entities(text)
        vector = Embedder.embed(text)
        VectorDBClient.store_embedding(doc_id, vector, metadata=entities)

Functional Requirements covered:
    FR2 - System parses documents, extracts text, and generates vector embeddings. (High)
    FR3 - Key terms, entities, and topics are extracted and displayed per document. (High)

Technical Spec (PRD Section 7 / HLD Section 4):
    Document Processing: Python NLP libraries (e.g., spaCy)
    Supported formats: PDF, DOCX, TXT (PRD Section 3 Document Upload)

Error Handling (LLD Section 5):
    Scenario: Invalid/unsupported file upload -> Show error message, skip file
"""


class DocParser:
    """Parses raw uploaded files into plain text and extracts entities/topics.

    Uses format-specific extractors:
        - PDF  -> pypdf
        - DOCX -> python-docx
        - TXT  -> direct decode
    Entity/topic extraction uses an NLP pipeline (e.g., spaCy) per HLD Section 4.
    """



    def extract_entities(self, text: str) -> dict:
        """Extract key terms, entities, and topics from text.

        Returns dict shaped like:
            {
                "entities": [...],   # named entities (orgs, amounts, dates, parties)
                "topics": [...],     # high-level topics/themes
                "key_terms": [...],  # banking-domain key terms
            }

        This satisfies FR3 "Key terms, entities, and topics are extracted
        and displayed per document."
        """
        raise NotImplementedError(
            "Implement in Phase 2: run a spaCy NLP pipeline (or LLM-based "
            "extraction) over `text` and return entities/topics/key_terms."
        )
