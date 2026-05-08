# Discrimination Audit

This audit checks whether the benchmark actually separates RAG systems.

## Verdict

- `end-to-end` / `finance`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `end-to-end` / `financebench-open-source`: **moderately discriminative**. The benchmark separates systems, but the margin is still narrow.
- `end-to-end` / `general-docs`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `generator-oracle` / `finance`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `generator-oracle` / `financebench-open-source`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `generator-oracle` / `general-docs`: **weakly discriminative**. Some systems separate, but too few questions drive the difference.
- `retrieval-only` / `finance`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `retrieval-only` / `financebench-open-source`: **moderately discriminative**. The benchmark separates systems, but the margin is still narrow.
- `retrieval-only` / `general-docs`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.

## Domain Metric Spread

| Track | Domain | Metric | Min | Max | Range | Unique Values |
|---|---|---|---:|---:|---:|---:|
| end-to-end | finance | answer_correctness | 0.421 | 0.895 | 0.474 | 10 |
| end-to-end | finance | evidence_recall | 0.632 | 1.000 | 0.368 | 5 |
| end-to-end | finance | context_precision | 0.175 | 0.289 | 0.114 | 6 |
| end-to-end | finance | citation_validity | 0.421 | 0.895 | 0.474 | 10 |
| end-to-end | finance | failure_rate | 0.105 | 0.579 | 0.474 | 10 |
| end-to-end | financebench-open-source | answer_correctness | 0.293 | 0.400 | 0.107 | 15 |
| end-to-end | financebench-open-source | evidence_recall | 0.343 | 0.456 | 0.112 | 11 |
| end-to-end | financebench-open-source | context_precision | 0.100 | 0.130 | 0.030 | 8 |
| end-to-end | financebench-open-source | citation_validity | 0.293 | 0.400 | 0.107 | 15 |
| end-to-end | financebench-open-source | failure_rate | 0.600 | 0.707 | 0.107 | 15 |
| end-to-end | general-docs | answer_correctness | 0.550 | 0.850 | 0.300 | 4 |
| end-to-end | general-docs | evidence_recall | 0.610 | 0.945 | 0.335 | 9 |
| end-to-end | general-docs | context_precision | 0.254 | 0.412 | 0.158 | 5 |
| end-to-end | general-docs | citation_validity | 0.550 | 0.900 | 0.350 | 6 |
| end-to-end | general-docs | failure_rate | 0.150 | 0.450 | 0.300 | 4 |
| generator-oracle | finance | answer_correctness | 0.632 | 0.895 | 0.263 | 3 |
| generator-oracle | finance | evidence_recall | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | finance | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | finance | citation_validity | 0.632 | 0.895 | 0.263 | 3 |
| generator-oracle | finance | failure_rate | 0.105 | 0.368 | 0.263 | 3 |
| generator-oracle | financebench-open-source | answer_correctness | 0.680 | 0.953 | 0.273 | 3 |
| generator-oracle | financebench-open-source | evidence_recall | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | financebench-open-source | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | financebench-open-source | citation_validity | 0.680 | 0.953 | 0.273 | 3 |
| generator-oracle | financebench-open-source | failure_rate | 0.047 | 0.320 | 0.273 | 3 |
| generator-oracle | general-docs | answer_correctness | 0.850 | 0.900 | 0.050 | 2 |
| generator-oracle | general-docs | evidence_recall | 0.940 | 0.990 | 0.050 | 2 |
| generator-oracle | general-docs | context_precision | 1.000 | 1.000 | 0.000 | 1 |
| generator-oracle | general-docs | citation_validity | 0.900 | 0.950 | 0.050 | 2 |
| generator-oracle | general-docs | failure_rate | 0.100 | 0.150 | 0.050 | 2 |
| retrieval-only | finance | answer_correctness | 0.632 | 1.000 | 0.368 | 5 |
| retrieval-only | finance | evidence_recall | 0.632 | 1.000 | 0.368 | 5 |
| retrieval-only | finance | context_precision | 0.175 | 0.289 | 0.114 | 6 |
| retrieval-only | finance | citation_validity | 0.632 | 1.000 | 0.368 | 5 |
| retrieval-only | finance | failure_rate | 0.000 | 0.368 | 0.368 | 5 |
| retrieval-only | financebench-open-source | answer_correctness | 0.320 | 0.420 | 0.100 | 9 |
| retrieval-only | financebench-open-source | evidence_recall | 0.343 | 0.456 | 0.112 | 11 |
| retrieval-only | financebench-open-source | context_precision | 0.100 | 0.130 | 0.030 | 8 |
| retrieval-only | financebench-open-source | citation_validity | 0.320 | 0.420 | 0.100 | 9 |
| retrieval-only | financebench-open-source | failure_rate | 0.580 | 0.680 | 0.100 | 9 |
| retrieval-only | general-docs | answer_correctness | 0.600 | 0.900 | 0.300 | 4 |
| retrieval-only | general-docs | evidence_recall | 0.660 | 0.945 | 0.285 | 5 |
| retrieval-only | general-docs | context_precision | 0.254 | 0.412 | 0.158 | 5 |
| retrieval-only | general-docs | citation_validity | 0.600 | 0.900 | 0.300 | 4 |
| retrieval-only | general-docs | failure_rate | 0.100 | 0.400 | 0.300 | 4 |

## Question-Level Discrimination

| Track | Domain | Questions | Quality-Diff Questions | Answer-Diff Questions | Recall-Diff Questions | Precision-Diff Questions |
|---|---|---:|---:|---:|---:|---:|
| end-to-end | finance | 19 | 11 | 11 | 7 | 9 |
| end-to-end | financebench-open-source | 150 | 71 | 62 | 68 | 68 |
| end-to-end | general-docs | 20 | 10 | 9 | 9 | 13 |
| generator-oracle | finance | 19 | 8 | 8 | 0 | 0 |
| generator-oracle | financebench-open-source | 150 | 69 | 69 | 0 | 0 |
| generator-oracle | general-docs | 20 | 4 | 4 | 2 | 0 |
| retrieval-only | finance | 19 | 7 | 7 | 7 | 9 |
| retrieval-only | financebench-open-source | 150 | 68 | 60 | 68 | 68 |
| retrieval-only | general-docs | 20 | 7 | 6 | 7 | 13 |

## Categories That Separated Systems

| Track | Domain | Category | Answer Range | Best Answer | Worst Answer |
|---|---|---|---:|---:|---:|
| end-to-end | finance | calculation | 0.667 | 0.667 | 0.000 |
| end-to-end | finance | direct_lookup | 0.500 | 1.000 | 0.500 |
| end-to-end | finance | section_navigation | 0.667 | 1.000 | 0.333 |
| end-to-end | finance | table_numeric | 1.000 | 1.000 | 0.000 |
| end-to-end | financebench-open-source | calculation | 0.164 | 0.239 | 0.075 |
| end-to-end | financebench-open-source | direct_lookup | 0.316 | 0.737 | 0.421 |
| end-to-end | financebench-open-source | section_navigation | 0.160 | 0.640 | 0.480 |
| end-to-end | financebench-open-source | table_numeric | 0.214 | 0.286 | 0.071 |
| end-to-end | general-docs | multi_section | 0.500 | 1.000 | 0.500 |
| end-to-end | general-docs | no_answer | 0.500 | 1.000 | 0.500 |
| end-to-end | general-docs | section_navigation | 0.556 | 1.000 | 0.444 |
| end-to-end | general-docs | table_numeric | 0.500 | 1.000 | 0.500 |
| generator-oracle | finance | calculation | 0.667 | 0.667 | 0.000 |
| generator-oracle | finance | section_navigation | 0.167 | 1.000 | 0.833 |
| generator-oracle | finance | table_numeric | 0.750 | 1.000 | 0.250 |
| generator-oracle | financebench-open-source | calculation | 0.522 | 0.940 | 0.418 |
| generator-oracle | financebench-open-source | direct_lookup | 0.053 | 1.000 | 0.947 |
| generator-oracle | financebench-open-source | section_navigation | 0.120 | 0.980 | 0.860 |
| generator-oracle | financebench-open-source | table_numeric | 0.286 | 0.857 | 0.571 |
| generator-oracle | general-docs | multi_document | 0.500 | 1.000 | 0.500 |
| generator-oracle | general-docs | no_answer | 0.500 | 1.000 | 0.500 |
| generator-oracle | general-docs | table_numeric | 0.500 | 1.000 | 0.500 |
| retrieval-only | finance | direct_lookup | 0.500 | 1.000 | 0.500 |
| retrieval-only | finance | section_navigation | 0.500 | 1.000 | 0.500 |
| retrieval-only | finance | table_numeric | 0.750 | 1.000 | 0.250 |
| retrieval-only | financebench-open-source | calculation | 0.119 | 0.254 | 0.134 |
| retrieval-only | financebench-open-source | direct_lookup | 0.263 | 0.737 | 0.474 |
| retrieval-only | financebench-open-source | section_navigation | 0.120 | 0.660 | 0.540 |
| retrieval-only | financebench-open-source | table_numeric | 0.286 | 0.429 | 0.143 |
| retrieval-only | general-docs | multi_section | 0.500 | 1.000 | 0.500 |
| retrieval-only | general-docs | section_navigation | 0.556 | 1.000 | 0.444 |

## Practical Reading

- Strong discrimination needs several systems to fail differently across many questions.
- A domain where every system scores the same is a harness smoke test, not a decision-grade benchmark.
- A single separating question can reveal a useful pattern, but it is too brittle for production selection.
