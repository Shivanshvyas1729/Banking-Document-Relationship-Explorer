"""
core/embedder.py
================

Generates numerical vector embeddings for parsed text chunks using OpenAI.
"""

import os
import sys
from typing import List

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_openai import OpenAIEmbeddings
import config
from utils.error_handling import handle_embedding_failure


class Embedder:
    """Handles text embedding generation using LangChain OpenAIEmbeddings."""

    def __init__(self):
        """Initializes the OpenAIEmbeddings provider using configurations."""
        try:
            api_key = config.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
            self.embeddings = OpenAIEmbeddings(
                model=config.EMBEDDING_MODEL_NAME,
                openai_api_key=api_key
            )
        except Exception as e:
            handle_embedding_failure("Initialization", f"Could not initialize OpenAIEmbeddings: {str(e)}")

    def embed(self, text: str) -> List[float]:
        """
        Generates numerical vector embedding for the input text.

        Args:
            text: Text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        if not text or not text.strip():
            return []

        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            handle_embedding_failure(text[:30] + "...", str(e))

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Embeds multiple texts in one or more batched API calls.

        Internally splits the input list into sub-batches of at most
        OPENAI_EMBED_BATCH_LIMIT (2048) texts to respect OpenAI's per-request
        limit, then concatenates the results. This reduces N round-trips to
        ceil(N / 2048) round-trips — typically just 1.

        Args:
            texts: A list of text strings to embed.

        Returns:
            A list of embedding vectors, one per input text, in the same order.
            Texts that are empty or whitespace-only receive an empty list [].
        """
        if not texts:
            return []

        BATCH_LIMIT = 2048

        # Separate non-empty texts while preserving original index positions
        # so we can re-insert [] for blank slots after the API call.
        index_map: list[int] = []       # maps sub-list position -> original index
        valid_texts: list[str] = []

        results: list[list[float]] = [[] for _ in texts]

        for i, t in enumerate(texts):
            if t and t.strip():
                index_map.append(i)
                valid_texts.append(t)

        if not valid_texts:
            return results

        # Split into sub-batches and call embed_documents once per batch
        try:
            vectors: list[list[float]] = []
            for start in range(0, len(valid_texts), BATCH_LIMIT):
                batch = valid_texts[start: start + BATCH_LIMIT]
                batch_vectors = self.embeddings.embed_documents(batch)
                vectors.extend(batch_vectors)

            # Map vectors back to original positions
            for sub_idx, orig_idx in enumerate(index_map):
                results[orig_idx] = vectors[sub_idx]

            return results

        except Exception as e:
            handle_embedding_failure(f"embed_batch({len(texts)} texts)", str(e))
