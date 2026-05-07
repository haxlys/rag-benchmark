from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

from .answer import generate_answer
from .datasets import enabled_domains, enabled_mvp_systems, load_domain
from .evaluation import evaluate
from .reporting import (
    aggregate,
    aggregate_by_category,
    build_recommendations,
    failure_summary,
    write_category_csv,
    write_failure_csv,
    write_jsonl,
    write_markdown_report,
    write_recommendations_csv,
    write_results,
    write_summary_csv,
)
from .retrievers import build_retriever
from .schemas import EvaluationResult


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_benchmark(
    *,
    root: Path,
    config_path: Path,
    domains: Iterable[str] | None = None,
    systems: Iterable[str] | None = None,
    top_k: int = 4,
    output_dir: Path | None = None,
) -> Path:
    config = load_config(config_path)
    selected_domains = list(domains) if domains else enabled_domains(config)
    selected_systems = list(systems) if systems else enabled_mvp_systems(config)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = output_dir or root / "runs" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    all_results: list[EvaluationResult] = []
    traces: list[dict] = []
    interpretation_warnings: list[str] = []

    for domain in selected_domains:
        documents, questions = load_domain(root, domain)
        max_evidence = max((len(question.evidence) for question in questions), default=0)
        if max_evidence > top_k:
            interpretation_warnings.append(
                f"{domain}: at least one question needs {max_evidence} evidence items, but top_k={top_k}."
            )
        unlabeled = sum(1 for question in questions if not question.no_answer and not question.evidence)
        if unlabeled:
            interpretation_warnings.append(
                f"{domain}: {unlabeled} answerable questions have no evidence labels; retrieval scores are limited."
            )
        for system_id in selected_systems:
            retriever = build_retriever(system_id, documents, top_k=top_k)
            for question in questions:
                retrieval = retriever.retrieve(question, top_k=top_k)
                answer = generate_answer(question, retrieval)
                result = evaluate(
                    run_id=run_id,
                    domain=domain,
                    system_id=system_id,
                    question=question,
                    retrieval=retrieval,
                    answer=answer,
                )
                all_results.append(result)
                traces.append(
                    {
                        "run_id": run_id,
                        "domain": domain,
                        "system_id": system_id,
                        "question": question.model_dump(),
                        "retrieval": retrieval.model_dump(),
                        "answer": answer.model_dump(),
                        "evaluation": result.model_dump(),
                    }
                )

    summary_rows = aggregate(all_results)
    category_rows = aggregate_by_category(all_results)
    recommendation_rows = build_recommendations(summary_rows)
    failure_rows = failure_summary(all_results)
    write_results(out_dir / "results.csv", all_results)
    write_summary_csv(out_dir / "summary.csv", summary_rows)
    write_category_csv(out_dir / "category_summary.csv", category_rows)
    write_recommendations_csv(out_dir / "recommendations.csv", recommendation_rows)
    write_failure_csv(out_dir / "failure_summary.csv", failure_rows)
    write_jsonl(out_dir / "traces.jsonl", traces)
    write_markdown_report(
        out_dir / "report.md",
        summary_rows,
        category_rows,
        recommendation_rows,
        failure_rows,
        run_id,
        interpretation_warnings,
    )
    copy_latest(root, out_dir)
    return out_dir


def copy_latest(root: Path, out_dir: Path) -> None:
    results_dir = root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    for name in [
        "summary.csv",
        "category_summary.csv",
        "recommendations.csv",
        "failure_summary.csv",
        "results.csv",
        "report.md",
    ]:
        source = out_dir / name
        target = results_dir / name
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def read_summary(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_report(path: Path) -> str:
    return path.read_text(encoding="utf-8")
