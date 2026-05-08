from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean

from .production import PRODUCTION_READINESS_FIELDS
from .schemas import EvaluationResult


SUMMARY_FIELDS = [
    "track",
    "domain",
    "system_id",
    "rag_method",
    "embedding_model",
    "reranker_model",
    "generator_model",
    "judge_model",
    "questions",
    "answer_correctness",
    "gold_answer_correctness",
    "evidence_recall",
    "context_precision",
    "citation_validity",
    "judge_human_agreement_proxy",
    "judge_false_accept_risk",
    "judge_false_reject_risk",
    "query_wall_time_ms",
    "query_wall_time_p50_ms",
    "query_wall_time_p95_ms",
    "generator_wall_time_ms",
    "generator_wall_time_p95_ms",
    "judge_wall_time_ms",
    "judge_wall_time_p95_ms",
    "index_wall_time_ms",
    "retrieved_token_count",
    "generator_input_tokens",
    "generator_output_tokens",
    "judge_input_tokens",
    "judge_estimated_cost",
    "estimated_cost",
    "failure_rate",
]

CATEGORY_FIELDS = [
    "track",
    "domain",
    "category",
    "system_id",
    "rag_method",
    "embedding_model",
    "generator_model",
    "judge_model",
    "questions",
    "answer_correctness",
    "gold_answer_correctness",
    "evidence_recall",
    "context_precision",
    "failure_rate",
]

RECOMMENDATION_FIELDS = [
    "track",
    "domain",
    "system_id",
    "rag_method",
    "embedding_model",
    "generator_model",
    "judge_model",
    "answer_correctness",
    "gold_answer_correctness",
    "evidence_recall",
    "context_precision",
    "failure_rate",
    "recommendation_score",
    "quality_score",
    "efficiency_score",
    "stability_score",
    "role",
]

AXIS_LEADERBOARD_FIELDS = [
    "domain",
    "axis",
    "candidate",
    "variants",
    "answer_correctness",
    "evidence_recall",
    "context_precision",
    "failure_rate",
    "estimated_cost",
    "recommendation_score",
    "reading",
]

JUDGE_AUDIT_FIELDS = [
    "domain",
    "judge_model",
    "variants",
    "judge_score",
    "answer_correctness",
    "gold_answer_correctness",
    "gold_delta",
    "human_agreement_proxy",
    "false_accept_risk",
    "false_reject_risk",
    "judge_wall_time_ms",
    "estimated_cost",
    "reading",
]

FAILURE_FIELDS = [
    "track",
    "domain",
    "system_id",
    "embedding_model",
    "generator_model",
    "judge_model",
    "failure_type",
    "count",
]


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
    grouped: dict[tuple[str, str, str, str, str, str, str, str], list[EvaluationResult]] = defaultdict(list)
    for result in results:
        grouped[
            (
                result.track,
                result.domain,
                result.system_id,
                result.rag_method,
                result.embedding_model,
                result.reranker_model,
                result.generator_model,
                result.judge_model,
            )
        ].append(result)
    rows = []
    for (
        track,
        domain,
        system_id,
        rag_method,
        embedding_model,
        reranker_model,
        generator_model,
        judge_model,
    ), items in sorted(grouped.items()):
        rows.append(
            {
                "track": track,
                "domain": domain,
                "system_id": system_id,
                "rag_method": rag_method,
                "embedding_model": embedding_model,
                "reranker_model": reranker_model,
                "generator_model": generator_model,
                "judge_model": judge_model,
                "questions": len(items),
                "answer_correctness": avg(items, "answer_correctness"),
                "gold_answer_correctness": avg(items, "gold_answer_correctness"),
                "evidence_recall": avg(items, "evidence_recall"),
                "context_precision": avg(items, "context_precision"),
                "citation_validity": avg(items, "citation_validity"),
                "judge_human_agreement_proxy": avg(items, "judge_human_agreement_proxy"),
                "judge_false_accept_risk": avg(items, "judge_false_accept_risk"),
                "judge_false_reject_risk": avg(items, "judge_false_reject_risk"),
                "query_wall_time_ms": avg(items, "query_wall_time_ms"),
                "query_wall_time_p50_ms": percentile(
                    [float(item.query_wall_time_ms) for item in items], 50
                ),
                "query_wall_time_p95_ms": percentile(
                    [float(item.query_wall_time_ms) for item in items], 95
                ),
                "generator_wall_time_ms": avg(items, "generator_wall_time_ms"),
                "generator_wall_time_p95_ms": percentile(
                    [float(item.generator_wall_time_ms) for item in items], 95
                ),
                "judge_wall_time_ms": avg(items, "judge_wall_time_ms"),
                "judge_wall_time_p95_ms": percentile(
                    [float(item.judge_wall_time_ms) for item in items], 95
                ),
                "index_wall_time_ms": avg(items, "index_wall_time_ms"),
                "retrieved_token_count": avg(items, "retrieved_token_count"),
                "generator_input_tokens": avg(items, "generator_input_tokens"),
                "generator_output_tokens": avg(items, "generator_output_tokens"),
                "judge_input_tokens": avg(items, "judge_input_tokens"),
                "judge_estimated_cost": avg(items, "judge_estimated_cost"),
                "estimated_cost": avg(items, "estimated_cost"),
                "failure_rate": sum(1 for item in items if item.failure_type) / len(items),
            }
        )
    return rows


def aggregate_by_category(results: list[EvaluationResult]) -> list[dict]:
    grouped: dict[tuple[str, str, str, str, str, str, str], list[EvaluationResult]] = defaultdict(list)
    for result in results:
        grouped[
            (
                result.track,
                result.domain,
                result.category,
                result.system_id,
                result.embedding_model,
                result.generator_model,
                result.judge_model,
            )
        ].append(result)
    rows = []
    for (track, domain, category, system_id, embedding_model, generator_model, judge_model), items in sorted(
        grouped.items()
    ):
        rows.append(
            {
                "track": track,
                "domain": domain,
                "category": category,
                "system_id": system_id,
                "rag_method": items[0].rag_method,
                "embedding_model": embedding_model,
                "generator_model": generator_model,
                "judge_model": judge_model,
                "questions": len(items),
                "answer_correctness": avg(items, "answer_correctness"),
                "gold_answer_correctness": avg(items, "gold_answer_correctness"),
                "evidence_recall": avg(items, "evidence_recall"),
                "context_precision": avg(items, "context_precision"),
                "failure_rate": sum(1 for item in items if item.failure_type) / len(items),
            }
        )
    return rows


def build_recommendations(summary_rows: list[dict]) -> list[dict]:
    candidate_rows = [
        row
        for row in summary_rows
        if row.get("track") == "end-to-end" and row.get("judge_model") == "exact-match-gold"
    ]
    if not candidate_rows:
        candidate_rows = [row for row in summary_rows if row.get("track") == "end-to-end"] or summary_rows

    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in candidate_rows:
        grouped[(row["track"], row["domain"])].append(row)

    recommendations = []
    for (track, domain), rows in grouped.items():
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
                    "track": track,
                    "domain": domain,
                    "system_id": row["system_id"],
                    "rag_method": row["rag_method"],
                    "embedding_model": row["embedding_model"],
                    "generator_model": row["generator_model"],
                    "judge_model": row["judge_model"],
                    "answer_correctness": row["answer_correctness"],
                    "gold_answer_correctness": row["gold_answer_correctness"],
                    "evidence_recall": row["evidence_recall"],
                    "context_precision": row["context_precision"],
                    "failure_rate": row["failure_rate"],
                    "recommendation_score": score,
                    "quality_score": quality,
                    "efficiency_score": efficiency,
                    "stability_score": stability,
                    "role": recommendation_role(row["rag_method"]),
                }
            )
    return sorted(
        recommendations,
        key=lambda row: (
            row["track"],
            row["domain"],
            -float(row["recommendation_score"]),
            row["system_id"],
        ),
    )


def failure_summary(results: list[EvaluationResult]) -> list[dict]:
    grouped: dict[tuple[str, str, str, str, str, str, str], int] = defaultdict(int)
    for result in results:
        if result.failure_type:
            grouped[
                (
                    result.track,
                    result.domain,
                    result.system_id,
                    result.embedding_model,
                    result.generator_model,
                    result.judge_model,
                    result.failure_type,
                )
            ] += 1
    return [
        {
            "track": track,
            "domain": domain,
            "system_id": system_id,
            "embedding_model": embedding_model,
            "generator_model": generator_model,
            "judge_model": judge_model,
            "failure_type": failure_type,
            "count": count,
        }
        for (track, domain, system_id, embedding_model, generator_model, judge_model, failure_type), count in sorted(
            grouped.items()
        )
    ]


def build_axis_leaderboard(summary_rows: list[dict]) -> list[dict]:
    canonical = [
        row
        for row in summary_rows
        if row.get("track") == "end-to-end" and row.get("judge_model") == "exact-match-gold"
    ]
    rows = []
    for domain in sorted({row["domain"] for row in canonical}):
        domain_rows = [row for row in canonical if row["domain"] == domain]
        rows.extend(axis_rows(domain_rows, domain, "rag_method", "best RAG system"))
        rows.extend(
            axis_rows(
                [row for row in domain_rows if row["embedding_model"] != "none"],
                domain,
                "embedding_model",
                "best embedding model",
            )
        )
        rows.extend(axis_rows(domain_rows, domain, "generator_model", "best generator model"))
    return sorted(rows, key=lambda row: (row["domain"], row["axis"], -row["recommendation_score"]))


def axis_rows(rows: list[dict], domain: str, field: str, reading: str) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row[field]].append(row)
    axis = field.replace("_model", "").replace("_method", "")
    output = []
    for candidate, items in grouped.items():
        output.append(
            {
                "domain": domain,
                "axis": axis,
                "candidate": candidate,
                "variants": len(items),
                "answer_correctness": avg_rows(items, "answer_correctness"),
                "evidence_recall": avg_rows(items, "evidence_recall"),
                "context_precision": avg_rows(items, "context_precision"),
                "failure_rate": avg_rows(items, "failure_rate"),
                "estimated_cost": avg_rows(items, "estimated_cost"),
                "recommendation_score": axis_recommendation_score(items),
                "reading": reading,
            }
        )
    return output


def build_judge_audit(summary_rows: list[dict]) -> list[dict]:
    rows = [row for row in summary_rows if row.get("track") == "end-to-end"]
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["domain"], row["judge_model"])].append(row)
    audits = []
    for (domain, judge_model), items in sorted(grouped.items()):
        answer_score = avg_rows(items, "answer_correctness")
        gold_score = avg_rows(items, "gold_answer_correctness")
        agreement = avg_rows(items, "judge_human_agreement_proxy")
        false_accept = avg_rows(items, "judge_false_accept_risk")
        false_reject = avg_rows(items, "judge_false_reject_risk")
        cost = avg_rows(items, "judge_estimated_cost")
        latency = avg_rows(items, "judge_wall_time_ms")
        judge_score = max(
            0.0,
            agreement
            - 0.40 * false_accept
            - 0.30 * false_reject
            - 0.10 * min(cost / max_judge_cost(items), 1.0)
            - 0.05 * min(latency / max_latency(items), 1.0),
        )
        audits.append(
            {
                "domain": domain,
                "judge_model": judge_model,
                "variants": len(items),
                "judge_score": judge_score,
                "answer_correctness": answer_score,
                "gold_answer_correctness": gold_score,
                "gold_delta": answer_score - gold_score,
                "human_agreement_proxy": agreement,
                "false_accept_risk": false_accept,
                "false_reject_risk": false_reject,
                "judge_wall_time_ms": latency,
                "estimated_cost": cost,
                "reading": judge_reading(judge_model),
            }
        )
    return sorted(audits, key=lambda row: (row["domain"], -row["judge_score"]))


def axis_recommendation_score(rows: list[dict]) -> float:
    quality = (
        avg_rows(rows, "answer_correctness") * 0.45
        + avg_rows(rows, "evidence_recall") * 0.30
        + avg_rows(rows, "context_precision") * 0.10
        + (1.0 - avg_rows(rows, "failure_rate")) * 0.15
    )
    cost_penalty = min(avg_rows(rows, "estimated_cost") / max_cost(rows), 1.0)
    return max(0.0, quality - 0.10 * cost_penalty)


def avg_rows(rows: list[dict], field: str) -> float:
    return mean(float(row[field]) for row in rows) if rows else 0.0


def max_cost(rows: list[dict]) -> float:
    return max((float(row["estimated_cost"]) for row in rows), default=1.0) or 1.0


def max_latency(rows: list[dict]) -> float:
    return max((float(row["judge_wall_time_ms"]) for row in rows), default=1.0) or 1.0


def max_judge_cost(rows: list[dict]) -> float:
    return max((float(row["judge_estimated_cost"]) for row in rows), default=1.0) or 1.0


def judge_reading(judge_model: str) -> str:
    readings = {
        "exact-match-gold": "canonical factual label evaluator; use for stack ranking",
        "llm-judge-balanced-proxy": "lenient LLM judge proxy; useful for paraphrase tolerance checks",
        "citation-strict-judge-proxy": "strict citation judge proxy; useful for compliance-style risk checks",
    }
    return readings.get(judge_model, "candidate judge profile")


def axis_reading_ko(axis: str) -> str:
    readings = {
        "rag": "RAG 방식 자체의 평균 운영 성능",
        "embedding": "임베딩 모델만 따로 봤을 때의 평균 검색 기여도",
        "generator": "생성 모델만 따로 봤을 때의 평균 답변 기여도",
    }
    return readings.get(axis, "후보 축별 성능")


def judge_reading_ko(judge_model: str) -> str:
    readings = {
        "exact-match-gold": "정규화된 gold label 기반 canonical evaluator",
        "llm-judge-balanced-proxy": "paraphrase 허용을 보는 관대한 LLM judge proxy",
        "citation-strict-judge-proxy": "citation을 엄격하게 보는 compliance형 judge proxy",
    }
    return readings.get(judge_model, "후보 judge profile")


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


def write_axis_leaderboard_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=AXIS_LEADERBOARD_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_judge_audit_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=JUDGE_AUDIT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_failure_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FAILURE_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_production_readiness_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PRODUCTION_READINESS_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_markdown_report(
    path: Path,
    summary_rows: list[dict],
    category_rows: list[dict],
    recommendation_rows: list[dict],
    axis_leaderboard_rows: list[dict],
    judge_audit_rows: list[dict],
    failure_rows: list[dict],
    run_id: str,
    warnings: list[str] | None = None,
    production_readiness_rows: list[dict] | None = None,
) -> None:
    score_rows = [
        row
        for row in summary_rows
        if row.get("track") == "end-to-end" and row.get("judge_model") == "exact-match-gold"
    ] or [row for row in summary_rows if row.get("track") == "end-to-end"] or summary_rows
    score_category_rows = [
        row
        for row in category_rows
        if row.get("track") == "end-to-end" and row.get("judge_model") == "exact-match-gold"
    ] or category_rows
    score_failure_rows = [
        row
        for row in failure_rows
        if row.get("track") == "end-to-end" and row.get("judge_model") == "exact-match-gold"
    ]
    lines = [
        f"# RAG Benchmark Report: {run_id}",
        "",
        "This report compares RAG strategies, embedding profiles, and generator profiles for practical operations decisions.",
        "Scores are generated from local fixture datasets and deterministic local profiles.",
        "",
        "## End-to-End Scorecard",
        "",
        "| Domain | RAG | Embedding | Generator | Answer | Evidence Recall | Context Precision | Citation | Latency ms | Cost | Failure |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in score_rows:
        lines.append(
            "| {domain} | {rag_method} | {embedding_model} | {generator_model} | "
            "{answer_correctness:.3f} | {evidence_recall:.3f} | "
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
            "## Production Readiness",
            "",
            "Suggested production gates: pass rate >= 0.80, answer correctness >= 0.80, evidence recall >= 0.85, citation validity >= 0.90, no-answer hallucination <= 0.05, and FinanceBench calculation pass rate >= 0.80 when applicable.",
            "",
            "| Source | Domain | System | Status | Readiness | Pass | Answer | Evidence | Citation | No-answer Hallucination | Calc Pass | Guidance |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for row in production_readiness_rows or []:
        lines.append(
            "| {source} | {domain} | `{system_id}` | {status} | {readiness_score:.3f} | "
            "{pass_rate:.3f} | {answer_correctness:.3f} | {evidence_recall:.3f} | "
            "{citation_validity:.3f} | {no_answer_hallucination_rate:.3f} | "
            "{calculation_pass_rate:.3f} | {guidance} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Best By Axis",
            "",
            "Product-stack ranking uses `exact-match-gold` as the canonical judge. Judge models are audited separately because they are measuring instruments, not deployable RAG components.",
            "",
            "| Domain | Axis | Rank | Candidate | Score | Answer | Evidence | Failure | Reading |",
            "|---|---|---:|---|---:|---:|---:|---:|---|",
        ]
    )
    rank_by_axis: dict[tuple[str, str], int] = defaultdict(int)
    for row in axis_leaderboard_rows:
        key = (row["domain"], row["axis"])
        rank_by_axis[key] += 1
        if rank_by_axis[key] > 3:
            continue
        lines.append(
            "| {domain} | {axis} | {rank} | `{candidate}` | {recommendation_score:.3f} | "
            "{answer_correctness:.3f} | {evidence_recall:.3f} | {failure_rate:.3f} | {reading} |".format(
                rank=rank_by_axis[key],
                **row,
            )
        )
    lines.extend(
        [
            "",
            "## Judge Model Audit",
            "",
            "| Domain | Rank | Judge | Judge Score | Gold Delta | Agreement Proxy | False Accept Risk | False Reject Risk | Reading |",
            "|---|---:|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    rank_by_judge_domain: dict[str, int] = defaultdict(int)
    for row in judge_audit_rows:
        rank_by_judge_domain[row["domain"]] += 1
        lines.append(
            "| {domain} | {rank} | `{judge_model}` | {judge_score:.3f} | {gold_delta:.3f} | "
            "{human_agreement_proxy:.3f} | {false_accept_risk:.3f} | {false_reject_risk:.3f} | {reading} |".format(
                rank=rank_by_judge_domain[row["domain"]],
                **row,
            )
        )
    lines.extend(
        [
            "",
            "## Failure Breakdown",
            "",
        ]
    )
    if score_failure_rows:
        lines.extend(
            [
                "| Domain | RAG | Embedding | Generator | Failure Type | Count |",
                "|---|---|---|---|---|---:|",
            ]
        )
        for row in score_failure_rows:
            lines.append(
                "| {domain} | `{system_id}` | {embedding_model} | {generator_model} | "
                "{failure_type} | {count} |".format(**row)
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
    category_keys = sorted({(row["domain"], row["category"]) for row in score_category_rows})
    for domain, category in category_keys:
        rows = [
            row
            for row in score_category_rows
            if row["domain"] == domain and row["category"] == category
        ]
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
    for domain in sorted({row["domain"] for row in score_rows}):
        domain_rows = [row for row in score_rows if row["domain"] == domain]
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
            "- Embedding and generator comparisons use deterministic local profiles by default; plug in real model adapters before claiming model-leaderboard results.",
            "- Judge comparisons are judge reliability audits. Do not rank product stacks with a judge until it is validated against human labels for the target domain.",
            "- `retrieval-only` isolates evidence retrieval, `generator-oracle` isolates answer generation with gold context, and `end-to-end` combines the full stack.",
            "- Add real corpora and human-graded questions before treating numbers as production proof.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_markdown_report_ko(
    path: Path,
    summary_rows: list[dict],
    category_rows: list[dict],
    recommendation_rows: list[dict],
    axis_leaderboard_rows: list[dict],
    judge_audit_rows: list[dict],
    failure_rows: list[dict],
    run_id: str,
    warnings: list[str] | None = None,
    production_readiness_rows: list[dict] | None = None,
) -> None:
    score_rows = [
        row
        for row in summary_rows
        if row.get("track") == "end-to-end" and row.get("judge_model") == "exact-match-gold"
    ] or [row for row in summary_rows if row.get("track") == "end-to-end"] or summary_rows
    score_category_rows = [
        row
        for row in category_rows
        if row.get("track") == "end-to-end" and row.get("judge_model") == "exact-match-gold"
    ] or category_rows
    score_failure_rows = [
        row
        for row in failure_rows
        if row.get("track") == "end-to-end" and row.get("judge_model") == "exact-match-gold"
    ]
    lines = [
        f"# RAG 벤치마크 리포트: {run_id}",
        "",
        "이 리포트는 실무 운영 의사결정을 위해 RAG 전략, 임베딩 프로필, 생성 LLM 프로필을 비교합니다.",
        "점수는 로컬 fixture 데이터셋과 결정론적 로컬 프로필로 생성됩니다.",
        "",
        "## End-to-End 점수표",
        "",
        "| 도메인 | RAG | 임베딩 | 생성 모델 | 답변 | Evidence Recall | Context Precision | Citation | 지연시간 ms | 비용 | 실패율 |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in score_rows:
        lines.append(
            "| {domain} | {rag_method} | {embedding_model} | {generator_model} | "
            "{answer_correctness:.3f} | {evidence_recall:.3f} | "
            "{context_precision:.3f} | {citation_validity:.3f} | {query_wall_time_ms:.2f} | "
            "{estimated_cost:.6f} | {failure_rate:.3f} |".format(**row)
        )

    lines.extend(
        [
            "",
            "## 추천 순위",
            "",
            "추천 점수는 품질, 효율, 안정성을 조합한 값입니다. 절대 정답이 아니라 의사결정 보조 지표입니다.",
            "",
            "| 도메인 | 순위 | 시스템 | 추천 점수 | 품질 | 효율 | 안정성 | 역할 |",
            "|---|---:|---|---:|---:|---:|---:|---|",
        ]
    )
    rank_by_domain: dict[str, int] = defaultdict(int)
    for row in recommendation_rows:
        rank_by_domain[row["domain"]] += 1
        row_ko = {
            **row,
            "rank": rank_by_domain[row["domain"]],
            "role": recommendation_role_ko(row["system_id"]),
        }
        lines.append(
            "| {domain} | {rank} | `{system_id}` | {recommendation_score:.3f} | "
            "{quality_score:.3f} | {efficiency_score:.3f} | {stability_score:.3f} | {role} |".format(**row_ko)
        )

    lines.extend(
        [
            "",
            "## 운영 적합성 판단",
            "",
            "제안 기준: 통과율 0.80 이상, 답변 정확도 0.80 이상, evidence recall 0.85 이상, citation validity 0.90 이상, no-answer hallucination 0.05 이하, FinanceBench 계산 문항은 해당 pass rate 0.80 이상입니다.",
            "",
            "| Source | 도메인 | 시스템 | 상태 | 적합성 | 통과율 | 답변 | Evidence | Citation | No-answer Hallucination | 계산 Pass | 안내 |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for row in production_readiness_rows or []:
        lines.append(
            "| {source} | {domain} | `{system_id}` | {status_ko} | {readiness_score:.3f} | "
            "{pass_rate:.3f} | {answer_correctness:.3f} | {evidence_recall:.3f} | "
            "{citation_validity:.3f} | {no_answer_hallucination_rate:.3f} | "
            "{calculation_pass_rate:.3f} | {guidance_ko} |".format(**row)
        )

    lines.extend(
        [
            "",
            "## 축별 최고 후보",
            "",
            "제품 stack ranking은 canonical judge인 `exact-match-gold` 기준입니다. Judge model은 배포 후보가 아니라 측정 도구이므로 별도 audit으로 봅니다.",
            "",
            "| 도메인 | 축 | 순위 | 후보 | 점수 | 답변 | Evidence | 실패율 | 해석 |",
            "|---|---|---:|---|---:|---:|---:|---:|---|",
        ]
    )
    rank_by_axis: dict[tuple[str, str], int] = defaultdict(int)
    for row in axis_leaderboard_rows:
        key = (row["domain"], row["axis"])
        rank_by_axis[key] += 1
        if rank_by_axis[key] > 3:
            continue
        row_ko = {**row, "reading": axis_reading_ko(row["axis"])}
        lines.append(
            "| {domain} | {axis} | {rank} | `{candidate}` | {recommendation_score:.3f} | "
            "{answer_correctness:.3f} | {evidence_recall:.3f} | {failure_rate:.3f} | {reading} |".format(
                rank=rank_by_axis[key],
                **row_ko,
            )
        )
    lines.extend(
        [
            "",
            "## 평가 모델 감사",
            "",
            "| 도메인 | 순위 | Judge | Judge Score | Gold Delta | Agreement Proxy | False Accept Risk | False Reject Risk | 해석 |",
            "|---|---:|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    rank_by_judge_domain: dict[str, int] = defaultdict(int)
    for row in judge_audit_rows:
        rank_by_judge_domain[row["domain"]] += 1
        row_ko = {**row, "reading": judge_reading_ko(row["judge_model"])}
        lines.append(
            "| {domain} | {rank} | `{judge_model}` | {judge_score:.3f} | {gold_delta:.3f} | "
            "{human_agreement_proxy:.3f} | {false_accept_risk:.3f} | {false_reject_risk:.3f} | {reading} |".format(
                rank=rank_by_judge_domain[row["domain"]],
                **row_ko,
            )
        )
    lines.extend(["", "## 실패 유형", ""])
    if score_failure_rows:
        lines.extend(
            [
                "| 도메인 | RAG | 임베딩 | 생성 모델 | 실패 유형 | 건수 |",
                "|---|---|---|---|---|---:|",
            ]
        )
        for row in score_failure_rows:
            row_ko = {**row, "failure_type": failure_type_ko(row["failure_type"])}
            lines.append(
                "| {domain} | `{system_id}` | {embedding_model} | {generator_model} | "
                "{failure_type} | {count} |".format(**row_ko)
            )
    else:
        lines.append("이번 실행에서는 실패가 기록되지 않았습니다.")

    lines.extend(
        [
            "",
            "## 카테고리별 보기",
            "",
            "| 도메인 | 카테고리 | 최고 시스템 | 최고 답변 점수 | 실패율이 가장 높은 시스템 |",
            "|---|---|---:|---:|---:|",
        ]
    )
    category_keys = sorted({(row["domain"], row["category"]) for row in score_category_rows})
    for domain, category in category_keys:
        rows = [
            row
            for row in score_category_rows
            if row["domain"] == domain and row["category"] == category
        ]
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

    lines.extend(["", "## 운영 가이드", ""])
    for domain in sorted({row["domain"] for row in score_rows}):
        domain_rows = [row for row in score_rows if row["domain"] == domain]
        best_quality = max(domain_rows, key=lambda row: (row["answer_correctness"], row["evidence_recall"]))
        cheapest = min(domain_rows, key=lambda row: row["estimated_cost"])
        fastest = min(domain_rows, key=lambda row: row["query_wall_time_ms"])
        recommended = next(row for row in recommendation_rows if row["domain"] == domain)
        lines.extend(
            [
                f"### {domain}",
                "",
                f"- 추천 기본값: `{recommended['system_id']}` "
                f"(score={recommended['recommendation_score']:.3f}; "
                f"{recommendation_role_ko(recommended['system_id'])}).",
                f"- 최고 품질: `{best_quality['system_id']}` "
                f"(answer={best_quality['answer_correctness']:.3f}, "
                f"evidence={best_quality['evidence_recall']:.3f}).",
                f"- 최저 query cost: `{cheapest['system_id']}` "
                f"(cost={cheapest['estimated_cost']:.6f}).",
                f"- 가장 빠른 query path: `{fastest['system_id']}` "
                f"(latency={fastest['query_wall_time_ms']:.2f} ms).",
                "",
            ]
        )

    if warnings:
        lines.extend(["", "## 해석 시 주의사항", ""])
        for warning in warnings:
            lines.append(f"- {warning_ko(warning)}")

    lines.extend(
        [
            "",
            "## 메모",
            "",
            "- `pageindex-oss`는 로컬 PageIndex-style tree adapter만 사용합니다. Hosted PageIndex API는 제외되어 있습니다.",
            "- 기본 임베딩/생성 비교는 결정론적 로컬 프로필입니다. 실제 모델 리더보드 성능으로 주장하려면 실제 모델 adapter를 연결해야 합니다.",
            "- Judge 비교는 평가 모델 신뢰성 audit입니다. 대상 도메인 human label로 검증하기 전에는 product stack ranking에 그대로 쓰면 안 됩니다.",
            "- `retrieval-only`는 검색 품질, `generator-oracle`은 gold context 기반 생성 능력, `end-to-end`는 전체 조합을 봅니다.",
            "- 실제 production 근거로 사용하려면 대표 corpus와 사람이 검수한 question/evidence label을 추가해야 합니다.",
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


def recommendation_role_ko(system_id: str) -> str:
    roles = {
        "bm25": "빠른 exact-term baseline",
        "dense-vector": "의미 기반 유사도 baseline",
        "hybrid": "exact와 semantic query가 섞인 경우의 균형형 기본값",
        "hybrid-rerank": "rerank latency를 감수할 수 있을 때의 품질 우선 retrieval",
        "parent-child": "작은 chunk 검색과 더 넓은 answer context",
        "pageindex-oss": "구조화된 긴 문서와 multi-section navigation",
    }
    return roles.get(system_id, "후보 RAG 전략")


def failure_type_ko(failure_type: str) -> str:
    labels = {
        "parse_failure": "문서 파싱 실패",
        "retrieval_miss": "검색 누락",
        "bad_ranking": "순위화 실패",
        "context_bloat": "불필요한 context 과다",
        "generation_hallucination": "생성 hallucination",
        "citation_mismatch": "citation 불일치",
        "timeout": "timeout",
        "tool_or_json_error": "tool/json 오류",
    }
    return labels.get(failure_type, failure_type)


def warning_ko(warning: str) -> str:
    evidence_match = re.match(
        r"(.+): at least one question needs (\d+) evidence items, but top_k=(\d+)\.",
        warning,
    )
    if evidence_match:
        domain, evidence_count, top_k = evidence_match.groups()
        return f"{domain}: 최소 한 질문이 {evidence_count}개의 evidence item을 필요로 하지만 top_k={top_k}입니다."
    if "answerable questions have no evidence labels" in warning:
        return warning.replace(
            "answerable questions have no evidence labels; retrieval scores are limited.",
            "개의 answerable question에 evidence label이 없어 retrieval score 해석이 제한됩니다.",
        )
    return warning
