from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException

from app.services.collection_service import CollectionService, get_collection_service

router = APIRouter()


@router.get("/collections")
async def list_collections(
    collection_svc: CollectionService = Depends(get_collection_service),
):
    """List all collections in the ChromaDB instance."""
    names = collection_svc.list_collections()
    return {
        "total": len(names),
        "collections": names,
    }


@router.get("/collections/{collection_name}")
async def get_collection_info(
    collection_name: str,
    collection_svc: CollectionService = Depends(get_collection_service),
):
    """Get detailed info about a specific collection."""
    try:
        info = collection_svc.get_collection_info(collection_name)
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
    collection_svc: CollectionService = Depends(get_collection_service),
):
    """Preview a few documents from a collection."""
    try:
        samples = collection_svc.peek(collection_name, limit=limit)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection_name}' not found.",
        )

    return {
        "name": collection_name,
        "total_chunks": collection_svc.count(collection_name),
        "showing": len(samples),
        "samples": [asdict(s) for s in samples],
    }


@router.get("/diagnostics")
async def diagnostics(
    collection_svc: CollectionService = Depends(get_collection_service),
):
    """
    Full diagnostic dump of the ChromaDB instance.
    Shows client info, all collections, and data counts.
    """
    return collection_svc.diagnostics()
