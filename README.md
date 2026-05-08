# RAG Benchmark

[English](README.md) | [한국어](README.ko.md)

Operational benchmark for comparing retrieval-augmented generation approaches,
including the open-source VectifyAI PageIndex repository.

This project is not a leaderboard-first benchmark. The goal is to answer a
practical production question:

> Which RAG implementation should we operate for a given document domain,
> quality target, latency budget, cost budget, and maintenance profile?

## Initial Scope

Domains:

- `finance`: financial filings and report-style documents.
- `financebench-open-source`: PatronusAI FinanceBench open-source sample, 150 questions.
- `general-docs`: general PDF, technical, policy, and knowledge-base documents.

PageIndex scope:

- Open-source PageIndex only.
- No PageIndex Cloud, hosted Chat API, hosted OCR, or hosted MCP in the first
  benchmark track.

Comparison goal:

- Product operations comparison, not only retrieval accuracy.
- Measure ingestion, indexing, query quality, latency, cost, failure modes,
  citation quality, and maintenance complexity.

## Planned Baselines

MVP systems:

- `bm25`: lexical sparse retrieval.
- `dense-vector`: chunk, embed, vector search.
- `hybrid`: sparse plus dense retrieval.
- `hybrid-rerank`: hybrid retrieval plus reranking.
- `parent-child`: small chunks for retrieval, larger parent context for answer generation.
- `pageindex-oss`: PageIndex open-source tree index plus agent/tool retrieval.

Expansion systems:

- `raptor`: recursive abstractive tree retrieval.
- `graphrag`: graph/community retrieval for corpus-level questions.
- `agentic-vector`: iterative query decomposition over vector/hybrid retrieval.

## Project Layout

- `docs/`: design notes and implementation plan. Korean versions use `.ko.md`.
- `configs/`: benchmark configuration.
- `src/rag_benchmark/`: future benchmark harness package.
- `scripts/`: future command-line helpers.
- `data/raw/`: downloaded or user-provided source documents.
- `data/processed/`: normalized extracts, gold labels, and intermediate artifacts.
- `runs/`: per-run traces and raw outputs.
- `results/`: aggregated scorecards and reports.

## First Milestone

Build a thin, reproducible benchmark harness that can run the same question set
against six MVP systems across both domains, then produce a scorecard covering:

- retrieval evidence recall and precision
- answer correctness
- groundedness and citation validity
- latency and cost
- ingestion/indexing time
- failure rate and operational notes

Status: complete for the local fixture benchmark.
The packaged fixtures are now intentionally discriminative: both default domains
separate systems on answer quality, evidence recall, and failure rate.

## Quick Start

Run the full MVP benchmark:

```bash
uv run rag-benchmark run --top-k 4
```

Print the latest summary:

```bash
uv run rag-benchmark summary
```

Print the latest report:

```bash
uv run rag-benchmark report
```

Print the latest Korean report:

```bash
uv run rag-benchmark report-ko
```

Print the operations recommendation ranking:

```bash
uv run rag-benchmark recommend
```

Audit whether the benchmark actually separated systems:

```bash
uv run rag-benchmark discrimination
```

Validate document/question/evidence labels:

```bash
uv run rag-benchmark validate-data --top-k 4
```

Run tests:

```bash
uv run --extra dev pytest -q
```

## Current Outputs

Each run writes:

- `runs/<run_id>/summary.csv`: domain/system scorecard.
- `runs/<run_id>/category_summary.csv`: domain/category/system scorecard.
- `runs/<run_id>/recommendations.csv`: quality/efficiency/stability recommendation ranking.
- `runs/<run_id>/failure_summary.csv`: failure type counts by domain/system.
- `runs/<run_id>/results.csv`: per-question metrics.
- `runs/<run_id>/traces.jsonl`: full retrieval, answer, and evaluation traces.
- `runs/<run_id>/report.md`: operations-oriented markdown report.
- `runs/<run_id>/report.ko.md`: Korean operations-oriented markdown report.

The latest run is also copied to:

- `results/summary.csv`
- `results/category_summary.csv`
- `results/recommendations.csv`
- `results/failure_summary.csv`
- `results/results.csv`
- `results/report.md`
- `results/report.ko.md`

## How To Interpret Results

Use the benchmark as an operations decision aid:

- Choose `bm25` when exact terms, speed, and low cost matter most.
- Choose `hybrid` or `hybrid-rerank` when semantic matching and exact terms both matter.
- Choose `parent-child` when chunk-level search works but answer generation needs more surrounding context.
- Choose `pageindex-oss` when document structure, sections, and multi-document navigation matter.

Do not treat fixture scores as production proof. They verify the harness and show
failure modes. Real decisions require adding representative documents, questions,
gold answers, and evidence labels.

## Adding Data

You can import local Markdown or text documents:

```bash
uv run rag-benchmark import-docs ~/my-docs --domain my-domain
```

Then import questions from JSONL, JSON, or CSV:

```bash
uv run rag-benchmark import-questions ~/my-questions.jsonl --domain my-domain
```

FinanceBench's open-source JSONL/Hugging Face schema has a dedicated importer:

```bash
uv run rag-benchmark import-financebench ~/financebench_merged.jsonl --domain finance
```

That importer creates evidence-page documents from FinanceBench labels. It is a
good OSS smoke test, but full-PDF ingestion is still needed for a harder
production retrieval evaluation.

The repository also includes a normalized `financebench-open-source` fixture
created from the public 150-question FinanceBench sample. The closed 10k+
FinanceBench dataset is not bundled.

This writes:

```text
data/fixtures/<domain>/documents.jsonl
data/fixtures/<domain>/questions.jsonl
```

Then add the domain to `configs/benchmark.yaml`.

Questions should include evidence coordinates whenever possible. JSONL rows can
look like this:

```json
{
  "question_id": "example",
  "domain": "general-docs",
  "category": "direct_lookup",
  "question": "What is the API rate limit?",
  "answer": "120 requests per minute per tenant",
  "answer_aliases": ["120 requests per minute"],
  "evidence": [{"doc_id": "platform_runbook", "page": 4, "section_id": "api_limits"}],
  "no_answer": false
}
```

The benchmark is intentionally evidence-first. Without evidence labels, retrieval
quality and citation validity cannot be measured reliably.

CSV question imports support the columns `question_id`, `category`, `question`,
`answer`, `answer_aliases`, `evidence_json`, `no_answer`, and `notes`.
`answer_aliases` can be separated with `|`; `evidence_json` should be a JSON
list of evidence objects.
