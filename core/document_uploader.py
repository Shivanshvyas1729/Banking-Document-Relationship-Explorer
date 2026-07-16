"""
core/document_uploader.py
=========================

Core engine for uploading, listing, and removing documents in a session.
"""

import uuid
from pathlib import Path
from typing import List, Dict

import config
from models.schemas import Document
from utils.error_handling import handle_invalid_file


class DocumentUploader:
    """Manages document uploads, validation, and storage for a session."""

    def __init__(self, upload_dir: str | Path = "data/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.documents: Dict[str, Document] = {}

        # Instantiate pipeline components
        from core.doc_parser import DocParser
        from core.embedder import Embedder
        from core.vector_db_client import VectorDBClient

        self.parser = DocParser()
        self.embedder = Embedder()
        self.vector_db = VectorDBClient()

    def upload_files(self, files: List) -> List[Document]:
        """
        Uploads and validates a batch of files.

        Args:
            files: A list of file-like objects (e.g. Streamlit UploadedFile or BytesIO).

        Returns:
            A list of successfully uploaded Document models.
        """
        uploaded_docs = []

        for file in files:
            # 1. Enforce session document limit
            if len(self.documents) >= config.MAX_DOCUMENTS_PER_SESSION:
                handle_invalid_file(
                    file.name,
                    f"Maximum document limit of {config.MAX_DOCUMENTS_PER_SESSION} reached."
                )

            # 2. Validate file extension
            filename = file.name
            path = Path(filename)
            suffix = path.suffix.lower().lstrip(".")

            if suffix not in config.SUPPORTED_FILE_TYPES:
                handle_invalid_file(
                    filename,
                    f"Unsupported file type '{suffix}'. Supported types: {config.SUPPORTED_FILE_TYPES}"
                )

            # 3. Save file to local disk
            file_path = self.upload_dir / filename
            
            # Make sure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            if hasattr(file, "seek"):
                file.seek(0)
            
            content_bytes = file.read()
            with open(file_path, "wb") as f:
                f.write(content_bytes)

            # Check if this filename is already uploaded, remove the old one from registry first
            # to avoid duplicate records for the same file path
            existing_id = None
            for doc_id, doc in self.documents.items():
                if doc.name == filename:
                    existing_id = doc_id
                    break
            if existing_id:
                del self.documents[existing_id]

            # 4. Register Document
            doc_id = str(uuid.uuid4())
            document = Document(
                id=doc_id,
                page_content="",
                metadata={
                    "name": filename,
                    "path": str(file_path),
                    "parsed_entities": {
                        "entities": [],
                        "topics": [],
                        "key_terms": []
                    }
                }
            )

            try:
                # A. Parse document text
                parsed_text = self.parser.parse(document.path)
                document.content = parsed_text

                # B. Extract entities, topics, and key terms
                nlp_features = self.parser.extract_entities(parsed_text)
                document.parsed_entities = nlp_features

                # C. Split document text into chunks
                from langchain_text_splitters import RecursiveCharacterTextSplitter
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = splitter.split_text(parsed_text)

                # D. Embed all chunks in one batched API call, then bulk-insert
                vectors = self.embedder.embed_batch(chunks)
                items = [
                    (
                        doc_id,
                        vectors[i],
                        {
                            "doc_id": doc_id,
                            "name": filename,
                            "text": chunks[i],
                            "chunk_index": i,
                        },
                    )
                    for i in range(len(chunks))
                    if vectors[i]           # skip empty-vector slots (blank chunks)
                ]
                self.vector_db.store_embeddings_batch(items)

                # E. Register document in session state if all steps succeed
                self.documents[doc_id] = document
                uploaded_docs.append(document)

            except Exception as e:
                # Cleanup saved file on error
                if file_path.exists():
                    try:
                        file_path.unlink()
                    except Exception:
                        pass
                raise e

        return uploaded_docs

    def get_file_list(self) -> List[Document]:
        """Returns list of currently uploaded Document objects."""
        return list(self.documents.values())

    def remove_file(self, file_id: str) -> bool:
        """
        Deletes a document from disk and removes it from the session.

        Args:
            file_id: The ID of the document to remove.

        Returns:
            True if removed successfully, False otherwise.
        """
        if file_id in self.documents:
            document = self.documents[file_id]
            file_path = Path(document.path)
            try:
                if file_path.exists():
                    file_path.unlink()
            except Exception:
                # Log or handle deletion failure silently for now
                pass
            del self.documents[file_id]
            return True
        return False
