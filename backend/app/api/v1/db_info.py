from fastapi import APIRouter, Depends, HTTPException

from app.core.chroma import ChromaService, get_chroma_service

router = APIRouter()


@router.get("/collections")
async def list_collections(chroma: ChromaService = Depends(get_chroma_service)):
    """List all collections in the ChromaDB instance."""
    collections = chroma.client.list_collections()
    return {
        "total": len(collections),
        "collections": [col.name for col in collections],
    }


@router.get("/collections/{collection_name}")
async def get_collection_info(
    collection_name: str,
    chroma: ChromaService = Depends(get_chroma_service),
):
    """Get detailed info about a specific collection."""
    try:
        col = chroma.client.get_collection(name=collection_name)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection_name}' not found.",
        )

    count = col.count()

    # Get a sample of documents to show stored filenames
    filenames = set()
    if count > 0:
        sample = col.get(limit=min(count, 100), include=["metadatas"])
        for meta in sample.get("metadatas", []):
            if meta and "filename" in meta:
                filenames.add(meta["filename"])

    return {
        "name": collection_name,
        "total_chunks": count,
        "unique_files": list(filenames),
        "unique_file_count": len(filenames),
    }


@router.get("/collections/{collection_name}/peek")
async def peek_collection(
    collection_name: str,
    limit: int = 5,
    chroma: ChromaService = Depends(get_chroma_service),
):
    """Preview a few documents from a collection."""
    try:
        col = chroma.client.get_collection(name=collection_name)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection_name}' not found.",
        )

    if col.count() == 0:
        return {"name": collection_name, "total_chunks": 0, "samples": []}

    sample = col.get(
        limit=min(limit, col.count()),
        include=["documents", "metadatas"],
    )

    samples = []
    for i in range(len(sample["ids"])):
        samples.append({
            "id": sample["ids"][i],
            "filename": sample["metadatas"][i].get("filename", "Unknown") if sample["metadatas"][i] else "Unknown",
            "snippet": (sample["documents"][i][:300] + "...") if sample["documents"][i] else "",
        })

    return {
        "name": collection_name,
        "total_chunks": col.count(),
        "showing": len(samples),
        "samples": samples,
    }


@router.get("/diagnostics")
async def diagnostics(chroma: ChromaService = Depends(get_chroma_service)):
    """
    Full diagnostic dump of the ChromaDB instance.
    Shows client info, all collections, and data counts.
    """
    info = {
        "client_type": "PersistentClient",
        "persist_dir": str(chroma.client._identifier),
    }

    # List all collections with counts
    try:
        collections = chroma.client.list_collections()
        col_details = []
        for col in collections:
            detail = {"name": col.name, "id": str(col.id)}
            try:
                detail["count"] = col.count()
            except Exception as e:
                detail["count_error"] = str(e)

            # Try raw get to see if data is accessible
            try:
                raw = col.get(limit=1, include=["documents", "metadatas"])
                detail["get_returned_ids"] = len(raw.get("ids", []))
                if raw.get("ids"):
                    detail["sample_id"] = raw["ids"][0]
                    detail["sample_metadata"] = raw["metadatas"][0] if raw.get("metadatas") else None
                    detail["sample_doc_preview"] = raw["documents"][0][:200] if raw.get("documents") and raw["documents"][0] else None
            except Exception as e:
                detail["get_error"] = str(e)

            col_details.append(detail)

        info["collections"] = col_details
        info["total_collections"] = len(collections)
    except Exception as e:
        info["list_error"] = str(e)

    return info
