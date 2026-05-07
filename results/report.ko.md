# RAG 벤치마크 리포트: 20260507T084114Z

이 리포트는 실무 운영 의사결정을 위해 여러 RAG 전략을 비교합니다.
점수는 로컬 fixture 데이터셋과 결정론적 extractive answerer로 생성됩니다.

## 점수표

| 도메인 | 시스템 | 답변 | Evidence Recall | Context Precision | Citation | 지연시간 ms | 비용 | 실패율 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| finance | bm25 | 0.632 | 0.632 | 0.175 | 0.632 | 0.02 | 0.000001 | 0.368 |
| finance | dense-vector | 1.000 | 1.000 | 0.329 | 1.000 | 0.04 | 0.000001 | 0.000 |
| finance | hybrid | 0.895 | 0.895 | 0.303 | 0.895 | 0.06 | 0.000001 | 0.105 |
| finance | hybrid-rerank | 1.000 | 1.000 | 0.329 | 1.000 | 0.09 | 0.000110 | 0.000 |
| finance | pageindex-oss | 1.000 | 1.000 | 0.250 | 1.000 | 0.06 | 0.000061 | 0.000 |
| finance | parent-child | 0.684 | 0.684 | 0.189 | 0.684 | 0.03 | 0.000001 | 0.316 |
| general-docs | bm25 | 0.650 | 0.710 | 0.258 | 0.650 | 0.02 | 0.000000 | 0.350 |
| general-docs | dense-vector | 0.900 | 0.935 | 0.417 | 0.900 | 0.04 | 0.000001 | 0.100 |
| general-docs | hybrid | 0.850 | 0.910 | 0.404 | 0.850 | 0.07 | 0.000001 | 0.150 |
| general-docs | hybrid-rerank | 0.900 | 0.935 | 0.417 | 0.900 | 0.09 | 0.000080 | 0.100 |
| general-docs | pageindex-oss | 0.900 | 0.945 | 0.263 | 0.900 | 0.07 | 0.000061 | 0.100 |
| general-docs | parent-child | 0.600 | 0.660 | 0.254 | 0.600 | 0.04 | 0.000000 | 0.400 |

## 추천 순위

추천 점수는 품질, 효율, 안정성을 조합한 값입니다. 절대 정답이 아니라 의사결정 보조 지표입니다.

| 도메인 | 순위 | 시스템 | 추천 점수 | 품질 | 효율 | 안정성 | 역할 |
|---|---:|---|---:|---:|---:|---:|---|
| finance | 1 | `dense-vector` | 0.869 | 0.933 | 0.562 | 1.000 | 의미 기반 유사도 baseline |
| finance | 2 | `pageindex-oss` | 0.810 | 0.925 | 0.294 | 1.000 | 구조화된 긴 문서와 multi-section navigation |
| finance | 3 | `hybrid` | 0.765 | 0.836 | 0.438 | 0.895 | exact와 semantic query가 섞인 경우의 균형형 기본값 |
| finance | 4 | `hybrid-rerank` | 0.759 | 0.933 | 0.013 | 1.000 | rerank latency를 감수할 수 있을 때의 품질 우선 retrieval |
| finance | 5 | `parent-child` | 0.643 | 0.635 | 0.637 | 0.684 | 작은 chunk 검색과 더 넓은 answer context |
| finance | 6 | `bm25` | 0.602 | 0.586 | 0.631 | 0.632 | 빠른 exact-term baseline |
| general-docs | 1 | `dense-vector` | 0.810 | 0.862 | 0.574 | 0.900 | 의미 기반 유사도 baseline |
| general-docs | 2 | `hybrid` | 0.754 | 0.823 | 0.458 | 0.850 | exact와 semantic query가 섞인 경우의 균형형 기본값 |
| general-docs | 3 | `pageindex-oss` | 0.720 | 0.850 | 0.164 | 0.900 | 구조화된 긴 문서와 multi-section navigation |
| general-docs | 4 | `hybrid-rerank` | 0.708 | 0.862 | 0.061 | 0.900 | rerank latency를 감수할 수 있을 때의 품질 우선 retrieval |
| general-docs | 5 | `bm25` | 0.643 | 0.629 | 0.683 | 0.650 | 빠른 exact-term baseline |
| general-docs | 6 | `parent-child` | 0.598 | 0.583 | 0.643 | 0.600 | 작은 chunk 검색과 더 넓은 answer context |

## 실패 유형

| 도메인 | 시스템 | 실패 유형 | 건수 |
|---|---|---|---:|
| finance | `bm25` | 검색 누락 | 7 |
| finance | `hybrid` | 검색 누락 | 2 |
| finance | `parent-child` | 검색 누락 | 6 |
| general-docs | `bm25` | 불필요한 context 과다 | 3 |
| general-docs | `bm25` | 검색 누락 | 4 |
| general-docs | `dense-vector` | 불필요한 context 과다 | 2 |
| general-docs | `hybrid` | 불필요한 context 과다 | 3 |
| general-docs | `hybrid-rerank` | 불필요한 context 과다 | 2 |
| general-docs | `pageindex-oss` | 불필요한 context 과다 | 1 |
| general-docs | `pageindex-oss` | 생성 hallucination | 1 |
| general-docs | `parent-child` | 불필요한 context 과다 | 2 |
| general-docs | `parent-child` | 생성 hallucination | 1 |
| general-docs | `parent-child` | 검색 누락 | 5 |

## 카테고리별 보기

| 도메인 | 카테고리 | 최고 시스템 | 최고 답변 점수 | 실패율이 가장 높은 시스템 |
|---|---|---:|---:|---:|
| finance | calculation | `bm25` | 1.000 | `bm25` 0.000 |
| finance | direct_lookup | `dense-vector` | 1.000 | `bm25` 0.500 |
| finance | multi_section | `bm25` | 1.000 | `bm25` 0.000 |
| finance | no_answer | `bm25` | 1.000 | `bm25` 0.000 |
| finance | section_navigation | `dense-vector` | 1.000 | `bm25` 0.500 |
| finance | table_numeric | `dense-vector` | 1.000 | `bm25` 0.750 |
| general-docs | direct_lookup | `bm25` | 1.000 | `bm25` 0.000 |
| general-docs | global_summary | `pageindex-oss` | 0.000 | `bm25` 1.000 |
| general-docs | multi_document | `bm25` | 0.500 | `bm25` 0.500 |
| general-docs | multi_section | `dense-vector` | 1.000 | `bm25` 0.500 |
| general-docs | no_answer | `bm25` | 1.000 | `bm25` 0.000 |
| general-docs | section_navigation | `dense-vector` | 1.000 | `parent-child` 0.556 |
| general-docs | table_numeric | `bm25` | 1.000 | `bm25` 0.000 |

## 운영 가이드

### finance

- 추천 기본값: `dense-vector` (score=0.869; 의미 기반 유사도 baseline).
- 최고 품질: `dense-vector` (answer=1.000, evidence=1.000).
- 최저 query cost: `parent-child` (cost=0.000001).
- 가장 빠른 query path: `bm25` (latency=0.02 ms).

### general-docs

- 추천 기본값: `dense-vector` (score=0.810; 의미 기반 유사도 baseline).
- 최고 품질: `pageindex-oss` (answer=0.900, evidence=0.945).
- 최저 query cost: `parent-child` (cost=0.000000).
- 가장 빠른 query path: `bm25` (latency=0.02 ms).


## 해석 시 주의사항

- general-docs: 최소 한 질문이 5개의 evidence item을 필요로 하지만 top_k=4입니다.

## 메모

- `pageindex-oss`는 로컬 PageIndex-style tree adapter만 사용합니다. Hosted PageIndex API는 제외되어 있습니다.
- 현재 answerer는 결정론적이므로 retrieval failure를 재현하고 분석하기 쉽습니다.
- 실제 production 근거로 사용하려면 대표 corpus와 사람이 검수한 question/evidence label을 추가해야 합니다.
