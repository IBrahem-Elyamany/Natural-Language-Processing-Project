"""
RAGService — orchestrates text chunking, embedding, and vector-DB storage.
"""

from __future__ import annotations
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import Depends

from app.core.config import settings
from app.store.vector_store import VectorStore, get_vector_store
from app.services.embedding_service import EmbeddingService, get_embedding_service
from app.schemas.collection import SearchResult, SearchResponse


class RAGService:

    def __init__(self, store: VectorStore, embedder: EmbeddingService) -> None:
        self._store = store
        self._embedder = embedder

    def count(self, collection_name: str | None = None) -> int:
        return self._store.count(collection_name)

    def chunk_text(self, text: str) -> List[str]:
        """Split *text* into overlapping chunks using the configured strategy."""
        chunk_overlap = int(settings.chunk_size * settings.chunk_overlap_percentage)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=chunk_overlap,
            separators=settings.custom_separators,
            is_separator_regex=False,
        )
        return splitter.split_text(text)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return embedding vectors for a list of texts."""
        return self._embedder.encode(texts)

    def upsert_document(
        self,
        filename: str,
        text: str,
        collection_name: str | None = None,
    ) -> int:
        """
        Chunk, embed, and upsert a single document.
        Returns the number of chunks stored.
        """
        chunks = self.chunk_text(text)
        if not chunks:
            return 0

        collection = self._store.get_collection(collection_name)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_chunk_{i}"
            embedding = self._embedder.encode_single(chunk)
            collection.upsert(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"filename": filename}],
            )

        return len(chunks)

    def search(
        self,
        query: str,
        top_n: int,
        collection_name: str | None = None,
    ) -> SearchResponse:
        """
        Embed *query*, run similarity search, and return formatted results
        together with a concatenated context string for LLM consumption.
        """
        collection = self._store.get_collection(collection_name)

        query_embedding = self._embedder.encode_single(query)
        raw = collection.query(query_embeddings=[query_embedding], n_results=top_n)

        response = SearchResponse()
        if not raw or not raw.get("documents"):
            return response

        response.context_docs = "\n---\n".join(raw["documents"][0])

        for i, doc in enumerate(raw["documents"][0]):
            metadata = raw["metadatas"][0][i]
            distance = raw["distances"][0][i] if "distances" in raw else 0.0

            response.results.append(
                SearchResult(
                    rank=i + 1,
                    filename=metadata.get("candidate_id", "Unknown"),
                    snippet=doc[:200] + "...",
                    distance=distance,
                )
            )

        return response


def get_rag_service(
    store: VectorStore = Depends(get_vector_store),
    embedder: EmbeddingService = Depends(get_embedding_service),
) -> RAGService:
    """
    FastAPI dependency.  Builds a RAGService backed by the
    singleton VectorStore and EmbeddingService.
    """
    return RAGService(store, embedder)
