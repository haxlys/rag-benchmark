# Implementation Plan

[English](IMPLEMENTATION_PLAN.md) | [한국어](IMPLEMENTATION_PLAN.ko.md)

Date: 2026-05-07

## Decisions

- Domains: implement `finance`, `financebench-open-source`, and `general-docs`.
- PageIndex scope: OSS only.
- Benchmark objective: product operations comparison.
- First implementation language: Python.
- First evaluation style: offline, reproducible, trace-heavy benchmark runs.
- Model comparison style: separate retrieval-only, generator-oracle, and end-to-end tracks.

## Design Principle

Separate three concerns that are often mixed together in RAG comparisons:

1. Document preparation: parsing, OCR, table handling, metadata extraction.
2. Retrieval and orchestration: BM25, dense, hybrid, rerank, tree search, agents.
3. Answer generation: common model and common answer prompt where possible.

For fair diagnosis, every run must record enough trace data to classify failures
as parsing, retrieval, ranking, orchestration, context packing, or generation
failures.

## Benchmark Tracks

### Track A: Controlled

Purpose: compare retrieval/orchestration methods with fewer confounders.

- Use the same normalized text and page metadata for all systems.
- Use the same generator model and answer prompt.
- Vary only the retrieval/orchestration module.
- Best for understanding algorithmic tradeoffs.

### Track B: Native Operations

Purpose: compare how a system performs when operated as intended.

- Each system can use its recommended ingestion strategy.
- PageIndex OSS can use its own tree generation flow.
- Vector systems can use their chosen parser/chunker stack.
- Best for product-style decisions.

## MVP Systems

### bm25

- Ingest normalized pages or sections.
- Index with lexical search.
- Retrieve top-k contexts.
- Generate answer with the common answer prompt.

Use as a cheap and surprisingly strong baseline for numbers, exact terms,
headers, and named entities.

### dense-vector

- Chunk documents.
- Embed chunks.
- Store in a local vector index.
- Retrieve top-k by semantic similarity.

Use as the naive RAG baseline.

### hybrid

- Run BM25 and dense retrieval.
- Merge results with reciprocal rank fusion or weighted fusion.
- Send top contexts to the common answer prompt.

Use as the practical default baseline.

### hybrid-rerank

- Retrieve a wider candidate set via hybrid.
- Rerank candidates with a cross-encoder or hosted/local reranker.
- Pack top contexts for generation.

Measure quality improvement against added latency and cost.

### parent-child

- Create small child chunks for retrieval.
- Map child chunks back to larger parent sections/pages.
- Generate from parent context.

Use to test whether preserving local context beats naive chunk retrieval.

### pageindex-oss

- Use VectifyAI/PageIndex open-source repo.
- Generate hierarchical tree indexes for PDFs or Markdown.
- Expose PageIndex tools:
  - `get_document`
  - `get_document_structure`
  - `get_page_content`
- Use an agent or deterministic tree-selection wrapper to retrieve tight page ranges.

Important: keep PageIndex Cloud, hosted OCR, hosted Retrieval API, and hosted MCP
out of the first implementation.

## Expansion Systems

### raptor

Use recursive clustering and abstractive summaries to test tree retrieval against
PageIndex-style document trees.

### graphrag

Use graph/community retrieval for questions about corpus-level themes, entity
relationships, and global summarization. This should not be over-weighted for
single-document factual QA.

### agentic-vector

Use query decomposition, iterative retrieval, and self-checking over vector or
hybrid retrieval. This helps separate "agentic orchestration" from the underlying
index type.

## Domain Plan

### finance

Candidate source:

- FinanceBench open-source sample.

Expected strengths:

- Page/filing citation evaluation is feasible.
- Financial questions include numeric, table-like, and evidence-grounded tasks.

Risks:

- PDF table parsing can dominate results.
- Some questions require calculations, not only retrieval.

### general-docs

Candidate sources:

- Technical PDFs.
- Policy manuals.
- Product documentation.
- Markdown knowledge-base exports.

Expected strengths:

- Tests broader production behavior beyond finance.
- Can include single-document and multi-document categories.

Risks:

- Need to create our own gold answers and evidence labels.
- Document diversity can make early results noisy.

## Question Categories

- direct_lookup: answer is in one tight passage or page.
- section_navigation: answer depends on finding the right section.
- multi_section: answer requires combining multiple parts of one document.
- multi_document: answer requires comparing across documents.
- table_numeric: answer requires table or numeric evidence.
- calculation: answer requires arithmetic using retrieved facts.
- no_answer: answer is not present and system should abstain.
- global_summary: corpus-level or whole-document synthesis.

## Metrics

Retrieval:

- hit_rate_at_k
- evidence_recall_at_k
- context_precision_at_k
- mrr
- ndcg
- retrieved_token_count

Answer:

- exact_or_numeric_match where applicable
- answer_correctness
- faithfulness
- groundedness
- citation_validity
- abstention_correctness

Operations:

- ingestion_wall_time
- index_wall_time
- query_wall_time_p50
- query_wall_time_p95
- llm_input_tokens
- llm_output_tokens
- embedding_tokens
- reranker_calls
- estimated_cost
- index_size_bytes
- failure_rate

Diagnostics:

- parse_failure
- retrieval_miss
- bad_ranking
- context_bloat
- generation_hallucination
- citation_mismatch
- timeout
- tool_or_json_error

## Data Model

Core entities:

- Document
- Page
- Section
- Question
- Evidence
- SystemConfig
- RetrievalTrace
- AnswerTrace
- EvaluationResult
- RunSummary

Minimum persisted trace per question:

- run_id
- system_id
- domain
- question_id
- retrieved contexts with document id, page, section, score, and rank
- final packed prompt context
- answer text
- citations emitted by the system
- timing and token counters
- errors or warnings

## Implementation Phases

### Phase 0: Project Skeleton

- Create project folder.
- Add implementation plan.
- Add initial benchmark config.
- Add minimal Python package skeleton.

Status: complete.

### Phase 1: Dataset Normalization

- Implement common document/page/section JSONL schema.
- Add local Markdown/text importer for general document domains.
- Add JSONL/JSON/CSV question importer for gold answers and evidence labels.
- Add FinanceBench JSONL importer that creates evidence-page documents and labels.
- Add evidence normalization to document/page coordinates.

Status: complete for local/imported text fixtures and FinanceBench evidence-page
imports. Full PDF/table-native FinanceBench ingestion remains a
production-readiness expansion.

### Phase 2: Baseline Harness

- Implement common retriever interface.
- Implement BM25 baseline.
- Implement dense vector baseline.
- Implement common answer generation wrapper.
- Persist traces for every question.

### Phase 3: Practical RAG Baselines

- Implement hybrid retrieval.
- Implement rerank stage.
- Implement parent-child retrieval.
- Add latency/cost instrumentation.

### Phase 4: PageIndex OSS

- Vendor or install PageIndex OSS as an external dependency.
- Build adapter around PageIndex workspace/index output.
- Implement agent/tool retrieval path.
- Add PageIndex-specific trace fields:
  - tree size
  - selected node ids
  - fetched page ranges
  - tool call count

### Phase 5: Evaluation

- Add retrieval metrics.
- Add answer scoring.
- Add citation validation.
- Add failure taxonomy.
- Generate scorecards by domain, system, and question category.
- Add embedding profile and generator profile axes.
- Add retrieval-only and oracle-context generator tracks.

Status: complete for deterministic local profiles.

### Phase 6: Operations Report

- Produce product-style report:
  - recommended default per domain
  - cost/latency tradeoffs
  - failure modes
  - maintenance notes
  - when not to use each approach

Status: complete for English/Korean reports and static visual dashboard.

### Phase 7: Real Model Adapter Expansion

- Replace deterministic embedding proxies with optional local model adapters.
- Add sentence-transformers or equivalent OSS backend behind a config flag.
- Add local generator adapters for open-weight models when hardware is available.
- Keep deterministic profiles as fast CI and smoke-test mode.

## Immediate Next Tasks

1. Add full-PDF FinanceBench ingestion, including table-native extraction.
2. Add actual OSS embedding adapters for at least two open-weight models.
3. Add optional local generator adapters for open-weight instruction models.
4. Expand user-document import runs with 100+ labeled questions per major domain.
5. Add deployment-oriented p95 latency and memory tracking for real model runs.
