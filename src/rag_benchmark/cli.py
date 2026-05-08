import csv
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.table import Table

from .datasets import (
    enabled_domains,
    enabled_mvp_embeddings,
    enabled_mvp_generators,
    enabled_mvp_judges,
    enabled_tracks,
)
from .discrimination import build_discrimination_report
from .dashboard import write_dashboard
from .importers import import_financebench, import_questions, import_text_documents
from .production import build_production_readiness
from .promptfoo import export_promptfoo_bundle
from .promptfoo_analysis import analyze_promptfoo_results, write_promptfoo_analysis
from .runner import read_report, read_summary, run_benchmark
from .validation import validate_domain_data

app = typer.Typer(help="Operational RAG benchmark harness.")
console = Console()


@app.callback()
def main() -> None:
    """Run and inspect RAG benchmark workflows."""


@app.command()
def plan(config: Path = Path("configs/benchmark.yaml")) -> None:
    """Print the configured benchmark scope."""
    with config.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    project = data.get("project", {})
    domains = data.get("domains", {})
    systems = data.get("systems", {})

    console.print(f"[bold]Project:[/bold] {project.get('name', 'unknown')}")
    console.print(f"[bold]Objective:[/bold] {project.get('objective', 'unknown')}")
    console.print(f"[bold]PageIndex scope:[/bold] {project.get('pageindex_scope', 'unknown')}")

    console.print("\n[bold]Enabled domains[/bold]")
    for name, domain in domains.items():
        if domain.get("enabled"):
            console.print(f"- {name}")

    console.print("\n[bold]Enabled MVP systems[/bold]")
    for name, system in systems.items():
        if system.get("enabled") and system.get("stage") == "mvp":
            console.print(f"- {name} ({system.get('family')})")

    console.print("\n[bold]Enabled embedding profiles[/bold]")
    for name in enabled_mvp_embeddings(data):
        item = data.get("embeddings", {}).get(name, {})
        console.print(f"- {name} ({item.get('model_ref', 'local')})")

    console.print("\n[bold]Enabled generator profiles[/bold]")
    for name in enabled_mvp_generators(data):
        item = data.get("generators", {}).get(name, {})
        console.print(f"- {name} ({item.get('family', 'profile')})")

    console.print("\n[bold]Enabled judge profiles[/bold]")
    for name in enabled_mvp_judges(data):
        item = data.get("judges", {}).get(name, {})
        console.print(f"- {name} ({item.get('family', 'profile')})")

    console.print("\n[bold]Enabled experiment tracks[/bold]")
    for name in enabled_tracks(data):
        console.print(f"- {name}")


@app.command()
def run(
    config: Path = Path("configs/benchmark.yaml"),
    domain: list[str] | None = typer.Option(None, "--domain", "-d", help="Domain to run."),
    system: list[str] | None = typer.Option(None, "--system", "-s", help="System to run."),
    embedding: list[str] | None = typer.Option(
        None,
        "--embedding",
        "-e",
        help="Embedding profile to run for embedding-aware systems.",
    ),
    generator: list[str] | None = typer.Option(
        None,
        "--generator",
        "-g",
        help="Generator profile to run.",
    ),
    judge: list[str] | None = typer.Option(
        None,
        "--judge",
        "-j",
        help="Judge/evaluator profile to run.",
    ),
    track: list[str] | None = typer.Option(
        None,
        "--track",
        "-t",
        help="Experiment track: retrieval-only, generator-oracle, end-to-end.",
    ),
    top_k: int = typer.Option(4, "--top-k", help="Number of contexts to retrieve."),
    output_dir: Path | None = typer.Option(None, "--output-dir", help="Run output directory."),
) -> None:
    """Run the benchmark and write scorecards."""
    out_dir = run_benchmark(
        root=Path.cwd(),
        config_path=config,
        domains=domain or None,
        systems=system or None,
        embeddings=embedding or None,
        generators=generator or None,
        judges=judge or None,
        tracks=track or None,
        top_k=top_k,
        output_dir=output_dir,
    )
    console.print(f"[bold green]Benchmark complete:[/bold green] {out_dir}")
    console.print(f"[bold cyan]Dashboard:[/bold cyan] {out_dir / 'dashboard.html'}")
    show_summary(out_dir / "summary.csv")


@app.command()
def summary(path: Path = Path("results/summary.csv")) -> None:
    """Print a scorecard summary."""
    show_summary(path)


@app.command()
def report(path: Path = Path("results/report.md")) -> None:
    """Print the latest markdown report."""
    console.print(read_report(path))


@app.command("report-ko")
def report_ko(path: Path = Path("results/report.ko.md")) -> None:
    """Print the latest Korean markdown report."""
    console.print(read_report(path))


@app.command("discrimination")
def discrimination(
    results_dir: Path = typer.Option(Path("results"), "--results-dir", help="Directory with benchmark CSV files."),
    output_path: Path | None = typer.Option(
        Path("results/discrimination.md"), "--output", "-o", help="Optional markdown output path."
    ),
) -> None:
    """Audit whether the benchmark separated systems."""
    text = build_discrimination_report(results_dir)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
        console.print(f"[green]wrote[/green] {output_path}")
    console.print(text)


@app.command("recommend")
def recommend(path: Path = Path("results/recommendations.csv")) -> None:
    """Print the latest operations recommendation ranking."""
    rows = read_summary(path)
    table = Table(title=f"RAG Recommendation Ranking: {path}")
    table.add_column("Domain")
    table.add_column("Track")
    table.add_column("System")
    table.add_column("Embedding")
    table.add_column("Generator")
    table.add_column("Judge")
    table.add_column("Score", justify="right")
    table.add_column("Quality", justify="right")
    table.add_column("Efficiency", justify="right")
    table.add_column("Stability", justify="right")
    table.add_column("Role")
    for row in rows:
        table.add_row(
            row["domain"],
            row.get("track", "end-to-end"),
            row["system_id"],
            row.get("embedding_model", "none"),
            row.get("generator_model", "unknown"),
            row.get("judge_model", "unknown"),
            f"{float(row['recommendation_score']):.3f}",
            f"{float(row['quality_score']):.3f}",
            f"{float(row['efficiency_score']):.3f}",
            f"{float(row['stability_score']):.3f}",
            row["role"],
        )
    console.print(table)


@app.command("analyze-promptfoo")
def analyze_promptfoo(
    input_path: Path = typer.Option(
        Path("integrations/promptfoo/promptfoo-results.json"),
        "--input",
        "-i",
        help="Promptfoo JSON output path.",
    ),
    output_dir: Path = typer.Option(Path("results"), "--output-dir", "-o", help="Directory for analysis CSVs."),
    update_dashboard: bool = typer.Option(
        True,
        "--update-dashboard/--no-update-dashboard",
        help="Attach promptfoo analysis and production readiness to results/dashboard.html.",
    ),
    benchmark_results_dir: Path = typer.Option(
        Path("results"),
        "--benchmark-results-dir",
        help="Directory containing canonical benchmark CSVs.",
    ),
) -> None:
    """Aggregate promptfoo results and attach production-readiness guidance."""
    analysis = analyze_promptfoo_results(input_path)
    write_promptfoo_analysis(output_dir, analysis)
    console.print(f"[green]wrote[/green] promptfoo analysis to {output_dir}")
    show_promptfoo_summary(analysis.summary_rows)

    if update_dashboard:
        update_dashboard_with_promptfoo(benchmark_results_dir, analysis)
        console.print(f"[green]updated[/green] {benchmark_results_dir / 'dashboard.html'}")


@app.command("validate-data")
def validate_data(
    config: Path = Path("configs/benchmark.yaml"),
    domain: list[str] | None = typer.Option(None, "--domain", "-d", help="Domain to validate."),
    top_k: int = typer.Option(4, "--top-k", help="Retrieval top-k used for interpretation warnings."),
) -> None:
    """Validate documents, questions, and evidence coordinates."""
    selected_domains = domain or enabled_domains(load_yaml(config))
    failed = False
    for name in selected_domains:
        report = validate_domain_data(Path.cwd(), name, top_k=top_k)
        status = "[green]ok[/green]" if report.ok else "[red]failed[/red]"
        console.print(
            f"[bold]{name}[/bold]: {status} "
            f"({report.documents} documents, {report.questions} questions)"
        )
        for error in report.errors:
            console.print(f"  [red]error[/red] {error}")
        for warning in report.warnings:
            console.print(f"  [yellow]warning[/yellow] {warning}")
        failed = failed or not report.ok
    if failed:
        raise typer.Exit(1)


@app.command("export-promptfoo")
def export_promptfoo(
    config: Path = Path("configs/benchmark.yaml"),
    output_dir: Path = typer.Option(
        Path("integrations/promptfoo"),
        "--output-dir",
        help="Directory for promptfoo config, tests, and provider.",
    ),
    domain: list[str] | None = typer.Option(None, "--domain", "-d", help="Domain to export."),
    system: list[str] | None = typer.Option(None, "--system", "-s", help="RAG system provider to export."),
    embedding: list[str] | None = typer.Option(
        None,
        "--embedding",
        "-e",
        help="Embedding profile for embedding-aware systems.",
    ),
    generator: list[str] | None = typer.Option(
        None,
        "--generator",
        "-g",
        help="Generator profile to export.",
    ),
    judge: list[str] | None = typer.Option(
        None,
        "--judge",
        "-j",
        help="Judge/evaluator profile to export.",
    ),
    track: list[str] | None = typer.Option(
        None,
        "--track",
        "-t",
        help="Experiment track to expose to promptfoo.",
    ),
    top_k: int = typer.Option(4, "--top-k", help="Number of contexts to retrieve."),
    max_questions_per_domain: int = typer.Option(
        0,
        "--max-questions-per-domain",
        help="Limit exported tests per domain. Default 0 exports all questions.",
    ),
    include_model_graded: bool = typer.Option(
        False,
        "--include-model-graded",
        help="Add promptfoo model-graded RAG assertions.",
    ),
    grader_provider: str | None = typer.Option(
        None,
        "--grader-provider",
        help="Promptfoo provider for model-graded assertions, e.g. ollama:chat:llama3.1.",
    ),
) -> None:
    """Export a promptfoo config that calls this benchmark as a Python provider."""
    summary = export_promptfoo_bundle(
        root=Path.cwd(),
        config_path=config,
        output_dir=output_dir,
        domains=domain or None,
        systems=system or None,
        embeddings=embedding or None,
        generators=generator or None,
        judges=judge or None,
        tracks=track or None,
        top_k=top_k,
        max_questions_per_domain=None if max_questions_per_domain <= 0 else max_questions_per_domain,
        include_model_graded=include_model_graded,
        grader_provider=grader_provider,
    )
    console.print(f"[green]wrote[/green] promptfoo config to {summary.config_path}")
    console.print(f"[green]wrote[/green] {summary.tests} tests to {summary.tests_path}")
    console.print(f"[green]wrote[/green] {summary.providers} provider variants via {summary.provider_path}")
    for warning in summary.warnings:
        console.print(f"  [yellow]warning[/yellow] {warning}")


@app.command("import-docs")
def import_docs(
    source_dir: Path = typer.Argument(..., help="Directory containing .md/.txt documents."),
    domain: str = typer.Option(..., "--domain", "-d", help="Benchmark domain name."),
    output_root: Path = typer.Option(
        Path("data/fixtures"), "--output-root", help="Fixture root for imported data."
    ),
    page_paragraphs: int = typer.Option(4, "--page-paragraphs", help="Paragraphs per synthetic page."),
    overwrite: bool = typer.Option(True, "--overwrite/--no-overwrite", help="Overwrite documents.jsonl."),
) -> None:
    """Import local markdown/text documents as benchmark documents."""
    summary = import_text_documents(
        source_dir=source_dir,
        output_dir=output_root / domain,
        domain=domain,
        page_paragraphs=page_paragraphs,
        overwrite=overwrite,
    )
    console.print(f"[green]wrote[/green] {summary.rows_written} documents to {summary.path}")
    for warning in summary.warnings:
        console.print(f"  [yellow]warning[/yellow] {warning}")


@app.command("import-questions")
def import_question_file(
    source_path: Path = typer.Argument(..., help="Question file: .jsonl, .json, or .csv."),
    domain: str = typer.Option(..., "--domain", "-d", help="Benchmark domain name."),
    output_root: Path = typer.Option(
        Path("data/fixtures"), "--output-root", help="Fixture root for imported data."
    ),
    overwrite: bool = typer.Option(True, "--overwrite/--no-overwrite", help="Overwrite questions.jsonl."),
) -> None:
    """Import questions, gold answers, and evidence labels."""
    summary = import_questions(
        source_path=source_path,
        output_dir=output_root / domain,
        domain=domain,
        overwrite=overwrite,
    )
    console.print(f"[green]wrote[/green] {summary.rows_written} questions to {summary.path}")
    for warning in summary.warnings:
        console.print(f"  [yellow]warning[/yellow] {warning}")


@app.command("import-financebench")
def import_financebench_file(
    source_path: Path = typer.Argument(
        ..., help="FinanceBench JSONL/JSON file, e.g. financebench_merged.jsonl."
    ),
    domain: str = typer.Option("finance", "--domain", "-d", help="Benchmark domain name."),
    output_root: Path = typer.Option(
        Path("data/fixtures"), "--output-root", help="Fixture root for imported data."
    ),
    limit: int | None = typer.Option(None, "--limit", help="Import only the first N rows."),
    overwrite: bool = typer.Option(True, "--overwrite/--no-overwrite", help="Overwrite benchmark files."),
) -> None:
    """Import open-source FinanceBench questions and evidence pages."""
    summary = import_financebench(
        source_path=source_path,
        output_dir=output_root / domain,
        domain=domain,
        limit=limit,
        overwrite=overwrite,
    )
    console.print(f"[green]wrote[/green] FinanceBench data for {summary.rows_written} questions to {summary.path}")
    for warning in summary.warnings:
        console.print(f"  [yellow]warning[/yellow] {warning}")


def show_summary(path: Path) -> None:
    rows = read_summary(path)
    table = Table(title=f"RAG Benchmark Summary: {path}")
    table.add_column("Track")
    table.add_column("Domain")
    table.add_column("System")
    table.add_column("Embedding")
    table.add_column("Generator")
    table.add_column("Judge")
    table.add_column("Answer", justify="right")
    table.add_column("Evidence", justify="right")
    table.add_column("Precision", justify="right")
    table.add_column("Citation", justify="right")
    table.add_column("Latency ms", justify="right")
    table.add_column("Cost", justify="right")
    table.add_column("Failure", justify="right")
    for row in rows:
        table.add_row(
            row.get("track", "end-to-end"),
            row["domain"],
            row["system_id"],
            row.get("embedding_model", "none"),
            row.get("generator_model", "unknown"),
            row.get("judge_model", "unknown"),
            f"{float(row['answer_correctness']):.3f}",
            f"{float(row['evidence_recall']):.3f}",
            f"{float(row['context_precision']):.3f}",
            f"{float(row['citation_validity']):.3f}",
            f"{float(row['query_wall_time_ms']):.2f}",
            f"{float(row['estimated_cost']):.6f}",
            f"{float(row['failure_rate']):.3f}",
        )
    console.print(table)


def show_promptfoo_summary(rows: list[dict]) -> None:
    table = Table(title="Promptfoo Quality Gate Summary")
    table.add_column("Domain")
    table.add_column("System")
    table.add_column("Pass", justify="right")
    table.add_column("Answer", justify="right")
    table.add_column("Evidence", justify="right")
    table.add_column("Citation", justify="right")
    for row in rows:
        table.add_row(
            row["domain"],
            row["system_id"],
            f"{float(row['pass_rate']):.3f}",
            f"{float(row['answer_correctness']):.3f}",
            f"{float(row['evidence_recall']):.3f}",
            f"{float(row['citation_validity']):.3f}",
        )
    console.print(table)


def update_dashboard_with_promptfoo(results_dir: Path, analysis) -> None:
    summary_rows = read_csv(results_dir / "summary.csv")
    category_rows = read_csv(results_dir / "category_summary.csv")
    recommendation_rows = read_csv(results_dir / "recommendations.csv")
    axis_rows = read_csv(results_dir / "axis_leaderboard.csv")
    judge_rows = read_csv(results_dir / "judge_audit.csv")
    result_rows = read_csv(results_dir / "results.csv")
    readiness_path = results_dir / "production_readiness.csv"
    if readiness_path.exists():
        readiness_rows = read_csv(readiness_path)
    else:
        readiness_rows = build_production_readiness(
            summary_rows,
            category_rows,
            result_rows,
            source="benchmark",
        )
    run_id = result_rows[0].get("run_id", "latest") if result_rows else "latest"
    write_dashboard(
        results_dir / "dashboard.html",
        summary_rows=summary_rows,
        category_rows=category_rows,
        recommendation_rows=recommendation_rows,
        axis_leaderboard_rows=axis_rows,
        judge_audit_rows=judge_rows,
        production_readiness_rows=readiness_rows,
        promptfoo_summary_rows=analysis.summary_rows,
        promptfoo_category_rows=analysis.category_rows,
        promptfoo_readiness_rows=analysis.readiness_rows,
        result_rows=result_rows,
        run_id=run_id,
    )


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    app()
