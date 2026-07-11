# BankDocLink

# 📁 BankDocLink Project Structure

A clean, modular architecture for the **BankDocLink** application following a layered design (UI → Core → Models → Utilities → Data).

```text
bankdoclink/
│
├── app.py
│   └── Streamlit application entry point
│
├── config.py
│   └── Central configuration
│       • Supported file types
│       • AI model names
│       • Timeouts
│       • Application limits
│
├── requirements.txt
│   └── Project dependencies
│
├── README.md
│   └── Project overview
│       • Installation
│       • Architecture
│       • Usage
│       • PRD / HLD / LLD mapping
│
├── PHASED_BUILD_PROMPT.md
│   └── Development roadmap
│       • Phase 0 → Phase 7
│
├── core/
│   ├── __init__.py
│   │
│   ├── document_uploader.py
│   │   └── Upload, list, and remove documents
│   │
│   ├── doc_parser.py
│   │   └── Parse PDF/DOCX and extract entities
│   │
│   ├── embedder.py
│   │   └── Generate text embeddings
│   │
│   ├── vector_db_client.py
│   │   └── Store and search vector embeddings
│   │
│   ├── rag_engine.py
│   │   └── Retrieval-Augmented Generation pipeline
│   │
│   └── ai_generator.py
│       └── Generate AI explanations and document relationships
│
├── models/
│   ├── __init__.py
│   │
│   └── schemas.py
│       └── Data models
│           • Document
│           • Embedding
│           • Query
│           • RetrievalResult
│           • Explanation
│
├── ui/
│   ├── __init__.py
│   │
│   ├── main_page.py
│   │   └── Dashboard
│   │       • Upload documents
│   │       • Manage uploaded files
│   │
│   ├── document_view.py
│   │   └── View extracted entities, keywords, and topics
│   │
│   ├── relationship_explorer.py
│   │   └── Interactive relationship/network graph
│   │
│   └── query_interface.py
│       └── Ask questions and receive AI-generated answers
│
├── utils/
│   ├── __init__.py
│   │
│   ├── error_handling.py
│   │   └── Custom exceptions and centralized error handling
│   │
│   └── logger.py
│       └── Logging utilities
│
├── tests/
│   ├── __init__.py
│   │
│   ├── test_document_uploader.py
│   ├── test_doc_parser.py
│   ├── test_embedder.py
│   ├── test_vector_db_client.py
│   └── test_rag_engine.py
│
└── data/
    └── vector_store/
        └── Temporary session-scoped vector database
```

---

# 📦 Folder Responsibilities

| Folder      | Purpose                                                                              |
| ----------- | ------------------------------------------------------------------------------------ |
| **core/**   | Business logic, AI pipeline, document processing, embeddings, and RAG implementation |
| **models/** | Shared data models and schemas used throughout the application                       |
| **ui/**     | Streamlit user interface components and pages                                        |
| **utils/**  | Common utilities such as logging and error handling                                  |
| **tests/**  | Unit tests for each major backend component                                          |
| **data/**   | Temporary storage for vector databases and runtime data                              |

---

# 🧩 Architecture Overview

```text
             User
               │
               ▼
        Streamlit Interface
               │
               ▼
        ┌───────────────┐
        │      UI       │
        └───────────────┘
               │
               ▼
        ┌───────────────┐
        │     Core      │
        ├───────────────┤
        │ Document Upload
        │ Document Parser
        │ Embeddings
        │ Vector Database
        │ RAG Engine
        │ AI Generator
        └───────────────┘
               │
               ▼
        ┌───────────────┐
        │    Models     │
        └───────────────┘
               │
               ▼
        ┌───────────────┐
        │ Vector Store  │
        └───────────────┘
```

---

# 🚀 Design Principles

* Modular and maintainable architecture
* Separation of concerns
* Independent UI and backend layers
* Easily testable components
* Scalable for future AI features
* Clean folder organization
* Suitable for production deployment
* Extensible for additional document types and AI models




