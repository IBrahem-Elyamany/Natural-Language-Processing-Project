from fastapi import FastAPI
from app.api.v1.cv_matcher import router as cv_matcher_router
from app.api.v1.db_info import router as db_info_router

app = FastAPI(title="RAG CV Matching API")

app.include_router(cv_matcher_router, prefix="/api/v1")
app.include_router(db_info_router, prefix="/api/v1/db", tags=["Database"])

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the RAG CV Matching API"}

