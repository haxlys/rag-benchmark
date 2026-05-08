from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any


PRODUCTION_THRESHOLDS = {
    "pass_rate": 0.80,
    "answer_correctness": 0.80,
    "evidence_recall": 0.85,
    "citation_validity": 0.90,
    "no_answer_hallucination_rate": 0.05,
    "financebench_calculation_pass_rate": 0.80,
}

PRODUCTION_READINESS_FIELDS = [
    "source",
    "track",
    "domain",
    "system_id",
    "rag_method",
    "embedding_model",
    "generator_model",
    "judge_model",
    "questions",
    "pass_rate",
    "answer_correctness",
    "evidence_recall",
    "context_precision",
    "citation_validity",
    "no_answer_hallucination_rate",
    "calculation_pass_rate",
    "readiness_score",
    "status",
    "status_ko",
    "blocking_issues",
    "guidance",
    "guidance_ko",
]


def build_production_readiness(
    summary_rows: list[dict[str, Any]],
    category_rows: list[dict[str, Any]] | None = None,
    result_rows: list[dict[str, Any]] | None = None,
    *,
    source: str = "benchmark",
) -> list[dict[str, Any]]:
    canonical_rows = [
        row
        for row in summary_rows
        if row.get("track") == "end-to-end" and row.get("judge_model") == "exact-match-gold"
    ]
    if not canonical_rows:
        canonical_rows = [row for row in summary_rows if row.get("track") == "end-to-end"] or summary_rows

    categories_by_variant = index_category_rows(category_rows or [])
    no_answer_rates = no_answer_hallucination_rates(result_rows or [])
    readiness_rows = []
    for row in canonical_rows:
        key = variant_key(row)
        category_items = categories_by_variant.get(key, [])
        pass_rate = metric(row, "pass_rate", 1.0 - metric(row, "failure_rate"))
        answer = metric(row, "answer_correctness")
        evidence = metric(row, "evidence_recall")
        precision = metric(row, "context_precision")
        citation = metric(row, "citation_validity")
        no_answer_rate = no_answer_rates.get(key, no_answer_rate_from_categories(category_items))
        calculation_pass_rate = category_pass_rate(category_items, "calculation")
        issues, minor_issues = readiness_issues(
            row,
            pass_rate=pass_rate,
            answer=answer,
            evidence=evidence,
            citation=citation,
            no_answer_hallucination_rate=no_answer_rate,
            calculation_pass_rate=calculation_pass_rate,
            category_items=category_items,
        )
        status = readiness_status(issues, minor_issues)
        readiness_rows.append(
            {
                "source": source,
                "track": row.get("track", "end-to-end"),
                "domain": row.get("domain", ""),
                "system_id": row.get("system_id", ""),
                "rag_method": row.get("rag_method", row.get("system_id", "")),
                "embedding_model": row.get("embedding_model", "none"),
                "generator_model": row.get("generator_model", ""),
                "judge_model": row.get("judge_model", ""),
                "questions": int(float(row.get("questions", 0) or 0)),
                "pass_rate": pass_rate,
                "answer_correctness": answer,
                "evidence_recall": evidence,
                "context_precision": precision,
                "citation_validity": citation,
                "no_answer_hallucination_rate": no_answer_rate,
                "calculation_pass_rate": calculation_pass_rate,
                "readiness_score": readiness_score(
                    pass_rate,
                    answer,
                    evidence,
                    citation,
                    no_answer_rate,
                    calculation_pass_rate,
                    has_calculation=has_category(category_items, "calculation"),
                ),
                "status": status,
                "status_ko": status_ko(status),
                "blocking_issues": ", ".join([*issues, *minor_issues]) or "none",
                "guidance": guidance(status, issues, minor_issues),
                "guidance_ko": guidance_ko(status, issues, minor_issues),
            }
        )
    return sorted(
        readiness_rows,
        key=lambda item: (
            item["source"],
            item["domain"],
            status_rank(item["status"]),
            -float(item["readiness_score"]),
            item["system_id"],
        ),
    )


def variant_key(row: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    return (
        str(row.get("track", "")),
        str(row.get("domain", "")),
        str(row.get("system_id", "")),
        str(row.get("embedding_model", "none")),
        str(row.get("generator_model", "")),
        str(row.get("judge_model", "")),
    )


def index_category_rows(rows: list[dict[str, Any]]) -> dict[tuple[str, str, str, str, str, str], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[variant_key(row)].append(row)
    return grouped


def no_answer_hallucination_rates(rows: list[dict[str, Any]]) -> dict[tuple[str, str, str, str, str, str], float]:
    grouped: dict[tuple[str, str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("category") == "no_answer":
            grouped[variant_key(row)].append(row)
    rates = {}
    for key, items in grouped.items():
        if items:
            hallucinations = sum(1 for item in items if item.get("failure_type") == "generation_hallucination")
            rates[key] = hallucinations / len(items)
    return rates


def no_answer_rate_from_categories(rows: list[dict[str, Any]]) -> float:
    no_answer = [row for row in rows if row.get("category") == "no_answer"]
    if not no_answer:
        return 0.0
    return mean(metric(row, "failure_rate", 1.0 - metric(row, "pass_rate", 1.0)) for row in no_answer)


def category_pass_rate(rows: list[dict[str, Any]], category: str) -> float:
    matches = [row for row in rows if row.get("category") == category]
    if not matches:
        return 1.0
    return mean(metric(row, "pass_rate", 1.0 - metric(row, "failure_rate")) for row in matches)


def has_category(rows: list[dict[str, Any]], category: str) -> bool:
    return any(row.get("category") == category for row in rows)


def readiness_issues(
    row: dict[str, Any],
    *,
    pass_rate: float,
    answer: float,
    evidence: float,
    citation: float,
    no_answer_hallucination_rate: float,
    calculation_pass_rate: float,
    category_items: list[dict[str, Any]],
) -> tuple[list[str], list[str]]:
    issues = []
    minor_issues = []
    if pass_rate < PRODUCTION_THRESHOLDS["pass_rate"]:
        issues.append("pass_rate")
    if answer < PRODUCTION_THRESHOLDS["answer_correctness"]:
        issues.append("answer_correctness")
    if evidence < PRODUCTION_THRESHOLDS["evidence_recall"]:
        issues.append("evidence_recall")
    if citation < 0.85:
        issues.append("citation_validity")
    elif citation < PRODUCTION_THRESHOLDS["citation_validity"]:
        minor_issues.append("citation_validity")
    if no_answer_hallucination_rate > PRODUCTION_THRESHOLDS["no_answer_hallucination_rate"]:
        issues.append("no_answer_hallucination")
    if "financebench" in str(row.get("domain", "")) and has_category(category_items, "calculation"):
        if calculation_pass_rate < PRODUCTION_THRESHOLDS["financebench_calculation_pass_rate"]:
            issues.append("financebench_calculation")
    return issues, minor_issues


def readiness_status(issues: list[str], minor_issues: list[str]) -> str:
    if not issues and not minor_issues:
        return "production_candidate"
    if not issues:
        return "pilot_candidate"
    return "not_ready"


def readiness_score(
    pass_rate: float,
    answer: float,
    evidence: float,
    citation: float,
    no_answer_rate: float,
    calculation_pass_rate: float,
    *,
    has_calculation: bool,
) -> float:
    score = (
        clamp(pass_rate) * 0.25
        + clamp(answer) * 0.25
        + clamp(evidence) * 0.25
        + clamp(citation) * 0.15
        + (1.0 - clamp(no_answer_rate)) * 0.10
    )
    if has_calculation:
        score = score * 0.85 + clamp(calculation_pass_rate) * 0.15
    return score


def status_rank(status: str) -> int:
    ranks = {"production_candidate": 0, "pilot_candidate": 1, "not_ready": 2}
    return ranks.get(status, 3)


def status_ko(status: str) -> str:
    labels = {
        "production_candidate": "운영 후보",
        "pilot_candidate": "파일럿 후보",
        "not_ready": "운영 전 개선 필요",
    }
    return labels.get(status, status)


def guidance(status: str, issues: list[str], minor_issues: list[str]) -> str:
    if status == "production_candidate":
        return "Meets the proposed production thresholds for this benchmark slice."
    if status == "pilot_candidate":
        return f"Close to production; review {issue_text(minor_issues)} before rollout."
    return f"Do not use as production default yet; improve {issue_text(issues)} first."


def guidance_ko(status: str, issues: list[str], minor_issues: list[str]) -> str:
    if status == "production_candidate":
        return "이 벤치마크 구간에서는 제안한 운영 기준을 충족합니다."
    if status == "pilot_candidate":
        return f"운영 후보에 가깝지만 {issue_text_ko(minor_issues)}를 먼저 점검해야 합니다."
    return f"아직 운영 기본값으로 쓰기 어렵습니다. 먼저 {issue_text_ko(issues)}를 개선해야 합니다."


def issue_text(issues: list[str]) -> str:
    return ", ".join(issues) if issues else "minor gaps"


def issue_text_ko(issues: list[str]) -> str:
    labels = {
        "pass_rate": "전체 통과율",
        "answer_correctness": "답변 정확도",
        "evidence_recall": "근거 회수율",
        "citation_validity": "인용 정확도",
        "no_answer_hallucination": "근거 없음 질문의 hallucination",
        "financebench_calculation": "FinanceBench 계산/표 질의",
    }
    return ", ".join(labels.get(issue, issue) for issue in issues) if issues else "작은 미달 항목"


def metric(row: dict[str, Any], field: str, default: float = 0.0) -> float:
    value = row.get(field, default)
    if value in (None, ""):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
