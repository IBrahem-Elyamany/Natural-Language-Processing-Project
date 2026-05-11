import os
import shutil
from dataclasses import asdict
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from typing import List

from app.core.config import settings
from app.services.collection_service import CollectionService, get_collection_service
from app.services.llm.llm_service import LLMService
from app.services.extractor.service import TextExtractorService

router = APIRouter()


@router.post("/match_cvs")
async def match_cvs(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...),
    top_n: int = Form(3),
    collection_svc: CollectionService = Depends(get_collection_service),
):
    if not files:
        raise HTTPException(status_code=400, detail="No CV files provided")

    uploaded_docs = []
    temp_dir = "/tmp/romi_uploads"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        extractor_svc = TextExtractorService()

        # Process each uploaded file
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Extract text
            text = extractor_svc.extract_text(file_path)
            if not text.strip():
                continue

            # Chunk, embed, and store via CollectionService
            chunks_stored = collection_svc.upsert_document(
                filename=file.filename, text=text
            )
            if chunks_stored > 0:
                uploaded_docs.append(file.filename)

        # Search the collection using the job description
        search_response = collection_svc.search(
            query=job_description, top_n=top_n
        )

        # Evaluate candidates using LLM
        llm_service = LLMService()
        evaluation_report = llm_service.evaluate_candidates(
            jd_text=job_description,
            top_n=top_n,
            context_docs=search_response.context_docs,
        )

        return {
            "message": f"Successfully processed {len(uploaded_docs)} CVs",
            "job_description": job_description,
            "results": [asdict(r) for r in search_response.results],
            "evaluation_report": evaluation_report,
        }

    finally:
        # Cleanup temporary files
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


@router.post("/search")
async def search_cvs(
    job_description: str = Form(...),
    top_n: int = Form(settings.default_top_n),
    collection_svc: CollectionService = Depends(get_collection_service),
):
    """
    Search existing CVs in the database against a job description.
    No file upload needed — queries the pre-indexed ChromaDB collection.
    """
    # Check that the collection has data
    if collection_svc.count() == 0:
        raise HTTPException(
            status_code=404,
            detail="No CVs found in the database. Upload CVs first using /match_cvs.",
        )

    # Search the collection
    search_response = collection_svc.search(
        query=job_description, top_n=top_n
    )

    # Evaluate candidates using LLM
    llm_service = LLMService()
    evaluation_report = llm_service.evaluate_candidates(
        jd_text=job_description,
        top_n=top_n,
        context_docs=search_response.context_docs,
    )

    return {
        "job_description": job_description,
        "total_cvs_in_db": collection_svc.count(),
        "results": [asdict(r) for r in search_response.results],
        "evaluation_report": evaluation_report,
    }
