"""
Ground Truth Generator for RAG CV Matching System Evaluation
=============================================================

This script generates a structured ground truth JSON dataset to evaluate
the ROMI CV-matching RAG system across five dimensions:

  1. Retrieval Accuracy   – Does the system retrieve the *correct category*
                            of CVs for a given job description?
  2. Edge-Case Queries    – How does the system handle ambiguous, vague, or
                            off-domain queries?
  3. Cross-Category       – Can the system distinguish categories that share
     Confusion              overlapping vocabulary (e.g., "Java Developer"
                            vs "React Developer")?
  4. Hallucination        – Does the LLM invent skills, names, or facts not
     Detection              present in the retrieved context?
  5. Ranking Quality      – For multi-candidate retrieval, are the most
                            relevant candidates ranked first?

Usage:
    python generate_ground_truth.py                     # defaults
    python generate_ground_truth.py --csv path/to.csv   # custom CSV
    python generate_ground_truth.py --output gt.json    # custom output

Outputs:
    ground_truth.json  – The evaluation dataset (human-reviewable)
"""

import argparse
import json
import random
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────

def _sample_cv_snippets(df: pd.DataFrame, category: str, n: int = 3, max_chars: int = 300) -> list[dict]:
    """Return *n* random CV snippets from *category*."""
    sub = df[df["category"] == category]
    if sub.empty:
        return []
    samples = sub.sample(n=min(n, len(sub)), random_state=42)
    snippets = []
    for _, row in samples.iterrows():
        text = str(row["text"])[:max_chars]
        snippets.append({
            "filename": row.get("filename", "unknown"),
            "text_preview": text,
        })
    return snippets


def _normalise_category(name: str) -> str:
    """Lower-case + collapse whitespace for consistent matching."""
    return re.sub(r"\s+", " ", name.strip().lower())


# ──────────────────────────────────────────────────────────────────────
# 1. Retrieval-Accuracy Test Cases
# ──────────────────────────────────────────────────────────────────────

def build_retrieval_accuracy_cases(df: pd.DataFrame) -> list[dict]:
    """
    Each case pairs a realistic job description with the category whose
    CVs *should* be retrieved.  We cover a range of domains from the
    dataset so the evaluation is not biased toward one profession.
    """
    cases = [
        {
            "id": "RA-01",
            "query": (
                "Looking for a Senior Data Scientist with 5+ years experience "
                "in machine learning, deep learning, NLP, and statistical modeling. "
                "Proficiency in Python, TensorFlow, and SQL required."
            ),
            "expected_categories": ["Data science", "Datascience"],
            "rationale": "Pure data-science query — keywords align cleanly with the category.",
        },
        {
            "id": "RA-02",
            "query": (
                "We need a React.js front-end developer experienced with Redux, "
                "TypeScript, REST APIs, and responsive UI design."
            ),
            "expected_categories": ["React developer", "React"],
            "rationale": "Front-end React role; should not retrieve generic IT or Java CVs.",
        },
        {
            "id": "RA-03",
            "query": (
                "Hiring a Certified Public Accountant (CPA) to manage financial "
                "statements, tax filings, and audit coordination for a mid-size firm."
            ),
            "expected_categories": ["Accountant"],
            "rationale": "Finance domain — must not confuse with Banking or Finance categories.",
        },
        {
            "id": "RA-04",
            "query": (
                "Seeking a DevOps Engineer skilled in CI/CD pipelines, Kubernetes, "
                "Docker, Terraform, and cloud platforms (AWS / GCP)."
            ),
            "expected_categories": ["Devops engineer", "Devopsengineer"],
            "rationale": "DevOps is a distinct role from generic IT or backend development.",
        },
        {
            "id": "RA-05",
            "query": (
                "Agricultural field technician needed for crop management, "
                "tractor operation, and farm equipment maintenance."
            ),
            "expected_categories": ["Agricultural", "Agriculture"],
            "rationale": "Niche domain; verifies that the system handles non-tech categories.",
        },
        {
            "id": "RA-06",
            "query": (
                "Hiring a Python backend developer with experience in Django, "
                "Flask, REST APIs, and PostgreSQL."
            ),
            "expected_categories": ["Python developer", "Pythondeveloper"],
            "rationale": "Python developer — should NOT retrieve generic Data Science CVs.",
        },
        {
            "id": "RA-07",
            "query": (
                "We are looking for a Civil Engineer with experience in structural "
                "design, AutoCAD, project management, and site supervision."
            ),
            "expected_categories": ["Civil engineer", "Civilengineer"],
            "rationale": "Engineering sub-domain; must not confuse with Mechanical or Electrical.",
        },
        {
            "id": "RA-08",
            "query": (
                "Need an HR Manager experienced in talent acquisition, employee "
                "relations, performance management, and labor law compliance."
            ),
            "expected_categories": ["Human resources", "Hr"],
            "rationale": "HR query — two category variants exist (Human resources / Hr).",
        },
        {
            "id": "RA-09",
            "query": (
                "Hiring a Java Developer with experience in Spring Boot, "
                "Microservices, Hibernate, and RESTful API development."
            ),
            "expected_categories": ["Java developer", "Javadeveloper"],
            "rationale": "Java vs other developer categories (React, Python, SAP) is a key distinction.",
        },
        {
            "id": "RA-10",
            "query": (
                "Looking for a Banking professional with expertise in trade finance, "
                "credit analysis, and relationship management."
            ),
            "expected_categories": ["Banking"],
            "rationale": "Financial services — Banking vs Accountant vs Finance disambiguation.",
        },
    ]

    # Attach real CV snippets that SHOULD match each case
    for case in cases:
        for cat in case["expected_categories"]:
            snippets = _sample_cv_snippets(df, cat, n=2)
            if snippets:
                case["ground_truth_cv_samples"] = snippets
                break

    return cases


# ──────────────────────────────────────────────────────────────────────
# 2. Edge-Case / Failure Test Cases
# ──────────────────────────────────────────────────────────────────────

def build_edge_case_cases() -> list[dict]:
    """
    Queries designed to expose system weaknesses:
    - ambiguous wording
    - off-domain topics
    - very short queries
    - contradictory requirements
    """
    return [
        {
            "id": "EC-01",
            "query": "developer",
            "expected_behavior": "ambiguous_retrieval",
            "description": (
                "Single-word query is highly ambiguous — could match React, Python, "
                "Java, SAP, SQL, ETL, or Dotnet developers. System should either "
                "return mixed results or flag low confidence."
            ),
            "failure_type": "ambiguity",
        },
        {
            "id": "EC-02",
            "query": (
                "Looking for a quantum computing researcher with publications "
                "in topological qubits and experience with IBM Qiskit."
            ),
            "expected_behavior": "no_relevant_match",
            "description": (
                "Quantum computing is NOT a category in the dataset. The system "
                "should return low-relevance results or admit no strong match."
            ),
            "failure_type": "off_domain",
        },
        {
            "id": "EC-03",
            "query": "",
            "expected_behavior": "error_or_empty",
            "description": (
                "Empty query — the system should return an error or empty results, "
                "not hallucinate a job description."
            ),
            "failure_type": "empty_input",
        },
        {
            "id": "EC-04",
            "query": "good person who works hard and is nice",
            "expected_behavior": "no_relevant_match",
            "description": (
                "Personality-only query with no technical skills or domain. "
                "System has no meaningful signal to match against."
            ),
            "failure_type": "vague_query",
        },
        {
            "id": "EC-05",
            "query": (
                "Need a chef who is also a certified public accountant and "
                "has experience in aviation engineering."
            ),
            "expected_behavior": "confused_retrieval",
            "description": (
                "Contradictory multi-domain query. No single CV will match all "
                "three domains. System may retrieve random mix or hallucinate."
            ),
            "failure_type": "contradictory",
        },
        {
            "id": "EC-06",
            "query": "مطلوب مهندس برمجيات لديه خبرة في تطوير تطبيقات الويب",
            "expected_behavior": "poor_or_no_match",
            "description": (
                "Arabic query ('Software engineer needed with web development "
                "experience'). The CV corpus is English-only so the embedding "
                "model may fail to bridge the language gap."
            ),
            "failure_type": "language_mismatch",
        },
        {
            "id": "EC-07",
            "query": "a]b[c{d}e<f>g!@#$%^&*()",
            "expected_behavior": "error_or_empty",
            "description": (
                "Special characters / garbage input — should be handled gracefully "
                "rather than crashing."
            ),
            "failure_type": "malformed_input",
        },
    ]


# ──────────────────────────────────────────────────────────────────────
# 3. Cross-Category Confusion Cases
# ──────────────────────────────────────────────────────────────────────

def build_cross_category_cases() -> list[dict]:
    """
    Pairs of categories that share significant vocabulary.  The system
    should still prefer the correct category over the confusing one.
    """
    return [
        {
            "id": "CC-01",
            "query": (
                "Hiring an Electrical Engineer with experience in circuit design, "
                "power systems, and PLC programming."
            ),
            "expected_category": "Electrical engineering",
            "confusing_categories": ["Mechanicalengineer", "Mechanical engineer"],
            "overlap_reason": "Both are engineering fields sharing project management and CAD vocabulary.",
        },
        {
            "id": "CC-02",
            "query": (
                "Need an ETL Developer experienced with SSIS, Informatica, "
                "data warehousing, and SQL Server."
            ),
            "expected_category": "Etl developer",
            "confusing_categories": ["Sql developer", "Database", "Sql"],
            "overlap_reason": "ETL, SQL, and Database roles all share SQL and data pipeline terminology.",
        },
        {
            "id": "CC-03",
            "query": (
                "Business Analyst needed — requirements gathering, stakeholder "
                "management, JIRA, and Agile methodology."
            ),
            "expected_category": "Business analyst",
            "confusing_categories": ["Consultant", "Management", "Consult"],
            "overlap_reason": "Business Analysts and Consultants share analysis and strategy vocabulary.",
        },
        {
            "id": "CC-04",
            "query": (
                "Hiring a Graphic Designer proficient in Photoshop, Illustrator, "
                "Figma, and brand identity design."
            ),
            "expected_category": "Designer",
            "confusing_categories": ["Web designing", "Webdesigning", "Digital media", "Digital"],
            "overlap_reason": "Design roles share creative-tool vocabulary (Adobe suite, UI/UX).",
        },
        {
            "id": "CC-05",
            "query": (
                "Public Relations Specialist needed for media outreach, press "
                "releases, and corporate communications."
            ),
            "expected_category": "Public relations",
            "confusing_categories": ["Public", "Digital media", "Digital-media"],
            "overlap_reason": "PR and Digital Media both deal with communications and media.",
        },
    ]


# ──────────────────────────────────────────────────────────────────────
# 4. Hallucination-Detection Cases
# ──────────────────────────────────────────────────────────────────────

def build_hallucination_cases(df: pd.DataFrame) -> list[dict]:
    """
    Each case provides a job description *and* the exact CV context text
    that the retriever should supply.  The evaluator can then check whether
    the LLM's output refers ONLY to facts in the context or invents data.
    """
    cases = []
    # Pick 5 diverse categories
    categories = ["Accountant", "Data science", "Civil engineer", "Designer", "Banking"]

    for i, cat in enumerate(categories, start=1):
        sub = df[df["category"] == cat]
        if sub.empty:
            continue
        sample = sub.sample(n=1, random_state=i)
        cv_text = str(sample.iloc[0]["text"])[:600]
        filename = sample.iloc[0].get("filename", "unknown")

        cases.append({
            "id": f"HD-{i:02d}",
            "query": f"Find the best {cat.lower()} candidate.",
            "retrieved_context": cv_text,
            "context_source_file": filename,
            "checks": [
                "LLM must NOT invent skills not present in retrieved_context.",
                "LLM must NOT fabricate a candidate name if none appears in context.",
                "LLM must NOT cite specific years of experience unless context states them.",
                "LLM must NOT reference companies not mentioned in context.",
            ],
            "description": (
                f"Provide the retrieved_context as the ONLY input to the LLM. "
                f"Any facts in the LLM output not traceable to this context "
                f"constitute a hallucination."
            ),
        })

    return cases


# ──────────────────────────────────────────────────────────────────────
# 5. Ranking-Quality Cases
# ──────────────────────────────────────────────────────────────────────

def build_ranking_cases(df: pd.DataFrame) -> list[dict]:
    """
    For each case we provide a query and manually specify which
    category should be ranked #1, #2, #3 if multiple categories
    are partially relevant.
    """
    return [
        {
            "id": "RQ-01",
            "query": (
                "Full-stack developer with React front-end and Python Django "
                "back-end experience."
            ),
            "expected_ranking": [
                {"rank": 1, "category": "React developer", "reason": "React is the primary skill mentioned."},
                {"rank": 2, "category": "Python developer", "reason": "Django back-end is secondary."},
                {"rank": 3, "category": "Web designing", "reason": "Web design is tangentially related."},
            ],
            "description": (
                "Query mentions both React and Python. Ideal retrieval should "
                "surface React CVs first, then Python, then generic web design."
            ),
        },
        {
            "id": "RQ-02",
            "query": (
                "Data analyst with SQL expertise and experience building "
                "ETL pipelines."
            ),
            "expected_ranking": [
                {"rank": 1, "category": "Data science", "reason": "Data analyst closest to data science."},
                {"rank": 2, "category": "Etl developer", "reason": "ETL pipeline expertise."},
                {"rank": 3, "category": "Sql developer", "reason": "SQL is a tool, not the core role."},
            ],
            "description": (
                "Overlapping skills across Data Science, ETL, and SQL categories. "
                "Ranking reveals retrieval precision."
            ),
        },
        {
            "id": "RQ-03",
            "query": (
                "Operations Manager for a manufacturing facility — supply chain, "
                "lean manufacturing, Six Sigma, team leadership."
            ),
            "expected_ranking": [
                {"rank": 1, "category": "Operations manager", "reason": "Direct role match."},
                {"rank": 2, "category": "Management", "reason": "General management overlap."},
                {"rank": 3, "category": "Mechanical engineer", "reason": "Manufacturing context overlap."},
            ],
            "description": (
                "Tests whether the system correctly prefers the exact role category "
                "over broader management or engineering categories."
            ),
        },
    ]


# ──────────────────────────────────────────────────────────────────────
# Assembler
# ──────────────────────────────────────────────────────────────────────

def generate_ground_truth(csv_path: str, output_path: str) -> dict:
    """Build the full ground-truth dataset and write to JSON."""
    print(f"📄 Loading CV dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"   → {len(df):,} rows | {df['category'].nunique()} categories\n")

    gt = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_csv": str(csv_path),
            "total_cvs": len(df),
            "total_categories": int(df["category"].nunique()),
            "categories": sorted(df["category"].unique().tolist()),
            "description": (
                "Ground truth dataset for evaluating the ROMI RAG CV-Matching "
                "system.  Covers retrieval accuracy, edge cases, cross-category "
                "confusion, hallucination detection, and ranking quality."
            ),
        },
        "evaluation_dimensions": {
            "retrieval_accuracy": {
                "description": (
                    "Does the system retrieve CVs from the correct professional "
                    "category when given a specific job description?"
                ),
                "how_to_evaluate": (
                    "For each case, submit the 'query' to the /search endpoint "
                    "and check whether the returned CV filenames / metadata "
                    "belong to one of the 'expected_categories'."
                ),
                "metric": "Precision@K — fraction of top-K results in expected category.",
                "test_cases": build_retrieval_accuracy_cases(df),
            },
            "edge_cases": {
                "description": (
                    "How does the system handle ambiguous, empty, off-domain, "
                    "or malformed queries?"
                ),
                "how_to_evaluate": (
                    "Submit each query and verify the 'expected_behavior'. "
                    "Record whether the system crashed, hallucinated, or "
                    "gracefully handled the failure."
                ),
                "metric": "Pass / Fail per case.  Document failure modes.",
                "test_cases": build_edge_case_cases(),
            },
            "cross_category_confusion": {
                "description": (
                    "Can the system distinguish between categories that share "
                    "overlapping domain vocabulary?"
                ),
                "how_to_evaluate": (
                    "Submit each query and check that the top-1 result belongs "
                    "to 'expected_category', not any of the 'confusing_categories'."
                ),
                "metric": "Confusion-free rate — % of cases where top-1 is correct.",
                "test_cases": build_cross_category_cases(),
            },
            "hallucination_detection": {
                "description": (
                    "Does the LLM fabricate information not present in the "
                    "retrieved context chunks?"
                ),
                "how_to_evaluate": (
                    "Feed the 'retrieved_context' as context_docs to the LLM "
                    "evaluate_candidates prompt.  Manually verify every claim "
                    "in the LLM output against the context using the 'checks' list."
                ),
                "metric": "Hallucination rate — fraction of outputs containing fabricated facts.",
                "test_cases": build_hallucination_cases(df),
            },
            "ranking_quality": {
                "description": (
                    "When multiple categories are partially relevant, does the "
                    "system rank the most relevant one first?"
                ),
                "how_to_evaluate": (
                    "Submit each query with top_n=10 and check whether the "
                    "category distribution of results matches 'expected_ranking'."
                ),
                "metric": "NDCG or manual rank correlation.",
                "test_cases": build_ranking_cases(df),
            },
        },
        "summary": {
            "total_test_cases": 0,  # filled below
            "per_dimension": {},
        },
    }

    # Fill summary counts
    total = 0
    for dim_name, dim_data in gt["evaluation_dimensions"].items():
        count = len(dim_data["test_cases"])
        gt["summary"]["per_dimension"][dim_name] = count
        total += count
    gt["summary"]["total_test_cases"] = total

    # Write
    output = Path(output_path)
    output.write_text(json.dumps(gt, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Ground truth written to: {output.resolve()}")
    print(f"   → {total} test cases across {len(gt['evaluation_dimensions'])} dimensions\n")

    # Print summary table
    print(f"{'Dimension':<30} | {'# Cases':>8}")
    print("-" * 42)
    for dim, count in gt["summary"]["per_dimension"].items():
        print(f"{dim:<30} | {count:>8}")
    print("-" * 42)
    print(f"{'TOTAL':<30} | {total:>8}")

    return gt


# ──────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate ground-truth evaluation data for the ROMI RAG system."
    )
    parser.add_argument(
        "--csv",
        default="final_24k_resumes_master.csv",
        help="Path to the master CV CSV file (default: final_24k_resumes_master.csv)",
    )
    parser.add_argument(
        "--output",
        default="ground_truth.json",
        help="Path for the output JSON file (default: ground_truth.json)",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path.resolve()}", file=sys.stderr)
        sys.exit(1)

    generate_ground_truth(str(csv_path), args.output)


if __name__ == "__main__":
    main()
