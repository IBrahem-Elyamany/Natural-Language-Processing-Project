import os
import shutil
from dataclasses import asdict
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from typing import List

from app.core.config import settings
from app.services.rag_service import RAGService, get_rag_service
from app.services.llm.llm_service import LLMService
from app.services.extractor.service import TextExtractorService

router = APIRouter()


@router.post("/match_cvs")
async def match_cvs(
    input: str = Form(...),
    files: List[UploadFile] = File(...),
    rag_svc: RAGService = Depends(get_rag_service),
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

            # Chunk, embed, and store via RAGService
            chunks_stored = rag_svc.upsert_document(
                filename=file.filename, text=text
            )
            if chunks_stored > 0:
                uploaded_docs.append(file.filename)

        llm_service = LLMService()
        # Search the collection
        jd_text, top_n = llm_service.extract_job_details(input)

        search_response = rag_svc.search(
            query=jd_text,
            top_n=top_n
        )

        # Evaluate candidates using LLM
        llm_service = LLMService()
        evaluation_report = llm_service.evaluate_candidates(
            jd_text=jd_text,
            top_n=top_n,
            context_docs=search_response.context_docs,
        )

        return {
            "message": f"Successfully processed {len(uploaded_docs)} CVs",
            "job_description": jd_text,
            "results": [asdict(r) for r in search_response.results],
            "evaluation_report": evaluation_report,
        }

    finally:
        # Cleanup temporary files
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


@router.post("/search")
async def search_cvs(
    input: str = Form(...),
    rag_svc: RAGService = Depends(get_rag_service),
):
    """
    Search existing CVs in the database against a job description.
    No file upload needed — queries the pre-indexed ChromaDB collection.
    """
    # Check that the collection has data
    if rag_svc.count() == 0:
        raise HTTPException(
            status_code=404,
            detail="No CVs found in the database. Upload CVs first using /match_cvs.",
        )

    llm_service = LLMService()
    # Search the collection
    jd_text, top_n = llm_service.extract_job_details(input)

    search_response = rag_svc.search(
        query=jd_text,
        top_n=top_n
    )

    # Evaluate candidates using LLM
    evaluation_report = llm_service.evaluate_candidates(
        jd_text=jd_text,
        top_n=top_n,
        context_docs=search_response.context_docs,
    )

    return {
        "job_description": jd_text,
        "total_cvs_in_db": rag_svc.count(),
        "results": [asdict(r) for r in search_response.results],
        "evaluation_report": evaluation_report,
    }
