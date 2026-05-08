from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


QUALITY_METRICS = [
    "answer_correctness",
    "evidence_recall",
    "context_precision",
    "citation_validity",
    "failure_rate",
]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_discrimination_report(results_dir: Path) -> str:
    summary_rows = load_csv(results_dir / "summary.csv")
    result_rows = load_csv(results_dir / "results.csv")
    category_rows = load_csv(results_dir / "category_summary.csv")

    lines = [
        "# Discrimination Audit",
        "",
        "This audit checks whether the benchmark actually separates RAG systems.",
        "",
        "## Verdict",
        "",
    ]
    for track, domain, judge in sorted(
        {
            (row.get("track", "end-to-end"), row["domain"], row.get("judge_model", "exact-match-gold"))
            for row in summary_rows
        }
    ):
        domain_summary = [
            row
            for row in summary_rows
            if row["domain"] == domain
            and row.get("track", "end-to-end") == track
            and row.get("judge_model", "exact-match-gold") == judge
        ]
        domain_results = [
            row
            for row in result_rows
            if row["domain"] == domain
            and row.get("track", "end-to-end") == track
            and row.get("judge_model", "exact-match-gold") == judge
        ]
        verdict, reason = domain_verdict(domain_summary, domain_results)
        lines.append(f"- `{track}` / `{domain}` / `{judge}`: **{verdict}**. {reason}")

    lines.extend(
        [
            "",
            "## Domain Metric Spread",
            "",
            "| Track | Domain | Judge | Metric | Min | Max | Range | Unique Values |",
            "|---|---|---|---|---:|---:|---:|---:|",
        ]
    )
    for track, domain, judge in sorted(
        {
            (row.get("track", "end-to-end"), row["domain"], row.get("judge_model", "exact-match-gold"))
            for row in summary_rows
        }
    ):
        domain_rows = [
            row
            for row in summary_rows
            if row["domain"] == domain
            and row.get("track", "end-to-end") == track
            and row.get("judge_model", "exact-match-gold") == judge
        ]
        for metric in QUALITY_METRICS:
            values = [float(row[metric]) for row in domain_rows]
            lines.append(
                f"| {track} | {domain} | {judge} | {metric} | {min(values):.3f} | {max(values):.3f} | "
                f"{max(values) - min(values):.3f} | {len({round(value, 6) for value in values})} |"
            )

    question_rows = question_discrimination(result_rows)
    lines.extend(
        [
            "",
            "## Question-Level Discrimination",
            "",
            "| Track | Domain | Judge | Questions | Quality-Diff Questions | Answer-Diff Questions | Recall-Diff Questions | Precision-Diff Questions |",
            "|---|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in question_rows:
        lines.append(
            "| {track} | {domain} | {judge_model} | {questions} | {quality_diff} | {answer_diff} | {recall_diff} | {precision_diff} |".format(
                **row
            )
        )

    lines.extend(
        [
            "",
            "## Categories That Separated Systems",
            "",
            "| Track | Domain | Judge | Category | Answer Range | Best Answer | Worst Answer |",
            "|---|---|---|---|---:|---:|---:|",
        ]
    )
    separating_categories = category_discrimination(category_rows)
    if separating_categories:
        for row in separating_categories:
            lines.append(
                "| {track} | {domain} | {judge_model} | {category} | {answer_range:.3f} | {best_answer:.3f} | {worst_answer:.3f} |".format(
                    **row
                )
            )
    else:
        lines.append("| none | none | none | none | 0.000 | 0.000 | 0.000 |")

    lines.extend(
        [
            "",
            "## Practical Reading",
            "",
            "- Strong discrimination needs several systems to fail differently across many questions.",
            "- A domain where every system scores the same is a harness smoke test, not a decision-grade benchmark.",
            "- A single separating question can reveal a useful pattern, but it is too brittle for production selection.",
            "",
        ]
    )
    return "\n".join(lines)


def domain_verdict(summary_rows: list[dict[str, str]], result_rows: list[dict[str, str]]) -> tuple[str, str]:
    answer_range = metric_range(summary_rows, "answer_correctness")
    recall_range = metric_range(summary_rows, "evidence_recall")
    precision_range = metric_range(summary_rows, "context_precision")
    question_rows = question_discrimination(result_rows)
    quality_diff_questions = question_rows[0]["quality_diff"] if question_rows else 0
    questions = question_rows[0]["questions"] if question_rows else 0

    if answer_range == 0 and recall_range == 0 and precision_range < 0.05:
        return (
            "not discriminative",
            "All systems produced effectively the same quality scores; use this only as a smoke test.",
        )
    if questions and int(quality_diff_questions) / int(questions) < 0.35:
        return (
            "weakly discriminative",
            "Some systems separate, but too few questions drive the difference.",
        )
    if answer_range >= 0.20 or recall_range >= 0.20:
        return (
            "strongly discriminative",
            "Multiple systems separate on answer or evidence quality.",
        )
    return (
        "moderately discriminative",
        "The benchmark separates systems, but the margin is still narrow.",
    )


def question_discrimination(result_rows: list[dict[str, str]]) -> list[dict[str, int | str]]:
    by_question: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in result_rows:
        by_question[
            (
                row.get("track", "end-to-end"),
                row["domain"],
                row.get("judge_model", "exact-match-gold"),
                row["question_id"],
            )
        ].append(row)

    by_domain: dict[tuple[str, str, str], dict[str, int | str]] = {}
    for (track, domain, judge_model, _question_id), rows in by_question.items():
        current = by_domain.setdefault(
            (track, domain, judge_model),
            {
                "track": track,
                "domain": domain,
                "judge_model": judge_model,
                "questions": 0,
                "quality_diff": 0,
                "answer_diff": 0,
                "recall_diff": 0,
                "precision_diff": 0,
            },
        )
        current["questions"] = int(current["questions"]) + 1
        answer_diff = has_spread(rows, "answer_correctness")
        recall_diff = has_spread(rows, "evidence_recall")
        if answer_diff or recall_diff:
            current["quality_diff"] = int(current["quality_diff"]) + 1
        if answer_diff:
            current["answer_diff"] = int(current["answer_diff"]) + 1
        if recall_diff:
            current["recall_diff"] = int(current["recall_diff"]) + 1
        if has_spread(rows, "context_precision"):
            current["precision_diff"] = int(current["precision_diff"]) + 1
    return [by_domain[key] for key in sorted(by_domain)]


def category_discrimination(category_rows: list[dict[str, str]]) -> list[dict[str, float | str]]:
    by_category: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in category_rows:
        by_category[
            (
                row.get("track", "end-to-end"),
                row["domain"],
                row.get("judge_model", "exact-match-gold"),
                row["category"],
            )
        ].append(row)

    rows = []
    for (track, domain, judge_model, category), items in sorted(by_category.items()):
        values = [float(row["answer_correctness"]) for row in items]
        answer_range = max(values) - min(values)
        if answer_range > 0:
            rows.append(
                {
                    "track": track,
                    "domain": domain,
                    "judge_model": judge_model,
                    "category": category,
                    "answer_range": answer_range,
                    "best_answer": max(values),
                    "worst_answer": min(values),
                }
            )
    return rows


def metric_range(rows: list[dict[str, str]], metric: str) -> float:
    values = [float(row[metric]) for row in rows]
    return max(values) - min(values) if values else 0.0


def has_spread(rows: list[dict[str, str]], metric: str) -> bool:
    values = {round(float(row[metric]), 6) for row in rows}
    return len(values) > 1
