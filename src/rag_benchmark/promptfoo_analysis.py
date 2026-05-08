from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any

from .production import (
    PRODUCTION_READINESS_FIELDS,
    build_production_readiness,
    metric,
)


PROMPTFOO_RESULT_FIELDS = [
    "eval_id",
    "track",
    "domain",
    "category",
    "question_id",
    "system_id",
    "rag_method",
    "embedding_model",
    "generator_model",
    "judge_model",
    "success",
    "score",
    "latency_ms",
    "estimated_cost",
    "answer_correctness",
    "evidence_recall",
    "context_precision",
    "citation_validity",
    "abstention_correctness",
    "failure_type",
    "failed_assertions",
]

PROMPTFOO_SUMMARY_FIELDS = [
    "source",
    "eval_id",
    "track",
    "domain",
    "system_id",
    "rag_method",
    "embedding_model",
    "generator_model",
    "judge_model",
    "questions",
    "passed",
    "failed",
    "pass_rate",
    "score",
    "answer_correctness",
    "evidence_recall",
    "context_precision",
    "citation_validity",
    "failure_rate",
    "no_answer_hallucination_rate",
    "latency_ms",
    "estimated_cost",
]

PROMPTFOO_CATEGORY_FIELDS = [
    "source",
    "eval_id",
    "track",
    "domain",
    "category",
    "system_id",
    "rag_method",
    "embedding_model",
    "generator_model",
    "judge_model",
    "questions",
    "passed",
    "failed",
    "pass_rate",
    "score",
    "answer_correctness",
    "evidence_recall",
    "context_precision",
    "citation_validity",
    "failure_rate",
]

PROMPTFOO_FAILURE_FIELDS = [
    "source",
    "eval_id",
    "track",
    "domain",
    "system_id",
    "embedding_model",
    "generator_model",
    "judge_model",
    "failure_type",
    "failed_assertion",
    "count",
]


@dataclass(frozen=True)
class PromptfooAnalysis:
    eval_id: str
    result_rows: list[dict[str, Any]]
    summary_rows: list[dict[str, Any]]
    category_rows: list[dict[str, Any]]
    failure_rows: list[dict[str, Any]]
    readiness_rows: list[dict[str, Any]]


def analyze_promptfoo_results(path: Path) -> PromptfooAnalysis:
    data = json.loads(path.read_text(encoding="utf-8"))
    eval_id = str(data.get("evalId") or data.get("results", {}).get("evalId") or "promptfoo")
    raw_results = data.get("results", {}).get("results", [])
    result_rows = [flatten_promptfoo_result(eval_id, item) for item in raw_results]
    summary_rows = summarize_promptfoo_rows(eval_id, result_rows)
    category_rows = summarize_promptfoo_categories(eval_id, result_rows)
    failure_rows = summarize_promptfoo_failures(eval_id, result_rows)
    readiness_rows = build_production_readiness(
        summary_rows,
        category_rows,
        result_rows,
        source="promptfoo",
    )
    return PromptfooAnalysis(
        eval_id=eval_id,
        result_rows=result_rows,
        summary_rows=summary_rows,
        category_rows=category_rows,
        failure_rows=failure_rows,
        readiness_rows=readiness_rows,
    )


def flatten_promptfoo_result(eval_id: str, item: dict[str, Any]) -> dict[str, Any]:
    metadata = item.get("response", {}).get("metadata", {})
    metrics = metadata.get("metrics") or parse_output_metrics(item)
    provider_label = item.get("provider", {}).get("label", "")
    parsed_label = parse_provider_label(provider_label)
    failed_assertions = [
        component.get("assertion", {}).get("metric") or component.get("assertion", {}).get("type")
        for component in item.get("gradingResult", {}).get("componentResults", [])
        if not component.get("pass")
    ]
    return {
        "eval_id": eval_id,
        "track": metrics.get("track") or parsed_label.get("track") or "end-to-end",
        "domain": metrics.get("domain") or item.get("vars", {}).get("domain", ""),
        "category": metrics.get("category") or item.get("vars", {}).get("category", ""),
        "question_id": metrics.get("question_id") or item.get("vars", {}).get("question_id", ""),
        "system_id": metrics.get("system_id") or parsed_label.get("system_id", ""),
        "rag_method": metrics.get("rag_method") or metrics.get("system_id") or parsed_label.get("system_id", ""),
        "embedding_model": metrics.get("embedding_model") or parsed_label.get("embedding_model", "none"),
        "generator_model": metrics.get("generator_model") or parsed_label.get("generator_model", ""),
        "judge_model": metrics.get("judge_model") or parsed_label.get("judge_model", ""),
        "success": bool(item.get("success")),
        "score": float(item.get("score") or 0.0),
        "latency_ms": float(item.get("latencyMs") or metrics.get("query_wall_time_ms") or 0.0),
        "estimated_cost": float(item.get("cost") or metrics.get("estimated_cost") or 0.0),
        "answer_correctness": metric(metrics, "answer_correctness"),
        "evidence_recall": metric(metrics, "evidence_recall"),
        "context_precision": metric(metrics, "context_precision"),
        "citation_validity": metric(metrics, "citation_validity"),
        "abstention_correctness": metric(metrics, "abstention_correctness"),
        "failure_type": metrics.get("failure_type") or "",
        "failed_assertions": ",".join(assertion for assertion in failed_assertions if assertion),
    }


def parse_output_metrics(item: dict[str, Any]) -> dict[str, Any]:
    output = item.get("response", {}).get("output")
    if not output:
        return {}
    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        return {}
    return payload.get("metrics", {})


def parse_provider_label(label: str) -> dict[str, str]:
    parts = label.split(":")
    if len(parts) >= 4:
        if len(parts) == 4:
            track, system_id, generator_model, judge_model = parts
            return {
                "track": track,
                "system_id": system_id,
                "embedding_model": "none",
                "generator_model": generator_model,
                "judge_model": judge_model,
            }
        track, system_id, embedding_model, generator_model, judge_model = parts[:5]
        return {
            "track": track,
            "system_id": system_id,
            "embedding_model": embedding_model,
            "generator_model": generator_model,
            "judge_model": judge_model,
        }
    return {}


def summarize_promptfoo_rows(eval_id: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[variant_key(row)].append(row)
    output = []
    for (track, domain, system_id, embedding_model, generator_model, judge_model), items in sorted(grouped.items()):
        output.append(summary_row(eval_id, items, track, domain, system_id, embedding_model, generator_model, judge_model))
    return output


def summarize_promptfoo_categories(eval_id: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(*variant_key(row), str(row.get("category", "")))].append(row)
    output = []
    for (track, domain, system_id, embedding_model, generator_model, judge_model, category), items in sorted(
        grouped.items()
    ):
        base = summary_row(eval_id, items, track, domain, system_id, embedding_model, generator_model, judge_model)
        output.append({"category": category, **base})
    return output


def summary_row(
    eval_id: str,
    items: list[dict[str, Any]],
    track: str,
    domain: str,
    system_id: str,
    embedding_model: str,
    generator_model: str,
    judge_model: str,
) -> dict[str, Any]:
    passed = sum(1 for item in items if item["success"])
    failed = len(items) - passed
    no_answer_items = [item for item in items if item.get("category") == "no_answer"]
    no_answer_hallucinations = sum(
        1 for item in no_answer_items if item.get("failure_type") == "generation_hallucination"
    )
    return {
        "source": "promptfoo",
        "eval_id": eval_id,
        "track": track,
        "domain": domain,
        "system_id": system_id,
        "rag_method": items[0].get("rag_method") or system_id,
        "embedding_model": embedding_model,
        "generator_model": generator_model,
        "judge_model": judge_model,
        "questions": len(items),
        "passed": passed,
        "failed": failed,
        "pass_rate": passed / len(items) if items else 0.0,
        "score": avg(items, "score"),
        "answer_correctness": avg(items, "answer_correctness"),
        "evidence_recall": avg(items, "evidence_recall"),
        "context_precision": avg(items, "context_precision"),
        "citation_validity": avg(items, "citation_validity"),
        "failure_rate": failed / len(items) if items else 0.0,
        "no_answer_hallucination_rate": (
            no_answer_hallucinations / len(no_answer_items) if no_answer_items else 0.0
        ),
        "latency_ms": avg(items, "latency_ms"),
        "estimated_cost": sum(float(item.get("estimated_cost") or 0.0) for item in items),
    }


def summarize_promptfoo_failures(eval_id: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counter: Counter[tuple[str, str, str, str, str, str, str, str]] = Counter()
    for row in rows:
        if row.get("failure_type") or row.get("failed_assertions"):
            assertions = str(row.get("failed_assertions") or "none").split(",")
            for assertion in assertions:
                counter[
                    (
                        row["track"],
                        row["domain"],
                        row["system_id"],
                        row["embedding_model"],
                        row["generator_model"],
                        row["judge_model"],
                        str(row.get("failure_type") or "none"),
                        assertion or "none",
                    )
                ] += 1
    return [
        {
            "source": "promptfoo",
            "eval_id": eval_id,
            "track": track,
            "domain": domain,
            "system_id": system_id,
            "embedding_model": embedding_model,
            "generator_model": generator_model,
            "judge_model": judge_model,
            "failure_type": failure_type,
            "failed_assertion": failed_assertion,
            "count": count,
        }
        for (
            track,
            domain,
            system_id,
            embedding_model,
            generator_model,
            judge_model,
            failure_type,
            failed_assertion,
        ), count in sorted(counter.items())
    ]


def write_promptfoo_analysis(output_dir: Path, analysis: PromptfooAnalysis) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "promptfoo_results.csv", analysis.result_rows, PROMPTFOO_RESULT_FIELDS)
    write_csv(output_dir / "promptfoo_summary.csv", analysis.summary_rows, PROMPTFOO_SUMMARY_FIELDS)
    write_csv(output_dir / "promptfoo_category_summary.csv", analysis.category_rows, PROMPTFOO_CATEGORY_FIELDS)
    write_csv(output_dir / "promptfoo_failure_summary.csv", analysis.failure_rows, PROMPTFOO_FAILURE_FIELDS)
    write_csv(output_dir / "promptfoo_production_readiness.csv", analysis.readiness_rows, PRODUCTION_READINESS_FIELDS)
    (output_dir / "promptfoo_report.md").write_text(build_promptfoo_report(analysis, korean=False), encoding="utf-8")
    (output_dir / "promptfoo_report.ko.md").write_text(build_promptfoo_report(analysis, korean=True), encoding="utf-8")


def build_promptfoo_report(analysis: PromptfooAnalysis, *, korean: bool) -> str:
    lines = (
        [f"# Promptfoo RAG 평가 리포트: {analysis.eval_id}", ""]
        if korean
        else [f"# Promptfoo RAG Evaluation Report: {analysis.eval_id}", ""]
    )
    total = len(analysis.result_rows)
    passed = sum(1 for row in analysis.result_rows if row["success"])
    pass_rate = passed / total if total else 0.0
    if korean:
        lines.extend(
            [
                f"- 전체 케이스: {total}",
                f"- 통과: {passed}",
                f"- 실패: {total - passed}",
                f"- 통과율: {pass_rate:.2%}",
                "",
                "## 시스템별 요약",
                "",
                "| 도메인 | 시스템 | 통과율 | 답변 | Evidence | Citation | 운영 판단 | 안내 |",
                "|---|---|---:|---:|---:|---:|---|---|",
            ]
        )
        readiness_by_key = {variant_key(row): row for row in analysis.readiness_rows}
        for row in analysis.summary_rows:
            ready = readiness_by_key.get(variant_key(row), {})
            lines.append(
                "| {domain} | `{system_id}` | {pass_rate:.2%} | {answer_correctness:.3f} | "
                "{evidence_recall:.3f} | {citation_validity:.3f} | {status} | {guidance} |".format(
                    status=ready.get("status_ko", ""),
                    guidance=ready.get("guidance_ko", ""),
                    **row,
                )
            )
    else:
        lines.extend(
            [
                f"- Total cases: {total}",
                f"- Passed: {passed}",
                f"- Failed: {total - passed}",
                f"- Pass rate: {pass_rate:.2%}",
                "",
                "## System Summary",
                "",
                "| Domain | System | Pass Rate | Answer | Evidence | Citation | Readiness | Guidance |",
                "|---|---|---:|---:|---:|---:|---|---|",
            ]
        )
        readiness_by_key = {variant_key(row): row for row in analysis.readiness_rows}
        for row in analysis.summary_rows:
            ready = readiness_by_key.get(variant_key(row), {})
            lines.append(
                "| {domain} | `{system_id}` | {pass_rate:.2%} | {answer_correctness:.3f} | "
                "{evidence_recall:.3f} | {citation_validity:.3f} | {status} | {guidance} |".format(
                    status=ready.get("status", ""),
                    guidance=ready.get("guidance", ""),
                    **row,
                )
            )
    lines.append("")
    return "\n".join(lines)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def avg(rows: list[dict[str, Any]], field: str) -> float:
    return mean(float(row.get(field) or 0.0) for row in rows) if rows else 0.0


def variant_key(row: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    return (
        str(row.get("track", "")),
        str(row.get("domain", "")),
        str(row.get("system_id", "")),
        str(row.get("embedding_model", "none")),
        str(row.get("generator_model", "")),
        str(row.get("judge_model", "")),
    )
