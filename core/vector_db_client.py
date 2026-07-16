"""
core/vector_db_client.py
========================

In-memory vector database interface.
Manages the storage and query operations of embeddings via FAISS or ChromaDB.
"""

import time
from typing import Any, Dict, List

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import config
from models.schemas import RetrievalResult
from utils.error_handling import handle_vector_db_error


class VectorDBClient:
    """Interface to manage session-scoped storage/retrieval of vector embeddings."""

    def __init__(self, backend: str = None):
        """
        Initializes the VectorDBClient with the configured database backend.

        Args:
            backend: Optional backend override ("faiss" or "chromadb").
        """
        self.backend = (backend or config.VECTOR_DB_BACKEND).lower()
        self._index = None
        self._client = None
        # Unique collection name per instance avoids cross-test collisions when
        # ChromaDB shares its in-memory singleton across a test session.
        self._collection_name = f"bank_docs_{id(self)}"

        try:
            # We initialize OpenAIEmbeddings to help FAISS construct and search vectors
            self.embeddings = OpenAIEmbeddings(
                model=config.EMBEDDING_MODEL_NAME,
                openai_api_key=config.OPENAI_API_KEY
            )
        except Exception as e:
            handle_vector_db_error("Initialization", f"Could not load OpenAIEmbeddings: {str(e)}")

    def store_embedding(self, doc_id: str, vector: List[float], metadata: Dict[str, Any] = None) -> None:
        """
        Stores a chunk's pre-computed embedding vector and its metadata into the database.
        Applies a retry policy of up to 3 attempts with exponential backoff on exceptions.

        Args:
            doc_id: Parent document UUID.
            vector: The embedding coordinates list.
            metadata: Custom chunk dictionaries containing parent doc_id, name, and chunk text.
        """
        metadata = metadata or {}
        text = metadata.get("text", "")

        max_attempts = 3
        last_error = None

        for attempt in range(1, max_attempts + 1):
            try:
                if self.backend == "faiss":
                    if self._index is None:
                        # Lazy instantiate the FAISS index with the first chunk
                        self._index = FAISS.from_embeddings(
                            text_embeddings=[(text, vector)],
                            embedding=self.embeddings,
                            metadatas=[metadata]
                        )
                    else:
                        # Add subsequent chunks
                        self._index.add_embeddings(
                            text_embeddings=[(text, vector)],
                            metadatas=[metadata]
                        )

                elif self.backend == "chromadb":
                    if self._index is None:
                        # Lazy instantiate raw chromadb in-memory Client and Collection
                        import chromadb
                        self._client = chromadb.Client()
                        self._index = self._client.create_collection(self._collection_name)

                    chunk_id = f"{doc_id}_{metadata.get('chunk_index', 0)}_{time.time_ns()}"
                    self._index.add(
                        ids=[chunk_id],
                        embeddings=[vector],
                        metadatas=[metadata],
                        documents=[text]
                    )
                else:
                    raise ValueError(f"Unsupported Vector DB backend: {self.backend}")

                # Success, return immediately
                return

            except Exception as e:
                last_error = e
                # Wait 0.5s, 1s, 1.5s before retrying
                time.sleep(0.5 * attempt)

        handle_vector_db_error(
            "store_embedding",
            f"Failed to persist embedding after {max_attempts} attempts. Last exception: {str(last_error)}"
        )

    def store_embeddings_batch(
        self,
        items: List[tuple],
    ) -> None:
        """
        Bulk-inserts a list of (doc_id, vector, metadata) tuples in a single
        database call per backend.

        FAISS:    calls add_embeddings() with all text/vector/metadata lists at
                  once, creating the index lazily on the first batch.
        ChromaDB: calls collection.add() with lists of ids, embeddings,
                  metadatas, and documents — one network call total.

        The same 3-attempt retry policy as store_embedding() is applied per
        batch, not per chunk.

        Args:
            items: List of (doc_id, vector, metadata_dict) tuples.
                   metadata_dict must contain at least "text" and "chunk_index".
        """
        if not items:
            return

        max_attempts = 3
        last_error = None

        for attempt in range(1, max_attempts + 1):
            try:
                if self.backend == "faiss":
                    texts = [meta.get("text", "") for _, _, meta in items]
                    vectors = [vec for _, vec, _ in items]
                    metadatas = [meta for _, _, meta in items]

                    if self._index is None:
                        self._index = FAISS.from_embeddings(
                            text_embeddings=list(zip(texts, vectors)),
                            embedding=self.embeddings,
                            metadatas=metadatas,
                        )
                    else:
                        self._index.add_embeddings(
                            text_embeddings=list(zip(texts, vectors)),
                            metadatas=metadatas,
                        )

                elif self.backend == "chromadb":
                    if self._index is None:
                        import chromadb
                        self._client = chromadb.Client()
                        self._index = self._client.create_collection(self._collection_name)

                    ids = [
                        f"{doc_id}_{meta.get('chunk_index', 0)}_{time.time_ns()}_{i}"
                        for i, (doc_id, _, meta) in enumerate(items)
                    ]
                    embeddings = [vec for _, vec, _ in items]
                    metadatas = [meta for _, _, meta in items]
                    documents = [meta.get("text", "") for _, _, meta in items]

                    self._index.add(
                        ids=ids,
                        embeddings=embeddings,
                        metadatas=metadatas,
                        documents=documents,
                    )
                else:
                    raise ValueError(f"Unsupported Vector DB backend: {self.backend}")

                return  # success

            except Exception as e:
                last_error = e
                time.sleep(0.5 * attempt)

        handle_vector_db_error(
            "store_embeddings_batch",
            f"Batch insert failed after {max_attempts} attempts. Last exception: {str(last_error)}"
        )

    def search(self, query_vector: List[float], top_k: int = None) -> List[RetrievalResult]:
        """
        Retrieves the top_k most similar document chunks based on distance metrics.

        Args:
            query_vector: Numerical query coordinate list.
            top_k: Number of chunks to retrieve (defaults to config.RAG_TOP_K).

        Returns:
            A list of RetrievalResult objects.
        """
        if self._index is None:
            return []

        k = top_k or config.RAG_TOP_K

        try:
            results = []

            if self.backend == "faiss":
                # FAISS similarity search returns List[Tuple[Document, float]]
                raw_results = self._index.similarity_search_with_score_by_vector(
                    embedding=query_vector,
                    k=k
                )
                for doc, score in raw_results:
                    results.append(RetrievalResult(
                        doc_id=doc.metadata.get("doc_id", ""),
                        score=float(score),
                        text=doc.page_content
                    ))

            elif self.backend == "chromadb":
                # Chroma collection query returns raw results dict
                raw_results = self._index.query(
                    query_embeddings=[query_vector],
                    n_results=k
                )
                ids_list = raw_results.get("ids", [])
                if ids_list and len(ids_list[0]) > 0:
                    documents = raw_results.get("documents", [[]])[0]
                    metadatas = raw_results.get("metadatas", [[]])[0]
                    distances = raw_results.get("distances", [[]])[0]

                    for i in range(len(documents)):
                        results.append(RetrievalResult(
                            doc_id=metadatas[i].get("doc_id", ""),
                            score=float(distances[i]),
                            text=documents[i]
                        ))
            else:
                raise ValueError(f"Unsupported Vector DB backend: {self.backend}")

            return results

        except Exception as e:
            handle_vector_db_error("search", str(e))
