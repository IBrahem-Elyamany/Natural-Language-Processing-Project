import os
import shutil
import fitz  # PyMuPDF
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from typing import List
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.core.chroma import ChromaService, get_chroma_service

router = APIRouter()

# Initialize Sentence Transformer model
model = SentenceTransformer(settings.sentence_transformer_model)


def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text


def chunk_text(text: str) -> List[str]:
    chunk_overlap = int(settings.chunk_size * settings.chunk_overlap_percentage)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=chunk_overlap,
        separators=settings.custom_separators,
        is_separator_regex=False,
    )
    return text_splitter.split_text(text)


@router.post("/match_cvs")
async def match_cvs(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...),
    top_n: int = Form(3),
    chroma: ChromaService = Depends(get_chroma_service),
):
    if not files:
        raise HTTPException(status_code=400, detail="No CV files provided")

    collection = chroma.get_collection()
    uploaded_docs = []
    temp_dir = "/tmp/romi_uploads"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Process each uploaded PDF
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Extract text
            text = extract_text_from_pdf(file_path)
            if not text.strip():
                continue

            # Chunk text
            chunks = chunk_text(text)

            # Embed and store chunks
            for i, chunk in enumerate(chunks):
                chunk_id = f"{file.filename}_chunk_{i}"
                embedding = model.encode([chunk])[0].tolist()

                collection.upsert(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{"filename": file.filename}],
                )

            uploaded_docs.append(file.filename)

        # Now query the job description against the collection
        query_embedding = model.encode([job_description])[0].tolist()

        results = collection.query(query_embeddings=[query_embedding], n_results=top_n)

        # Format results and build context
        formatted_results = []
        context_docs = ""
        if results and results["documents"]:
            context_docs = "\n---\n".join(results["documents"][0])
            for i in range(len(results["documents"][0])):
                doc = results["documents"][0][i]
                metadata = results["metadatas"][0][i]
                distance = results["distances"][0][i] if "distances" in results else 0

                formatted_results.append(
                    {
                        "rank": i + 1,
                        "filename": metadata.get("filename", "Unknown"),
                        "snippet": doc[:200] + "...",
                        "distance": distance,
                    }
                )

        # Evaluate candidates using LLM
        from app.services.llm.llm_service import LLMService

        llm_service = LLMService()
        evaluation_report = llm_service.evaluate_candidates(
            jd_text=job_description, top_n=top_n, context_docs=context_docs
        )

        return {
            "message": f"Successfully processed {len(uploaded_docs)} CVs",
            "job_description": job_description,
            "results": formatted_results,
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
    chroma: ChromaService = Depends(get_chroma_service),
):
    """
    Search existing CVs in the database against a job description.
    No file upload needed — queries the pre-indexed ChromaDB collection.
    """
    collection = chroma.get_collection()

    # Check that the collection has data
    if collection.count() == 0:
        raise HTTPException(
            status_code=404,
            detail="No CVs found in the database. Upload CVs first using /match_cvs.",
        )

    # Embed the job description and query ChromaDB
    query_embedding = model.encode([job_description])[0].tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_n)

    # Format results and build context for LLM
    formatted_results = []
    context_docs = ""

    if results and results["documents"]:
        context_docs = "\n---\n".join(results["documents"][0])

        for i in range(len(results["documents"][0])):
            doc = results["documents"][0][i]
            metadata = results["metadatas"][0][i]
            distance = results["distances"][0][i] if "distances" in results else 0

            formatted_results.append(
                {
                    "rank": i + 1,
                    "filename": metadata.get("filename", "Unknown"),
                    "snippet": doc[:200] + "...",
                    "distance": distance,
                }
            )

    # Evaluate candidates using LLM
    from app.services.llm.llm_service import LLMService

    llm_service = LLMService()
    evaluation_report = llm_service.evaluate_candidates(
        jd_text=job_description, top_n=top_n, context_docs=context_docs
    )

    return {
        "job_description": job_description,
        "total_cvs_in_db": collection.count(),
        "results": formatted_results,
        "evaluation_report": evaluation_report,
    }
