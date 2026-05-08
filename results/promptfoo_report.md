# Promptfoo RAG Evaluation Report: eval-wF9-2026-05-08T11:38:13

- Total cases: 567
- Passed: 264
- Failed: 303
- Pass rate: 46.56%

## System Summary

| Domain | System | Pass Rate | Answer | Evidence | Citation | Readiness | Guidance |
|---|---|---:|---:|---:|---:|---|---|
| finance | `bm25` | 57.89% | 0.579 | 0.632 | 0.579 | not_ready | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity first. |
| finance | `hybrid` | 84.21% | 0.842 | 0.947 | 0.842 | not_ready | Do not use as production default yet; improve citation_validity first. |
| finance | `pageindex-oss` | 89.47% | 0.895 | 1.000 | 0.895 | pilot_candidate | Close to production; review citation_validity before rollout. |
| financebench-open-source | `bm25` | 38.67% | 0.387 | 0.419 | 0.387 | not_ready | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| financebench-open-source | `hybrid` | 40.00% | 0.400 | 0.456 | 0.400 | not_ready | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| financebench-open-source | `pageindex-oss` | 37.33% | 0.373 | 0.414 | 0.373 | not_ready | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| general-docs | `bm25` | 60.00% | 0.600 | 0.660 | 0.650 | not_ready | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, no_answer_hallucination first. |
| general-docs | `hybrid` | 85.00% | 0.850 | 0.885 | 0.900 | not_ready | Do not use as production default yet; improve no_answer_hallucination first. |
| general-docs | `pageindex-oss` | 85.00% | 0.850 | 0.895 | 0.900 | not_ready | Do not use as production default yet; improve no_answer_hallucination first. |
