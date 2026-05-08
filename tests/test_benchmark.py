import json
from pathlib import Path

import yaml

from rag_benchmark.datasets import load_domain, read_jsonl
from rag_benchmark.discrimination import build_discrimination_report
from rag_benchmark.embeddings import embedding_counter
from rag_benchmark.importers import import_financebench, import_questions, import_text_documents
from rag_benchmark.promptfoo import call_promptfoo_provider, export_promptfoo_bundle
from rag_benchmark.runner import read_summary, run_benchmark
from rag_benchmark.schemas import Document
from rag_benchmark.text import tokenize
from rag_benchmark.validation import validate_domain_data


ROOT = Path(__file__).resolve().parents[1]


def test_fixture_domains_load() -> None:
    finance_docs, finance_questions = load_domain(ROOT, "finance")
    financebench_docs, financebench_questions = load_domain(ROOT, "financebench-open-source")
    general_docs, general_questions = load_domain(ROOT, "general-docs")

    assert len(finance_docs) == 4
    assert len(financebench_docs) == 84
    assert len(general_docs) == 5
    assert len(finance_questions) >= 19
    assert len(financebench_questions) == 150
    assert len(general_questions) >= 20


def test_semantic_token_aliases() -> None:
    assert "rate_limit" in tokenize("API throttle quota limit", semantic=True)
    assert "recovery" in tokenize("RTO recovery target", semantic=True)
    assert "capital_expenditure" in tokenize("capex property equipment additions", semantic=True)
    assert "export_window" in tokenize("portability package bundle expires", semantic=True)


def test_embedding_profiles_shape_tokens_differently() -> None:
    text = "Revenue increased 12% while cash and debt changed."
    e5 = embedding_counter(text, "e5-large-v2-proxy")
    bge = embedding_counter(text, "bge-m3-proxy")
    finance = embedding_counter(text, "finance-e5-proxy")

    assert e5["revenue"] > 0
    assert bge["percentage"] > e5["percentage"]
    assert finance["revenue"] > e5["revenue"]


def test_full_benchmark_smoke(tmp_path: Path) -> None:
    out_dir = run_benchmark(
        root=ROOT,
        config_path=ROOT / "configs" / "benchmark.yaml",
        top_k=4,
        output_dir=tmp_path / "run",
        copy_to_results=False,
    )
    summary_rows = read_summary(out_dir / "summary.csv")
    assert len(summary_rows) == 531

    rows_by_key = {
        (
            row["track"],
            row["domain"],
            row["system_id"],
            row["embedding_model"],
            row["generator_model"],
            row["judge_model"],
        ): row
        for row in summary_rows
    }
    assert float(
        rows_by_key[("end-to-end", "finance", "bm25", "none", "reasoning-oss-llm", "exact-match-gold")][
            "answer_correctness"
        ]
    ) < float(
        rows_by_key[
            (
                "end-to-end",
                "finance",
                "pageindex-oss",
                "bge-m3-proxy",
                "reasoning-oss-llm",
                "exact-match-gold",
            )
        ]["answer_correctness"]
    )
    assert float(
        rows_by_key[
            (
                "retrieval-only",
                "general-docs",
                "pageindex-oss",
                "bge-m3-proxy",
                "retrieval-probe",
                "exact-match-gold",
            )
        ]["evidence_recall"]
    ) >= float(
        rows_by_key[
            ("retrieval-only", "general-docs", "bm25", "none", "retrieval-probe", "exact-match-gold")
        ]["evidence_recall"]
    )
    assert (out_dir / "category_summary.csv").exists()
    assert (out_dir / "recommendations.csv").exists()
    assert (out_dir / "axis_leaderboard.csv").exists()
    assert (out_dir / "judge_audit.csv").exists()
    assert (out_dir / "failure_summary.csv").exists()
    assert (out_dir / "report.md").exists()
    assert (out_dir / "report.ko.md").exists()
    assert (out_dir / "dashboard.html").exists()
    assert "RAG 벤치마크 리포트" in (out_dir / "report.ko.md").read_text(encoding="utf-8")
    assert "RAG Benchmark Dashboard" in (out_dir / "dashboard.html").read_text(encoding="utf-8")
    assert "Judge Model Audit" in (out_dir / "report.md").read_text(encoding="utf-8")

    discrimination_report = build_discrimination_report(out_dir)
    assert "`end-to-end` / `finance` / `exact-match-gold`: **strongly discriminative**" in discrimination_report
    assert (
        "`end-to-end` / `financebench-open-source` / `exact-match-gold`: **moderately discriminative**"
        in discrimination_report
    )
    assert "`retrieval-only` / `general-docs` / `exact-match-gold`: **strongly discriminative**" in discrimination_report


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


def test_promptfoo_export_and_provider(tmp_path: Path) -> None:
    out_dir = tmp_path / "promptfoo"
    summary = export_promptfoo_bundle(
        root=ROOT,
        config_path=ROOT / "configs" / "benchmark.yaml",
        output_dir=out_dir,
        domains=["finance"],
        systems=["hybrid", "pageindex-oss"],
        embeddings=["bge-m3-proxy"],
        generators=["reasoning-oss-llm"],
        judges=["exact-match-gold"],
        tracks=["end-to-end"],
        max_questions_per_domain=2,
    )

    assert summary.providers == 2
    assert summary.tests == 2
    assert summary.config_path.exists()
    assert summary.tests_path.exists()
    assert summary.provider_path.exists()
    exported_config = yaml.safe_load(summary.config_path.read_text(encoding="utf-8"))
    exported_tests = yaml.safe_load(summary.tests_path.read_text(encoding="utf-8"))
    assert exported_config["providers"][0]["id"] == "file://./rag_benchmark_provider.py"
    assert exported_config["defaultTest"]["assert"][1]["metric"] == "answer_correctness"
    assert exported_tests[0]["vars"]["question_id"] == "fin_direct_revenue"

    provider_response = call_promptfoo_provider(
        "What was ACME Robotics revenue in fiscal 2025?",
        {
            "config": {
                "basePath": str(out_dir),
                "repoRoot": str(ROOT),
                "configPath": str(ROOT / "configs" / "benchmark.yaml"),
                "track": "end-to-end",
                "system": "hybrid",
                "embedding": "bge-m3-proxy",
                "generator": "reasoning-oss-llm",
                "judge": "exact-match-gold",
                "topK": 4,
            }
        },
        {
            "vars": {
                "domain": "finance",
                "question_id": "fin_direct_revenue",
                "query": "What was ACME Robotics revenue in fiscal 2025?",
            }
        },
    )
    payload = json.loads(provider_response["output"])
    assert payload["answer"] == "$12.4 billion"
    assert payload["metrics"]["answer_correctness"] == 1.0
    assert payload["metrics"]["evidence_recall"] == 1.0
    assert provider_response["tokenUsage"]["total"] > 0
