# Operating Guide

[English](OPERATING_GUIDE.md) | [한국어](OPERATING_GUIDE.ko.md)

## Purpose

This benchmark helps decide which RAG pattern is appropriate for a practical
document product. It is designed to show tradeoffs, not just a single accuracy
number.

## Decision Matrix

| Situation | Recommended Starting Point | Why |
|---|---|---|
| Unsure whether retrieval or LLM is the bottleneck | `retrieval-only` then `generator-oracle` | Separates search failures from answer synthesis failures. |
| Exact names, numbers, IDs, and short policies | `bm25` | Cheap, fast, strong lexical matching. |
| Mixed exact and semantic questions | `hybrid` | Combines sparse and dense retrieval signals. |
| High quality required and latency budget exists | `hybrid-rerank` | Reranking can improve candidate order at extra cost. |
| Good retrieval but weak answer context | `parent-child` | Retrieves small chunks but answers from larger parent sections. |
| Long structured PDFs and section navigation | `pageindex-oss` | Tree-style section retrieval preserves document structure. |
| Domain-specific language, especially finance | compare embedding profiles | General embedding leaderboards may not predict domain performance. |
| Corpus-level themes and entity relationships | future `graphrag` | Graph/community methods fit global questions better. |

## What To Watch

- High answer score with low context precision means the system works but wastes context.
- High evidence recall with low answer score points to generation or context packing issues.
- Low evidence recall points to parser, chunking, retrieval, or query routing problems.
- Embedding model changes should first be judged with retrieval-only evidence recall, MRR, and nDCG.
- Generator changes should first be judged with oracle-context runs, where gold evidence is guaranteed.
- High citation validity is important for finance, legal, compliance, and support use cases.
- Low query latency can hide high ingestion/indexing cost, especially for tree or graph methods.

## Current Fixture Findings

The included fixture run shows:

- Both fixture domains are now intentionally discriminative rather than smoke-test easy.
- `financebench-open-source` adds the public 150-question FinanceBench sample for a larger real-data retrieval run.
- The benchmark now runs three tracks: `retrieval-only`, `generator-oracle`, and `end-to-end`.
- End-to-end runs compare RAG method, embedding profile, and generator profile together.
- `results/dashboard.html` provides ranking, scatter, distribution, and category heatmap views.
- Finance includes semantic financial terms such as capex, deferred revenue, backlog, covenant, and lease obligations.
- General-docs includes semantic, section-navigation, multi-section, and multi-document distractors.
- `pageindex-oss`, dense-style retrieval, and reranking separate from BM25 on synonym-heavy and structure-heavy questions.
- `parent-child` keeps context smaller and cheaper, but can miss title-only or synonym-heavy evidence.
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
   uv run rag-benchmark report-ko
   ```

   Open `results/dashboard.html` for the visual dashboard.

The recommendation ranking combines quality, efficiency, and stability. Use it
to pick a starting point, then inspect `traces.jsonl` for the cases that failed.

## Production Readiness Checklist

Before using results for a real product decision:

- Add at least 100 questions per major domain.
- Label evidence pages or sections for every answerable question.
- Include no-answer questions.
- Include table/numeric and multi-document questions.
- Run with realistic top-k and context-token budgets.
- Compare at least two embedding models or profiles before blaming the RAG method.
- Run oracle-context generator checks before blaming the LLM.
- Review at least 10-20% of answers manually.
- Track parser failures separately from retrieval failures.
- Re-run after changing chunking, parsing, embedding model, or reranker.
