from pathlib import Path

PROJECT_NAME = "."

structure = {
    "": [
        "app.py",
        "config.py",
        "requirements.txt",
        "README.md",
        "PHASED_BUILD_PROMPT.md",
    ],
    "core": [
        "__init__.py",
        "document_uploader.py",
        "doc_parser.py",
        "embedder.py",
        "vector_db_client.py",
        "rag_engine.py",
        "ai_generator.py",
    ],
    "models": [
        "__init__.py",
        "schemas.py",
    ],
    "ui": [
        "__init__.py",
        "main_page.py",
        "document_view.py",
        "relationship_explorer.py",
        "query_interface.py",
    ],
    "utils": [
        "__init__.py",
        "error_handling.py",
        "logger.py",
    ],
    "tests": [
        "__init__.py",
        "test_document_uploader.py",
        "test_doc_parser.py",
        "test_embedder.py",
        "test_vector_db_client.py",
        "test_rag_engine.py",
    ],
    "data/vector_store": [],
}

comments = {
    "app.py": "# Streamlit entry point\n",
    "config.py": "# Central configuration\n",
    "requirements.txt": "",
    "README.md": "# BankDocLink\n",
    "PHASED_BUILD_PROMPT.md": "# Phased Build Plan\n",
    "core/document_uploader.py": "# DocumentUploader\n",
    "core/doc_parser.py": "# DocParser\n",
    "core/embedder.py": "# Embedder\n",
    "core/vector_db_client.py": "# Vector Database Client\n",
    "core/rag_engine.py": "# RAG Engine\n",
    "core/ai_generator.py": "# AI Generator\n",
    "models/schemas.py": "# Data Models\n",
    "ui/main_page.py": "# Main Streamlit Page\n",
    "ui/document_view.py": "# Document Viewer\n",
    "ui/relationship_explorer.py": "# Relationship Explorer\n",
    "ui/query_interface.py": "# Query Interface\n",
    "utils/error_handling.py": "# Error Handling\n",
    "utils/logger.py": "# Logger\n",
}

root = Path(PROJECT_NAME)
root.mkdir(exist_ok=True)

for folder, files in structure.items():
    folder_path = root / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    for file in files:
        file_path = folder_path / file
        file_path.touch(exist_ok=True)

        key = str(file_path.relative_to(root)).replace("\\", "/")
        if key in comments:
            file_path.write_text(comments[key], encoding="utf-8")

print(f"\n✅ '{PROJECT_NAME}' project structure created successfully!")