from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

from .answer import generate_answer
from .dashboard import write_dashboard
from .datasets import (
    enabled_domains,
    enabled_mvp_embeddings,
    enabled_mvp_generators,
    enabled_mvp_judges,
    enabled_mvp_systems,
    enabled_tracks,
    load_domain,
    page_chunks,
)
from .evaluation import evaluate
from .judges import judge_answer
from .reporting import (
    aggregate,
    aggregate_by_category,
    build_axis_leaderboard,
    build_judge_audit,
    build_recommendations,
    failure_summary,
    write_axis_leaderboard_csv,
    write_category_csv,
    write_failure_csv,
    write_judge_audit_csv,
    write_jsonl,
    write_markdown_report,
    write_markdown_report_ko,
    write_recommendations_csv,
    write_results,
    write_summary_csv,
)
from .retrievers import build_retriever
from .retrievers.factory import uses_embedding
from .schemas import EvaluationResult, Question, RetrievedContext, RetrievalTrace
from .text import token_count


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_benchmark(
    *,
    root: Path,
    config_path: Path,
    domains: Iterable[str] | None = None,
    systems: Iterable[str] | None = None,
    embeddings: Iterable[str] | None = None,
    generators: Iterable[str] | None = None,
    judges: Iterable[str] | None = None,
    tracks: Iterable[str] | None = None,
    top_k: int = 4,
    output_dir: Path | None = None,
    copy_to_results: bool = True,
) -> Path:
    config = load_config(config_path)
    selected_domains = list(domains) if domains else enabled_domains(config)
    selected_systems = list(systems) if systems else enabled_mvp_systems(config)
    selected_embeddings = list(embeddings) if embeddings else enabled_mvp_embeddings(config)
    selected_generators = list(generators) if generators else enabled_mvp_generators(config)
    selected_judges = list(judges) if judges else enabled_mvp_judges(config)
    selected_tracks = list(tracks) if tracks else enabled_tracks(config)
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
        if "retrieval-only" in selected_tracks:
            for system_id, embedding_model in system_embedding_matrix(
                selected_systems,
                selected_embeddings,
            ):
                retriever = build_retriever(
                    system_id,
                    documents,
                    top_k=top_k,
                    embedding_model=embedding_model,
                )
                for question in questions:
                    retrieval = retriever.retrieve(question, top_k=top_k)
                    answer = generate_answer(question, retrieval, "retrieval-probe")
                    append_result(
                        all_results=all_results,
                        traces=traces,
                        run_id=run_id,
                        track="retrieval-only",
                        domain=domain,
                        system_id=system_id,
                        question=question,
                        retrieval=retrieval,
                        answer=answer,
                        judges=selected_judges,
                    )

        if "generator-oracle" in selected_tracks:
            for question in questions:
                retrieval = oracle_retrieval(
                    question,
                    documents,
                    top_k=top_k,
                    run_id=run_id,
                )
                for generator_model in selected_generators:
                    answer = generate_answer(question, retrieval, generator_model)
                    append_result(
                        all_results=all_results,
                        traces=traces,
                        run_id=run_id,
                        track="generator-oracle",
                        domain=domain,
                        system_id="oracle-context",
                        question=question,
                        retrieval=retrieval,
                        answer=answer,
                        judges=selected_judges,
                    )

        if "end-to-end" in selected_tracks:
            for system_id, embedding_model in system_embedding_matrix(
                selected_systems,
                selected_embeddings,
            ):
                retriever = build_retriever(
                    system_id,
                    documents,
                    top_k=top_k,
                    embedding_model=embedding_model,
                )
                for question in questions:
                    retrieval = retriever.retrieve(question, top_k=top_k)
                    for generator_model in selected_generators:
                        answer = generate_answer(question, retrieval, generator_model)
                        append_result(
                            all_results=all_results,
                            traces=traces,
                            run_id=run_id,
                            track="end-to-end",
                            domain=domain,
                            system_id=system_id,
                            question=question,
                            retrieval=retrieval,
                            answer=answer,
                            judges=selected_judges,
                        )

    summary_rows = aggregate(all_results)
    category_rows = aggregate_by_category(all_results)
    recommendation_rows = build_recommendations(summary_rows)
    axis_leaderboard_rows = build_axis_leaderboard(summary_rows)
    judge_audit_rows = build_judge_audit(summary_rows)
    failure_rows = failure_summary(all_results)
    write_results(out_dir / "results.csv", all_results)
    write_summary_csv(out_dir / "summary.csv", summary_rows)
    write_category_csv(out_dir / "category_summary.csv", category_rows)
    write_recommendations_csv(out_dir / "recommendations.csv", recommendation_rows)
    write_axis_leaderboard_csv(out_dir / "axis_leaderboard.csv", axis_leaderboard_rows)
    write_judge_audit_csv(out_dir / "judge_audit.csv", judge_audit_rows)
    write_failure_csv(out_dir / "failure_summary.csv", failure_rows)
    write_jsonl(out_dir / "traces.jsonl", traces)
    write_markdown_report(
        out_dir / "report.md",
        summary_rows,
        category_rows,
        recommendation_rows,
        axis_leaderboard_rows,
        judge_audit_rows,
        failure_rows,
        run_id,
        interpretation_warnings,
    )
    write_markdown_report_ko(
        out_dir / "report.ko.md",
        summary_rows,
        category_rows,
        recommendation_rows,
        axis_leaderboard_rows,
        judge_audit_rows,
        failure_rows,
        run_id,
        interpretation_warnings,
    )
    write_dashboard(
        out_dir / "dashboard.html",
        summary_rows=summary_rows,
        category_rows=category_rows,
        recommendation_rows=recommendation_rows,
        axis_leaderboard_rows=axis_leaderboard_rows,
        judge_audit_rows=judge_audit_rows,
        result_rows=[result.model_dump() for result in all_results],
        run_id=run_id,
    )
    if copy_to_results:
        copy_latest(root, out_dir)
    return out_dir


def append_result(
    *,
    all_results: list[EvaluationResult],
    traces: list[dict],
    run_id: str,
    track: str,
    domain: str,
    system_id: str,
    question: Question,
    retrieval: RetrievalTrace,
    answer,
    judges: list[str],
) -> None:
    for judge_model in judges:
        judgement = judge_answer(question, retrieval, answer, judge_model)
        result = evaluate(
            run_id=run_id,
            track=track,
            domain=domain,
            system_id=system_id,
            question=question,
            retrieval=retrieval,
            answer=answer,
            judgement=judgement,
        )
        all_results.append(result)
        traces.append(
            {
                "run_id": run_id,
                "track": track,
                "domain": domain,
                "system_id": system_id,
                "judge_model": judge_model,
                "question": question.model_dump(),
                "retrieval": retrieval.model_dump(),
                "answer": answer.model_dump(),
                "judgement": judgement.model_dump(),
                "evaluation": result.model_dump(),
            }
        )


def system_embedding_matrix(
    systems: list[str],
    embeddings: list[str],
) -> list[tuple[str, str]]:
    pairs = []
    for system_id in systems:
        if uses_embedding(system_id):
            for embedding_model in embeddings:
                pairs.append((system_id, embedding_model))
        else:
            pairs.append((system_id, "none"))
    return pairs


def oracle_retrieval(
    question: Question,
    documents,
    *,
    top_k: int,
    run_id: str,
) -> RetrievalTrace:
    chunks = page_chunks(documents)
    selected = []
    seen = set()
    for evidence in question.evidence:
        for chunk in chunks:
            if chunk.chunk_id in seen:
                continue
            if chunk.overlaps(evidence):
                seen.add(chunk.chunk_id)
                selected.append(chunk)
                break
    contexts = [
        RetrievedContext(
            chunk=chunk,
            score=1.0,
            rank=rank,
            retriever="oracle-context",
        )
        for rank, chunk in enumerate(selected[:top_k], 1)
    ]
    return RetrievalTrace(
        system_id="oracle-context",
        rag_method="oracle-context",
        embedding_model="gold-context",
        reranker_model="none",
        question_id=question.question_id,
        contexts=contexts,
        query_wall_time_ms=0.0,
        index_wall_time_ms=0.0,
        retrieved_token_count=sum(token_count(context.chunk.text) for context in contexts),
        embedding_tokens=0,
        reranker_calls=0,
        tool_calls=0,
        estimated_cost=0.0,
        warnings=[f"{run_id}: oracle context uses gold evidence labels."],
    )


def copy_latest(root: Path, out_dir: Path) -> None:
    results_dir = root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    for name in [
        "summary.csv",
        "category_summary.csv",
        "recommendations.csv",
        "axis_leaderboard.csv",
        "judge_audit.csv",
        "failure_summary.csv",
        "results.csv",
        "report.md",
        "report.ko.md",
        "dashboard.html",
    ]:
        source = out_dir / name
        target = results_dir / name
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def read_summary(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_report(path: Path) -> str:
    return path.read_text(encoding="utf-8")
