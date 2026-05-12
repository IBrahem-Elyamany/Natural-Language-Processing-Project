"""
CollectionService — single responsibility layer for all vector-DB operations.

This service owns:
  • Text chunking
  • Upserting documents into ChromaDB
  • Querying / similarity search
  • Collection introspection (count, peek, diagnostics)

Neither the API routes nor the LLM service need to know *how* vectors are
stored — they just call methods here.
"""

from __future__ import annotations
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import Depends

from app.core.config import settings
from app.core.chroma import ChromaService, get_chroma_service
from app.services.embedding_service import EmbeddingService, get_embedding_service
from app.schemas.collection import SearchResult, SearchResponse, CollectionInfo, PeekSample


# ── Service ──────────────────────────────────────────────────────────

class CollectionService:
    """
    Encapsulates all interaction with the vector store.

    Depends on:
      - ChromaService       (low-level client lifecycle)
      - EmbeddingService    (singleton embedding model)
      - RecursiveCharacterTextSplitter  (chunking)
    """

    def __init__(self, chroma: ChromaService, embedder: EmbeddingService) -> None:
        self._chroma = chroma
        self._embedder = embedder

    # ── helpers ──────────────────────────────────────────────────────

    def _get_collection(self, name: str | None = None):
        return self._chroma.get_collection(name)

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

    # ── write operations ─────────────────────────────────────────────

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

        collection = self._get_collection(collection_name)

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

    # ── read / search operations ─────────────────────────────────────

    def search(
        self,
        query: str,
        collection_name: str | None = None,
    ) -> SearchResponse:
        """
        Embed *query*, run similarity search, and return formatted results
        together with a concatenated context string for LLM consumption.
        """
        collection = self._get_collection(collection_name)

        try:
            jd_text = query.split("|")[0].replace("JD:", "").strip()
            top_n   = int(query.split("|")[1].replace("N:", "").strip())
        except:
            jd_text = query
            top_n   = settings.default_top_n

        query_embedding = self._embedder.encode_single(jd_text)
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
                    filename=metadata.get("filename", "Unknown"),
                    snippet=doc[:200] + "...",
                    distance=distance,
                )
            )

        return response
        
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
        collection = self._get_collection(collection_name)

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
                    filename=metadata.get("filename", "Unknown"),
                    snippet=doc[:200] + "...",
                    distance=distance,
                )
            )

        return response

    def count(self, collection_name: str | None = None) -> int:
        """Return the total number of chunks in the collection."""
        return self._get_collection(collection_name).count()

    # ── introspection ────────────────────────────────────────────────

    def get_collection_info(self, collection_name: str) -> CollectionInfo:
        """Return summary info about a named collection."""
        col = self._chroma.client.get_collection(name=collection_name)
        count = col.count()

        filenames: set[str] = set()
        if count > 0:
            sample = col.get(limit=min(count, 100), include=["metadatas"])
            for meta in sample.get("metadatas", []):
                if meta and "filename" in meta:
                    filenames.add(meta["filename"])

        return CollectionInfo(
            name=collection_name,
            total_chunks=count,
            unique_files=sorted(filenames),
            unique_file_count=len(filenames),
        )

    def peek(self, collection_name: str, limit: int = 5) -> list[PeekSample]:
        """Return a few document previews from a collection."""
        col = self._chroma.client.get_collection(name=collection_name)
        if col.count() == 0:
            return []

        sample = col.get(
            limit=min(limit, col.count()),
            include=["documents", "metadatas"],
        )

        results: list[PeekSample] = []
        for i in range(len(sample["ids"])):
            meta = sample["metadatas"][i]
            doc = sample["documents"][i]
            results.append(
                PeekSample(
                    id=sample["ids"][i],
                    filename=meta.get("filename", "Unknown") if meta else "Unknown",
                    snippet=(doc[:300] + "...") if doc else "",
                )
            )
        return results

    def diagnostics(self) -> dict:
        """Full diagnostic dump of the ChromaDB instance."""
        info = {
            "client_type": "PersistentClient",
            "persist_dir": str(self._chroma.client._identifier),
        }

        try:
            collections = self._chroma.client.list_collections()
            col_details = []
            for col in collections:
                detail = {"name": col.name, "id": str(col.id)}
                try:
                    detail["count"] = col.count()
                except Exception as e:
                    detail["count_error"] = str(e)

                try:
                    raw = col.get(limit=1, include=["documents", "metadatas"])
                    detail["get_returned_ids"] = len(raw.get("ids", []))
                    if raw.get("ids"):
                        detail["sample_id"] = raw["ids"][0]
                        detail["sample_metadata"] = (
                            raw["metadatas"][0] if raw.get("metadatas") else None
                        )
                        detail["sample_doc_preview"] = (
                            raw["documents"][0][:200]
                            if raw.get("documents") and raw["documents"][0]
                            else None
                        )
                except Exception as e:
                    detail["get_error"] = str(e)

                col_details.append(detail)

            info["collections"] = col_details
            info["total_collections"] = len(collections)
        except Exception as e:
            info["list_error"] = str(e)

        return info

    def list_collections(self) -> list[str]:
        """Return names of all collections."""
        return [col.name for col in self._chroma.client.list_collections()]


# ── FastAPI dependency ───────────────────────────────────────────────

def get_collection_service(
    chroma: ChromaService = Depends(get_chroma_service),
    embedder: EmbeddingService = Depends(get_embedding_service),
) -> CollectionService:
    """
    FastAPI dependency.  Builds a CollectionService backed by the
    singleton ChromaService and EmbeddingService.
    """
    return CollectionService(chroma, embedder)

