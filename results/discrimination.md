# Discrimination Audit

This audit checks whether the benchmark actually separates RAG systems.

## Verdict

- `finance`: **not discriminative**. All systems produced effectively the same quality scores; use this only as a smoke test.
- `general-docs`: **weakly discriminative**. Some systems separate, but too few questions drive the difference.

## Domain Metric Spread

| Domain | Metric | Min | Max | Range | Unique Values |
|---|---|---:|---:|---:|---:|
| finance | answer_correctness | 1.000 | 1.000 | 0.000 | 1 |
| finance | evidence_recall | 1.000 | 1.000 | 0.000 | 1 |
| finance | context_precision | 0.250 | 0.278 | 0.028 | 2 |
| finance | citation_validity | 1.000 | 1.000 | 0.000 | 1 |
| finance | failure_rate | 0.000 | 0.000 | 0.000 | 1 |
| general-docs | answer_correctness | 0.714 | 0.857 | 0.143 | 2 |
| general-docs | evidence_recall | 0.814 | 0.914 | 0.100 | 2 |
| general-docs | context_precision | 0.286 | 0.429 | 0.143 | 4 |
| general-docs | citation_validity | 0.714 | 0.857 | 0.143 | 2 |
| general-docs | failure_rate | 0.143 | 0.286 | 0.143 | 2 |

## Question-Level Discrimination

| Domain | Questions | Quality-Diff Questions | Answer-Diff Questions | Recall-Diff Questions | Precision-Diff Questions |
|---|---:|---:|---:|---:|---:|
| finance | 6 | 0 | 0 | 0 | 2 |
| general-docs | 7 | 2 | 1 | 2 | 6 |

## Categories That Separated Systems

| Domain | Category | Answer Range | Best Answer | Worst Answer |
|---|---|---:|---:|---:|
| general-docs | multi_document | 1.000 | 1.000 | 0.000 |

## Practical Reading

- Strong discrimination needs several systems to fail differently across many questions.
- A domain where every system scores the same is a harness smoke test, not a decision-grade benchmark.
- A single separating question can reveal a useful pattern, but it is too brittle for production selection.
