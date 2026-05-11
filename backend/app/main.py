from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.cv_matcher import router as cv_matcher_router
from app.api.v1.db_info import router as db_info_router
from app.api.v1.tester import router as tester_router

app = FastAPI(title="RAG CV Matching API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Allow your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv_matcher_router, prefix="/api/v1", tags=["CVs"])
app.include_router(db_info_router, prefix="/api/v1/db", tags=["Database"])
app.include_router(tester_router, prefix="/api/v1/test", tags=["Evaluation"])


@app.get("/")
def read_root():
    return {"Hello": "Welcome to the RAG CV Matching API"}
