from __future__ import annotations

import csv
import json
import re
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


def write_markdown_report_ko(
    path: Path,
    summary_rows: list[dict],
    category_rows: list[dict],
    recommendation_rows: list[dict],
    failure_rows: list[dict],
    run_id: str,
    warnings: list[str] | None = None,
) -> None:
    lines = [
        f"# RAG 벤치마크 리포트: {run_id}",
        "",
        "이 리포트는 실무 운영 의사결정을 위해 여러 RAG 전략을 비교합니다.",
        "점수는 로컬 fixture 데이터셋과 결정론적 extractive answerer로 생성됩니다.",
        "",
        "## 점수표",
        "",
        "| 도메인 | 시스템 | 답변 | Evidence Recall | Context Precision | Citation | 지연시간 ms | 비용 | 실패율 |",
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

    lines.extend(["", "## 실패 유형", ""])
    if failure_rows:
        lines.extend(["| 도메인 | 시스템 | 실패 유형 | 건수 |", "|---|---|---|---:|"])
        for row in failure_rows:
            row_ko = {**row, "failure_type": failure_type_ko(row["failure_type"])}
            lines.append(
                "| {domain} | `{system_id}` | {failure_type} | {count} |".format(**row_ko)
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

    lines.extend(["", "## 운영 가이드", ""])
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
            "- 현재 answerer는 결정론적이므로 retrieval failure를 재현하고 분석하기 쉽습니다.",
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
