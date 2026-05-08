# Discrimination Audit

This audit checks whether the benchmark actually separates RAG systems.

## Verdict

- `finance`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.
- `financebench-open-source`: **moderately discriminative**. The benchmark separates systems, but the margin is still narrow.
- `general-docs`: **strongly discriminative**. Multiple systems separate on answer or evidence quality.

## Domain Metric Spread

| Domain | Metric | Min | Max | Range | Unique Values |
|---|---|---:|---:|---:|---:|
| finance | answer_correctness | 0.632 | 1.000 | 0.368 | 4 |
| finance | evidence_recall | 0.632 | 1.000 | 0.368 | 4 |
| finance | context_precision | 0.175 | 0.329 | 0.154 | 5 |
| finance | citation_validity | 0.632 | 1.000 | 0.368 | 4 |
| finance | failure_rate | 0.000 | 0.368 | 0.368 | 4 |
| financebench-open-source | answer_correctness | 0.333 | 0.420 | 0.087 | 6 |
| financebench-open-source | evidence_recall | 0.343 | 0.442 | 0.099 | 6 |
| financebench-open-source | context_precision | 0.100 | 0.128 | 0.028 | 6 |
| financebench-open-source | citation_validity | 0.320 | 0.413 | 0.093 | 5 |
| financebench-open-source | failure_rate | 0.580 | 0.667 | 0.087 | 6 |
| general-docs | answer_correctness | 0.600 | 0.900 | 0.300 | 4 |
| general-docs | evidence_recall | 0.660 | 0.945 | 0.285 | 5 |
| general-docs | context_precision | 0.254 | 0.417 | 0.163 | 5 |
| general-docs | citation_validity | 0.600 | 0.900 | 0.300 | 4 |
| general-docs | failure_rate | 0.100 | 0.400 | 0.300 | 4 |

## Question-Level Discrimination

| Domain | Questions | Quality-Diff Questions | Answer-Diff Questions | Recall-Diff Questions | Precision-Diff Questions |
|---|---:|---:|---:|---:|---:|
| finance | 19 | 7 | 7 | 7 | 9 |
| financebench-open-source | 150 | 70 | 61 | 68 | 68 |
| general-docs | 20 | 7 | 6 | 7 | 13 |

## Categories That Separated Systems

| Domain | Category | Answer Range | Best Answer | Worst Answer |
|---|---|---:|---:|---:|
| finance | direct_lookup | 0.500 | 1.000 | 0.500 |
| finance | section_navigation | 0.500 | 1.000 | 0.500 |
| finance | table_numeric | 0.750 | 1.000 | 0.250 |
| financebench-open-source | calculation | 0.164 | 0.299 | 0.134 |
| financebench-open-source | direct_lookup | 0.263 | 0.737 | 0.474 |
| financebench-open-source | section_navigation | 0.100 | 0.660 | 0.560 |
| financebench-open-source | table_numeric | 0.214 | 0.357 | 0.143 |
| general-docs | multi_section | 0.500 | 1.000 | 0.500 |
| general-docs | section_navigation | 0.556 | 1.000 | 0.444 |

## Practical Reading

- Strong discrimination needs several systems to fail differently across many questions.
- A domain where every system scores the same is a harness smoke test, not a decision-grade benchmark.
- A single separating question can reveal a useful pattern, but it is too brittle for production selection.
