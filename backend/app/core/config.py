from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # ChromaDB Configuration
    chroma_persist_dir: str = "/data/chroma"
    chroma_collection: str = "cv_matching"

    # Sentence Transformer Configuration
    sentence_transformer_model: str = "all-MiniLM-L6-v2"

    # Text Splitting Configuration
    chunk_size: int = 500
    chunk_overlap_percentage: float = 0.20
    custom_separators: List[str] = [
         "\n\n", "experience", "summary", "education", "skills", ". ", "! ", "? ", "\n", " ", ""
    ]

    # LLM Provider Configuration
    llm_provider: str = "gemini"  # "ollama" or "gemini"

    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral"

    # Gemini Configuration
    gemini_base_url: str = "https://generativelanguage.googleapis.com"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    default_top_n: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()