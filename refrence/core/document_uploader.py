"""
core/document_uploader.py
==========================
Class: DocumentUploader
Source: LLD Section 2 "Class/Interface Overview"

    Description: Handles file uploads in UI
    Key Methods/Attributes: upload_files(), get_file_list()

Relationship (LLD Section 2): DocumentUploader -> DocParser -> Embedder -> VectorDBClient
This is step 1 of the pipeline described in PRD Section 12 "Example Workflow (Pseudocode)":

    for doc in uploaded_documents:
        text = extract_text(doc)
        embedding = generate_embedding(text)
        store_in_vector_db(doc.id, embedding)
        entities, topics = extract_entities_topics(text)
        display_entities_topics(doc.id, entities, topics)

Functional Requirements covered:
    FR1 - Users can upload, view, and remove multiple documents. (High)

Non-Functional Requirements covered:
    NFR3 - Support for at least 10 documents/session. (Medium)

Error Handling (LLD Section 5):
    Scenario: Invalid/unsupported file upload
    Handling Approach: Show error message, skip file
"""

from models.schemas import Document
import config


class DocumentUploader:
    """Handles file uploads in the Streamlit UI Layer.

    Responsible only for accepting raw uploaded files and turning them into
    `Document` records with a stable id + filename. Text extraction is
    delegated to DocParser (separation of concerns per LLD Section 1).
    """

    def __init__(self):
        # In-memory only, per NFR4 "No persistent storage of user documents"
        # and HLD Security: "User uploads and data access are restricted to
        # session scope."
        self._documents: dict[str, Document] = {}

    def upload_files(self, files: list) -> list[Document]:
        """Accept a batch of uploaded files (Streamlit `UploadedFile` objects).

        - Validates file type against config.SUPPORTED_FILE_TYPES (pdf, docx, txt).
        - Enforces config.MAX_DOCUMENTS_PER_SESSION (NFR3).
        - Invalid/unsupported files: show error message, skip file (LLD Section 5).

        Returns the list of successfully registered Document objects.
        """
        raise NotImplementedError(
            "Implement in Phase 1: validate extension against "
            "config.SUPPORTED_FILE_TYPES, enforce MAX_DOCUMENTS_PER_SESSION, "
            "create Document(id=uuid4, filename=file.name) for each valid file, "
            "store in self._documents, and return the list."
        )

    def get_file_list(self) -> list[Document]:
        """Return all Document objects uploaded in the current session."""
        raise NotImplementedError(
            "Implement in Phase 1: return list(self._documents.values())"
        )

    def remove_file(self, doc_id: str) -> bool:
        """Remove a document from the session (supports PRD FR1 'remove').

        Returns True if removed, False if doc_id was not found.
        """
        raise NotImplementedError(
            "Implement in Phase 1: pop doc_id from self._documents if present."
        )
