from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException

from app.store.vector_store import VectorStore, get_vector_store

router = APIRouter()


@router.get("/collections")
async def list_collections(
    store: VectorStore = Depends(get_vector_store),
):
    """List all collections in the ChromaDB instance."""
    names = store.list_collections()
    return {
        "total": len(names),
        "collections": names,
    }


@router.get("/collections/{collection_name}")
async def get_collection_info(
    collection_name: str,
    store: VectorStore = Depends(get_vector_store),
):
    """Get detailed info about a specific collection."""
    try:
        info = store.get_collection_info(collection_name)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection_name}' not found.",
        )
    return asdict(info)


@router.get("/collections/{collection_name}/peek")
async def peek_collection(
    collection_name: str,
    limit: int = 5,
    store: VectorStore = Depends(get_vector_store),
):
    """Preview a few documents from a collection."""
    try:
        samples = store.peek(collection_name, limit=limit)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection_name}' not found.",
        )

    return {
        "name": collection_name,
        "total_chunks": store.count(collection_name),
        "showing": len(samples),
        "samples": [asdict(s) for s in samples],
    }


@router.get("/diagnostics")
async def diagnostics(
    store: VectorStore = Depends(get_vector_store),
):
    """
    Full diagnostic dump of the ChromaDB instance.
    Shows client info, all collections, and data counts.
    """
    return store.diagnostics()
