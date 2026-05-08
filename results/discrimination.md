# Discrimination Audit

This audit checks whether the benchmark actually separates RAG systems.

## Verdict

- `end-to-end` / `finance` / `citation-strict-judge-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `end-to-end` / `finance` / `exact-match-gold`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `end-to-end` / `finance` / `llm-judge-balanced-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `end-to-end` / `financebench-open-source` / `citation-strict-judge-proxy`: **moderately discriminative**. The benchmark separates systems, but the margin is still narrow.
- `end-to-end` / `financebench-open-source` / `exact-match-gold`: **moderately discriminative**. The benchmark separates systems, but the margin is still narrow.
- `end-to-end` / `financebench-open-source` / `llm-judge-balanced-proxy`: **moderately discriminative**. The benchmark separates systems, but the margin is still narrow.
- `end-to-end` / `general-docs` / `citation-strict-judge-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `end-to-end` / `general-docs` / `exact-match-gold`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `end-to-end` / `general-docs` / `llm-judge-balanced-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `generator-oracle` / `finance` / `citation-strict-judge-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `generator-oracle` / `finance` / `exact-match-gold`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `generator-oracle` / `finance` / `llm-judge-balanced-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `generator-oracle` / `financebench-open-source` / `citation-strict-judge-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `generator-oracle` / `financebench-open-source` / `exact-match-gold`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `generator-oracle` / `financebench-open-source` / `llm-judge-balanced-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `generator-oracle` / `general-docs` / `citation-strict-judge-proxy`: **weakly discriminative**. Some systems separate, but too few questions drive the difference.
- `generator-oracle` / `general-docs` / `exact-match-gold`: **weakly discriminative**. Some systems separate, but too few questions drive the difference.
- `generator-oracle` / `general-docs` / `llm-judge-balanced-proxy`: **weakly discriminative**. Some systems separate, but too few questions drive the difference.
- `retrieval-only` / `finance` / `citation-strict-judge-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `retrieval-only` / `finance` / `exact-match-gold`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `retrieval-only` / `finance` / `llm-judge-balanced-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `retrieval-only` / `financebench-open-source` / `citation-strict-judge-proxy`: **moderately discriminative**. The benchmark separates systems, but the margin is still narrow.
- `retrieval-only` / `financebench-open-source` / `exact-match-gold`: **moderately discriminative**. The benchmark separates systems, but the margin is still narrow.
- `retrieval-only` / `financebench-open-source` / `llm-judge-balanced-proxy`: **moderately discriminative**. The benchmark separates systems, but the margin is still narrow.
- `retrieval-only` / `general-docs` / `citation-strict-judge-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `retrieval-only` / `general-docs` / `exact-match-gold`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `retrieval-only` / `general-docs` / `llm-judge-balanced-proxy`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.

## Domain Metric Spread

| Track | Domain | Judge | Metric | Min | Max | Range | Unique Values |
|---|---|---|---|---:|---:|---:|---:|
| end-to-end | finance | citation-strict-judge-proxy | answer_correctness | 0.368 | 0.842 | 0.474 | 10 |
| end-to-end | finance | citation-strict-judge-proxy | evidence_recall | 0.632 | 1.000 | 0.368 | 5 |
| end-to-end | finance | citation-strict-judge-proxy | context_precision | 0.175 | 0.289 | 0.114 | 6 |
| end-to-end | finance | citation-strict-judge-proxy | citation_validity | 0.421 | 0.895 | 0.474 | 10 |
| end-to-end | finance | citation-strict-judge-proxy | failure_rate | 0.158 | 0.632 | 0.474 | 10 |
| end-to-end | finance | exact-match-gold | answer_correctness | 0.421 | 0.895 | 0.474 | 10 |
| end-to-end | finance | exact-match-gold | evidence_recall | 0.632 | 1.000 | 0.368 | 5 |
| end-to-end | finance | exact-match-gold | context_precision | 0.175 | 0.289 | 0.114 | 6 |
| end-to-end | finance | exact-match-gold | citation_validity | 0.421 | 0.895 | 0.474 | 10 |
| end-to-end | finance | exact-match-gold | failure_rate | 0.105 | 0.579 | 0.474 | 10 |
| end-to-end | finance | llm-judge-balanced-proxy | answer_correctness | 0.368 | 0.842 | 0.474 | 10 |
| end-to-end | finance | llm-judge-balanced-proxy | evidence_recall | 0.632 | 1.000 | 0.368 | 5 |
| end-to-end | finance | llm-judge-balanced-proxy | context_precision | 0.175 | 0.289 | 0.114 | 6 |
| end-to-end | finance | llm-judge-balanced-proxy | citation_validity | 0.421 | 0.895 | 0.474 | 10 |
| end-to-end | finance | llm-judge-balanced-proxy | failure_rate | 0.158 | 0.632 | 0.474 | 10 |
| end-to-end | financebench-open-source | citation-strict-judge-proxy | answer_correctness | 0.260 | 0.347 | 0.087 | 14 |
| end-to-end | financebench-open-source | citation-strict-judge-proxy | evidence_recall | 0.343 | 0.456 | 0.112 | 11 |
| end-to-end | financebench-open-source | citation-strict-judge-proxy | context_precision | 0.100 | 0.130 | 0.030 | 8 |
| end-to-end | financebench-open-source | citation-strict-judge-proxy | citation_validity | 0.293 | 0.400 | 0.107 | 15 |
| end-to-end | financebench-open-source | citation-strict-judge-proxy | failure_rate | 0.653 | 0.740 | 0.087 | 14 |
| end-to-end | financebench-open-source | exact-match-gold | answer_correctness | 0.293 | 0.400 | 0.107 | 15 |
| end-to-end | financebench-open-source | exact-match-gold | evidence_recall | 0.343 | 0.456 | 0.112 | 11 |
| end-to-end | financebench-open-source | exact-match-gold | context_precision | 0.100 | 0.130 | 0.030 | 8 |
| end-to-end | financebench-open-source | exact-match-gold | citation_validity | 0.293 | 0.400 | 0.107 | 15 |
| end-to-end | financebench-open-source | exact-match-gold | failure_rate | 0.600 | 0.707 | 0.107 | 15 |
| end-to-end | financebench-open-source | llm-judge-balanced-proxy | answer_correctness | 0.273 | 0.373 | 0.100 | 15 |
| end-to-end | financebench-open-source | llm-judge-balanced-proxy | evidence_recall | 0.343 | 0.456 | 0.112 | 11 |
| end-to-end | financebench-open-source | llm-judge-balanced-proxy | context_precision | 0.100 | 0.130 | 0.030 | 8 |
| end-to-end | financebench-open-source | llm-judge-balanced-proxy | citation_validity | 0.293 | 0.400 | 0.107 | 15 |
| end-to-end | financebench-open-source | llm-judge-balanced-proxy | failure_rate | 0.627 | 0.727 | 0.100 | 15 |
| end-to-end | general-docs | citation-strict-judge-proxy | answer_correctness | 0.500 | 0.800 | 0.300 | 6 |
| end-to-end | general-docs | citation-strict-judge-proxy | evidence_recall | 0.610 | 0.945 | 0.335 | 9 |
| end-to-end | general-docs | citation-strict-judge-proxy | context_precision | 0.254 | 0.412 | 0.158 | 5 |
| end-to-end | general-docs | citation-strict-judge-proxy | citation_validity | 0.550 | 0.900 | 0.350 | 6 |
| end-to-end | general-docs | citation-strict-judge-proxy | failure_rate | 0.200 | 0.500 | 0.300 | 6 |
| end-to-end | general-docs | exact-match-gold | answer_correctness | 0.550 | 0.850 | 0.300 | 4 |
| end-to-end | general-docs | exact-match-gold | evidence_recall | 0.610 | 0.945 | 0.335 | 9 |
| end-to-end | general-docs | exact-match-gold | context_precision | 0.254 | 0.412 | 0.158 | 5 |
| end-to-end | general-docs | exact-match-gold | citation_validity | 0.550 | 0.900 | 0.350 | 6 |
| end-to-end | general-docs | exact-match-gold | failure_rate | 0.150 | 0.450 | 0.300 | 4 |
| end-to-end | general-docs | llm-judge-balanced-proxy | answer_correctness | 0.550 | 0.850 | 0.300 | 4 |
| end-to-end | general-docs | llm-judge-balanced-proxy | evidence_recall | 0.610 | 0.945 | 0.335 | 9 |
| end-to-end | general-docs | llm-judge-balanced-proxy | context_precision | 0.254 | 0.412 | 0.158 | 5 |
| end-to-end | general-docs | llm-judge-balanced-proxy | citation_validity | 0.550 | 0.900 | 0.350 | 6 |
| end-to-end | general-docs | llm-judge-balanced-proxy | failure_rate | 0.150 | 0.450 | 0.300 | 4 |
| generator-oracle | finance | citation-strict-judge-proxy | answer_correctness | 0.579 | 0.842 | 0.263 | 3 |
| generator-oracle | finance | citation-strict-judge-proxy | evidence_recall | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | finance | citation-strict-judge-proxy | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | finance | citation-strict-judge-proxy | citation_validity | 0.632 | 0.895 | 0.263 | 3 |
| generator-oracle | finance | citation-strict-judge-proxy | failure_rate | 0.158 | 0.421 | 0.263 | 3 |
| generator-oracle | finance | exact-match-gold | answer_correctness | 0.632 | 0.895 | 0.263 | 3 |
| generator-oracle | finance | exact-match-gold | evidence_recall | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | finance | exact-match-gold | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | finance | exact-match-gold | citation_validity | 0.632 | 0.895 | 0.263 | 3 |
| generator-oracle | finance | exact-match-gold | failure_rate | 0.105 | 0.368 | 0.263 | 3 |
| generator-oracle | finance | llm-judge-balanced-proxy | answer_correctness | 0.579 | 0.842 | 0.263 | 3 |
| generator-oracle | finance | llm-judge-balanced-proxy | evidence_recall | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | finance | llm-judge-balanced-proxy | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | finance | llm-judge-balanced-proxy | citation_validity | 0.632 | 0.895 | 0.263 | 3 |
| generator-oracle | finance | llm-judge-balanced-proxy | failure_rate | 0.158 | 0.421 | 0.263 | 3 |
| generator-oracle | financebench-open-source | citation-strict-judge-proxy | answer_correctness | 0.593 | 0.853 | 0.260 | 3 |
| generator-oracle | financebench-open-source | citation-strict-judge-proxy | evidence_recall | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | financebench-open-source | citation-strict-judge-proxy | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | financebench-open-source | citation-strict-judge-proxy | citation_validity | 0.680 | 0.953 | 0.273 | 3 |
| generator-oracle | financebench-open-source | citation-strict-judge-proxy | failure_rate | 0.147 | 0.407 | 0.260 | 3 |
| generator-oracle | financebench-open-source | exact-match-gold | answer_correctness | 0.680 | 0.953 | 0.273 | 3 |
| generator-oracle | financebench-open-source | exact-match-gold | evidence_recall | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | financebench-open-source | exact-match-gold | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | financebench-open-source | exact-match-gold | citation_validity | 0.680 | 0.953 | 0.273 | 3 |
| generator-oracle | financebench-open-source | exact-match-gold | failure_rate | 0.047 | 0.320 | 0.273 | 3 |
| generator-oracle | financebench-open-source | llm-judge-balanced-proxy | answer_correctness | 0.660 | 0.907 | 0.247 | 3 |
| generator-oracle | financebench-open-source | llm-judge-balanced-proxy | evidence_recall | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | financebench-open-source | llm-judge-balanced-proxy | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | financebench-open-source | llm-judge-balanced-proxy | citation_validity | 0.680 | 0.953 | 0.273 | 3 |
| generator-oracle | financebench-open-source | llm-judge-balanced-proxy | failure_rate | 0.093 | 0.340 | 0.247 | 3 |
| generator-oracle | general-docs | citation-strict-judge-proxy | answer_correctness | 0.750 | 0.850 | 0.100 | 3 |
| generator-oracle | general-docs | citation-strict-judge-proxy | evidence_recall | 0.940 | 0.990 | 0.050 | 2 |
| generator-oracle | general-docs | citation-strict-judge-proxy | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | general-docs | citation-strict-judge-proxy | citation_validity | 0.900 | 0.950 | 0.050 | 2 |
| generator-oracle | general-docs | citation-strict-judge-proxy | failure_rate | 0.150 | 0.250 | 0.100 | 3 |
| generator-oracle | general-docs | exact-match-gold | answer_correctness | 0.850 | 0.900 | 0.050 | 2 |
| generator-oracle | general-docs | exact-match-gold | evidence_recall | 0.940 | 0.990 | 0.050 | 2 |
| generator-oracle | general-docs | exact-match-gold | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | general-docs | exact-match-gold | citation_validity | 0.900 | 0.950 | 0.050 | 2 |
| generator-oracle | general-docs | exact-match-gold | failure_rate | 0.100 | 0.150 | 0.050 | 2 |
| generator-oracle | general-docs | llm-judge-balanced-proxy | answer_correctness | 0.850 | 0.900 | 0.050 | 2 |
| generator-oracle | general-docs | llm-judge-balanced-proxy | evidence_recall | 0.940 | 0.990 | 0.050 | 2 |
| generator-oracle | general-docs | llm-judge-balanced-proxy | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | general-docs | llm-judge-balanced-proxy | citation_validity | 0.900 | 0.950 | 0.050 | 2 |
| generator-oracle | general-docs | llm-judge-balanced-proxy | failure_rate | 0.100 | 0.150 | 0.050 | 2 |
| retrieval-only | finance | citation-strict-judge-proxy | answer_correctness | 0.579 | 0.947 | 0.368 | 5 |
| retrieval-only | finance | citation-strict-judge-proxy | evidence_recall | 0.632 | 1.000 | 0.368 | 5 |
| retrieval-only | finance | citation-strict-judge-proxy | context_precision | 0.175 | 0.289 | 0.114 | 6 |
| retrieval-only | finance | citation-strict-judge-proxy | citation_validity | 0.632 | 1.000 | 0.368 | 5 |
| retrieval-only | finance | citation-strict-judge-proxy | failure_rate | 0.053 | 0.421 | 0.368 | 5 |
| retrieval-only | finance | exact-match-gold | answer_correctness | 0.632 | 1.000 | 0.368 | 5 |
| retrieval-only | finance | exact-match-gold | evidence_recall | 0.632 | 1.000 | 0.368 | 5 |
| retrieval-only | finance | exact-match-gold | context_precision | 0.175 | 0.289 | 0.114 | 6 |
| retrieval-only | finance | exact-match-gold | citation_validity | 0.632 | 1.000 | 0.368 | 5 |
| retrieval-only | finance | exact-match-gold | failure_rate | 0.000 | 0.368 | 0.368 | 5 |
| retrieval-only | finance | llm-judge-balanced-proxy | answer_correctness | 0.579 | 0.947 | 0.368 | 5 |
| retrieval-only | finance | llm-judge-balanced-proxy | evidence_recall | 0.632 | 1.000 | 0.368 | 5 |
| retrieval-only | finance | llm-judge-balanced-proxy | context_precision | 0.175 | 0.289 | 0.114 | 6 |
| retrieval-only | finance | llm-judge-balanced-proxy | citation_validity | 0.632 | 1.000 | 0.368 | 5 |
| retrieval-only | finance | llm-judge-balanced-proxy | failure_rate | 0.053 | 0.421 | 0.368 | 5 |
| retrieval-only | financebench-open-source | citation-strict-judge-proxy | answer_correctness | 0.287 | 0.367 | 0.080 | 9 |
| retrieval-only | financebench-open-source | citation-strict-judge-proxy | evidence_recall | 0.343 | 0.456 | 0.112 | 11 |
| retrieval-only | financebench-open-source | citation-strict-judge-proxy | context_precision | 0.100 | 0.130 | 0.030 | 8 |
| retrieval-only | financebench-open-source | citation-strict-judge-proxy | citation_validity | 0.320 | 0.420 | 0.100 | 9 |
| retrieval-only | financebench-open-source | citation-strict-judge-proxy | failure_rate | 0.633 | 0.713 | 0.080 | 9 |
| retrieval-only | financebench-open-source | exact-match-gold | answer_correctness | 0.320 | 0.420 | 0.100 | 9 |
| retrieval-only | financebench-open-source | exact-match-gold | evidence_recall | 0.343 | 0.456 | 0.112 | 11 |
| retrieval-only | financebench-open-source | exact-match-gold | context_precision | 0.100 | 0.130 | 0.030 | 8 |
| retrieval-only | financebench-open-source | exact-match-gold | citation_validity | 0.320 | 0.420 | 0.100 | 9 |
| retrieval-only | financebench-open-source | exact-match-gold | failure_rate | 0.580 | 0.680 | 0.100 | 9 |
| retrieval-only | financebench-open-source | llm-judge-balanced-proxy | answer_correctness | 0.307 | 0.393 | 0.087 | 9 |
| retrieval-only | financebench-open-source | llm-judge-balanced-proxy | evidence_recall | 0.343 | 0.456 | 0.112 | 11 |
| retrieval-only | financebench-open-source | llm-judge-balanced-proxy | context_precision | 0.100 | 0.130 | 0.030 | 8 |
| retrieval-only | financebench-open-source | llm-judge-balanced-proxy | citation_validity | 0.320 | 0.420 | 0.100 | 9 |
| retrieval-only | financebench-open-source | llm-judge-balanced-proxy | failure_rate | 0.607 | 0.693 | 0.087 | 9 |
| retrieval-only | general-docs | citation-strict-judge-proxy | answer_correctness | 0.550 | 0.800 | 0.250 | 4 |
| retrieval-only | general-docs | citation-strict-judge-proxy | evidence_recall | 0.660 | 0.945 | 0.285 | 5 |
| retrieval-only | general-docs | citation-strict-judge-proxy | context_precision | 0.254 | 0.412 | 0.158 | 5 |
| retrieval-only | general-docs | citation-strict-judge-proxy | citation_validity | 0.600 | 0.900 | 0.300 | 4 |
| retrieval-only | general-docs | citation-strict-judge-proxy | failure_rate | 0.200 | 0.450 | 0.250 | 4 |
| retrieval-only | general-docs | exact-match-gold | answer_correctness | 0.600 | 0.900 | 0.300 | 4 |
| retrieval-only | general-docs | exact-match-gold | evidence_recall | 0.660 | 0.945 | 0.285 | 5 |
| retrieval-only | general-docs | exact-match-gold | context_precision | 0.254 | 0.412 | 0.158 | 5 |
| retrieval-only | general-docs | exact-match-gold | citation_validity | 0.600 | 0.900 | 0.300 | 4 |
| retrieval-only | general-docs | exact-match-gold | failure_rate | 0.100 | 0.400 | 0.300 | 4 |
| retrieval-only | general-docs | llm-judge-balanced-proxy | answer_correctness | 0.600 | 0.900 | 0.300 | 4 |
| retrieval-only | general-docs | llm-judge-balanced-proxy | evidence_recall | 0.660 | 0.945 | 0.285 | 5 |
| retrieval-only | general-docs | llm-judge-balanced-proxy | context_precision | 0.254 | 0.412 | 0.158 | 5 |
| retrieval-only | general-docs | llm-judge-balanced-proxy | citation_validity | 0.600 | 0.900 | 0.300 | 4 |
| retrieval-only | general-docs | llm-judge-balanced-proxy | failure_rate | 0.100 | 0.400 | 0.300 | 4 |

## Question-Level Discrimination

| Track | Domain | Judge | Questions | Quality-Diff Questions | Answer-Diff Questions | Recall-Diff Questions | Precision-Diff Questions |
|---|---|---|---:|---:|---:|---:|---:|
| end-to-end | finance | citation-strict-judge-proxy | 19 | 11 | 11 | 7 | 9 |
| end-to-end | finance | exact-match-gold | 19 | 11 | 11 | 7 | 9 |
| end-to-end | finance | llm-judge-balanced-proxy | 19 | 11 | 11 | 7 | 9 |
| end-to-end | financebench-open-source | citation-strict-judge-proxy | 150 | 70 | 55 | 68 | 68 |
| end-to-end | financebench-open-source | exact-match-gold | 150 | 71 | 62 | 68 | 68 |
| end-to-end | financebench-open-source | llm-judge-balanced-proxy | 150 | 71 | 58 | 68 | 68 |
| end-to-end | general-docs | citation-strict-judge-proxy | 20 | 9 | 7 | 9 | 13 |
| end-to-end | general-docs | exact-match-gold | 20 | 10 | 9 | 9 | 13 |
| end-to-end | general-docs | llm-judge-balanced-proxy | 20 | 10 | 9 | 9 | 13 |
| generator-oracle | finance | citation-strict-judge-proxy | 19 | 8 | 8 | 0 | 0 |
| generator-oracle | finance | exact-match-gold | 19 | 8 | 8 | 0 | 0 |
| generator-oracle | finance | llm-judge-balanced-proxy | 19 | 8 | 8 | 0 | 0 |
| generator-oracle | financebench-open-source | citation-strict-judge-proxy | 150 | 65 | 65 | 0 | 0 |
| generator-oracle | financebench-open-source | exact-match-gold | 150 | 69 | 69 | 0 | 0 |
| generator-oracle | financebench-open-source | llm-judge-balanced-proxy | 150 | 64 | 64 | 0 | 0 |
| generator-oracle | general-docs | citation-strict-judge-proxy | 20 | 3 | 3 | 2 | 0 |
| generator-oracle | general-docs | exact-match-gold | 20 | 4 | 4 | 2 | 0 |
| generator-oracle | general-docs | llm-judge-balanced-proxy | 20 | 4 | 4 | 2 | 0 |
| retrieval-only | finance | citation-strict-judge-proxy | 19 | 7 | 7 | 7 | 9 |
| retrieval-only | finance | exact-match-gold | 19 | 7 | 7 | 7 | 9 |
| retrieval-only | finance | llm-judge-balanced-proxy | 19 | 7 | 7 | 7 | 9 |
| retrieval-only | financebench-open-source | citation-strict-judge-proxy | 150 | 68 | 54 | 68 | 68 |
| retrieval-only | financebench-open-source | exact-match-gold | 150 | 68 | 60 | 68 | 68 |
| retrieval-only | financebench-open-source | llm-judge-balanced-proxy | 150 | 68 | 55 | 68 | 68 |
| retrieval-only | general-docs | citation-strict-judge-proxy | 20 | 7 | 5 | 7 | 13 |
| retrieval-only | general-docs | exact-match-gold | 20 | 7 | 6 | 7 | 13 |
| retrieval-only | general-docs | llm-judge-balanced-proxy | 20 | 7 | 6 | 7 | 13 |

## Categories That Separated Systems

| Track | Domain | Judge | Category | Answer Range | Best Answer | Worst Answer |
|---|---|---|---|---:|---:|---:|
| end-to-end | finance | citation-strict-judge-proxy | calculation | 0.667 | 0.667 | 0.000 |
| end-to-end | finance | citation-strict-judge-proxy | direct_lookup | 0.500 | 0.500 | 0.000 |
| end-to-end | finance | citation-strict-judge-proxy | section_navigation | 0.667 | 1.000 | 0.333 |
| end-to-end | finance | citation-strict-judge-proxy | table_numeric | 1.000 | 1.000 | 0.000 |
| end-to-end | finance | exact-match-gold | calculation | 0.667 | 0.667 | 0.000 |
| end-to-end | finance | exact-match-gold | direct_lookup | 0.500 | 1.000 | 0.500 |
| end-to-end | finance | exact-match-gold | section_navigation | 0.667 | 1.000 | 0.333 |
| end-to-end | finance | exact-match-gold | table_numeric | 1.000 | 1.000 | 0.000 |
| end-to-end | finance | llm-judge-balanced-proxy | calculation | 0.667 | 0.667 | 0.000 |
| end-to-end | finance | llm-judge-balanced-proxy | direct_lookup | 0.500 | 1.000 | 0.500 |
| end-to-end | finance | llm-judge-balanced-proxy | section_navigation | 0.667 | 0.833 | 0.167 |
| end-to-end | finance | llm-judge-balanced-proxy | table_numeric | 1.000 | 1.000 | 0.000 |
| end-to-end | financebench-open-source | citation-strict-judge-proxy | calculation | 0.149 | 0.209 | 0.060 |
| end-to-end | financebench-open-source | citation-strict-judge-proxy | direct_lookup | 0.211 | 0.632 | 0.421 |
| end-to-end | financebench-open-source | citation-strict-judge-proxy | section_navigation | 0.140 | 0.600 | 0.460 |
| end-to-end | financebench-open-source | citation-strict-judge-proxy | table_numeric | 0.214 | 0.214 | 0.000 |
| end-to-end | financebench-open-source | exact-match-gold | calculation | 0.164 | 0.239 | 0.075 |
| end-to-end | financebench-open-source | exact-match-gold | direct_lookup | 0.316 | 0.737 | 0.421 |
| end-to-end | financebench-open-source | exact-match-gold | section_navigation | 0.160 | 0.640 | 0.480 |
| end-to-end | financebench-open-source | exact-match-gold | table_numeric | 0.214 | 0.286 | 0.071 |
| end-to-end | financebench-open-source | llm-judge-balanced-proxy | calculation | 0.149 | 0.224 | 0.075 |
| end-to-end | financebench-open-source | llm-judge-balanced-proxy | direct_lookup | 0.316 | 0.632 | 0.316 |
| end-to-end | financebench-open-source | llm-judge-balanced-proxy | section_navigation | 0.120 | 0.600 | 0.480 |
| end-to-end | financebench-open-source | llm-judge-balanced-proxy | table_numeric | 0.214 | 0.286 | 0.071 |
| end-to-end | general-docs | citation-strict-judge-proxy | multi_section | 0.500 | 1.000 | 0.500 |
| end-to-end | general-docs | citation-strict-judge-proxy | no_answer | 0.500 | 1.000 | 0.500 |
| end-to-end | general-docs | citation-strict-judge-proxy | section_navigation | 0.444 | 0.889 | 0.444 |
| end-to-end | general-docs | exact-match-gold | multi_section | 0.500 | 1.000 | 0.500 |
| end-to-end | general-docs | exact-match-gold | no_answer | 0.500 | 1.000 | 0.500 |
| end-to-end | general-docs | exact-match-gold | section_navigation | 0.556 | 1.000 | 0.444 |
| end-to-end | general-docs | exact-match-gold | table_numeric | 0.500 | 1.000 | 0.500 |
| end-to-end | general-docs | llm-judge-balanced-proxy | multi_section | 0.500 | 1.000 | 0.500 |
| end-to-end | general-docs | llm-judge-balanced-proxy | no_answer | 0.500 | 1.000 | 0.500 |
| end-to-end | general-docs | llm-judge-balanced-proxy | section_navigation | 0.556 | 1.000 | 0.444 |
| end-to-end | general-docs | llm-judge-balanced-proxy | table_numeric | 0.500 | 1.000 | 0.500 |
| generator-oracle | finance | citation-strict-judge-proxy | calculation | 0.667 | 0.667 | 0.000 |
| generator-oracle | finance | citation-strict-judge-proxy | section_navigation | 0.167 | 1.000 | 0.833 |
| generator-oracle | finance | citation-strict-judge-proxy | table_numeric | 0.750 | 1.000 | 0.250 |
| generator-oracle | finance | exact-match-gold | calculation | 0.667 | 0.667 | 0.000 |
| generator-oracle | finance | exact-match-gold | section_navigation | 0.167 | 1.000 | 0.833 |
| generator-oracle | finance | exact-match-gold | table_numeric | 0.750 | 1.000 | 0.250 |
| generator-oracle | finance | llm-judge-balanced-proxy | calculation | 0.667 | 0.667 | 0.000 |
| generator-oracle | finance | llm-judge-balanced-proxy | section_navigation | 0.167 | 0.833 | 0.667 |
| generator-oracle | finance | llm-judge-balanced-proxy | table_numeric | 0.750 | 1.000 | 0.250 |
| generator-oracle | financebench-open-source | citation-strict-judge-proxy | calculation | 0.507 | 0.881 | 0.373 |
| generator-oracle | financebench-open-source | citation-strict-judge-proxy | section_navigation | 0.100 | 0.880 | 0.780 |
| generator-oracle | financebench-open-source | citation-strict-judge-proxy | table_numeric | 0.214 | 0.714 | 0.500 |
| generator-oracle | financebench-open-source | exact-match-gold | calculation | 0.522 | 0.940 | 0.418 |
| generator-oracle | financebench-open-source | exact-match-gold | direct_lookup | 0.053 | 1.000 | 0.947 |
| generator-oracle | financebench-open-source | exact-match-gold | section_navigation | 0.120 | 0.980 | 0.860 |
| generator-oracle | financebench-open-source | exact-match-gold | table_numeric | 0.286 | 0.857 | 0.571 |
| generator-oracle | financebench-open-source | llm-judge-balanced-proxy | calculation | 0.478 | 0.896 | 0.418 |
| generator-oracle | financebench-open-source | llm-judge-balanced-proxy | direct_lookup | 0.053 | 0.895 | 0.842 |
| generator-oracle | financebench-open-source | llm-judge-balanced-proxy | section_navigation | 0.100 | 0.940 | 0.840 |
| generator-oracle | financebench-open-source | llm-judge-balanced-proxy | table_numeric | 0.286 | 0.857 | 0.571 |
| generator-oracle | general-docs | citation-strict-judge-proxy | multi_document | 0.500 | 1.000 | 0.500 |
| generator-oracle | general-docs | citation-strict-judge-proxy | no_answer | 0.500 | 1.000 | 0.500 |
| generator-oracle | general-docs | exact-match-gold | multi_document | 0.500 | 1.000 | 0.500 |
| generator-oracle | general-docs | exact-match-gold | no_answer | 0.500 | 1.000 | 0.500 |
| generator-oracle | general-docs | exact-match-gold | table_numeric | 0.500 | 1.000 | 0.500 |
| generator-oracle | general-docs | llm-judge-balanced-proxy | multi_document | 0.500 | 1.000 | 0.500 |
| generator-oracle | general-docs | llm-judge-balanced-proxy | no_answer | 0.500 | 1.000 | 0.500 |
| generator-oracle | general-docs | llm-judge-balanced-proxy | table_numeric | 0.500 | 1.000 | 0.500 |
| retrieval-only | finance | citation-strict-judge-proxy | direct_lookup | 0.500 | 0.500 | 0.000 |
| retrieval-only | finance | citation-strict-judge-proxy | section_navigation | 0.500 | 1.000 | 0.500 |
| retrieval-only | finance | citation-strict-judge-proxy | table_numeric | 0.750 | 1.000 | 0.250 |
| retrieval-only | finance | exact-match-gold | direct_lookup | 0.500 | 1.000 | 0.500 |
| retrieval-only | finance | exact-match-gold | section_navigation | 0.500 | 1.000 | 0.500 |
| retrieval-only | finance | exact-match-gold | table_numeric | 0.750 | 1.000 | 0.250 |
| retrieval-only | finance | llm-judge-balanced-proxy | direct_lookup | 0.500 | 1.000 | 0.500 |
| retrieval-only | finance | llm-judge-balanced-proxy | section_navigation | 0.500 | 0.833 | 0.333 |
| retrieval-only | finance | llm-judge-balanced-proxy | table_numeric | 0.750 | 1.000 | 0.250 |
| retrieval-only | financebench-open-source | citation-strict-judge-proxy | calculation | 0.104 | 0.224 | 0.119 |
| retrieval-only | financebench-open-source | citation-strict-judge-proxy | direct_lookup | 0.211 | 0.632 | 0.421 |
| retrieval-only | financebench-open-source | citation-strict-judge-proxy | section_navigation | 0.100 | 0.620 | 0.520 |
| retrieval-only | financebench-open-source | citation-strict-judge-proxy | table_numeric | 0.214 | 0.286 | 0.071 |
| retrieval-only | financebench-open-source | exact-match-gold | calculation | 0.119 | 0.254 | 0.134 |
| retrieval-only | financebench-open-source | exact-match-gold | direct_lookup | 0.263 | 0.737 | 0.474 |
| retrieval-only | financebench-open-source | exact-match-gold | section_navigation | 0.120 | 0.660 | 0.540 |
| retrieval-only | financebench-open-source | exact-match-gold | table_numeric | 0.286 | 0.429 | 0.143 |
| retrieval-only | financebench-open-source | llm-judge-balanced-proxy | calculation | 0.090 | 0.224 | 0.134 |
| retrieval-only | financebench-open-source | llm-judge-balanced-proxy | direct_lookup | 0.263 | 0.632 | 0.368 |
| retrieval-only | financebench-open-source | llm-judge-balanced-proxy | section_navigation | 0.100 | 0.620 | 0.520 |
| retrieval-only | financebench-open-source | llm-judge-balanced-proxy | table_numeric | 0.286 | 0.429 | 0.143 |
| retrieval-only | general-docs | citation-strict-judge-proxy | multi_section | 0.500 | 1.000 | 0.500 |
| retrieval-only | general-docs | citation-strict-judge-proxy | section_navigation | 0.444 | 0.889 | 0.444 |
| retrieval-only | general-docs | exact-match-gold | multi_section | 0.500 | 1.000 | 0.500 |
| retrieval-only | general-docs | exact-match-gold | section_navigation | 0.556 | 1.000 | 0.444 |
| retrieval-only | general-docs | llm-judge-balanced-proxy | multi_section | 0.500 | 1.000 | 0.500 |
| retrieval-only | general-docs | llm-judge-balanced-proxy | section_navigation | 0.556 | 1.000 | 0.444 |

## Practical Reading

- Strong discrimination needs several systems to fail differently across many questions.
- A domain where every system scores the same is a harness smoke test, not a decision-grade benchmark.
- A single separating question can reveal a useful pattern, but it is too brittle for production selection.
