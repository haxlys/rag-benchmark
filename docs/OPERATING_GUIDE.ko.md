# 운영 가이드

[English](OPERATING_GUIDE.md) | [한국어](OPERATING_GUIDE.ko.md)

## 목적

이 벤치마크는 실제 문서 제품에서 어떤 RAG pattern을 선택할지 판단하기 위한 도구입니다. 하나의 accuracy 숫자만 보는 것이 아니라, 품질, 비용, 지연시간, 실패 원인을 함께 봅니다.

## 의사결정 매트릭스

| 상황 | 먼저 볼 방식 | 이유 |
|---|---|---|
| retrieval 문제인지 LLM 문제인지 애매함 | `retrieval-only` 후 `generator-oracle` | 검색 실패와 답변 생성 실패를 분리해서 봅니다. |
| 평가 모델이 믿을 만한지 애매함 | `judge_audit.csv` | judge 신뢰성을 product stack 품질과 분리해서 봅니다. |
| CI quality gate 또는 외부 eval UI가 필요함 | `export-promptfoo` | promptfoo가 로컬 Python provider를 통해 이 benchmark를 호출하게 합니다. |
| promptfoo 결과를 운영 판단으로 바꾸고 싶음 | `analyze-promptfoo` | promptfoo JSON을 summary, failure, production-readiness 결과로 집계합니다. |
| 정확한 이름, 숫자, ID, 짧은 정책 검색 | `bm25` | 저렴하고 빠르며 exact lexical matching이 강합니다. |
| exact term과 semantic question이 섞임 | `hybrid` | sparse와 dense retrieval signal을 함께 씁니다. |
| 품질이 중요하고 latency budget이 있음 | `hybrid-rerank` | 추가 비용과 지연시간을 감수하고 candidate order를 개선할 수 있습니다. |
| 검색은 되지만 답변 context가 부족함 | `parent-child` | 작은 chunk로 검색하고 더 큰 parent section으로 답변합니다. |
| 길고 구조화된 PDF, section navigation | `pageindex-oss` | tree-style section retrieval로 문서 구조를 보존합니다. |
| 금융처럼 도메인 특화 용어가 많음 | embedding profile 비교 | 일반 embedding leaderboard가 도메인 성능을 그대로 예측하지 못할 수 있습니다. |
| corpus-level theme, entity relationship | future `graphrag` | 전체 corpus 관계와 global question에 더 잘 맞습니다. |

## 볼 때 주의할 점

- answer score는 높은데 context precision이 낮으면, 답은 맞지만 context를 낭비하고 있는 상태입니다.
- evidence recall은 높은데 answer score가 낮으면, generation 또는 context packing 문제일 가능성이 큽니다.
- evidence recall이 낮으면 parser, chunking, retrieval, query routing 문제를 봐야 합니다.
- embedding model 변경은 먼저 retrieval-only evidence recall, MRR, nDCG로 봅니다.
- generator 변경은 gold evidence가 보장되는 oracle-context run으로 먼저 봅니다.
- judge/evaluator 변경은 product stack ranking에 쓰기 전에 gold 또는 human label 기준으로 audit합니다.
- citation validity는 finance, legal, compliance, support use case에서 특히 중요합니다.
- query latency가 낮아도 ingestion/indexing cost가 높을 수 있습니다. tree 또는 graph 방식에서 자주 생깁니다.

## 현재 fixture 결과 해석

포함된 fixture run 기준:

- 두 fixture domain은 이제 단순 smoke test가 아니라 의도적으로 변별력이 생기도록 구성되어 있습니다.
- `financebench-open-source`는 더 큰 실제 데이터 retrieval run을 위해 공개 FinanceBench 150문항 sample을 추가합니다.
- 이제 `retrieval-only`, `generator-oracle`, `end-to-end` 세 track을 실행합니다.
- end-to-end run은 RAG 방식, embedding profile, generator profile 조합을 함께 비교합니다.
- `axis_leaderboard.csv`에서 최고의 RAG 방식, embedding profile, generator profile을 축별로 분리해서 봅니다.
- `judge_audit.csv`에서 judge/evaluator 신뢰성을 product stack 품질과 분리해서 봅니다.
- `integrations/promptfoo/`는 결정론적 CI check 또는 선택적 model-graded RAG assertion을 위한 promptfoo config, tests, Python provider를 export합니다.
- `analyze-promptfoo`는 promptfoo JSON 결과를 CSV 리포트와 같은 dashboard에 반영합니다.
- `results/dashboard.html`에서 ranking, scatter, distribution, category heatmap, axis leaderboard, judge audit, promptfoo, 운영 적합성 판단을 볼 수 있습니다.
- Finance에는 capex, deferred revenue, backlog, covenant, lease obligation 같은 semantic financial term이 포함됩니다.
- General-docs에는 semantic question, section-navigation, multi-section, multi-document distractor가 포함됩니다.
- synonym-heavy 또는 structure-heavy question에서 `pageindex-oss`, dense-style retrieval, reranking이 BM25와 분리됩니다.
- `parent-child`는 context를 더 작고 싸게 유지하지만, title-only 또는 synonym-heavy evidence를 놓칠 수 있습니다.
- Top-k가 중요합니다. global summary question은 context budget이 모든 evidence를 담지 못해서 실패할 수 있습니다.

## 내 데이터로 실행하기

1. 로컬 문서 import:

   ```bash
   uv run rag-benchmark import-docs ~/my-docs --domain my-domain
   ```

2. 질문 label import:

   ```bash
   uv run rag-benchmark import-questions ~/my-questions.jsonl --domain my-domain
   ```

   FinanceBench 공개 JSONL을 쓰는 경우:

   ```bash
   uv run rag-benchmark import-financebench ~/financebench_merged.jsonl --domain finance
   ```

3. `configs/benchmark.yaml`에 `my-domain`을 추가합니다.

4. evidence coordinate 검증:

   ```bash
   uv run rag-benchmark validate-data --domain my-domain --top-k 4
   ```

5. 실행 및 확인:

   ```bash
   uv run rag-benchmark run --domain my-domain --top-k 4
   uv run rag-benchmark recommend
   uv run rag-benchmark report
   uv run rag-benchmark report-ko
   uv run rag-benchmark discrimination
   ```

   시각화 대시보드는 `results/dashboard.html`을 열면 됩니다.

6. CI gate 또는 promptfoo eval UI가 필요하면 promptfoo check를 export합니다.

   ```bash
   uv run rag-benchmark export-promptfoo --domain my-domain
   cd integrations/promptfoo
   npx promptfoo@latest eval -c promptfooconfig.yaml --output promptfoo-results.html --output promptfoo-results.json --no-share
   cd ../..
   uv run rag-benchmark analyze-promptfoo --input integrations/promptfoo/promptfoo-results.json --output-dir results
   ```

recommendation ranking은 quality, efficiency, stability를 조합합니다. 이 값으로 시작점을 고르고, 실패한 case는 `traces.jsonl`에서 확인합니다.

## production readiness checklist

실제 제품 결정을 위해서는 최소한 다음을 충족하는 것이 좋습니다.

- 운영 후보로 보려면 제안 기준을 모두 통과해야 합니다. 기준은 pass rate 80% 이상, answer correctness 80% 이상, evidence recall 85% 이상, citation validity 90% 이상, no-answer hallucination rate 5% 이하, 계산 문항이 있으면 FinanceBench calculation pass rate 80% 이상입니다.
- 주요 도메인별 최소 100개 질문 추가.
- answerable question마다 evidence page 또는 section label 추가.
- no-answer question 포함.
- table/numeric question과 multi-document question 포함.
- 실제 top-k와 context-token budget으로 실행.
- RAG 방식을 탓하기 전에 최소 두 개 이상의 embedding model/profile 비교.
- LLM을 탓하기 전에 oracle-context generator check 실행.
- LLM judge를 정답 채점 기준으로 쓰기 전에 human label 기준 judge audit 실행.
- prompt, chunking, retrieval, generation, judge 설정을 바꾼 뒤 promptfoo deterministic check를 CI에서 실행.
- production launch 전 promptfoo red-team workflow로 prompt injection, overreliance, hallucination, PII leakage, RAG poisoning 점검.
- 답변의 10-20% 이상을 사람이 검토.
- parser failure를 retrieval failure와 분리해서 기록.
- chunking, parsing, embedding model, reranker를 바꿀 때마다 재실행.
