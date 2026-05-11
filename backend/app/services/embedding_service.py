"""
EmbeddingService — singleton wrapper around SentenceTransformer.

Loading the model is expensive (~1–2 s + GPU/RAM).  This singleton ensures
the model is loaded exactly once and shared across the entire application.
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingService:
    """Singleton that owns the SentenceTransformer model."""

    _instance: EmbeddingService | None = None
    _model: SentenceTransformer | None = None

    def __new__(cls) -> EmbeddingService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._model = SentenceTransformer(settings.sentence_transformer_model)
        return cls._instance

    @property
    def model_name(self) -> str:
        return settings.sentence_transformer_model

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Return embedding vectors for a list of texts."""
        return self._model.encode(texts).tolist()

    def encode_single(self, text: str) -> list[float]:
        """Return a single embedding vector."""
        return self._model.encode([text])[0].tolist()


def get_embedding_service() -> EmbeddingService:
    """FastAPI dependency that returns the singleton EmbeddingService."""
    return EmbeddingService()
