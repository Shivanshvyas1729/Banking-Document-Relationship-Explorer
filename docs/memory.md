# Project Memory: BankDocLink

This document acts as a persistent log of completed implementations, architectural decisions, and context for subsequent development phases, reducing token usage for future updates.

---

## 📅 Chronological Milestones

### Phase 1: MVP UI & Document Upload
- **Objective**: Establish document uploads, session constraints, and file listings in UI/backend.
- **Completed Components**:
  - `models/schemas.py`: Implemented a subclass of LangChain's `Document` model that exposes backward-compatible properties (`id`, `name`, `path`, `parsed_entities`, and `content`) mapped to standard LangChain fields.
  - `utils/error_handling.py`: Implemented `InvalidFileError` custom exception and `handle_invalid_file` helper.
  - `core/document_uploader.py`: Created the file uploader validating types against `config.SUPPORTED_FILE_TYPES`, session limit against `config.MAX_DOCUMENTS_PER_SESSION`, and saving files to `data/uploads/` on local disk.
  - `tests/test_document_uploader.py`: Verified upload success/failure paths, limit enforcement, and file unlinking.
  - `ui/main_page.py` & `app.py`: Created Streamlit layout with sidebar navigation, drag-and-drop uploader widget, warning banners, and card list items with deletion action buttons.

---

### Phase 2, Part A: Parsing & Embedding
- **Objective**: Parse documents, extract metadata with NLP, generate vectors, and configure API-driven embeddings.
- **Completed Components**:
  - `core/doc_parser.py`: Implemented text extraction logic (dispatching to `pymupdf4llm` for PDFs, `unstructured` for Word DOCX, and falling back to UTF-8 decoders for TXT). Added `extract_entities(text)` mapping spaCy `en_core_web_sm` processing output to the exact schema:
    ```python
    {
        "entities": [...],  # PERSON, ORG, GPE, DATE, MONEY
        "topics": [...],    # deduplicated noun chunks
        "key_terms": [...]  # lemmatized keywords
    }
    ```
  - `core/embedder.py`: Implemented `Embedder` wrapping LangChain's `OpenAIEmbeddings` using `config.EMBEDDING_MODEL_NAME` and `config.OPENAI_API_KEY`.
  - `utils/error_handling.py`: Created custom `EmbeddingFailureError` and `handle_embedding_failure` error wrapper.
  - `tests/test_doc_parser.py` & `tests/test_embedder.py`: Added parser unit checks and embedder mock checks verifying all vectors, outputs, formats, and exception raises.

---

### Phase 3: Embedding & Vector DB Integration (Part B: Storage)
- **Objective**: Store and query vector chunks in-memory with custom retry loops, and wire up the full upload pipeline.
- **Completed Components**:
  - `core/vector_db_client.py`: Created `VectorDBClient` supporting **FAISS** (via LangChain's local wrapper) and **ChromaDB** (via raw in-memory `chromadb` collections). Implemented a **3-attempt store retry loop** with exponential backoff and mapped query outputs to `RetrievalResult`.
  - `utils/error_handling.py`: Implemented `VectorDBError` custom exception and `handle_vector_db_error` helper.
  - `core/document_uploader.py`: Integrated the complete document pipeline. Uploading automatically triggers parsing (via `DocParser`), metadata extraction, recursive chunk splitting, embedding coordinates generation (via `Embedder`), and vector DB insertion (via `VectorDBClient`).
  - `tests/test_vector_db_client.py` & `tests/test_document_uploader.py`: Added DB store/search unit tests, retry mock handlers, and uploader mock fixtures to isolate tests from OpenAI API limits.

---

## 🛠️ Verification Command Reference
- Run all test suites:
  ```bash
  C:\Users\DELL\miniconda3\envs\bank\python.exe -m pytest tests/
  ```
- Run the web application:
  ```bash
  C:\Users\DELL\miniconda3\envs\bank\python.exe -m streamlit run app.py
  ```
