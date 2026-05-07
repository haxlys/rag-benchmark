# RAG Benchmark

[English](README.md) | [한국어](README.ko.md)

VectifyAI PageIndex 오픈소스와 전통적인 RAG 방식을 비교하기 위한 운영형 벤치마크입니다.

이 프로젝트는 단순 리더보드가 아닙니다. 목표는 실제 제품 운영에서 다음 질문에 답하는 것입니다.

> 특정 문서 도메인, 품질 목표, 지연시간 예산, 비용 예산, 유지보수 조건에서 어떤 RAG 구현을 운영해야 하는가?

## 초기 범위

도메인:

- `finance`: 금융 공시, 재무 보고서, 숫자 중심 문서.
- `general-docs`: 일반 PDF, 기술 문서, 정책 문서, 지식베이스 문서.

PageIndex 범위:

- PageIndex 오픈소스만 사용합니다.
- 첫 벤치마크 트랙에서는 PageIndex Cloud, hosted Chat API, hosted OCR, hosted MCP를 제외합니다.

비교 목표:

- 검색 정확도만이 아니라 제품 운영 관점으로 비교합니다.
- ingestion, indexing, query quality, latency, cost, failure mode, citation quality, maintenance complexity를 함께 측정합니다.

## 비교 대상

MVP 시스템:

- `bm25`: lexical sparse retrieval.
- `dense-vector`: chunk, embed, vector search.
- `hybrid`: sparse retrieval + dense retrieval.
- `hybrid-rerank`: hybrid retrieval + reranking.
- `parent-child`: 작은 chunk로 검색하고 큰 parent context로 답변.
- `pageindex-oss`: PageIndex 오픈소스 tree index + agent/tool retrieval.

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

동일한 질문 세트를 두 도메인과 여섯 MVP 시스템에 실행하고, 다음 항목을 포함한 scorecard를 생성합니다.

- retrieval evidence recall and precision
- answer correctness
- groundedness and citation validity
- latency and cost
- ingestion/indexing time
- failure rate and operational notes
- discrimination audit

상태: local fixture benchmark 기준 완료.

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

운영 추천 ranking 출력:

```bash
uv run rag-benchmark recommend
```

테스트가 시스템을 실제로 구분했는지 진단:

```bash
uv run rag-benchmark discrimination
```

문서, 질문, evidence label 검증:

```bash
uv run rag-benchmark validate-data --top-k 4
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
- `runs/<run_id>/failure_summary.csv`: domain/system별 failure type count.
- `runs/<run_id>/results.csv`: question별 metric.
- `runs/<run_id>/traces.jsonl`: retrieval, answer, evaluation trace 전체.
- `runs/<run_id>/report.md`: 운영 관점 Markdown report.

최신 실행 결과는 다음 위치에도 복사됩니다.

- `results/summary.csv`
- `results/category_summary.csv`
- `results/recommendations.csv`
- `results/failure_summary.csv`
- `results/results.csv`
- `results/report.md`
- `results/discrimination.md`

## 결과 해석 방법

벤치마크는 운영 의사결정 보조 도구로 사용합니다.

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
