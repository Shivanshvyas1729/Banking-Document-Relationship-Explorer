# Logic Flowcharts: BankDocLink

This document describes the step-by-step logic in plain English for core systems in BankDocLink.

---

## 1. Document Upload & Validation (Phase 1)

![alt text](<Streamlit File Upload-2026-07-11-122715.png>)
### Plain English steps:
1. When files are uploaded in the UI, iterate through each file.
2. Check if the current number of registered documents is already at the maximum limit (`MAX_DOCUMENTS_PER_SESSION`). If so, log the error and raise `InvalidFileError`.
3. Check if the file's extension (lowercase, no dot) is in the supported file formats (`pdf`, `docx`, `txt`). If not, log the error and raise `InvalidFileError`.
4. Read the file bytes and write them to a unique file in the upload directory.
5. Instantiate a `Document` metadata record with a newly generated UUID, the file name, and file path.
6. Register the document in the session registry.

---

## 2. Document Parsing & NLP Feature Extraction (Phase 2)
![alt text](<File Content Parsing-2026-07-11-123249.png>)

### Plain English steps:
1. **Parsing**:
   - Check if the file exists at the given path.
   - Extract the lowercase file extension.
   - If the extension is `.txt`, read it with UTF-8 encoding.
   - If the extension is `.pdf`, parse it to markdown using `pymupdf4llm`.
   - If the extension is `.docx`, partition it using `python-docx` or `unstructured.partition.docx`, joining the texts of all elements.
   - If the extension is unsupported, raise a `ValueError`.
2. **Feature Extraction (`extract_entities`)**:
   - Process the raw document text using a spaCy language model (e.g. `en_core_web_sm`).
   - **Entities**: Extract unique entity texts from `doc.ents` that are tagged as ORG, PERSON, GPE, DATE, or MONEY.
   - **Topics**: Extract unique noun chunks or main topics from the document.
   - **Key Terms**: Extract unique keywords/lemmatized terms, ignoring common stop words and punctuation.
   - Return a dictionary mapping `"entities"`, `"topics"`, and `"key_terms"` to their respective list of strings.
3. **Embedding Generation**:
   - Initialize the `SentenceTransformer` embedder with the configured model (e.g. `all-MiniLM-L6-v2`).
   - If embedding fails due to an API or system error, log it and raise a customized error using `handle_embedding_failure()`.
