# Operating Guide

[English](OPERATING_GUIDE.md) | [한국어](OPERATING_GUIDE.ko.md)

## Purpose

This benchmark helps decide which RAG pattern is appropriate for a practical
document product. It is designed to show tradeoffs, not just a single accuracy
number.

## Decision Matrix

| Situation | Recommended Starting Point | Why |
|---|---|---|
| Exact names, numbers, IDs, and short policies | `bm25` | Cheap, fast, strong lexical matching. |
| Mixed exact and semantic questions | `hybrid` | Combines sparse and dense retrieval signals. |
| High quality required and latency budget exists | `hybrid-rerank` | Reranking can improve candidate order at extra cost. |
| Good retrieval but weak answer context | `parent-child` | Retrieves small chunks but answers from larger parent sections. |
| Long structured PDFs and section navigation | `pageindex-oss` | Tree-style section retrieval preserves document structure. |
| Corpus-level themes and entity relationships | future `graphrag` | Graph/community methods fit global questions better. |

## What To Watch

- High answer score with low context precision means the system works but wastes context.
- High evidence recall with low answer score points to generation or context packing issues.
- Low evidence recall points to parser, chunking, retrieval, or query routing problems.
- High citation validity is important for finance, legal, compliance, and support use cases.
- Low query latency can hide high ingestion/indexing cost, especially for tree or graph methods.

## Current Fixture Findings

The included fixture run shows:

- Finance fixture questions are currently easy; all MVP systems retrieve enough evidence.
- General-docs exposes more realistic differences.
- `pageindex-oss` is better on multi-document/section-navigation style retrieval in the fixture.
- `parent-child` keeps context smaller and cheaper, but does not solve broad global-summary questions.
- Top-k matters: global summary questions can fail simply because the context budget cannot include all evidence.

## Running On Your Own Data

1. Import local documents:

   ```bash
   uv run rag-benchmark import-docs ~/my-docs --domain my-domain
   ```

2. Import question labels:

   ```bash
   uv run rag-benchmark import-questions ~/my-questions.jsonl --domain my-domain
   ```

   For FinanceBench open-source JSONL:

   ```bash
   uv run rag-benchmark import-financebench ~/financebench_merged.jsonl --domain finance
   ```

3. Add `my-domain` to `configs/benchmark.yaml`.

4. Validate evidence coordinates:

   ```bash
   uv run rag-benchmark validate-data --domain my-domain --top-k 4
   ```

5. Run and inspect:

   ```bash
   uv run rag-benchmark run --domain my-domain --top-k 4
   uv run rag-benchmark recommend
   uv run rag-benchmark report
   ```

The recommendation ranking combines quality, efficiency, and stability. Use it
to pick a starting point, then inspect `traces.jsonl` for the cases that failed.

## Production Readiness Checklist

Before using results for a real product decision:

- Add at least 100 questions per major domain.
- Label evidence pages or sections for every answerable question.
- Include no-answer questions.
- Include table/numeric and multi-document questions.
- Run with realistic top-k and context-token budgets.
- Review at least 10-20% of answers manually.
- Track parser failures separately from retrieval failures.
- Re-run after changing chunking, parsing, embedding model, or reranker.
