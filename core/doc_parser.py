"""
core/doc_parser.py
==================

Document parsing and NLP feature extraction engine.
"""

from pathlib import Path
from typing import Dict, List
import spacy
import pymupdf4llm
from unstructured.partition.docx import partition_docx
from langchain_community.document_loaders import TextLoader
import subprocess
import sys

class DocParser:
    """Parses uploaded documents into plain text and extracts metadata/entities."""

    def __init__(self):
        """Initializes the DocParser and loads the spaCy NLP pipeline."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if download was missed/fails in a specific execution path

            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
            self.nlp = spacy.load("en_core_web_sm")

    def parse(self, file_path: str | Path) -> str:
        """
        Parses the document text based on its file extension.

        Args:
            file_path: Absolute path to the file.

        Returns:
            Extracted text content of the document.
        """
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

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extracts named entities, topics, and key terms from the document text using spaCy.

        Args:
            text: Raw string content.

        Returns:
            A structured dict containing entities, topics, and key_terms lists.
        """
        if not text or not text.strip():
            return {"entities": [], "topics": [], "key_terms": []}

        # Increase max length dynamically if needed, to avoid spacy length warnings
        doc = self.nlp(text[:])

        # 1. Named Entities (people, orgs, gpe, date, money values)

        allowed_types = {"PERSON", "ORG", "GPE", "DATE", "MONEY"}

        entities = []
        seen = set()

        for ent in doc.ents:
            if ent.label_ not in allowed_types:
                continue

            text = " ".join(ent.text.split())
            key = (text, ent.label_)

        allowed_types = {"PERSON", "ORG", "GPE", "DATE", "MONEY"}

        entities = []
        seen = set()

        for ent in doc.ents:
            if ent.label_ not in allowed_types:
                continue

            text = " ".join(ent.text.split())
            key = (text, ent.label_)

            if not text or key in seen:
                continue

            seen.add(key)
            entities.append(text)


            seen.add(key)
            entities.append(text)

        # 2. Topics (Noun Chunks)
        topics = []
        seen = set()

        for chunk in doc.noun_chunks:
            text = " ".join(chunk.text.lower().split())

            if (
                len(text) <= 2
                or chunk.root.is_stop
                or text.isdigit()
                or text in seen
            ):
                continue

            seen.add(text)
            topics.append(text)

        # 3. Key Terms
        key_terms = []
        seen = set()

        for token in doc:
            if (
                token.is_stop
                or token.is_punct
                or token.is_space
                or not token.is_alpha
                or len(token.text) <= 2
            ):
                continue

            term = token.lemma_.lower()

            if not term or term in seen:
                continue

            seen.add(term)
            key_terms.append(term)

        # this will be sent to llm to refine and form connection
        return {
            "entities": entities,
            "topics": topics,
            "key_terms": key_terms,
        }