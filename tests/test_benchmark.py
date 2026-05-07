from pathlib import Path

from rag_benchmark.datasets import load_domain, read_jsonl
from rag_benchmark.discrimination import build_discrimination_report
from rag_benchmark.importers import import_financebench, import_questions, import_text_documents
from rag_benchmark.runner import read_summary, run_benchmark
from rag_benchmark.schemas import Document
from rag_benchmark.text import tokenize
from rag_benchmark.validation import validate_domain_data


ROOT = Path(__file__).resolve().parents[1]


def test_fixture_domains_load() -> None:
    finance_docs, finance_questions = load_domain(ROOT, "finance")
    general_docs, general_questions = load_domain(ROOT, "general-docs")

    assert len(finance_docs) == 4
    assert len(general_docs) == 5
    assert len(finance_questions) >= 19
    assert len(general_questions) >= 20


def test_semantic_token_aliases() -> None:
    assert "rate_limit" in tokenize("API throttle quota limit", semantic=True)
    assert "recovery" in tokenize("RTO recovery target", semantic=True)
    assert "capital_expenditure" in tokenize("capex property equipment additions", semantic=True)
    assert "export_window" in tokenize("portability package bundle expires", semantic=True)


def test_full_benchmark_smoke(tmp_path: Path) -> None:
    out_dir = run_benchmark(
        root=ROOT,
        config_path=ROOT / "configs" / "benchmark.yaml",
        top_k=4,
        output_dir=tmp_path / "run",
    )
    summary_rows = read_summary(out_dir / "summary.csv")
    assert len(summary_rows) == 12

    rows_by_key = {(row["domain"], row["system_id"]): row for row in summary_rows}
    assert float(rows_by_key[("finance", "bm25")]["answer_correctness"]) < float(
        rows_by_key[("finance", "pageindex-oss")]["answer_correctness"]
    )
    assert float(rows_by_key[("general-docs", "pageindex-oss")]["answer_correctness"]) >= float(
        rows_by_key[("general-docs", "bm25")]["answer_correctness"]
    )
    assert (out_dir / "category_summary.csv").exists()
    assert (out_dir / "recommendations.csv").exists()
    assert (out_dir / "failure_summary.csv").exists()
    assert (out_dir / "report.md").exists()
    assert (out_dir / "report.ko.md").exists()
    assert "RAG 벤치마크 리포트" in (out_dir / "report.ko.md").read_text(encoding="utf-8")

    discrimination_report = build_discrimination_report(out_dir)
    assert "`finance`: **strongly discriminative**" in discrimination_report
    assert "`general-docs`: **strongly discriminative**" in discrimination_report


def test_import_text_documents_and_questions(tmp_path: Path) -> None:
    docs_dir = tmp_path / "source_docs"
    docs_dir.mkdir()
    (docs_dir / "runbook.md").write_text(
        "# API Limits\n\nRequests are limited to 120 per minute.\n\n"
        "## Bursts\n\nShort bursts are allowed for five seconds.\n",
        encoding="utf-8",
    )

    fixtures_dir = tmp_path / "data" / "fixtures" / "ops"
    doc_summary = import_text_documents(
        source_dir=docs_dir,
        output_dir=fixtures_dir,
        domain="ops",
        page_paragraphs=1,
    )
    assert doc_summary.rows_written == 1

    documents = [Document.model_validate(row) for row in read_jsonl(fixtures_dir / "documents.jsonl")]
    doc_id = documents[0].doc_id

    questions_jsonl = tmp_path / "questions.jsonl"
    questions_jsonl.write_text(
        (
            '{"question_id":"q1","category":"direct_lookup",'
            '"question":"What is the API limit?","answer":"120 per minute",'
            f'"evidence":[{{"doc_id":"{doc_id}","page":1}}]}}\n'
        ),
        encoding="utf-8",
    )
    question_summary = import_questions(source_path=questions_jsonl, output_dir=fixtures_dir, domain="ops")
    assert question_summary.rows_written == 1

    report = validate_domain_data(tmp_path, "ops", top_k=4)
    assert report.ok
    assert report.questions == 1


def test_import_financebench_schema(tmp_path: Path) -> None:
    source = tmp_path / "financebench.jsonl"
    source.write_text(
        (
            '{"financebench_id":"financebench_id_1","company":"ExampleCo",'
            '"doc_name":"EXAMPLE_2024_10K","question_type":"metrics-generated",'
            '"question_reasoning":"Information extraction",'
            '"question":"What was revenue?","answer":"$10.00",'
            '"evidence":[{"doc_name":"EXAMPLE_2024_10K","evidence_page_num":4,'
            '"evidence_text_full_page":"Revenue was $10.00."}]}\n'
        ),
        encoding="utf-8",
    )
    fixtures_dir = tmp_path / "data" / "fixtures" / "finance"
    summary = import_financebench(source_path=source, output_dir=fixtures_dir)
    assert summary.rows_written == 1

    documents, questions = load_domain(tmp_path, "finance")
    assert documents[0].pages[0].page == 5
    assert questions[0].evidence[0].page == 5
    assert validate_domain_data(tmp_path, "finance").ok
