# BankDocLink — Phased Build Prompt

Use this document as a prompt (e.g. paste each phase into Claude Code, one at a time, in order) to implement the BankDocLink scaffold that's already been generated.

Each phase corresponds to a milestone in the PRD (Section 11) and targets specific requirement IDs from the PRD/LLD/HLD so nothing gets missed and nothing gets built out of order.

The scaffold already contains every file with docstrings describing exactly what to build and where — treat each `NotImplementedError` as a TODO marker.

---

# 📖 How to Use This

For each phase below:

1. Paste the phase's prompt block into your coding assistant.
2. Point it at the existing file(s) listed — **do not create new files unless the phase says to.**
3. Ask it to replace only the `NotImplementedError` bodies with working code, preserving the existing docstrings/comments as documentation.
4. Run the phase's test file(s) before moving to the next phase.

---

# 🚀 Phase 0 — Environment Setup (Week 1, Prep)

> Set up the BankDocLink project environment.
>
> Create a virtual environment, install everything in `requirements.txt`, and add a `.env.example` file with placeholders for:
>
> - `OPENAI_API_KEY`
> - `EMBEDDING_PROVIDER`
> - `VECTOR_DB_BACKEND`
> - `LLM_PROVIDER`
>
> (See `config.py` for the exact environment variables it reads.)
>
> Confirm `streamlit run app.py` launches without import errors even though features aren't implemented yet. They should fail gracefully with `NotImplementedError`, **not import errors**.

### Files Touched

- `requirements.txt`
- `.env.example` *(new)*
- `config.py` *(read-only)*

---

# 🚀 Phase 1 — MVP UI & Document Upload (Week 2)

> Implement `core/document_uploader.py`'s `DocumentUploader` class:
>
> - `upload_files()`
> - `get_file_list()`
> - `remove_file()`
>
> Follow the in-code TODOs exactly:
>
> - validate file extensions against `config.SUPPORTED_FILE_TYPES`
> - enforce `config.MAX_DOCUMENTS_PER_SESSION`
> - use `utils/error_handling.py`'s `handle_invalid_file()` for rejected files
>
> Then implement `ui/main_page.py`'s `render()` using:
>
> - `st.file_uploader(accept_multiple_files=True)`
> - a simple table/list with per-row remove buttons
>
> Run `tests/test_document_uploader.py` and make all tests pass.

### Requirements Targeted

- FR1
- NFR1
- NFR3

### Files Touched

- `core/document_uploader.py`
- `ui/main_page.py`
- `tests/test_document_uploader.py`

---

# 🚀 Phase 2 — Embedding & Vector DB Integration (Part A: Parsing) (Week 3)

> Implement `core/doc_parser.py`'s `DocParser` class:
>
> - `parse(file)`
>   - dispatch on extension:
>     - PDF → `pypdf`
>     - DOCX → `python-docx`
>     - TXT → plain decode
>
> - `extract_entities(text)`
>   - spaCy NLP pipeline returning:
>
> ```python
> {
>     "entities": [...],
>     "topics": [...],
>     "key_terms": [...]
> }
> ```
>
> Then implement `core/embedder.py`'s `Embedder` class:
>
> - `embed(text)` — single-query embedding (used for query-time retrieval only).
> - `embed_batch(texts)` — **primary method for document indexing**. Sends all chunk
>   texts in a single `embed_documents()` call (or multiple calls if
>   `len(texts) > 2048` to respect OpenAI's per-request limit). Returns a
>   list of vectors aligned by position; blank/whitespace slots receive `[]`.
>
> ⚠️ **Do NOT loop `embed(chunk)` per chunk during document upload.** Always
> use `embed_batch(chunks)` once for the full chunk list, then call
> `store_embeddings_batch()` once. The per-chunk loop pattern generates N
> round-trips to the OpenAI API and N individual DB writes — it must not be
> used in the indexing path.
>
> Wire failures through `utils/error_handling.py`'s `handle_embedding_failure()`.
>
> Run:
>
> - `tests/test_doc_parser.py`
> - `tests/test_embedder.py`

### Requirements Targeted

- FR2
- FR3
- NFR2

### Files Touched

- `core/doc_parser.py`
- `core/embedder.py`
- `tests/test_doc_parser.py`
- `tests/test_embedder.py`

---

# 🚀 Phase 3 — Embedding & Vector DB Integration (Part B: Storage) (Week 3–4)

> Implement `core/vector_db_client.py`'s `VectorDBClient` class:
>
> - `store_embedding(doc_id, vector, metadata)` — kept for single-item / incremental use.
> - `search(query_vector, top_k)` — similarity retrieval.
> - `store_embeddings_batch(items)` — **required for document indexing**.
>   Accepts a list of `(doc_id, vector, metadata)` tuples and writes them
>   all in one backend call:
>   - FAISS: `FAISS.from_embeddings(zip(texts, vectors), ...)` on first call,
>     then `add_embeddings(...)` for subsequent batches.
>   - ChromaDB: `collection.add(ids=[...], embeddings=[...], metadatas=[...],
>     documents=[...])` — one call.
>
> Backed by:
>
> - FAISS *(default, `config.VECTOR_DB_BACKEND == "faiss"`)*.
> - ChromaDB alternative path.
>
> Keep the index **in memory only** (do **not** set a persist directory — see `config.VECTOR_DB_PERSIST_DIR`).
>
> Add a retry policy for connection errors using `utils/error_handling.py`'s `handle_vector_db_error()`.
> The retry wraps the **entire batch call**, not individual chunks.
>
> Wire `DocumentUploader.upload_files()` to call this exact pipeline:
>
> ```python
> parsed_text  = parser.parse(file)
> nlp_features = parser.extract_entities(parsed_text)
> chunks       = splitter.split_text(parsed_text)
> vectors      = embedder.embed_batch(chunks)          # ONE API call
> items        = [(doc_id, v, meta) for v in vectors if v]
> vector_db.store_embeddings_batch(items)              # ONE DB call
> ```
>
> ⚠️ **Do NOT use a `for chunk in chunks: embed → store` loop.**
> That approach causes N API round-trips and N DB writes per document.
> The correct pattern above reduces this to ≈ 1 API call + 1 DB call regardless
> of chunk count.
>
> Run:
>
> - `tests/test_vector_db_client.py`

### Requirements Targeted

- FR2
- NFR4
- NFR5

### Files Touched

- `core/vector_db_client.py`
- `app.py`
- `tests/test_vector_db_client.py`

---

# 🚀 Phase 4 — RAG Query & Explanation (Week 5)

> Implement `core/ai_generator.py`'s `AIGenerator.explain_relationships()` using `config.LLM_PROVIDER` *(OpenAI by default)*.
>
> Enforce:
>
> - `config.QUERY_RESPONSE_TIMEOUT_SECONDS`
>
> Fall back gracefully via:
>
> - `utils/error_handling.py`'s `handle_ai_generation_failure()`
>
> on timeout/failure.
>
> Then implement `core/rag_engine.py`'s:
>
> - `RAGEngine.retrieve()`
> - `RAGEngine.generate_answer()`
>
> exactly matching the `answer_query()` pseudocode in:
>
> - LLD Section 4 — *Query & Relationship Exploration*
>
> including the **"no relevant documents"** branch using:
>
> - `utils/error_handling.py`'s `handle_no_results()`
>
> Run:
>
> - `tests/test_rag_engine.py`

### Requirements Targeted

- FR5
- NFR2 *(implicitly via timeout)*
- Success Metric: query response time < 10s

### Files Touched

- `core/ai_generator.py`
- `core/rag_engine.py`
- `tests/test_rag_engine.py`

---

# 🚀 Phase 5 — Document Insights UI (Week 4–5, Parallel with Phase 4)

> Implement `ui/document_view.py`'s `render()` to display, per uploaded document:
>
> - `entities`
> - `topics`
> - `key_terms`
>
> from `Document.parsed_entities` *(populated in Phase 2/3)*.
>
> Display each document inside an expander with:
>
> - tag-style chips **or**
> - bullet lists
>
> Keep it responsive per NFR1.

### Requirements Targeted

- FR3
- NFR1

### Files Touched

- `ui/document_view.py`

---

# 🚀 Phase 6 — Relationship Visualization & Query Interface (Week 6)

> Implement `ui/relationship_explorer.py`:
>
> `build_relationship_graph()`
>
> using `networkx`:
>
> - document nodes
> - shared entity/topic nodes
> - edges where a document contains that entity/topic
>
> Render interactively via `pyvis`, embedded through:
>
> `st.components.v1.html()`
>
> Then implement `ui/query_interface.py`'s `render()`:
>
> - text input
> - submit button
> - spinner while `RAGEngine.generate_answer()` runs
> - results panel showing:
>   - `Explanation.generated_text`
>   - `related_docs` as source citations

### Requirements Targeted

- FR4
- FR5
- NFR1
- Success Metric: relationship accuracy > 85%

### Files Touched

- `ui/relationship_explorer.py`
- `ui/query_interface.py`

---

# 🚀 Phase 7 — Testing & Launch (Week 7)

> Run the full `tests/` suite and fix any failures.
>
> Manually verify against PRD Section 9 Success Metrics:
>
> - Document upload success rate > 99% *(test with a batch of 10 mixed-format files)*
> - Query response time < 10 seconds *(time `RAGEngine.generate_answer()` calls)*
> - Relationship accuracy > 85% *(manual evaluation against a labeled sample set)*
>
> Confirm NFR4 *(no persistent storage)* by checking nothing in `data/` or on disk survives a Streamlit session restart.
>
> Confirm all LLD Section 5 error scenarios are handled:
>
> - invalid file
> - embedding failure
> - vector DB error
> - no results
> - AI generation failure
>
> Trigger each one manually.
>
> Then finalize `README.md` with any deviations from this plan.

### Requirements Targeted

- All Success Metrics (PRD Section 9)
- FR6
- NFR4

### Files Touched

- all *(verification pass)*
- `README.md`

---

# 📋 Quick Reference — Requirement → Phase Map

| ID | Requirement | Phase |
|:---|:------------|:-----:|
| FR1 | Upload/view/remove documents | 1 |
| FR2 | Parse, extract text, generate embeddings | 2, 3 |
| FR3 | Extract & display key terms/entities/topics | 2, 5 |
| FR4 | Visualize cross-document relationships | 6 |
| FR5 | RAG-based query & explanation | 4, 6 |
| FR6 | Secure, session-based processing | 0, 3, 7 |
| NFR1 | Responsive, intuitive UI | 1, 5, 6 |
| NFR2 | < 30s/file processing | 2 |
| NFR3 | ≥ 10 documents/session | 1 |
| NFR4 | No persistent storage | 0, 3, 7 |
| NFR5 | Modular, maintainable codebase | 3 *(and throughout, by construction)* |