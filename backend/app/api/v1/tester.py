"""
Test Router — API endpoints for evaluating the ROMI RAG system.

Exposes endpoints to run individual evaluation dimensions or a full
suite against the ground_truth.json dataset.
"""

from dataclasses import asdict

from fastapi import APIRouter, Depends, Query

from app.services.tester_service import TesterService, get_tester_service

router = APIRouter()


@router.get("/run_all")
async def run_full_evaluation(
    top_n: int = Query(5, ge=1, le=20, description="Number of results to retrieve per query"),
    tester: TesterService = Depends(get_tester_service),
):
    """
    Run ALL evaluation dimensions and return a unified report.

    Dimensions: retrieval_accuracy, edge_cases, cross_category_confusion,
    hallucination_detection, ranking_quality.

    ⚠️  This endpoint makes multiple search + LLM calls and may take
    a few minutes to complete.
    """
    report = tester.run_full_evaluation(top_n=top_n)
    return {
        "timestamp": report.timestamp,
        "total_test_cases": report.total_test_cases,
        "overall_pass_rate": report.overall_pass_rate,
        "dimensions": {
            name: asdict(summary)
            for name, summary in report.dimensions.items()
        },
    }


@router.get("/retrieval_accuracy")
async def test_retrieval_accuracy(
    top_n: int = Query(5, ge=1, le=20, description="Number of results per query"),
    tester: TesterService = Depends(get_tester_service),
):
    """
    Evaluate retrieval accuracy (Precision@K).

    For each test case, submits the query and checks whether retrieved
    CVs belong to the expected professional categories.
    """
    result = tester.evaluate_retrieval_accuracy(top_n=top_n)
    return asdict(result)


@router.get("/edge_cases")
async def test_edge_cases(
    top_n: int = Query(5, ge=1, le=20, description="Number of results per query"),
    tester: TesterService = Depends(get_tester_service),
):
    """
    Evaluate edge-case handling (Pass / Fail).

    Tests ambiguous, empty, off-domain, non-English, and malformed queries
    to verify the system handles them gracefully.
    """
    result = tester.evaluate_edge_cases(top_n=top_n)
    return asdict(result)


@router.get("/cross_category")
async def test_cross_category_confusion(
    top_n: int = Query(5, ge=1, le=20, description="Number of results per query"),
    tester: TesterService = Depends(get_tester_service),
):
    """
    Evaluate cross-category confusion (confusion-free rate).

    Checks that the system distinguishes between categories with
    overlapping vocabulary (e.g., Electrical vs Mechanical Engineer).
    """
    result = tester.evaluate_cross_category(top_n=top_n)
    return asdict(result)


@router.get("/hallucination")
async def test_hallucination_detection(
    tester: TesterService = Depends(get_tester_service),
):
    """
    Run hallucination detection tests.

    Feeds known context to the LLM and captures the output for manual
    review against the ground-truth checks. Results include the LLM
    output and the checklist to verify against.

    ⚠️  This calls the LLM for each test case and may take a while.
    """
    result = tester.evaluate_hallucination()
    return asdict(result)


@router.get("/ranking_quality")
async def test_ranking_quality(
    top_n: int = Query(10, ge=1, le=30, description="Number of results per query"),
    tester: TesterService = Depends(get_tester_service),
):
    """
    Evaluate ranking quality (NDCG).

    Submits multi-domain queries and checks whether the system ranks
    results in the expected category priority order.
    """
    result = tester.evaluate_ranking_quality(top_n=top_n)
    return asdict(result)


@router.get("/ground_truth")
async def get_ground_truth(
    tester: TesterService = Depends(get_tester_service),
):
    """
    Return the raw ground truth JSON used for evaluation.

    Useful for inspecting test cases and expected behaviours.
    """
    return tester._ground_truth
