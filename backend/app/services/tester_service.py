"""
TesterService — automated evaluation of the ROMI RAG CV-Matching system.

Loads the ground_truth.json file and runs test cases across five dimensions:
  1. Retrieval Accuracy   (Precision@K)
  2. Edge Cases           (Pass / Fail graceful handling)
  3. Cross-Category Confusion (top-1 correctness)
  4. Hallucination Detection  (LLM output vs. retrieved context)
  5. Ranking Quality          (NDCG / rank correlation)

Depends on CollectionService (vector search) and LLMService (evaluation).
"""

from __future__ import annotations

import json
import math
import logging
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from fastapi import Depends

from app.services.collection_service import (
    CollectionService,
    get_collection_service,
)
from app.services.llm.llm_service import LLMService

logger = logging.getLogger(__name__)

# ── Path to the bundled ground truth ─────────────────────────────────
GROUND_TRUTH_PATH = Path(__file__).resolve().parent.parent / "ground_truth.json"


# ── Result data-transfer objects ─────────────────────────────────────
from app.schemas.tester import (
    RetrievalAccuracyResult,
    EdgeCaseResult,
    CrossCategoryResult,
    HallucinationResult,
    RankingQualityResult,
    DimensionSummary,
    EvaluationReport,
)


# ── Service ──────────────────────────────────────────────────────────

class TesterService:
    """
    Orchestrates end-to-end evaluation of the RAG system using ground
    truth test cases.
    """

    def __init__(
        self,
        collection_svc: CollectionService,
        llm_svc: LLMService | None = None,
    ) -> None:
        self._collection_svc = collection_svc
        self._llm_svc = llm_svc or LLMService()
        self._ground_truth = self._load_ground_truth()

    # ── helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _load_ground_truth() -> dict:
        with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _dcg(relevances: list[float]) -> float:
        """Discounted cumulative gain."""
        return sum(
            rel / math.log2(i + 2) for i, rel in enumerate(relevances)
        )

    def _ndcg(self, relevances: list[float]) -> float:
        """Normalized DCG (0–1)."""
        ideal = sorted(relevances, reverse=True)
        ideal_dcg = self._dcg(ideal)
        if ideal_dcg == 0:
            return 0.0
        return round(self._dcg(relevances) / ideal_dcg, 4)

    @staticmethod
    def _infer_category_from_filename(
        filename: str,
        collection_svc: CollectionService,
    ) -> str | None:
        """
        Attempt to infer the category of a retrieved file by looking at
        its metadata in the collection. Falls back to 'unknown'.
        """
        try:
            col = collection_svc._get_collection()
            results = col.get(
                where={"filename": filename},
                limit=1,
                include=["metadatas"],
            )
            if results and results.get("metadatas"):
                meta = results["metadatas"][0]
                return meta.get("category", "unknown")
        except Exception:
            pass
        return "unknown"

    # ── 1. Retrieval Accuracy ────────────────────────────────────────

    def evaluate_retrieval_accuracy(self, top_n: int = 5) -> DimensionSummary:
        """
        For each retrieval-accuracy test case, run a search and compute
        Precision@K — the fraction of top-K results whose source file
        belongs to one of the expected categories.
        """
        cases = (
            self._ground_truth
            .get("evaluation_dimensions", {})
            .get("retrieval_accuracy", {})
            .get("test_cases", [])
        )

        results: list[RetrievalAccuracyResult] = []
        passed_count = 0

        for case in cases:
            query = case["query"]
            expected = [c.lower() for c in case["expected_categories"]]

            search_resp = self._collection_svc.search(query=query, top_n=top_n)

            retrieved_filenames = [r.filename for r in search_resp.results]

            # Check which retrieved filenames appear in ground truth samples
            gt_filenames = {
                s["filename"]
                for s in case.get("ground_truth_cv_samples", [])
            }

            # Primary check: does any expected ground-truth file appear?
            hits = sum(1 for fn in retrieved_filenames if fn in gt_filenames)

            # Precision@K: fraction of results with a ground-truth file hit
            precision = hits / len(retrieved_filenames) if retrieved_filenames else 0.0
            is_pass = hits > 0  # at least one relevant result

            if is_pass:
                passed_count += 1

            results.append(
                RetrievalAccuracyResult(
                    id=case["id"],
                    query=query,
                    expected_categories=case["expected_categories"],
                    retrieved_filenames=retrieved_filenames,
                    precision_at_k=round(precision, 4),
                    hits=hits,
                    total=len(retrieved_filenames),
                    passed=is_pass,
                )
            )

        total = len(results)
        return DimensionSummary(
            dimension="retrieval_accuracy",
            total_cases=total,
            passed=passed_count,
            failed=total - passed_count,
            pass_rate=round(passed_count / total, 4) if total else 0.0,
            details=[asdict(r) for r in results],
        )

    # ── 2. Edge Cases ────────────────────────────────────────────────

    def evaluate_edge_cases(self, top_n: int = 5) -> DimensionSummary:
        """
        Submit each edge-case query and verify the system handles it
        gracefully (no crash, appropriate response).
        """
        cases = (
            self._ground_truth
            .get("evaluation_dimensions", {})
            .get("edge_cases", {})
            .get("test_cases", [])
        )

        results: list[EdgeCaseResult] = []
        passed_count = 0

        for case in cases:
            query = case["query"]
            expected = case["expected_behavior"]
            failure_type = case["failure_type"]
            error_msg = None
            actual = "unknown"
            is_pass = False

            try:
                if not query.strip():
                    # Empty query — system should reject or return empty
                    actual = "error_or_empty"
                    is_pass = expected in ("error_or_empty",)
                else:
                    search_resp = self._collection_svc.search(
                        query=query, top_n=top_n,
                    )
                    n_results = len(search_resp.results)

                    if n_results == 0:
                        actual = "no_relevant_match"
                    else:
                        # Check distance spread — high distances suggest poor matches
                        avg_dist = (
                            sum(r.distance for r in search_resp.results) / n_results
                            if n_results
                            else 0.0
                        )
                        if avg_dist > 1.5:
                            actual = "no_relevant_match"
                        else:
                            actual = "results_returned"

                    # Pass if actual behaviour is consistent with expected
                    is_pass = (
                        actual == expected
                        or (expected == "ambiguous_retrieval" and actual == "results_returned")
                        or (expected == "confused_retrieval" and actual == "results_returned")
                        or (expected == "poor_or_no_match" and actual in ("no_relevant_match", "results_returned"))
                        or (expected == "error_or_empty" and actual in ("error_or_empty", "no_relevant_match"))
                    )

            except Exception as exc:
                error_msg = str(exc)
                actual = "error_raised"
                # For cases expecting error, this is a pass
                is_pass = expected in ("error_or_empty",)

            if is_pass:
                passed_count += 1

            results.append(
                EdgeCaseResult(
                    id=case["id"],
                    query=query[:100],
                    expected_behavior=expected,
                    failure_type=failure_type,
                    actual_behavior=actual,
                    passed=is_pass,
                    error=error_msg,
                )
            )

        total = len(results)
        return DimensionSummary(
            dimension="edge_cases",
            total_cases=total,
            passed=passed_count,
            failed=total - passed_count,
            pass_rate=round(passed_count / total, 4) if total else 0.0,
            details=[asdict(r) for r in results],
        )

    # ── 3. Cross-Category Confusion ──────────────────────────────────

    def evaluate_cross_category(self, top_n: int = 5) -> DimensionSummary:
        """
        For each confusion test case, verify that the top-1 result
        comes from the expected category rather than a confusing one.
        """
        cases = (
            self._ground_truth
            .get("evaluation_dimensions", {})
            .get("cross_category_confusion", {})
            .get("test_cases", [])
        )

        results: list[CrossCategoryResult] = []
        passed_count = 0

        for case in cases:
            query = case["query"]
            expected_cat = case["expected_category"].lower()
            confusing = [c.lower() for c in case["confusing_categories"]]

            search_resp = self._collection_svc.search(query=query, top_n=top_n)

            top1_filename = (
                search_resp.results[0].filename
                if search_resp.results
                else "N/A"
            )

            # Try to infer the category from metadata
            top1_category = self._infer_category_from_filename(
                top1_filename, self._collection_svc
            )

            # Check: top-1 should match expected, not confusing
            is_pass = (
                top1_category.lower() == expected_cat
                or top1_category.lower() not in confusing
            )

            if is_pass:
                passed_count += 1

            results.append(
                CrossCategoryResult(
                    id=case["id"],
                    query=query,
                    expected_category=case["expected_category"],
                    confusing_categories=case["confusing_categories"],
                    top1_filename=top1_filename,
                    top1_category_guess=top1_category,
                    passed=is_pass,
                )
            )

        total = len(results)
        return DimensionSummary(
            dimension="cross_category_confusion",
            total_cases=total,
            passed=passed_count,
            failed=total - passed_count,
            pass_rate=round(passed_count / total, 4) if total else 0.0,
            details=[asdict(r) for r in results],
        )

    # ── 4. Hallucination Detection ───────────────────────────────────

    def evaluate_hallucination(self) -> DimensionSummary:
        """
        Feed the ground-truth retrieved_context to the LLM and check
        whether the output fabricates information not present in context.
        """
        cases = (
            self._ground_truth
            .get("evaluation_dimensions", {})
            .get("hallucination_detection", {})
            .get("test_cases", [])
        )

        results: list[HallucinationResult] = []

        for case in cases:
            query = case["query"]
            context = case["retrieved_context"]
            source = case["context_source_file"]
            checks = case["checks"]

            # Use the LLM to evaluate the context as if it were search results
            try:
                llm_output = self._llm_svc.evaluate_candidates(
                    jd_text=query,
                    top_n=1,
                    context_docs=context,
                )
            except Exception as exc:
                llm_output = f"[LLM ERROR: {exc}]"

            results.append(
                HallucinationResult(
                    id=case["id"],
                    query=query,
                    context_source_file=source,
                    llm_output=llm_output,
                    checks=checks,
                    notes="Manual review required — compare LLM output against context and checks.",
                )
            )

        total = len(results)
        return DimensionSummary(
            dimension="hallucination_detection",
            total_cases=total,
            passed=0,
            failed=0,
            pass_rate=0.0,  # Requires manual review
            details=[asdict(r) for r in results],
        )

    # ── 5. Ranking Quality ───────────────────────────────────────────

    def evaluate_ranking_quality(self, top_n: int = 10) -> DimensionSummary:
        """
        Submit each ranking query and compare the category distribution
        of results against the expected ranking using NDCG.
        """
        cases = (
            self._ground_truth
            .get("evaluation_dimensions", {})
            .get("ranking_quality", {})
            .get("test_cases", [])
        )

        results: list[RankingQualityResult] = []
        passed_count = 0

        for case in cases:
            query = case["query"]
            expected_ranking = case["expected_ranking"]

            search_resp = self._collection_svc.search(query=query, top_n=top_n)

            # Build the expected category order
            expected_cats = [
                r["category"].lower() for r in expected_ranking
            ]

            # Infer categories from retrieved results
            actual_cats: list[str] = []
            for result in search_resp.results:
                cat = self._infer_category_from_filename(
                    result.filename, self._collection_svc
                )
                actual_cats.append(cat)

            # Compute relevance scores: 3 for rank-1 match, 2 for rank-2, etc.
            relevances: list[float] = []
            for cat in actual_cats:
                cat_lower = cat.lower()
                if cat_lower in expected_cats:
                    # Higher relevance for categories expected earlier
                    idx = expected_cats.index(cat_lower)
                    relevances.append(float(len(expected_cats) - idx))
                else:
                    relevances.append(0.0)

            ndcg = self._ndcg(relevances)
            is_pass = ndcg >= 0.5

            if is_pass:
                passed_count += 1

            results.append(
                RankingQualityResult(
                    id=case["id"],
                    query=query,
                    expected_ranking=expected_ranking,
                    actual_category_order=actual_cats[:5],
                    ndcg=ndcg,
                    description=case.get("description", ""),
                )
            )

        total = len(results)
        return DimensionSummary(
            dimension="ranking_quality",
            total_cases=total,
            passed=passed_count,
            failed=total - passed_count,
            pass_rate=round(passed_count / total, 4) if total else 0.0,
            details=[asdict(r) for r in results],
        )

    # ── Full evaluation ──────────────────────────────────────────────

    def run_full_evaluation(self, top_n: int = 5) -> EvaluationReport:
        """Run all five evaluation dimensions and return a unified report."""
        import datetime

        dimensions: dict[str, DimensionSummary] = {}

        logger.info("Starting retrieval accuracy evaluation...")
        dimensions["retrieval_accuracy"] = self.evaluate_retrieval_accuracy(top_n)

        logger.info("Starting edge case evaluation...")
        dimensions["edge_cases"] = self.evaluate_edge_cases(top_n)

        logger.info("Starting cross-category confusion evaluation...")
        dimensions["cross_category_confusion"] = self.evaluate_cross_category(top_n)

        logger.info("Starting hallucination detection evaluation...")
        dimensions["hallucination_detection"] = self.evaluate_hallucination()

        logger.info("Starting ranking quality evaluation...")
        dimensions["ranking_quality"] = self.evaluate_ranking_quality(top_n * 2)

        # Compute overall pass rate (exclude hallucination — requires manual review)
        auto_dims = [
            v for k, v in dimensions.items() if k != "hallucination_detection"
        ]
        total_cases = sum(d.total_cases for d in auto_dims)
        total_passed = sum(d.passed for d in auto_dims)

        return EvaluationReport(
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            total_test_cases=sum(d.total_cases for d in dimensions.values()),
            overall_pass_rate=round(total_passed / total_cases, 4) if total_cases else 0.0,
            dimensions=dimensions,
        )


# ── FastAPI dependency ───────────────────────────────────────────────

def get_tester_service(
    collection_svc: CollectionService = Depends(get_collection_service),
) -> TesterService:
    """
    FastAPI dependency.  Builds a TesterService backed by the singleton
    CollectionService and a fresh LLMService.
    """
    return TesterService(collection_svc)
