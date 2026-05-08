# 구현 계획

[English](IMPLEMENTATION_PLAN.md) | [한국어](IMPLEMENTATION_PLAN.ko.md)

Date: 2026-05-07

## 결정 사항

- 도메인: `finance`, `financebench-open-source`, `general-docs`를 구현합니다.
- PageIndex 범위: OSS only.
- 벤치마크 목적: 제품 운영 관점 비교.
- 첫 구현 언어: Python.
- 첫 평가 방식: offline, reproducible, trace-heavy benchmark run.
- 모델 비교 방식: retrieval-only, generator-oracle, end-to-end track을 분리합니다.
- 평가 모델 방식: judge/evaluator 신뢰성을 product stack 품질과 분리합니다.

## 설계 원칙

RAG 비교에서 자주 섞이는 세 가지 관심사를 분리합니다.

1. 문서 준비: parsing, OCR, table handling, metadata extraction.
2. 검색과 orchestration: BM25, dense, hybrid, rerank, tree search, agent.
3. 답변 생성: 가능한 경우 common model과 common answer prompt 사용.
4. 평가 모델: judge/evaluator behavior, agreement, bias risk.

공정한 진단을 위해 모든 run은 failure를 분류할 수 있을 만큼 trace를 남겨야 합니다. 예를 들어 parsing, retrieval, ranking, orchestration, context packing, generation failure를 구분할 수 있어야 합니다.

## 벤치마크 트랙

### Track A: Controlled

목적: confounder를 줄이고 retrieval/orchestration method를 비교합니다.

- 모든 시스템에 동일한 normalized text와 page metadata를 사용합니다.
- 동일한 generator model과 answer prompt를 사용합니다.
- retrieval/orchestration module만 바꿉니다.
- algorithmic tradeoff를 이해하는 데 적합합니다.

### Track B: Native Operations

목적: 각 시스템을 의도된 운영 방식대로 썼을 때의 성능을 비교합니다.

- 각 시스템은 권장 ingestion strategy를 사용할 수 있습니다.
- PageIndex OSS는 자체 tree generation flow를 사용할 수 있습니다.
- Vector system은 선택한 parser/chunker stack을 사용할 수 있습니다.
- product-style decision에 적합합니다.

## MVP 시스템

### bm25

- normalized page 또는 section을 ingest합니다.
- lexical search index를 만듭니다.
- top-k context를 검색합니다.
- common answer prompt로 답변을 생성합니다.

숫자, exact term, header, named entity에 강한 저비용 baseline입니다.

### dense-vector

- 문서를 chunking합니다.
- chunk embedding을 만듭니다.
- local vector index에 저장합니다.
- semantic similarity로 top-k를 검색합니다.

naive RAG baseline으로 사용합니다.

### hybrid

- BM25와 dense retrieval을 함께 실행합니다.
- reciprocal rank fusion 또는 weighted fusion으로 결과를 병합합니다.
- top context를 common answer prompt에 전달합니다.

실무 default baseline으로 적합합니다.

### hybrid-rerank

- hybrid로 넓은 candidate set을 가져옵니다.
- cross-encoder 또는 local/hosted reranker로 candidate를 재정렬합니다.
- top context를 answer generation에 사용합니다.

품질 향상과 추가 latency/cost의 tradeoff를 측정합니다.

### parent-child

- 작은 child chunk를 retrieval에 사용합니다.
- child chunk를 더 큰 parent section/page로 매핑합니다.
- parent context로 답변을 생성합니다.

local context 보존이 naive chunk retrieval보다 나은지 확인합니다.

### pageindex-oss

- VectifyAI/PageIndex 오픈소스 repo를 기준으로 합니다.
- PDF 또는 Markdown에서 hierarchical tree index를 생성합니다.
- PageIndex tool concept을 모델링합니다.
  - `get_document`
  - `get_document_structure`
  - `get_page_content`
- agent 또는 deterministic tree-selection wrapper로 좁은 page range를 가져옵니다.

중요: 첫 구현에서는 PageIndex Cloud, hosted OCR, hosted Retrieval API, hosted MCP를 제외합니다.

## 확장 시스템

### raptor

recursive clustering과 abstractive summary를 사용해 PageIndex-style tree retrieval과 비교합니다.

### graphrag

corpus-level theme, entity relationship, global summarization question에 사용합니다. single-document factual QA에 과도하게 가중하지 않습니다.

### agentic-vector

vector 또는 hybrid retrieval 위에서 query decomposition, iterative retrieval, self-checking을 수행합니다. agentic orchestration과 underlying index type을 분리해서 봅니다.

## 도메인 계획

### finance

후보 source:

- FinanceBench open-source sample.

장점:

- page/filing citation evaluation이 가능합니다.
- numeric, table-like, evidence-grounded question을 포함합니다.

위험:

- PDF table parsing이 결과를 지배할 수 있습니다.
- 일부 질문은 retrieval뿐 아니라 calculation이 필요합니다.

### general-docs

후보 source:

- Technical PDF.
- Policy manual.
- Product documentation.
- Markdown knowledge-base export.

장점:

- finance 밖의 production behavior를 테스트합니다.
- single-document와 multi-document category를 모두 포함할 수 있습니다.

위험:

- gold answer와 evidence label을 직접 만들어야 합니다.
- 문서 다양성이 초기 결과를 noisy하게 만들 수 있습니다.

## 질문 카테고리

- direct_lookup: 한 passage 또는 page에 답이 있습니다.
- section_navigation: 올바른 section을 찾는 것이 핵심입니다.
- multi_section: 한 문서의 여러 부분을 결합해야 합니다.
- multi_document: 여러 문서를 비교하거나 결합해야 합니다.
- table_numeric: table 또는 numeric evidence가 필요합니다.
- calculation: 검색한 fact로 계산이 필요합니다.
- no_answer: 답이 문서에 없고 abstain해야 합니다.
- global_summary: corpus-level 또는 whole-document synthesis입니다.

## Metric

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

## 데이터 모델

Core entity:

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

질문별 최소 trace:

- run_id
- system_id
- domain
- question_id
- retrieved context: document id, page, section, score, rank
- final packed prompt context
- answer text
- emitted citation
- timing and token counter
- error or warning

## 구현 단계

### Phase 0: Project Skeleton

- project folder 생성.
- implementation plan 추가.
- initial benchmark config 추가.
- minimal Python package skeleton 추가.

Status: complete.

### Phase 1: Dataset Normalization

- common document/page/section JSONL schema 구현.
- general document domain용 local Markdown/text importer 추가.
- gold answer와 evidence label용 JSONL/JSON/CSV question importer 추가.
- evidence-page document와 label을 생성하는 FinanceBench JSONL importer 추가.
- document/page coordinate 기준 evidence normalization 추가.

Status: local/imported text fixture와 FinanceBench evidence-page import 기준 complete. Full PDF/table-native FinanceBench ingestion은 production-readiness expansion으로 남아 있습니다.

### Phase 2: Baseline Harness

- common retriever interface 구현.
- BM25 baseline 구현.
- dense vector baseline 구현.
- common answer generation wrapper 구현.
- 모든 question trace 저장.

### Phase 3: Practical RAG Baselines

- hybrid retrieval 구현.
- rerank stage 구현.
- parent-child retrieval 구현.
- latency/cost instrumentation 추가.

### Phase 4: PageIndex OSS

- PageIndex OSS를 external dependency로 vendor 또는 install.
- PageIndex workspace/index output 주변 adapter 구현.
- agent/tool retrieval path 구현.
- PageIndex-specific trace field 추가:
  - tree size
  - selected node ids
  - fetched page ranges
  - tool call count

### Phase 5: Evaluation

- retrieval metric 추가.
- answer scoring 추가.
- citation validation 추가.
- failure taxonomy 추가.
- domain, system, question category별 scorecard 생성.
- embedding profile과 generator profile 축 추가.
- retrieval-only와 oracle-context generator track 추가.
- judge/evaluator profile 축과 judge reliability audit 추가.

Status: deterministic local profile과 judge audit profile 기준 complete.

### Phase 6: Operations Report

- product-style report 생성:
  - domain별 recommended default
  - RAG, embedding, generator, judge를 축별로 분리한 최고 후보
  - judge/evaluator audit
  - cost/latency tradeoff
  - failure mode
  - maintenance note
  - 각 접근법을 쓰지 말아야 하는 경우

Status: 영어/한국어 report와 정적 시각화 dashboard 기준 complete.

### Phase 7: Real Model Adapter Expansion

- deterministic embedding proxy를 optional local model adapter로 교체 가능하게 만들기.
- config flag 뒤에 sentence-transformers 또는 동급 OSS backend 추가.
- 하드웨어가 있을 때 open-weight generator adapter 추가.
- deterministic profile은 빠른 CI와 smoke-test mode로 유지.
- LLM-as-judge 결과를 신뢰하기 전에 human-labeled judge validation set 추가.

## 다음 작업 후보

1. table-native extraction을 포함한 full-PDF FinanceBench ingestion 추가.
2. 최소 두 개 이상의 실제 OSS embedding adapter 추가.
3. open-weight instruction model용 optional local generator adapter 추가.
4. 실제 judge/evaluator adapter와 human-agreement check 추가.
5. 주요 도메인별 100개 이상 labeled question으로 사용자 문서 run 확장.
6. 실제 모델 run 기준 p95 latency와 memory tracking 추가.
