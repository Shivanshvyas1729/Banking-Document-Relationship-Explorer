# Vision & Scope: BankDocLink

### 1. Core Goals
- Enable users to upload, analyze, and explore relationships between multiple banking documents using AI-powered tools.
- Extract and visualize key terms, entities, and topics across documents.
- Enable exploration of relationships and connections between documents (graph/network view).
- Provide AI-generated explanations and answers to user queries about document relationships via RAG.

### 2. Target Audience
- Banking professionals
- Researchers
- Students
- AI/FinTech enthusiasts

### 3. Primary Functionality
- **Document Upload** — upload, view, and remove multiple banking documents (PDF, DOCX, TXT)
- **Document Parsing & Embedding** — extract text, generate vector embeddings, store in a vector database
- **Entity & Topic Extraction** — identify and display key terms, entities, and topics per document
- **Relationship Exploration** — visualize how terms/entities/topics connect across documents
- **RAG-based Querying** — ask natural-language questions and get AI-generated explanations grounded in retrieved document content
- **Interactive UI** — Streamlit-based interface for document management, exploration, and querying
- **Security & Privacy** — session-based processing only; no document retention beyond the session (MVP)

### 4. Key Success Metrics
| Metric | Target |
|---|---|
| Document upload success rate | > 99% |
| Query response time | < 10 seconds |
| User satisfaction (survey) | > 80% positive |
| Relationship accuracy (manual eval) | > 85% |
| Document processing time | < 30 seconds/file |
| Documents supported per session | ≥ 10 |
