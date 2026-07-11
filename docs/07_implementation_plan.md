# Execution Plan: Phase 2 (Embedding & Vector DB - Parsing)

This plan details the implementation order and verification steps for Phase 2: Document Parsing & NLP Feature Extraction.

## 1. Implementation Order
1. **Core Parser Extension**: Enhance the existing `core/doc_parser.py` to extract named entities, topics, and key terms via a spaCy pipeline.
2. **Embedder Core**: Implement the SentenceTransformer-based embedding generation logic in `core/embedder.py`.
3. **Parser Tests**: Implement and execute test cases in `tests/test_doc_parser.py` to verify correct text parsing and NLP extraction.
4. **Embedder Tests**: Implement and execute test cases in `tests/test_embedder.py` to verify vector output shapes, types, and error handling.

---

## 2. Proposed File Modifications

### Component: Document Parser

#### [MODIFY] [doc_parser.py](file:///c:/Users/DELL/Desktop/internship1/core/doc_parser.py)
- Import `spacy`.
- Add `extract_entities(self, text: str) -> dict[str, list[str]]`:
  - Load the English small spaCy model `en_core_web_sm`.
  - Process text and filter named entities by category (PERSON, ORG, GPE, DATE, MONEY).
  - Extract noun chunks/phrases as topics.
  - Tokenize and filter keywords (excluding stopwords and punctuation) as key terms.
  - Return the results in a dict.

---

### Component: Document Embedder

#### [MODIFY] [embedder.py](file:///c:/Users/DELL/Desktop/internship1/core/embedder.py)
- Implement the `Embedder` class:
  - Load SentenceTransformer with the model defined in `config.EMBEDDING_MODEL_NAME`.
  - Add `embed(self, text: str) -> list[float]`:
    - Generate embedding vectors.
    - Catch exceptions and raise custom errors via `utils/error_handling.py`'s `handle_embedding_failure()`.

---

### Component: Error Handling

#### [MODIFY] [error_handling.py](file:///c:/Users/DELL/Desktop/internship1/utils/error_handling.py)
- Define custom `EmbeddingFailureError` class.
- Implement `handle_embedding_failure(filename_or_err: str, reason: str)` to log and raise `EmbeddingFailureError`.

---

### Component: Unit Tests

#### [MODIFY] [test_doc_parser.py](file:///c:/Users/DELL/Desktop/internship1/tests/test_doc_parser.py)
- Write unit tests verifying:
  - Text parsing from sample files.
  - Extraction of entities, topics, and key terms.

#### [MODIFY] [test_embedder.py](file:///c:/Users/DELL/Desktop/internship1/tests/test_embedder.py)
- Write unit tests verifying:
  - Generating embedding vectors from text.
  - Proper embedding shapes (e.g. 384 dimensions).
  - Proper error raising on failed inputs.

---

## 3. Verification Plan

### Automated Tests
- Run `pytest` on the parser and embedder tests:
  ```bash
  conda run -n bank python -m pytest tests/test_doc_parser.py
  conda run -n bank python -m pytest tests/test_embedder.py
  ```
