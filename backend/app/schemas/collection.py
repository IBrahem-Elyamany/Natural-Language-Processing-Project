from dataclasses import dataclass, field
from typing import List

@dataclass
class SearchResult:
    """A single ranked search hit."""
    rank: int
    filename: str
    snippet: str
    distance: float

@dataclass
class SearchResponse:
    """Everything a route needs after a similarity search."""
    results: list[SearchResult] = field(default_factory=list)
    context_docs: str = ""

@dataclass
class CollectionInfo:
    """Summary info about a collection."""
    name: str
    total_chunks: int
    unique_files: list[str]
    unique_file_count: int

@dataclass
class PeekSample:
    """A single document preview."""
    id: str
    filename: str
    snippet: str
