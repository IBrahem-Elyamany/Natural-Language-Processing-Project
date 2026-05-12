from dataclasses import dataclass, field

@dataclass
class RetrievalAccuracyResult:
    """Result for a single retrieval-accuracy test case."""
    id: str
    query: str
    expected_categories: list[str]
    retrieved_filenames: list[str]
    precision_at_k: float
    hits: int
    total: int
    passed: bool

@dataclass
class EdgeCaseResult:
    """Result for a single edge-case test."""
    id: str
    query: str
    expected_behavior: str
    failure_type: str
    actual_behavior: str
    passed: bool
    error: str | None = None

@dataclass
class CrossCategoryResult:
    """Result for a single cross-category confusion test."""
    id: str
    query: str
    expected_category: str
    confusing_categories: list[str]
    top1_filename: str
    top1_category_guess: str
    passed: bool

@dataclass
class HallucinationResult:
    """Result for a single hallucination detection test."""
    id: str
    query: str
    context_source_file: str
    llm_output: str
    checks: list[str]
    notes: str

@dataclass
class RankingQualityResult:
    """Result for a single ranking quality test."""
    id: str
    query: str
    expected_ranking: list[dict]
    actual_category_order: list[str]
    ndcg: float
    description: str

@dataclass
class DimensionSummary:
    """Summary metrics for one evaluation dimension."""
    dimension: str
    total_cases: int
    passed: int
    failed: int
    pass_rate: float
    details: list[dict] = field(default_factory=list)

@dataclass
class EvaluationReport:
    """Full evaluation report across all dimensions."""
    timestamp: str
    total_test_cases: int
    overall_pass_rate: float
    dimensions: dict[str, DimensionSummary] = field(default_factory=dict)
