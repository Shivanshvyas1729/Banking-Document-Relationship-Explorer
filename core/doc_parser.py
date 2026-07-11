# DocParser

from pathlib import Path

import pymupdf4llm
from unstructured.partition.docx import partition_docx

from langchain_community.document_loaders import TextLoader


class DocParser:
    """Parses uploaded documents into plain text."""

    def parse(self, file_path: str | Path) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Specified file not found: {path}"
            )

        suffix = path.suffix.lower()

        try:
            if suffix == ".txt":
                loader = TextLoader(
                    str(path),
                    encoding="utf-8",
                    autodetect_encoding=True,
                )

                documents = loader.load()

                return "\n\n".join(
                    document.page_content
                    for document in documents
                )

            if suffix == ".pdf":
                return pymupdf4llm.to_markdown(
                    str(path)
                )

            if suffix == ".docx":
                elements = partition_docx(
                    filename=str(path)
                )

                return "\n\n".join(
                    element.text
                    for element in elements
                    if getattr(element, "text", "").strip()
                )

            raise ValueError(
                f"Unsupported file type: {suffix}"
            )

        except Exception as e:
            raise RuntimeError(
                f"Failed to parse '{path.name}'."
            ) from e