from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

from .schemas import EvaluationResult


SUMMARY_FIELDS = [
    "domain",
    "system_id",
    "questions",
    "answer_correctness",
    "evidence_recall",
    "context_precision",
    "citation_validity",
    "query_wall_time_ms",
    "query_wall_time_p50_ms",
    "query_wall_time_p95_ms",
    "index_wall_time_ms",
    "retrieved_token_count",
    "estimated_cost",
    "failure_rate",
]

CATEGORY_FIELDS = [
    "domain",
    "category",
    "system_id",
    "questions",
    "answer_correctness",
    "evidence_recall",
    "context_precision",
    "failure_rate",
]

RECOMMENDATION_FIELDS = [
    "domain",
    "system_id",
    "recommendation_score",
    "quality_score",
    "efficiency_score",
    "stability_score",
    "role",
]

FAILURE_FIELDS = ["domain", "system_id", "failure_type", "count"]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_results(path: Path, results: list[EvaluationResult]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].model_dump().keys()))
        writer.writeheader()
        for result in results:
            writer.writerow(result.model_dump())


def aggregate(results: list[EvaluationResult]) -> list[dict]:
    grouped: dict[tuple[str, str], list[EvaluationResult]] = defaultdict(list)
    for result in results:
        grouped[(result.domain, result.system_id)].append(result)
    rows = []
    for (domain, system_id), items in sorted(grouped.items()):
        rows.append(
            {
                "domain": domain,
                "system_id": system_id,
                "questions": len(items),
                "answer_correctness": avg(items, "answer_correctness"),
                "evidence_recall": avg(items, "evidence_recall"),
                "context_precision": avg(items, "context_precision"),
                "citation_validity": avg(items, "citation_validity"),
                "query_wall_time_ms": avg(items, "query_wall_time_ms"),
                "query_wall_time_p50_ms": percentile(
                    [float(item.query_wall_time_ms) for item in items], 50
                ),
                "query_wall_time_p95_ms": percentile(
                    [float(item.query_wall_time_ms) for item in items], 95
                ),
                "index_wall_time_ms": avg(items, "index_wall_time_ms"),
                "retrieved_token_count": avg(items, "retrieved_token_count"),
                "estimated_cost": avg(items, "estimated_cost"),
                "failure_rate": sum(1 for item in items if item.failure_type) / len(items),
            }
        )
    return rows


def aggregate_by_category(results: list[EvaluationResult]) -> list[dict]:
    grouped: dict[tuple[str, str, str], list[EvaluationResult]] = defaultdict(list)
    for result in results:
        grouped[(result.domain, result.category, result.system_id)].append(result)
    rows = []
    for (domain, category, system_id), items in sorted(grouped.items()):
        rows.append(
            {
                "domain": domain,
                "category": category,
                "system_id": system_id,
                "questions": len(items),
                "answer_correctness": avg(items, "answer_correctness"),
                "evidence_recall": avg(items, "evidence_recall"),
                "context_precision": avg(items, "context_precision"),
                "failure_rate": sum(1 for item in items if item.failure_type) / len(items),
            }
        )
    return rows


def build_recommendations(summary_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in summary_rows:
        grouped[row["domain"]].append(row)

    recommendations = []
    for domain, rows in grouped.items():
        max_latency = max(float(row["query_wall_time_ms"]) for row in rows) or 1.0
        max_cost = max(float(row["estimated_cost"]) for row in rows) or 1.0
        max_tokens = max(float(row["retrieved_token_count"]) for row in rows) or 1.0
        for row in rows:
            quality = (
                float(row["answer_correctness"]) * 0.45
                + float(row["evidence_recall"]) * 0.30
                + float(row["citation_validity"]) * 0.15
                + float(row["context_precision"]) * 0.10
            )
            latency_penalty = float(row["query_wall_time_ms"]) / max_latency
            cost_penalty = float(row["estimated_cost"]) / max_cost
            token_penalty = float(row["retrieved_token_count"]) / max_tokens
            efficiency = max(0.0, 1.0 - (0.40 * latency_penalty + 0.30 * cost_penalty + 0.30 * token_penalty))
            stability = 1.0 - float(row["failure_rate"])
            score = (quality * 0.65) + (efficiency * 0.20) + (stability * 0.15)
            recommendations.append(
                {
                    "domain": domain,
                    "system_id": row["system_id"],
                    "recommendation_score": score,
                    "quality_score": quality,
                    "efficiency_score": efficiency,
                    "stability_score": stability,
                    "role": recommendation_role(row["system_id"]),
                }
            )
    return sorted(
        recommendations,
        key=lambda row: (row["domain"], -float(row["recommendation_score"]), row["system_id"]),
    )


def failure_summary(results: list[EvaluationResult]) -> list[dict]:
    grouped: dict[tuple[str, str, str], int] = defaultdict(int)
    for result in results:
        if result.failure_type:
            grouped[(result.domain, result.system_id, result.failure_type)] += 1
    return [
        {
            "domain": domain,
            "system_id": system_id,
            "failure_type": failure_type,
            "count": count,
        }
        for (domain, system_id, failure_type), count in sorted(grouped.items())
    ]


def write_summary_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_category_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CATEGORY_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_recommendations_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=RECOMMENDATION_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_failure_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FAILURE_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_markdown_report(
    path: Path,
    summary_rows: list[dict],
    category_rows: list[dict],
    recommendation_rows: list[dict],
    failure_rows: list[dict],
    run_id: str,
    warnings: list[str] | None = None,
) -> None:
    lines = [
        f"# RAG Benchmark Report: {run_id}",
        "",
        "This report compares RAG strategies for practical operations decisions.",
        "Scores are generated from local fixture datasets and deterministic extractive answering.",
        "",
        "## Scorecard",
        "",
        "| Domain | System | Answer | Evidence Recall | Context Precision | Citation | Latency ms | Cost | Failure |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(
            "| {domain} | {system_id} | {answer_correctness:.3f} | {evidence_recall:.3f} | "
            "{context_precision:.3f} | {citation_validity:.3f} | {query_wall_time_ms:.2f} | "
            "{estimated_cost:.6f} | {failure_rate:.3f} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Recommendation Ranking",
            "",
            "Recommendation score combines quality, efficiency, and stability. It is a decision aid, not a universal truth.",
            "",
            "| Domain | Rank | System | Recommendation | Quality | Efficiency | Stability | Role |",
            "|---|---:|---|---:|---:|---:|---:|---|",
        ]
    )
    rank_by_domain: dict[str, int] = defaultdict(int)
    for row in recommendation_rows:
        rank_by_domain[row["domain"]] += 1
        lines.append(
            "| {domain} | {rank} | `{system_id}` | {recommendation_score:.3f} | "
            "{quality_score:.3f} | {efficiency_score:.3f} | {stability_score:.3f} | {role} |".format(
                rank=rank_by_domain[row["domain"]], **row
            )
        )
    lines.extend(
        [
            "",
            "## Failure Breakdown",
            "",
        ]
    )
    if failure_rows:
        lines.extend(
            [
                "| Domain | System | Failure Type | Count |",
                "|---|---|---|---:|",
            ]
        )
        for row in failure_rows:
            lines.append(
                "| {domain} | `{system_id}` | {failure_type} | {count} |".format(**row)
            )
    else:
        lines.append("No failures were recorded in this run.")
    lines.extend(
        [
            "",
            "## Category View",
            "",
            "| Domain | Category | Best System | Best Answer | Hardest System Failure |",
            "|---|---|---:|---:|---:|",
        ]
    )
    category_keys = sorted({(row["domain"], row["category"]) for row in category_rows})
    for domain, category in category_keys:
        rows = [row for row in category_rows if row["domain"] == domain and row["category"] == category]
        best = max(rows, key=lambda row: (row["answer_correctness"], row["evidence_recall"]))
        hardest = max(rows, key=lambda row: row["failure_rate"])
        lines.append(
            "| {domain} | {category} | `{best_system}` | {best_answer:.3f} | "
            "`{hard_system}` {hard_failure:.3f} |".format(
                domain=domain,
                category=category,
                best_system=best["system_id"],
                best_answer=best["answer_correctness"],
                hard_system=hardest["system_id"],
                hard_failure=hardest["failure_rate"],
            )
        )
    lines.extend(["", "## Operational Guidance", ""])
    for domain in sorted({row["domain"] for row in summary_rows}):
        domain_rows = [row for row in summary_rows if row["domain"] == domain]
        best_quality = max(domain_rows, key=lambda row: (row["answer_correctness"], row["evidence_recall"]))
        cheapest = min(domain_rows, key=lambda row: row["estimated_cost"])
        fastest = min(domain_rows, key=lambda row: row["query_wall_time_ms"])
        recommended = next(row for row in recommendation_rows if row["domain"] == domain)
        lines.extend(
            [
                f"### {domain}",
                "",
                f"- Recommended default: `{recommended['system_id']}` "
                f"(score={recommended['recommendation_score']:.3f}; {recommended['role']}).",
                f"- Best quality: `{best_quality['system_id']}` "
                f"(answer={best_quality['answer_correctness']:.3f}, "
                f"evidence={best_quality['evidence_recall']:.3f}).",
                f"- Lowest query cost: `{cheapest['system_id']}` "
                f"(cost={cheapest['estimated_cost']:.6f}).",
                f"- Fastest query path: `{fastest['system_id']}` "
                f"(latency={fastest['query_wall_time_ms']:.2f} ms).",
                "",
            ]
        )
    if warnings:
        lines.extend(["", "## Interpretation Warnings", ""])
        for warning in warnings:
            lines.append(f"- {warning}")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `pageindex-oss` uses a local PageIndex-style tree adapter only; hosted PageIndex APIs are excluded.",
            "- The current answerer is deterministic so retrieval failures are visible and reproducible.",
            "- Add real corpora and human-graded questions before treating numbers as production proof.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def avg(items: list[EvaluationResult], field: str) -> float:
    return mean(float(getattr(item, field)) for item in items)


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * (pct / 100)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def recommendation_role(system_id: str) -> str:
    roles = {
        "bm25": "fast exact-term baseline",
        "dense-vector": "semantic similarity baseline",
        "hybrid": "balanced default for mixed queries",
        "hybrid-rerank": "quality-first retrieval when rerank latency is acceptable",
        "parent-child": "small-chunk search with broader answer context",
        "pageindex-oss": "structured long-document and multi-section navigation",
    }
    return roles.get(system_id, "candidate RAG strategy")
