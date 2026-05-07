# RAG Benchmark Report: 20260507T081639Z

This report compares RAG strategies for practical operations decisions.
Scores are generated from local fixture datasets and deterministic extractive answering.

## Scorecard

| Domain | System | Answer | Evidence Recall | Context Precision | Citation | Latency ms | Cost | Failure |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| finance | bm25 | 1.000 | 1.000 | 0.278 | 1.000 | 0.03 | 0.000001 | 0.000 |
| finance | dense-vector | 1.000 | 1.000 | 0.278 | 1.000 | 0.04 | 0.000001 | 0.000 |
| finance | hybrid | 1.000 | 1.000 | 0.278 | 1.000 | 0.05 | 0.000001 | 0.000 |
| finance | hybrid-rerank | 1.000 | 1.000 | 0.278 | 1.000 | 0.08 | 0.000114 | 0.000 |
| finance | pageindex-oss | 1.000 | 1.000 | 0.250 | 1.000 | 0.03 | 0.000061 | 0.000 |
| finance | parent-child | 1.000 | 1.000 | 0.278 | 1.000 | 0.02 | 0.000001 | 0.000 |
| general-docs | bm25 | 0.714 | 0.814 | 0.405 | 0.714 | 0.01 | 0.000000 | 0.286 |
| general-docs | dense-vector | 0.714 | 0.814 | 0.393 | 0.714 | 0.03 | 0.000001 | 0.286 |
| general-docs | hybrid | 0.714 | 0.814 | 0.393 | 0.714 | 0.04 | 0.000001 | 0.286 |
| general-docs | hybrid-rerank | 0.714 | 0.814 | 0.393 | 0.714 | 0.05 | 0.000049 | 0.286 |
| general-docs | pageindex-oss | 0.857 | 0.914 | 0.286 | 0.857 | 0.03 | 0.000061 | 0.143 |
| general-docs | parent-child | 0.714 | 0.814 | 0.429 | 0.714 | 0.02 | 0.000000 | 0.286 |

## Recommendation Ranking

Recommendation score combines quality, efficiency, and stability. It is a decision aid, not a universal truth.

| Domain | Rank | System | Recommendation | Quality | Efficiency | Stability | Role |
|---|---:|---|---:|---:|---:|---:|---|
| finance | 1 | `parent-child` | 0.878 | 0.928 | 0.624 | 1.000 | small-chunk search with broader answer context |
| finance | 2 | `bm25` | 0.868 | 0.928 | 0.573 | 1.000 | fast exact-term baseline |
| finance | 3 | `dense-vector` | 0.856 | 0.928 | 0.517 | 1.000 | semantic similarity baseline |
| finance | 4 | `hybrid` | 0.840 | 0.928 | 0.434 | 1.000 | balanced default for mixed queries |
| finance | 5 | `pageindex-oss` | 0.829 | 0.925 | 0.391 | 1.000 | structured long-document and multi-section navigation |
| finance | 6 | `hybrid-rerank` | 0.753 | 0.928 | 0.000 | 1.000 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 1 | `parent-child` | 0.716 | 0.716 | 0.720 | 0.714 | small-chunk search with broader answer context |
| general-docs | 2 | `bm25` | 0.712 | 0.713 | 0.708 | 0.714 | fast exact-term baseline |
| general-docs | 3 | `dense-vector` | 0.689 | 0.712 | 0.596 | 0.714 | semantic similarity baseline |
| general-docs | 4 | `pageindex-oss` | 0.687 | 0.817 | 0.136 | 0.857 | structured long-document and multi-section navigation |
| general-docs | 5 | `hybrid` | 0.674 | 0.712 | 0.520 | 0.714 | balanced default for mixed queries |
| general-docs | 6 | `hybrid-rerank` | 0.603 | 0.712 | 0.163 | 0.714 | quality-first retrieval when rerank latency is acceptable |

## Failure Breakdown

| Domain | System | Failure Type | Count |
|---|---|---|---:|
| general-docs | `bm25` | context_bloat | 2 |
| general-docs | `dense-vector` | context_bloat | 2 |
| general-docs | `hybrid` | context_bloat | 2 |
| general-docs | `hybrid-rerank` | context_bloat | 2 |
| general-docs | `pageindex-oss` | generation_hallucination | 1 |
| general-docs | `parent-child` | context_bloat | 1 |
| general-docs | `parent-child` | generation_hallucination | 1 |

## Category View

| Domain | Category | Best System | Best Answer | Hardest System Failure |
|---|---|---:|---:|---:|
| finance | calculation | `bm25` | 1.000 | `bm25` 0.000 |
| finance | direct_lookup | `bm25` | 1.000 | `bm25` 0.000 |
| finance | multi_section | `bm25` | 1.000 | `bm25` 0.000 |
| finance | no_answer | `bm25` | 1.000 | `bm25` 0.000 |
| finance | section_navigation | `bm25` | 1.000 | `bm25` 0.000 |
| finance | table_numeric | `bm25` | 1.000 | `bm25` 0.000 |
| general-docs | direct_lookup | `bm25` | 1.000 | `bm25` 0.000 |
| general-docs | global_summary | `pageindex-oss` | 0.000 | `bm25` 1.000 |
| general-docs | multi_document | `pageindex-oss` | 1.000 | `bm25` 1.000 |
| general-docs | multi_section | `bm25` | 1.000 | `bm25` 0.000 |
| general-docs | no_answer | `bm25` | 1.000 | `bm25` 0.000 |
| general-docs | section_navigation | `bm25` | 1.000 | `bm25` 0.000 |
| general-docs | table_numeric | `bm25` | 1.000 | `bm25` 0.000 |

## Operational Guidance

### finance

- Recommended default: `parent-child` (score=0.878; small-chunk search with broader answer context).
- Best quality: `bm25` (answer=1.000, evidence=1.000).
- Lowest query cost: `parent-child` (cost=0.000001).
- Fastest query path: `parent-child` (latency=0.02 ms).

### general-docs

- Recommended default: `parent-child` (score=0.716; small-chunk search with broader answer context).
- Best quality: `pageindex-oss` (answer=0.857, evidence=0.914).
- Lowest query cost: `parent-child` (cost=0.000000).
- Fastest query path: `bm25` (latency=0.01 ms).


## Interpretation Warnings

- general-docs: at least one question needs 5 evidence items, but top_k=4.

## Notes

- `pageindex-oss` uses a local PageIndex-style tree adapter only; hosted PageIndex APIs are excluded.
- The current answerer is deterministic so retrieval failures are visible and reproducible.
- Add real corpora and human-graded questions before treating numbers as production proof.
