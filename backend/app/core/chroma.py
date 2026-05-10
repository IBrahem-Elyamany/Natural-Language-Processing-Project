import chromadb
from app.core.config import settings


class ChromaService:
    """Singleton ChromaDB PersistentClient."""

    _instance: "ChromaService | None" = None
    _client: chromadb.ClientAPI | None = None

    def __new__(cls) -> "ChromaService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        return cls._instance

    @property
    def client(self) -> chromadb.ClientAPI:
        return self._client

    def get_collection(self, name: str | None = None):
        """Get a collection by name (defaults to the configured collection)."""
        return self._client.get_or_create_collection(
            name=name or settings.chroma_collection,
        )


def get_chroma_service() -> ChromaService:
    """FastAPI dependency that returns the singleton ChromaService."""
    return ChromaService()
