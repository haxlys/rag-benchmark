# RAG Benchmark Report: 20260507T083403Z

This report compares RAG strategies for practical operations decisions.
Scores are generated from local fixture datasets and deterministic extractive answering.

## Scorecard

| Domain | System | Answer | Evidence Recall | Context Precision | Citation | Latency ms | Cost | Failure |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| finance | bm25 | 0.632 | 0.632 | 0.175 | 0.632 | 0.02 | 0.000001 | 0.368 |
| finance | dense-vector | 1.000 | 1.000 | 0.329 | 1.000 | 0.03 | 0.000001 | 0.000 |
| finance | hybrid | 0.895 | 0.895 | 0.303 | 0.895 | 0.06 | 0.000001 | 0.105 |
| finance | hybrid-rerank | 1.000 | 1.000 | 0.329 | 1.000 | 0.09 | 0.000110 | 0.000 |
| finance | pageindex-oss | 1.000 | 1.000 | 0.250 | 1.000 | 0.05 | 0.000061 | 0.000 |
| finance | parent-child | 0.684 | 0.684 | 0.189 | 0.684 | 0.03 | 0.000001 | 0.316 |
| general-docs | bm25 | 0.650 | 0.710 | 0.258 | 0.650 | 0.02 | 0.000000 | 0.350 |
| general-docs | dense-vector | 0.900 | 0.935 | 0.417 | 0.900 | 0.04 | 0.000001 | 0.100 |
| general-docs | hybrid | 0.850 | 0.910 | 0.404 | 0.850 | 0.06 | 0.000001 | 0.150 |
| general-docs | hybrid-rerank | 0.900 | 0.935 | 0.417 | 0.900 | 0.08 | 0.000080 | 0.100 |
| general-docs | pageindex-oss | 0.900 | 0.945 | 0.263 | 0.900 | 0.07 | 0.000061 | 0.100 |
| general-docs | parent-child | 0.600 | 0.660 | 0.254 | 0.600 | 0.03 | 0.000000 | 0.400 |

## Recommendation Ranking

Recommendation score combines quality, efficiency, and stability. It is a decision aid, not a universal truth.

| Domain | Rank | System | Recommendation | Quality | Efficiency | Stability | Role |
|---|---:|---|---:|---:|---:|---:|---|
| finance | 1 | `dense-vector` | 0.868 | 0.933 | 0.557 | 1.000 | semantic similarity baseline |
| finance | 2 | `pageindex-oss` | 0.811 | 0.925 | 0.299 | 1.000 | structured long-document and multi-section navigation |
| finance | 3 | `hybrid` | 0.766 | 0.836 | 0.442 | 0.895 | balanced default for mixed queries |
| finance | 4 | `hybrid-rerank` | 0.759 | 0.933 | 0.013 | 1.000 | quality-first retrieval when rerank latency is acceptable |
| finance | 5 | `parent-child` | 0.642 | 0.635 | 0.636 | 0.684 | small-chunk search with broader answer context |
| finance | 6 | `bm25` | 0.601 | 0.586 | 0.629 | 0.632 | fast exact-term baseline |
| general-docs | 1 | `dense-vector` | 0.809 | 0.862 | 0.569 | 0.900 | semantic similarity baseline |
| general-docs | 2 | `hybrid` | 0.753 | 0.823 | 0.451 | 0.850 | balanced default for mixed queries |
| general-docs | 3 | `pageindex-oss` | 0.719 | 0.850 | 0.161 | 0.900 | structured long-document and multi-section navigation |
| general-docs | 4 | `hybrid-rerank` | 0.708 | 0.862 | 0.061 | 0.900 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 5 | `bm25` | 0.642 | 0.629 | 0.677 | 0.650 | fast exact-term baseline |
| general-docs | 6 | `parent-child` | 0.604 | 0.583 | 0.673 | 0.600 | small-chunk search with broader answer context |

## Failure Breakdown

| Domain | System | Failure Type | Count |
|---|---|---|---:|
| finance | `bm25` | retrieval_miss | 7 |
| finance | `hybrid` | retrieval_miss | 2 |
| finance | `parent-child` | retrieval_miss | 6 |
| general-docs | `bm25` | context_bloat | 3 |
| general-docs | `bm25` | retrieval_miss | 4 |
| general-docs | `dense-vector` | context_bloat | 2 |
| general-docs | `hybrid` | context_bloat | 3 |
| general-docs | `hybrid-rerank` | context_bloat | 2 |
| general-docs | `pageindex-oss` | context_bloat | 1 |
| general-docs | `pageindex-oss` | generation_hallucination | 1 |
| general-docs | `parent-child` | context_bloat | 2 |
| general-docs | `parent-child` | generation_hallucination | 1 |
| general-docs | `parent-child` | retrieval_miss | 5 |

## Category View

| Domain | Category | Best System | Best Answer | Hardest System Failure |
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

## Operational Guidance

### finance

- Recommended default: `dense-vector` (score=0.868; semantic similarity baseline).
- Best quality: `dense-vector` (answer=1.000, evidence=1.000).
- Lowest query cost: `parent-child` (cost=0.000001).
- Fastest query path: `bm25` (latency=0.02 ms).

### general-docs

- Recommended default: `dense-vector` (score=0.809; semantic similarity baseline).
- Best quality: `pageindex-oss` (answer=0.900, evidence=0.945).
- Lowest query cost: `parent-child` (cost=0.000000).
- Fastest query path: `bm25` (latency=0.02 ms).


## Interpretation Warnings

- general-docs: at least one question needs 5 evidence items, but top_k=4.

## Notes

- `pageindex-oss` uses a local PageIndex-style tree adapter only; hosted PageIndex APIs are excluded.
- The current answerer is deterministic so retrieval failures are visible and reproducible.
- Add real corpora and human-graded questions before treating numbers as production proof.
