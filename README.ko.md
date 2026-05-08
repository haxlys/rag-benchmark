# RAG Benchmark

[English](README.md) | [한국어](README.ko.md)

VectifyAI PageIndex 오픈소스와 전통적인 RAG 방식을 비교하기 위한 운영형 벤치마크입니다.

이 프로젝트는 단순 리더보드가 아닙니다. 목표는 실제 제품 운영에서 다음 질문에 답하는 것입니다.

> 특정 문서 도메인, 품질 목표, 지연시간 예산, 비용 예산, 유지보수 조건에서 어떤 RAG 구현을 운영해야 하는가?

## 초기 범위

도메인:

- `finance`: 금융 공시, 재무 보고서, 숫자 중심 문서.
- `financebench-open-source`: PatronusAI FinanceBench 공개 sample 150문항.
- `general-docs`: 일반 PDF, 기술 문서, 정책 문서, 지식베이스 문서.

PageIndex 범위:

- PageIndex 오픈소스만 사용합니다.
- 첫 벤치마크 트랙에서는 PageIndex Cloud, hosted Chat API, hosted OCR, hosted MCP를 제외합니다.

비교 목표:

- 검색 정확도만이 아니라 제품 운영 관점으로 비교합니다.
- retrieval 품질, generator 품질, judge/evaluator 신뢰성, end-to-end 품질을 분리해서 봅니다.
- ingestion, indexing, query quality, latency, cost, failure mode, citation quality, maintenance complexity를 함께 측정합니다.

## 비교 대상

MVP 시스템:

- `bm25`: lexical sparse retrieval.
- `dense-vector`: chunk, embed, vector search.
- `hybrid`: sparse retrieval + dense retrieval.
- `hybrid-rerank`: hybrid retrieval + reranking.
- `parent-child`: 작은 chunk로 검색하고 큰 parent context로 답변.
- `pageindex-oss`: PageIndex 오픈소스 tree index + agent/tool retrieval.

MVP 임베딩 프로필:

- `e5-large-v2-proxy`: `intfloat/e5-large-v2` 계열을 흉내 내는 로컬 결정론적 proxy.
- `bge-m3-proxy`: `BAAI/bge-m3` 계열을 흉내 내는 로컬 결정론적 proxy.
- `finance-e5-proxy`: FinanceMTEB/Fin-E5 스타일의 금융 특화 모델 가설을 검증하는 로컬 proxy.

MVP 생성 LLM 프로필:

- `extractive-strict`: 보수적인 context-bound 답변 생성.
- `balanced-oss-llm`: multi-section, table 처리 능력을 더 높게 둔 profile.
- `reasoning-oss-llm`: table, calculation, evidence integration을 더 강하게 둔 profile.

MVP 평가 모델/Judge 프로필:

- `exact-match-gold`: product stack ranking에 쓰는 canonical deterministic gold-label evaluator.
- `llm-judge-balanced-proxy`: 더 관대한 LLM-as-judge를 흉내 내는 로컬 결정론적 proxy.
- `citation-strict-judge-proxy`: citation-first compliance judge를 흉내 내는 로컬 결정론적 proxy.

이 프로필들은 OSS-only, 빠른 실행, 재현성을 위해 만든 결정론적 로컬 proxy입니다. 실제 모델 weight를 다운로드해서 측정한 값은 아니므로, 모델 리더보드 성능 주장에는 실제 adapter 연결이 필요합니다.

확장 후보:

- `raptor`: recursive abstractive tree retrieval.
- `graphrag`: corpus-level question을 위한 graph/community retrieval.
- `agentic-vector`: vector/hybrid retrieval 위의 iterative query decomposition.

## 프로젝트 구조

- `docs/`: 설계 노트와 구현 계획. 한국어 버전은 `.ko.md` 파일입니다.
- `configs/`: 벤치마크 설정.
- `src/rag_benchmark/`: 벤치마크 harness Python 패키지.
- `data/raw/`: 다운로드하거나 사용자가 제공한 원본 문서.
- `data/processed/`: 정규화된 추출물, gold label, 중간 산출물.
- `runs/`: 실행별 trace와 원본 output. 실제 run 폴더는 git ignore됩니다.
- `results/`: 집계된 scorecard와 report.

## 현재 상태

동일한 질문 세트를 여러 도메인, RAG 방식, 임베딩 프로필, 생성 LLM 프로필 조합에 실행하고, 다음 항목을 포함한 scorecard를 생성합니다.

- retrieval-only evidence quality
- oracle-context generator quality
- end-to-end stack quality
- judge/evaluator reliability audit
- RAG, embedding, generator, judge를 분리한 leaderboard
- retrieval evidence recall and precision
- answer correctness
- groundedness and citation validity
- latency and cost
- ingestion/indexing time
- failure rate and operational notes
- discrimination audit

상태: local fixture benchmark 기준 완료.
포함된 fixture는 이제 의도적으로 변별력이 생기도록 구성되어 있으며, 기본 두 도메인 모두 answer quality, evidence recall, failure rate에서 시스템 차이를 보여줍니다.

## 빠른 시작

전체 MVP 벤치마크 실행:

```bash
uv run rag-benchmark run --top-k 4
```

최신 summary 출력:

```bash
uv run rag-benchmark summary
```

최신 report 출력:

```bash
uv run rag-benchmark report
```

최신 한국어 report 출력:

```bash
uv run rag-benchmark report-ko
```

운영 추천 ranking 출력:

```bash
uv run rag-benchmark recommend
```

최신 시각화 대시보드 열기:

```text
results/dashboard.html
```

테스트가 시스템을 실제로 구분했는지 진단:

```bash
uv run rag-benchmark discrimination
```

문서, 질문, evidence label 검증:

```bash
uv run rag-benchmark validate-data --top-k 4
```

promptfoo quality gate export:

```bash
uv run rag-benchmark export-promptfoo
cd integrations/promptfoo
npx promptfoo@latest eval -c promptfooconfig.yaml --output promptfoo-results.html --output promptfoo-results.json --no-share
cd ../..
uv run rag-benchmark analyze-promptfoo --input integrations/promptfoo/promptfoo-results.json --output-dir results
```

테스트 실행:

```bash
uv run --extra dev pytest -q
```

## 산출물

각 실행은 다음 파일을 생성합니다.

- `runs/<run_id>/summary.csv`: domain/system scorecard.
- `runs/<run_id>/category_summary.csv`: domain/category/system scorecard.
- `runs/<run_id>/recommendations.csv`: quality, efficiency, stability 기반 추천 ranking.
- `runs/<run_id>/production_readiness.csv`: 운영 투입 기준에 따른 stack별 판단 결과.
- `runs/<run_id>/axis_leaderboard.csv`: RAG, embedding, generator 후보를 축별로 분리한 ranking.
- `runs/<run_id>/judge_audit.csv`: evaluator/judge 신뢰성 및 risk summary.
- `runs/<run_id>/failure_summary.csv`: domain/system별 failure type count.
- `runs/<run_id>/results.csv`: question별 metric.
- `runs/<run_id>/traces.jsonl`: retrieval, answer, evaluation trace 전체.
- `runs/<run_id>/report.md`: 운영 관점 Markdown report.
- `runs/<run_id>/report.ko.md`: 한국어 운영 관점 Markdown report.
- `runs/<run_id>/dashboard.html`: ranking, scatter, histogram, heatmap, axis, judge, 운영 적합성 판단을 포함한 정적 시각화 대시보드.

최신 실행 결과는 다음 위치에도 복사됩니다.

- `results/summary.csv`
- `results/category_summary.csv`
- `results/recommendations.csv`
- `results/production_readiness.csv`
- `results/axis_leaderboard.csv`
- `results/judge_audit.csv`
- `results/failure_summary.csv`
- `results/results.csv`
- `results/report.md`
- `results/report.ko.md`
- `results/dashboard.html`
- `results/discrimination.md`

Promptfoo 통합 파일은 다음 위치에 생성됩니다.

- `integrations/promptfoo/promptfooconfig.yaml`
- `integrations/promptfoo/tests.yaml`
- `integrations/promptfoo/rag_benchmark_provider.py`

`analyze-promptfoo` 실행 후 promptfoo 분석 결과는 `results/`에 생성됩니다.

- `results/promptfoo_summary.csv`
- `results/promptfoo_category_summary.csv`
- `results/promptfoo_failure_summary.csv`
- `results/promptfoo_production_readiness.csv`
- `results/promptfoo_report.md`
- `results/promptfoo_report.ko.md`

## 결과 해석 방법

벤치마크는 운영 의사결정 보조 도구로 사용합니다.

- `retrieval-only`는 LLM 이야기를 하기 전에 검색/indexing layer가 정답 근거를 찾는지 확인합니다.
- `generator-oracle`은 정답 근거가 주어졌을 때 generator profile 차이를 봅니다.
- `end-to-end`는 실제 배포 후보인 RAG 방식, 임베딩 프로필, 생성 프로필 조합을 비교합니다.
- `axis_leaderboard.csv`는 최고의 RAG 방식, embedding model, generator model을 따로 볼 때 사용합니다.
- `judge_audit.csv`는 평가 모델을 비교할 때 사용합니다. Judge는 제품 후보가 아니라 측정 도구이므로, production ranking에 쓰기 전 human label 기준 검증이 필요합니다.
- `integrations/promptfoo/`는 CI quality gate 또는 외부 eval view로 사용합니다. 기본 export는 결정론적 로컬 assertion만 쓰며, OSS-only run이 필요하면 model-graded assertion에는 로컬/OSS grader를 지정해야 합니다.
- `production_readiness.csv`와 dashboard의 운영 적합성 패널은 실제 운영 판단에 사용합니다. 제안 기준은 pass rate 80% 이상, answer correctness 80% 이상, evidence recall 85% 이상, citation validity 90% 이상, no-answer hallucination rate 5% 이하, FinanceBench calculation pass rate 80% 이상입니다.
- 정확한 용어, 숫자, ID, 짧은 정책이 중요하면 `bm25`를 먼저 봅니다.
- exact match와 semantic match가 모두 필요하면 `hybrid` 또는 `hybrid-rerank`를 봅니다.
- 검색 chunk는 잘 잡히지만 답변 context가 부족하면 `parent-child`를 봅니다.
- 문서 구조, section navigation, multi-document retrieval이 중요하면 `pageindex-oss`를 봅니다.

fixture 점수를 production proof로 해석하면 안 됩니다. 현재 fixture는 harness와 failure mode를 검증하기 위한 출발점입니다. 실제 의사결정에는 대표 문서, 질문, gold answer, evidence label이 필요합니다.

## 데이터 추가

로컬 Markdown 또는 text 문서를 import할 수 있습니다.

```bash
uv run rag-benchmark import-docs ~/my-docs --domain my-domain
```

질문은 JSONL, JSON, CSV에서 import할 수 있습니다.

```bash
uv run rag-benchmark import-questions ~/my-questions.jsonl --domain my-domain
```

FinanceBench 공개 JSONL/Hugging Face schema는 전용 importer가 있습니다.

```bash
uv run rag-benchmark import-financebench ~/financebench_merged.jsonl --domain finance
```

FinanceBench importer는 evidence label에서 evidence-page document를 만듭니다. OSS smoke test로는 좋지만, 더 어려운 production retrieval 평가는 full PDF ingestion이 필요합니다.

이 저장소에는 공개 150문항 FinanceBench sample에서 정규화한 `financebench-open-source` fixture도 포함되어 있습니다. Closed 10k+ FinanceBench dataset은 포함하지 않습니다.

위 명령은 다음 파일을 생성합니다.

```text
data/fixtures/<domain>/documents.jsonl
data/fixtures/<domain>/questions.jsonl
```

그 다음 `configs/benchmark.yaml`에 도메인을 추가합니다.

질문에는 가능하면 evidence coordinate를 포함해야 합니다. JSONL row 예시는 다음과 같습니다.

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

이 벤치마크는 evidence-first 방식입니다. evidence label이 없으면 retrieval quality와 citation validity를 안정적으로 측정할 수 없습니다.

CSV question import는 `question_id`, `category`, `question`, `answer`, `answer_aliases`, `evidence_json`, `no_answer`, `notes` column을 지원합니다. `answer_aliases`는 `|`로 구분할 수 있고, `evidence_json`은 evidence object list 형태의 JSON이어야 합니다.

## 관련 문서

- [운영 가이드](docs/OPERATING_GUIDE.ko.md)
- [구현 계획](docs/IMPLEMENTATION_PLAN.ko.md)
- [리서치 출처](docs/SOURCES.ko.md)
