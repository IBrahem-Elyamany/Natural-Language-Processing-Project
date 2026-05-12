from __future__ import annotations
from fastapi import Depends
from app.core.chroma import ChromaService, get_chroma_service
from app.schemas.collection import CollectionInfo, PeekSample

class VectorStore:
    def __init__(self, chroma: ChromaService):
        self._chroma = chroma
        
    def get_collection(self, name: str | None = None):
        return self._chroma.get_collection(name)

    def count(self, collection_name: str | None = None) -> int:
        return self.get_collection(collection_name).count()

    def get_collection_info(self, collection_name: str) -> CollectionInfo:
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
        return [col.name for col in self._chroma.client.list_collections()]

    def get_metadata_by_filename(self, filename: str, collection_name: str | None = None) -> dict | None:
        col = self.get_collection(collection_name)
        results = col.get(
            where={"filename": filename},
            limit=1,
            include=["metadatas"],
        )
        if results and results.get("metadatas"):
            return results["metadatas"][0]
        return None

def get_vector_store(chroma: ChromaService = Depends(get_chroma_service)) -> VectorStore:
    return VectorStore(chroma)
