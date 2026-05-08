# RAG Benchmark Report: 20260508T113736Z

This report compares RAG strategies, embedding profiles, and generator profiles for practical operations decisions.
Scores are generated from local fixture datasets and deterministic local profiles.

## End-to-End Scorecard

| Domain | RAG | Embedding | Generator | Answer | Evidence Recall | Context Precision | Citation | Latency ms | Cost | Failure |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| finance | bm25 | none | balanced-oss-llm | 0.421 | 0.632 | 0.175 | 0.421 | 0.02 | 0.000029 | 0.579 |
| finance | bm25 | none | extractive-strict | 0.421 | 0.632 | 0.175 | 0.421 | 0.02 | 0.000017 | 0.579 |
| finance | bm25 | none | reasoning-oss-llm | 0.579 | 0.632 | 0.175 | 0.579 | 0.02 | 0.000045 | 0.421 |
| finance | dense-vector | bge-m3-proxy | balanced-oss-llm | 0.737 | 1.000 | 0.289 | 0.737 | 0.04 | 0.000031 | 0.263 |
| finance | dense-vector | bge-m3-proxy | extractive-strict | 0.632 | 1.000 | 0.289 | 0.632 | 0.04 | 0.000018 | 0.368 |
| finance | dense-vector | bge-m3-proxy | reasoning-oss-llm | 0.895 | 1.000 | 0.289 | 0.895 | 0.04 | 0.000048 | 0.105 |
| finance | dense-vector | e5-large-v2-proxy | balanced-oss-llm | 0.737 | 1.000 | 0.289 | 0.737 | 0.04 | 0.000031 | 0.263 |
| finance | dense-vector | e5-large-v2-proxy | extractive-strict | 0.632 | 1.000 | 0.289 | 0.632 | 0.04 | 0.000018 | 0.368 |
| finance | dense-vector | e5-large-v2-proxy | reasoning-oss-llm | 0.895 | 1.000 | 0.289 | 0.895 | 0.04 | 0.000048 | 0.105 |
| finance | dense-vector | finance-e5-proxy | balanced-oss-llm | 0.737 | 1.000 | 0.289 | 0.737 | 0.04 | 0.000031 | 0.263 |
| finance | dense-vector | finance-e5-proxy | extractive-strict | 0.632 | 1.000 | 0.289 | 0.632 | 0.04 | 0.000018 | 0.368 |
| finance | dense-vector | finance-e5-proxy | reasoning-oss-llm | 0.895 | 1.000 | 0.289 | 0.895 | 0.04 | 0.000049 | 0.105 |
| finance | hybrid | bge-m3-proxy | balanced-oss-llm | 0.684 | 0.947 | 0.276 | 0.684 | 0.09 | 0.000031 | 0.316 |
| finance | hybrid | bge-m3-proxy | extractive-strict | 0.579 | 0.947 | 0.276 | 0.579 | 0.09 | 0.000018 | 0.421 |
| finance | hybrid | bge-m3-proxy | reasoning-oss-llm | 0.842 | 0.947 | 0.276 | 0.842 | 0.09 | 0.000048 | 0.158 |
| finance | hybrid | e5-large-v2-proxy | balanced-oss-llm | 0.684 | 0.947 | 0.276 | 0.684 | 0.08 | 0.000031 | 0.316 |
| finance | hybrid | e5-large-v2-proxy | extractive-strict | 0.579 | 0.947 | 0.276 | 0.579 | 0.08 | 0.000018 | 0.421 |
| finance | hybrid | e5-large-v2-proxy | reasoning-oss-llm | 0.842 | 0.947 | 0.276 | 0.842 | 0.08 | 0.000048 | 0.158 |
| finance | hybrid | finance-e5-proxy | balanced-oss-llm | 0.632 | 0.895 | 0.263 | 0.632 | 0.07 | 0.000032 | 0.368 |
| finance | hybrid | finance-e5-proxy | extractive-strict | 0.526 | 0.895 | 0.263 | 0.526 | 0.07 | 0.000018 | 0.474 |
| finance | hybrid | finance-e5-proxy | reasoning-oss-llm | 0.789 | 0.895 | 0.263 | 0.789 | 0.07 | 0.000049 | 0.211 |
| finance | hybrid-rerank | bge-m3-proxy | balanced-oss-llm | 0.737 | 1.000 | 0.289 | 0.737 | 0.11 | 0.000164 | 0.263 |
| finance | hybrid-rerank | bge-m3-proxy | extractive-strict | 0.632 | 1.000 | 0.289 | 0.632 | 0.11 | 0.000151 | 0.368 |
| finance | hybrid-rerank | bge-m3-proxy | reasoning-oss-llm | 0.895 | 1.000 | 0.289 | 0.895 | 0.11 | 0.000181 | 0.105 |
| finance | hybrid-rerank | e5-large-v2-proxy | balanced-oss-llm | 0.737 | 1.000 | 0.289 | 0.737 | 0.10 | 0.000164 | 0.263 |
| finance | hybrid-rerank | e5-large-v2-proxy | extractive-strict | 0.632 | 1.000 | 0.289 | 0.632 | 0.10 | 0.000151 | 0.368 |
| finance | hybrid-rerank | e5-large-v2-proxy | reasoning-oss-llm | 0.895 | 1.000 | 0.289 | 0.895 | 0.10 | 0.000181 | 0.105 |
| finance | hybrid-rerank | finance-e5-proxy | balanced-oss-llm | 0.737 | 1.000 | 0.289 | 0.737 | 0.11 | 0.000164 | 0.263 |
| finance | hybrid-rerank | finance-e5-proxy | extractive-strict | 0.632 | 1.000 | 0.289 | 0.632 | 0.11 | 0.000151 | 0.368 |
| finance | hybrid-rerank | finance-e5-proxy | reasoning-oss-llm | 0.895 | 1.000 | 0.289 | 0.895 | 0.11 | 0.000181 | 0.105 |
| finance | pageindex-oss | bge-m3-proxy | balanced-oss-llm | 0.737 | 1.000 | 0.250 | 0.737 | 0.06 | 0.000091 | 0.263 |
| finance | pageindex-oss | bge-m3-proxy | extractive-strict | 0.632 | 1.000 | 0.250 | 0.632 | 0.06 | 0.000078 | 0.368 |
| finance | pageindex-oss | bge-m3-proxy | reasoning-oss-llm | 0.895 | 1.000 | 0.250 | 0.895 | 0.06 | 0.000107 | 0.105 |
| finance | pageindex-oss | e5-large-v2-proxy | balanced-oss-llm | 0.737 | 1.000 | 0.250 | 0.737 | 0.06 | 0.000091 | 0.263 |
| finance | pageindex-oss | e5-large-v2-proxy | extractive-strict | 0.632 | 1.000 | 0.250 | 0.632 | 0.06 | 0.000078 | 0.368 |
| finance | pageindex-oss | e5-large-v2-proxy | reasoning-oss-llm | 0.895 | 1.000 | 0.250 | 0.895 | 0.06 | 0.000107 | 0.105 |
| finance | pageindex-oss | finance-e5-proxy | balanced-oss-llm | 0.737 | 1.000 | 0.250 | 0.737 | 0.06 | 0.000091 | 0.263 |
| finance | pageindex-oss | finance-e5-proxy | extractive-strict | 0.632 | 1.000 | 0.250 | 0.632 | 0.06 | 0.000078 | 0.368 |
| finance | pageindex-oss | finance-e5-proxy | reasoning-oss-llm | 0.895 | 1.000 | 0.250 | 0.895 | 0.06 | 0.000107 | 0.105 |
| finance | parent-child | none | balanced-oss-llm | 0.474 | 0.684 | 0.189 | 0.474 | 0.03 | 0.000027 | 0.526 |
| finance | parent-child | none | extractive-strict | 0.474 | 0.684 | 0.189 | 0.474 | 0.03 | 0.000015 | 0.526 |
| finance | parent-child | none | reasoning-oss-llm | 0.632 | 0.684 | 0.189 | 0.632 | 0.03 | 0.000041 | 0.368 |
| financebench-open-source | bm25 | none | balanced-oss-llm | 0.327 | 0.419 | 0.117 | 0.327 | 1.45 | 0.000864 | 0.673 |
| financebench-open-source | bm25 | none | extractive-strict | 0.340 | 0.419 | 0.117 | 0.340 | 1.45 | 0.000504 | 0.660 |
| financebench-open-source | bm25 | none | reasoning-oss-llm | 0.387 | 0.419 | 0.117 | 0.387 | 1.45 | 0.001345 | 0.613 |
| financebench-open-source | dense-vector | bge-m3-proxy | balanced-oss-llm | 0.307 | 0.424 | 0.127 | 0.307 | 2.11 | 0.000740 | 0.693 |
| financebench-open-source | dense-vector | bge-m3-proxy | extractive-strict | 0.313 | 0.424 | 0.127 | 0.313 | 2.11 | 0.000432 | 0.687 |
| financebench-open-source | dense-vector | bge-m3-proxy | reasoning-oss-llm | 0.367 | 0.424 | 0.127 | 0.367 | 2.11 | 0.001152 | 0.633 |
| financebench-open-source | dense-vector | e5-large-v2-proxy | balanced-oss-llm | 0.307 | 0.418 | 0.125 | 0.307 | 2.13 | 0.000740 | 0.693 |
| financebench-open-source | dense-vector | e5-large-v2-proxy | extractive-strict | 0.307 | 0.418 | 0.125 | 0.307 | 2.13 | 0.000432 | 0.693 |
| financebench-open-source | dense-vector | e5-large-v2-proxy | reasoning-oss-llm | 0.360 | 0.418 | 0.125 | 0.360 | 2.13 | 0.001152 | 0.640 |
| financebench-open-source | dense-vector | finance-e5-proxy | balanced-oss-llm | 0.300 | 0.418 | 0.123 | 0.300 | 2.12 | 0.000712 | 0.700 |
| financebench-open-source | dense-vector | finance-e5-proxy | extractive-strict | 0.307 | 0.418 | 0.123 | 0.307 | 2.12 | 0.000416 | 0.693 |
| financebench-open-source | dense-vector | finance-e5-proxy | reasoning-oss-llm | 0.360 | 0.418 | 0.123 | 0.360 | 2.12 | 0.001109 | 0.640 |
| financebench-open-source | hybrid | bge-m3-proxy | balanced-oss-llm | 0.340 | 0.456 | 0.130 | 0.340 | 3.58 | 0.000800 | 0.660 |
| financebench-open-source | hybrid | bge-m3-proxy | extractive-strict | 0.360 | 0.456 | 0.130 | 0.360 | 3.58 | 0.000467 | 0.640 |
| financebench-open-source | hybrid | bge-m3-proxy | reasoning-oss-llm | 0.400 | 0.456 | 0.130 | 0.400 | 3.58 | 0.001245 | 0.600 |
| financebench-open-source | hybrid | e5-large-v2-proxy | balanced-oss-llm | 0.340 | 0.446 | 0.127 | 0.340 | 3.60 | 0.000805 | 0.660 |
| financebench-open-source | hybrid | e5-large-v2-proxy | extractive-strict | 0.353 | 0.446 | 0.127 | 0.353 | 3.60 | 0.000470 | 0.647 |
| financebench-open-source | hybrid | e5-large-v2-proxy | reasoning-oss-llm | 0.393 | 0.446 | 0.127 | 0.393 | 3.60 | 0.001253 | 0.607 |
| financebench-open-source | hybrid | finance-e5-proxy | balanced-oss-llm | 0.333 | 0.432 | 0.123 | 0.333 | 3.60 | 0.000795 | 0.667 |
| financebench-open-source | hybrid | finance-e5-proxy | extractive-strict | 0.353 | 0.432 | 0.123 | 0.353 | 3.60 | 0.000464 | 0.647 |
| financebench-open-source | hybrid | finance-e5-proxy | reasoning-oss-llm | 0.400 | 0.432 | 0.123 | 0.400 | 3.60 | 0.001237 | 0.600 |
| financebench-open-source | hybrid-rerank | bge-m3-proxy | balanced-oss-llm | 0.307 | 0.400 | 0.110 | 0.307 | 5.38 | 0.001216 | 0.693 |
| financebench-open-source | hybrid-rerank | bge-m3-proxy | extractive-strict | 0.333 | 0.400 | 0.110 | 0.333 | 5.38 | 0.000843 | 0.667 |
| financebench-open-source | hybrid-rerank | bge-m3-proxy | reasoning-oss-llm | 0.367 | 0.400 | 0.110 | 0.367 | 5.38 | 0.001714 | 0.633 |
| financebench-open-source | hybrid-rerank | e5-large-v2-proxy | balanced-oss-llm | 0.307 | 0.400 | 0.110 | 0.307 | 5.08 | 0.001219 | 0.693 |
| financebench-open-source | hybrid-rerank | e5-large-v2-proxy | extractive-strict | 0.333 | 0.400 | 0.110 | 0.333 | 5.08 | 0.000845 | 0.667 |
| financebench-open-source | hybrid-rerank | e5-large-v2-proxy | reasoning-oss-llm | 0.367 | 0.400 | 0.110 | 0.367 | 5.08 | 0.001719 | 0.633 |
| financebench-open-source | hybrid-rerank | finance-e5-proxy | balanced-oss-llm | 0.313 | 0.403 | 0.112 | 0.313 | 5.10 | 0.001214 | 0.687 |
| financebench-open-source | hybrid-rerank | finance-e5-proxy | extractive-strict | 0.333 | 0.403 | 0.112 | 0.333 | 5.10 | 0.000842 | 0.667 |
| financebench-open-source | hybrid-rerank | finance-e5-proxy | reasoning-oss-llm | 0.373 | 0.403 | 0.112 | 0.373 | 5.10 | 0.001711 | 0.627 |
| financebench-open-source | pageindex-oss | bge-m3-proxy | balanced-oss-llm | 0.300 | 0.414 | 0.125 | 0.300 | 2.34 | 0.000793 | 0.700 |
| financebench-open-source | pageindex-oss | bge-m3-proxy | extractive-strict | 0.307 | 0.414 | 0.125 | 0.307 | 2.34 | 0.000488 | 0.693 |
| financebench-open-source | pageindex-oss | bge-m3-proxy | reasoning-oss-llm | 0.373 | 0.414 | 0.125 | 0.373 | 2.34 | 0.001202 | 0.627 |
| financebench-open-source | pageindex-oss | e5-large-v2-proxy | balanced-oss-llm | 0.300 | 0.414 | 0.125 | 0.300 | 2.35 | 0.000793 | 0.700 |
| financebench-open-source | pageindex-oss | e5-large-v2-proxy | extractive-strict | 0.307 | 0.414 | 0.125 | 0.307 | 2.35 | 0.000488 | 0.693 |
| financebench-open-source | pageindex-oss | e5-large-v2-proxy | reasoning-oss-llm | 0.373 | 0.414 | 0.125 | 0.373 | 2.35 | 0.001202 | 0.627 |
| financebench-open-source | pageindex-oss | finance-e5-proxy | balanced-oss-llm | 0.300 | 0.411 | 0.123 | 0.300 | 2.35 | 0.000789 | 0.700 |
| financebench-open-source | pageindex-oss | finance-e5-proxy | extractive-strict | 0.300 | 0.411 | 0.123 | 0.300 | 2.35 | 0.000485 | 0.700 |
| financebench-open-source | pageindex-oss | finance-e5-proxy | reasoning-oss-llm | 0.367 | 0.411 | 0.123 | 0.367 | 2.35 | 0.001194 | 0.633 |
| financebench-open-source | parent-child | none | balanced-oss-llm | 0.293 | 0.343 | 0.100 | 0.293 | 2.50 | 0.000853 | 0.707 |
| financebench-open-source | parent-child | none | extractive-strict | 0.293 | 0.343 | 0.100 | 0.293 | 2.50 | 0.000498 | 0.707 |
| financebench-open-source | parent-child | none | reasoning-oss-llm | 0.320 | 0.343 | 0.100 | 0.320 | 2.50 | 0.001328 | 0.680 |
| general-docs | bm25 | none | balanced-oss-llm | 0.600 | 0.660 | 0.258 | 0.650 | 0.02 | 0.000024 | 0.400 |
| general-docs | bm25 | none | extractive-strict | 0.600 | 0.710 | 0.258 | 0.600 | 0.02 | 0.000014 | 0.400 |
| general-docs | bm25 | none | reasoning-oss-llm | 0.600 | 0.660 | 0.258 | 0.650 | 0.02 | 0.000038 | 0.400 |
| general-docs | dense-vector | bge-m3-proxy | balanced-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.05 | 0.000027 | 0.150 |
| general-docs | dense-vector | bge-m3-proxy | extractive-strict | 0.850 | 0.935 | 0.412 | 0.850 | 0.05 | 0.000016 | 0.150 |
| general-docs | dense-vector | bge-m3-proxy | reasoning-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.05 | 0.000042 | 0.150 |
| general-docs | dense-vector | e5-large-v2-proxy | balanced-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.05 | 0.000027 | 0.150 |
| general-docs | dense-vector | e5-large-v2-proxy | extractive-strict | 0.850 | 0.935 | 0.412 | 0.850 | 0.05 | 0.000016 | 0.150 |
| general-docs | dense-vector | e5-large-v2-proxy | reasoning-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.05 | 0.000042 | 0.150 |
| general-docs | dense-vector | finance-e5-proxy | balanced-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.05 | 0.000027 | 0.150 |
| general-docs | dense-vector | finance-e5-proxy | extractive-strict | 0.850 | 0.935 | 0.412 | 0.850 | 0.05 | 0.000016 | 0.150 |
| general-docs | dense-vector | finance-e5-proxy | reasoning-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.05 | 0.000042 | 0.150 |
| general-docs | hybrid | bge-m3-proxy | balanced-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.08 | 0.000027 | 0.150 |
| general-docs | hybrid | bge-m3-proxy | extractive-strict | 0.850 | 0.935 | 0.412 | 0.850 | 0.08 | 0.000016 | 0.150 |
| general-docs | hybrid | bge-m3-proxy | reasoning-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.08 | 0.000043 | 0.150 |
| general-docs | hybrid | e5-large-v2-proxy | balanced-oss-llm | 0.800 | 0.860 | 0.400 | 0.850 | 0.08 | 0.000027 | 0.200 |
| general-docs | hybrid | e5-large-v2-proxy | extractive-strict | 0.800 | 0.910 | 0.400 | 0.800 | 0.08 | 0.000015 | 0.200 |
| general-docs | hybrid | e5-large-v2-proxy | reasoning-oss-llm | 0.800 | 0.860 | 0.400 | 0.850 | 0.08 | 0.000042 | 0.200 |
| general-docs | hybrid | finance-e5-proxy | balanced-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.08 | 0.000027 | 0.150 |
| general-docs | hybrid | finance-e5-proxy | extractive-strict | 0.850 | 0.935 | 0.412 | 0.850 | 0.08 | 0.000016 | 0.150 |
| general-docs | hybrid | finance-e5-proxy | reasoning-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.08 | 0.000043 | 0.150 |
| general-docs | hybrid-rerank | bge-m3-proxy | balanced-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.11 | 0.000125 | 0.150 |
| general-docs | hybrid-rerank | bge-m3-proxy | extractive-strict | 0.850 | 0.935 | 0.412 | 0.850 | 0.11 | 0.000114 | 0.150 |
| general-docs | hybrid-rerank | bge-m3-proxy | reasoning-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.11 | 0.000140 | 0.150 |
| general-docs | hybrid-rerank | e5-large-v2-proxy | balanced-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.12 | 0.000125 | 0.150 |
| general-docs | hybrid-rerank | e5-large-v2-proxy | extractive-strict | 0.850 | 0.935 | 0.412 | 0.850 | 0.12 | 0.000114 | 0.150 |
| general-docs | hybrid-rerank | e5-large-v2-proxy | reasoning-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.12 | 0.000140 | 0.150 |
| general-docs | hybrid-rerank | finance-e5-proxy | balanced-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.10 | 0.000125 | 0.150 |
| general-docs | hybrid-rerank | finance-e5-proxy | extractive-strict | 0.850 | 0.935 | 0.412 | 0.850 | 0.10 | 0.000114 | 0.150 |
| general-docs | hybrid-rerank | finance-e5-proxy | reasoning-oss-llm | 0.850 | 0.885 | 0.412 | 0.900 | 0.10 | 0.000140 | 0.150 |
| general-docs | pageindex-oss | bge-m3-proxy | balanced-oss-llm | 0.850 | 0.895 | 0.263 | 0.900 | 0.07 | 0.000092 | 0.150 |
| general-docs | pageindex-oss | bge-m3-proxy | extractive-strict | 0.850 | 0.945 | 0.263 | 0.850 | 0.07 | 0.000078 | 0.150 |
| general-docs | pageindex-oss | bge-m3-proxy | reasoning-oss-llm | 0.850 | 0.895 | 0.263 | 0.900 | 0.07 | 0.000110 | 0.150 |
| general-docs | pageindex-oss | e5-large-v2-proxy | balanced-oss-llm | 0.850 | 0.895 | 0.263 | 0.900 | 0.08 | 0.000092 | 0.150 |
| general-docs | pageindex-oss | e5-large-v2-proxy | extractive-strict | 0.850 | 0.945 | 0.263 | 0.850 | 0.08 | 0.000078 | 0.150 |
| general-docs | pageindex-oss | e5-large-v2-proxy | reasoning-oss-llm | 0.850 | 0.895 | 0.263 | 0.900 | 0.08 | 0.000110 | 0.150 |
| general-docs | pageindex-oss | finance-e5-proxy | balanced-oss-llm | 0.850 | 0.895 | 0.263 | 0.900 | 0.07 | 0.000092 | 0.150 |
| general-docs | pageindex-oss | finance-e5-proxy | extractive-strict | 0.850 | 0.945 | 0.263 | 0.850 | 0.07 | 0.000078 | 0.150 |
| general-docs | pageindex-oss | finance-e5-proxy | reasoning-oss-llm | 0.850 | 0.895 | 0.263 | 0.900 | 0.07 | 0.000110 | 0.150 |
| general-docs | parent-child | none | balanced-oss-llm | 0.550 | 0.610 | 0.254 | 0.600 | 0.03 | 0.000023 | 0.450 |
| general-docs | parent-child | none | extractive-strict | 0.550 | 0.660 | 0.254 | 0.550 | 0.03 | 0.000013 | 0.450 |
| general-docs | parent-child | none | reasoning-oss-llm | 0.550 | 0.610 | 0.254 | 0.600 | 0.03 | 0.000035 | 0.450 |

## Recommendation Ranking

Recommendation score combines quality, efficiency, and stability. It is a decision aid, not a universal truth.

| Domain | Rank | System | Recommendation | Quality | Efficiency | Stability | Role |
|---|---:|---|---:|---:|---:|---:|---|
| finance | 1 | `dense-vector` | 0.791 | 0.866 | 0.469 | 0.895 | semantic similarity baseline |
| finance | 2 | `dense-vector` | 0.789 | 0.866 | 0.461 | 0.895 | semantic similarity baseline |
| finance | 3 | `dense-vector` | 0.789 | 0.866 | 0.461 | 0.895 | semantic similarity baseline |
| finance | 4 | `pageindex-oss` | 0.756 | 0.862 | 0.310 | 0.895 | structured long-document and multi-section navigation |
| finance | 5 | `pageindex-oss` | 0.755 | 0.862 | 0.304 | 0.895 | structured long-document and multi-section navigation |
| finance | 6 | `pageindex-oss` | 0.755 | 0.862 | 0.301 | 0.895 | structured long-document and multi-section navigation |
| finance | 7 | `hybrid` | 0.726 | 0.817 | 0.344 | 0.842 | balanced default for mixed queries |
| finance | 8 | `hybrid` | 0.718 | 0.817 | 0.301 | 0.842 | balanced default for mixed queries |
| finance | 9 | `dense-vector` | 0.711 | 0.771 | 0.497 | 0.737 | semantic similarity baseline |
| finance | 10 | `dense-vector` | 0.710 | 0.771 | 0.489 | 0.737 | semantic similarity baseline |
| finance | 11 | `dense-vector` | 0.709 | 0.771 | 0.489 | 0.737 | semantic similarity baseline |
| finance | 12 | `hybrid-rerank` | 0.702 | 0.866 | 0.024 | 0.895 | quality-first retrieval when rerank latency is acceptable |
| finance | 13 | `hybrid-rerank` | 0.701 | 0.866 | 0.020 | 0.895 | quality-first retrieval when rerank latency is acceptable |
| finance | 14 | `hybrid-rerank` | 0.697 | 0.866 | 0.001 | 0.895 | quality-first retrieval when rerank latency is acceptable |
| finance | 15 | `hybrid` | 0.689 | 0.768 | 0.354 | 0.789 | balanced default for mixed queries |
| finance | 16 | `pageindex-oss` | 0.677 | 0.767 | 0.337 | 0.737 | structured long-document and multi-section navigation |
| finance | 17 | `pageindex-oss` | 0.675 | 0.767 | 0.331 | 0.737 | structured long-document and multi-section navigation |
| finance | 18 | `pageindex-oss` | 0.675 | 0.767 | 0.329 | 0.737 | structured long-document and multi-section navigation |
| finance | 19 | `dense-vector` | 0.659 | 0.708 | 0.519 | 0.632 | semantic similarity baseline |
| finance | 20 | `dense-vector` | 0.657 | 0.708 | 0.511 | 0.632 | semantic similarity baseline |
| finance | 21 | `dense-vector` | 0.657 | 0.708 | 0.510 | 0.632 | semantic similarity baseline |
| finance | 22 | `hybrid` | 0.647 | 0.722 | 0.373 | 0.684 | balanced default for mixed queries |
| finance | 23 | `hybrid` | 0.638 | 0.722 | 0.329 | 0.684 | balanced default for mixed queries |
| finance | 24 | `pageindex-oss` | 0.624 | 0.704 | 0.358 | 0.632 | structured long-document and multi-section navigation |
| finance | 25 | `pageindex-oss` | 0.623 | 0.704 | 0.352 | 0.632 | structured long-document and multi-section navigation |
| finance | 26 | `pageindex-oss` | 0.622 | 0.704 | 0.350 | 0.632 | structured long-document and multi-section navigation |
| finance | 27 | `hybrid-rerank` | 0.622 | 0.771 | 0.052 | 0.737 | quality-first retrieval when rerank latency is acceptable |
| finance | 28 | `hybrid-rerank` | 0.621 | 0.771 | 0.048 | 0.737 | quality-first retrieval when rerank latency is acceptable |
| finance | 29 | `hybrid-rerank` | 0.618 | 0.771 | 0.029 | 0.737 | quality-first retrieval when rerank latency is acceptable |
| finance | 30 | `hybrid` | 0.609 | 0.674 | 0.382 | 0.632 | balanced default for mixed queries |
| finance | 31 | `parent-child` | 0.605 | 0.603 | 0.589 | 0.632 | small-chunk search with broader answer context |
| finance | 32 | `hybrid` | 0.594 | 0.659 | 0.394 | 0.579 | balanced default for mixed queries |
| finance | 33 | `hybrid` | 0.586 | 0.659 | 0.351 | 0.579 | balanced default for mixed queries |
| finance | 34 | `hybrid-rerank` | 0.570 | 0.708 | 0.074 | 0.632 | quality-first retrieval when rerank latency is acceptable |
| finance | 35 | `hybrid-rerank` | 0.569 | 0.708 | 0.070 | 0.632 | quality-first retrieval when rerank latency is acceptable |
| finance | 36 | `hybrid-rerank` | 0.565 | 0.708 | 0.051 | 0.632 | quality-first retrieval when rerank latency is acceptable |
| finance | 37 | `bm25` | 0.564 | 0.554 | 0.585 | 0.579 | fast exact-term baseline |
| finance | 38 | `hybrid` | 0.557 | 0.611 | 0.404 | 0.526 | balanced default for mixed queries |
| finance | 39 | `parent-child` | 0.528 | 0.508 | 0.631 | 0.474 | small-chunk search with broader answer context |
| finance | 40 | `parent-child` | 0.524 | 0.508 | 0.613 | 0.474 | small-chunk search with broader answer context |
| finance | 41 | `bm25` | 0.488 | 0.460 | 0.632 | 0.421 | fast exact-term baseline |
| finance | 42 | `bm25` | 0.484 | 0.460 | 0.612 | 0.421 | fast exact-term baseline |
| financebench-open-source | 1 | `bm25` | 0.376 | 0.341 | 0.516 | 0.340 | fast exact-term baseline |
| financebench-open-source | 2 | `bm25` | 0.372 | 0.369 | 0.369 | 0.387 | fast exact-term baseline |
| financebench-open-source | 3 | `hybrid` | 0.369 | 0.366 | 0.386 | 0.360 | balanced default for mixed queries |
| financebench-open-source | 4 | `dense-vector` | 0.368 | 0.360 | 0.396 | 0.367 | semantic similarity baseline |
| financebench-open-source | 5 | `dense-vector` | 0.366 | 0.354 | 0.413 | 0.360 | semantic similarity baseline |
| financebench-open-source | 6 | `pageindex-oss` | 0.365 | 0.361 | 0.372 | 0.373 | structured long-document and multi-section navigation |
| financebench-open-source | 7 | `pageindex-oss` | 0.365 | 0.361 | 0.372 | 0.373 | structured long-document and multi-section navigation |
| financebench-open-source | 8 | `dense-vector` | 0.365 | 0.328 | 0.522 | 0.313 | semantic similarity baseline |
| financebench-open-source | 9 | `hybrid` | 0.363 | 0.390 | 0.250 | 0.400 | balanced default for mixed queries |
| financebench-open-source | 10 | `dense-vector` | 0.363 | 0.354 | 0.394 | 0.360 | semantic similarity baseline |
| financebench-open-source | 11 | `hybrid` | 0.362 | 0.358 | 0.383 | 0.353 | balanced default for mixed queries |
| financebench-open-source | 12 | `dense-vector` | 0.362 | 0.322 | 0.534 | 0.307 | semantic similarity baseline |
| financebench-open-source | 13 | `pageindex-oss` | 0.361 | 0.356 | 0.375 | 0.367 | structured long-document and multi-section navigation |
| financebench-open-source | 14 | `hybrid` | 0.360 | 0.354 | 0.387 | 0.353 | balanced default for mixed queries |
| financebench-open-source | 15 | `dense-vector` | 0.359 | 0.322 | 0.520 | 0.307 | semantic similarity baseline |
| financebench-open-source | 16 | `hybrid` | 0.359 | 0.382 | 0.252 | 0.400 | balanced default for mixed queries |
| financebench-open-source | 17 | `hybrid` | 0.357 | 0.382 | 0.246 | 0.393 | balanced default for mixed queries |
| financebench-open-source | 18 | `bm25` | 0.356 | 0.333 | 0.453 | 0.327 | fast exact-term baseline |
| financebench-open-source | 19 | `pageindex-oss` | 0.354 | 0.321 | 0.497 | 0.307 | structured long-document and multi-section navigation |
| financebench-open-source | 20 | `pageindex-oss` | 0.354 | 0.321 | 0.496 | 0.307 | structured long-document and multi-section navigation |
| financebench-open-source | 21 | `dense-vector` | 0.350 | 0.324 | 0.468 | 0.307 | semantic similarity baseline |
| financebench-open-source | 22 | `pageindex-oss` | 0.350 | 0.316 | 0.499 | 0.300 | structured long-document and multi-section navigation |
| financebench-open-source | 23 | `dense-vector` | 0.348 | 0.322 | 0.466 | 0.307 | semantic similarity baseline |
| financebench-open-source | 24 | `dense-vector` | 0.348 | 0.318 | 0.482 | 0.300 | semantic similarity baseline |
| financebench-open-source | 25 | `hybrid` | 0.346 | 0.354 | 0.328 | 0.340 | balanced default for mixed queries |
| financebench-open-source | 26 | `hybrid` | 0.344 | 0.350 | 0.324 | 0.340 | balanced default for mixed queries |
| financebench-open-source | 27 | `pageindex-oss` | 0.340 | 0.317 | 0.443 | 0.300 | structured long-document and multi-section navigation |
| financebench-open-source | 28 | `pageindex-oss` | 0.340 | 0.317 | 0.443 | 0.300 | structured long-document and multi-section navigation |
| financebench-open-source | 29 | `pageindex-oss` | 0.339 | 0.316 | 0.446 | 0.300 | structured long-document and multi-section navigation |
| financebench-open-source | 30 | `hybrid` | 0.338 | 0.342 | 0.329 | 0.333 | balanced default for mixed queries |
| financebench-open-source | 31 | `parent-child` | 0.320 | 0.289 | 0.442 | 0.293 | small-chunk search with broader answer context |
| financebench-open-source | 32 | `parent-child` | 0.308 | 0.289 | 0.380 | 0.293 | small-chunk search with broader answer context |
| financebench-open-source | 33 | `parent-child` | 0.306 | 0.305 | 0.297 | 0.320 | small-chunk search with broader answer context |
| financebench-open-source | 34 | `hybrid-rerank` | 0.301 | 0.332 | 0.176 | 0.333 | quality-first retrieval when rerank latency is acceptable |
| financebench-open-source | 35 | `hybrid-rerank` | 0.300 | 0.331 | 0.175 | 0.333 | quality-first retrieval when rerank latency is acceptable |
| financebench-open-source | 36 | `hybrid-rerank` | 0.296 | 0.331 | 0.154 | 0.333 | quality-first retrieval when rerank latency is acceptable |
| financebench-open-source | 37 | `hybrid-rerank` | 0.292 | 0.356 | 0.024 | 0.373 | quality-first retrieval when rerank latency is acceptable |
| financebench-open-source | 38 | `hybrid-rerank` | 0.288 | 0.351 | 0.022 | 0.367 | quality-first retrieval when rerank latency is acceptable |
| financebench-open-source | 39 | `hybrid-rerank` | 0.284 | 0.351 | 0.002 | 0.367 | quality-first retrieval when rerank latency is acceptable |
| financebench-open-source | 40 | `hybrid-rerank` | 0.277 | 0.320 | 0.111 | 0.313 | quality-first retrieval when rerank latency is acceptable |
| financebench-open-source | 41 | `hybrid-rerank` | 0.273 | 0.315 | 0.110 | 0.307 | quality-first retrieval when rerank latency is acceptable |
| financebench-open-source | 42 | `hybrid-rerank` | 0.269 | 0.315 | 0.089 | 0.307 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 1 | `dense-vector` | 0.780 | 0.832 | 0.558 | 0.850 | semantic similarity baseline |
| general-docs | 2 | `dense-vector` | 0.779 | 0.832 | 0.555 | 0.850 | semantic similarity baseline |
| general-docs | 3 | `dense-vector` | 0.779 | 0.832 | 0.553 | 0.850 | semantic similarity baseline |
| general-docs | 4 | `dense-vector` | 0.770 | 0.824 | 0.533 | 0.850 | semantic similarity baseline |
| general-docs | 5 | `dense-vector` | 0.769 | 0.824 | 0.530 | 0.850 | semantic similarity baseline |
| general-docs | 6 | `dense-vector` | 0.769 | 0.824 | 0.528 | 0.850 | semantic similarity baseline |
| general-docs | 7 | `dense-vector` | 0.763 | 0.824 | 0.500 | 0.850 | semantic similarity baseline |
| general-docs | 8 | `dense-vector` | 0.763 | 0.824 | 0.498 | 0.850 | semantic similarity baseline |
| general-docs | 9 | `dense-vector` | 0.762 | 0.824 | 0.496 | 0.850 | semantic similarity baseline |
| general-docs | 10 | `hybrid` | 0.760 | 0.832 | 0.459 | 0.850 | balanced default for mixed queries |
| general-docs | 11 | `hybrid` | 0.758 | 0.832 | 0.449 | 0.850 | balanced default for mixed queries |
| general-docs | 12 | `hybrid` | 0.750 | 0.824 | 0.434 | 0.850 | balanced default for mixed queries |
| general-docs | 13 | `hybrid` | 0.748 | 0.824 | 0.424 | 0.850 | balanced default for mixed queries |
| general-docs | 14 | `hybrid` | 0.744 | 0.824 | 0.402 | 0.850 | balanced default for mixed queries |
| general-docs | 15 | `hybrid` | 0.742 | 0.824 | 0.391 | 0.850 | balanced default for mixed queries |
| general-docs | 16 | `hybrid` | 0.727 | 0.793 | 0.455 | 0.800 | balanced default for mixed queries |
| general-docs | 17 | `hybrid` | 0.717 | 0.786 | 0.431 | 0.800 | balanced default for mixed queries |
| general-docs | 18 | `pageindex-oss` | 0.716 | 0.820 | 0.278 | 0.850 | structured long-document and multi-section navigation |
| general-docs | 19 | `pageindex-oss` | 0.716 | 0.820 | 0.276 | 0.850 | structured long-document and multi-section navigation |
| general-docs | 20 | `pageindex-oss` | 0.715 | 0.820 | 0.272 | 0.850 | structured long-document and multi-section navigation |
| general-docs | 21 | `hybrid` | 0.710 | 0.786 | 0.399 | 0.800 | balanced default for mixed queries |
| general-docs | 22 | `pageindex-oss` | 0.705 | 0.812 | 0.249 | 0.850 | structured long-document and multi-section navigation |
| general-docs | 23 | `pageindex-oss` | 0.705 | 0.812 | 0.247 | 0.850 | structured long-document and multi-section navigation |
| general-docs | 24 | `pageindex-oss` | 0.704 | 0.812 | 0.243 | 0.850 | structured long-document and multi-section navigation |
| general-docs | 25 | `hybrid-rerank` | 0.699 | 0.832 | 0.152 | 0.850 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 26 | `hybrid-rerank` | 0.698 | 0.832 | 0.150 | 0.850 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 27 | `pageindex-oss` | 0.698 | 0.812 | 0.211 | 0.850 | structured long-document and multi-section navigation |
| general-docs | 28 | `pageindex-oss` | 0.697 | 0.812 | 0.209 | 0.850 | structured long-document and multi-section navigation |
| general-docs | 29 | `pageindex-oss` | 0.696 | 0.812 | 0.205 | 0.850 | structured long-document and multi-section navigation |
| general-docs | 30 | `hybrid-rerank` | 0.691 | 0.832 | 0.114 | 0.850 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 31 | `hybrid-rerank` | 0.689 | 0.824 | 0.127 | 0.850 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 32 | `hybrid-rerank` | 0.688 | 0.824 | 0.125 | 0.850 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 33 | `hybrid-rerank` | 0.682 | 0.824 | 0.095 | 0.850 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 34 | `hybrid-rerank` | 0.682 | 0.824 | 0.093 | 0.850 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 35 | `hybrid-rerank` | 0.681 | 0.824 | 0.089 | 0.850 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 36 | `hybrid-rerank` | 0.675 | 0.824 | 0.057 | 0.850 | quality-first retrieval when rerank latency is acceptable |
| general-docs | 37 | `bm25` | 0.614 | 0.599 | 0.674 | 0.600 | fast exact-term baseline |
| general-docs | 38 | `bm25` | 0.605 | 0.591 | 0.652 | 0.600 | fast exact-term baseline |
| general-docs | 39 | `bm25` | 0.599 | 0.591 | 0.623 | 0.600 | fast exact-term baseline |
| general-docs | 40 | `parent-child` | 0.578 | 0.553 | 0.679 | 0.550 | small-chunk search with broader answer context |
| general-docs | 41 | `parent-child` | 0.569 | 0.546 | 0.658 | 0.550 | small-chunk search with broader answer context |
| general-docs | 42 | `parent-child` | 0.564 | 0.546 | 0.631 | 0.550 | small-chunk search with broader answer context |

## Production Readiness

Suggested production gates: pass rate >= 0.80, answer correctness >= 0.80, evidence recall >= 0.85, citation validity >= 0.90, no-answer hallucination <= 0.05, and FinanceBench calculation pass rate >= 0.80 when applicable.

| Source | Domain | System | Status | Readiness | Pass | Answer | Evidence | Citation | No-answer Hallucination | Calc Pass | Guidance |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| benchmark | finance | `dense-vector` | pilot_candidate | 0.892 | 0.895 | 0.895 | 1.000 | 0.895 | 0.000 | 0.667 | Close to production; review citation_validity before rollout. |
| benchmark | finance | `dense-vector` | pilot_candidate | 0.892 | 0.895 | 0.895 | 1.000 | 0.895 | 0.000 | 0.667 | Close to production; review citation_validity before rollout. |
| benchmark | finance | `dense-vector` | pilot_candidate | 0.892 | 0.895 | 0.895 | 1.000 | 0.895 | 0.000 | 0.667 | Close to production; review citation_validity before rollout. |
| benchmark | finance | `hybrid-rerank` | pilot_candidate | 0.892 | 0.895 | 0.895 | 1.000 | 0.895 | 0.000 | 0.667 | Close to production; review citation_validity before rollout. |
| benchmark | finance | `hybrid-rerank` | pilot_candidate | 0.892 | 0.895 | 0.895 | 1.000 | 0.895 | 0.000 | 0.667 | Close to production; review citation_validity before rollout. |
| benchmark | finance | `hybrid-rerank` | pilot_candidate | 0.892 | 0.895 | 0.895 | 1.000 | 0.895 | 0.000 | 0.667 | Close to production; review citation_validity before rollout. |
| benchmark | finance | `pageindex-oss` | pilot_candidate | 0.892 | 0.895 | 0.895 | 1.000 | 0.895 | 0.000 | 0.667 | Close to production; review citation_validity before rollout. |
| benchmark | finance | `pageindex-oss` | pilot_candidate | 0.892 | 0.895 | 0.895 | 1.000 | 0.895 | 0.000 | 0.667 | Close to production; review citation_validity before rollout. |
| benchmark | finance | `pageindex-oss` | pilot_candidate | 0.892 | 0.895 | 0.895 | 1.000 | 0.895 | 0.000 | 0.667 | Close to production; review citation_validity before rollout. |
| benchmark | finance | `hybrid` | not_ready | 0.852 | 0.842 | 0.842 | 0.947 | 0.842 | 0.000 | 0.667 | Do not use as production default yet; improve citation_validity first. |
| benchmark | finance | `hybrid` | not_ready | 0.852 | 0.842 | 0.842 | 0.947 | 0.842 | 0.000 | 0.667 | Do not use as production default yet; improve citation_validity first. |
| benchmark | finance | `hybrid` | not_ready | 0.811 | 0.789 | 0.789 | 0.895 | 0.789 | 0.000 | 0.667 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `dense-vector` | not_ready | 0.705 | 0.737 | 0.737 | 1.000 | 0.737 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `dense-vector` | not_ready | 0.705 | 0.737 | 0.737 | 1.000 | 0.737 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `dense-vector` | not_ready | 0.705 | 0.737 | 0.737 | 1.000 | 0.737 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `hybrid-rerank` | not_ready | 0.705 | 0.737 | 0.737 | 1.000 | 0.737 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `hybrid-rerank` | not_ready | 0.705 | 0.737 | 0.737 | 1.000 | 0.737 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `hybrid-rerank` | not_ready | 0.705 | 0.737 | 0.737 | 1.000 | 0.737 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `pageindex-oss` | not_ready | 0.705 | 0.737 | 0.737 | 1.000 | 0.737 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `pageindex-oss` | not_ready | 0.705 | 0.737 | 0.737 | 1.000 | 0.737 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `pageindex-oss` | not_ready | 0.705 | 0.737 | 0.737 | 1.000 | 0.737 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `parent-child` | not_ready | 0.679 | 0.632 | 0.632 | 0.684 | 0.632 | 0.000 | 0.667 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity first. |
| benchmark | finance | `hybrid` | not_ready | 0.664 | 0.684 | 0.684 | 0.947 | 0.684 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `hybrid` | not_ready | 0.664 | 0.684 | 0.684 | 0.947 | 0.684 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `dense-vector` | not_ready | 0.646 | 0.632 | 0.632 | 1.000 | 0.632 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `dense-vector` | not_ready | 0.646 | 0.632 | 0.632 | 1.000 | 0.632 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `dense-vector` | not_ready | 0.646 | 0.632 | 0.632 | 1.000 | 0.632 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `hybrid-rerank` | not_ready | 0.646 | 0.632 | 0.632 | 1.000 | 0.632 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `hybrid-rerank` | not_ready | 0.646 | 0.632 | 0.632 | 1.000 | 0.632 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `hybrid-rerank` | not_ready | 0.646 | 0.632 | 0.632 | 1.000 | 0.632 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `pageindex-oss` | not_ready | 0.646 | 0.632 | 0.632 | 1.000 | 0.632 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `pageindex-oss` | not_ready | 0.646 | 0.632 | 0.632 | 1.000 | 0.632 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `pageindex-oss` | not_ready | 0.646 | 0.632 | 0.632 | 1.000 | 0.632 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `bm25` | not_ready | 0.639 | 0.579 | 0.579 | 0.632 | 0.579 | 0.000 | 0.667 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity first. |
| benchmark | finance | `hybrid` | not_ready | 0.624 | 0.632 | 0.632 | 0.895 | 0.632 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `hybrid` | not_ready | 0.606 | 0.579 | 0.579 | 0.947 | 0.579 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `hybrid` | not_ready | 0.606 | 0.579 | 0.579 | 0.947 | 0.579 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `hybrid` | not_ready | 0.566 | 0.526 | 0.526 | 0.895 | 0.526 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, citation_validity first. |
| benchmark | finance | `parent-child` | not_ready | 0.492 | 0.474 | 0.474 | 0.684 | 0.474 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity first. |
| benchmark | finance | `parent-child` | not_ready | 0.492 | 0.474 | 0.474 | 0.684 | 0.474 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity first. |
| benchmark | finance | `bm25` | not_ready | 0.452 | 0.421 | 0.421 | 0.632 | 0.421 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity first. |
| benchmark | finance | `bm25` | not_ready | 0.452 | 0.421 | 0.421 | 0.632 | 0.421 | 0.000 | 0.000 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity first. |
| benchmark | financebench-open-source | `hybrid` | not_ready | 0.430 | 0.400 | 0.400 | 0.456 | 0.400 | 0.000 | 0.179 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid` | not_ready | 0.427 | 0.400 | 0.400 | 0.432 | 0.400 | 0.000 | 0.194 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid` | not_ready | 0.424 | 0.393 | 0.393 | 0.446 | 0.393 | 0.000 | 0.179 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `pageindex-oss` | not_ready | 0.415 | 0.373 | 0.373 | 0.414 | 0.373 | 0.000 | 0.239 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `pageindex-oss` | not_ready | 0.415 | 0.373 | 0.373 | 0.414 | 0.373 | 0.000 | 0.239 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `pageindex-oss` | not_ready | 0.409 | 0.367 | 0.367 | 0.411 | 0.367 | 0.000 | 0.224 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `bm25` | not_ready | 0.408 | 0.387 | 0.387 | 0.419 | 0.387 | 0.000 | 0.134 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `dense-vector` | not_ready | 0.405 | 0.367 | 0.367 | 0.424 | 0.367 | 0.000 | 0.179 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `dense-vector` | not_ready | 0.400 | 0.360 | 0.360 | 0.418 | 0.360 | 0.000 | 0.179 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `dense-vector` | not_ready | 0.400 | 0.360 | 0.360 | 0.418 | 0.360 | 0.000 | 0.179 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid-rerank` | not_ready | 0.399 | 0.373 | 0.373 | 0.403 | 0.373 | 0.000 | 0.149 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid` | not_ready | 0.396 | 0.360 | 0.360 | 0.456 | 0.360 | 0.000 | 0.104 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid-rerank` | not_ready | 0.393 | 0.367 | 0.367 | 0.400 | 0.367 | 0.000 | 0.134 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid-rerank` | not_ready | 0.393 | 0.367 | 0.367 | 0.400 | 0.367 | 0.000 | 0.134 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid` | not_ready | 0.392 | 0.353 | 0.353 | 0.432 | 0.353 | 0.000 | 0.134 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid` | not_ready | 0.391 | 0.353 | 0.353 | 0.446 | 0.353 | 0.000 | 0.104 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid` | not_ready | 0.388 | 0.340 | 0.340 | 0.456 | 0.340 | 0.000 | 0.119 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid` | not_ready | 0.385 | 0.340 | 0.340 | 0.446 | 0.340 | 0.000 | 0.119 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid` | not_ready | 0.381 | 0.333 | 0.333 | 0.432 | 0.333 | 0.000 | 0.134 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `bm25` | not_ready | 0.373 | 0.340 | 0.340 | 0.419 | 0.340 | 0.000 | 0.075 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid-rerank` | not_ready | 0.368 | 0.333 | 0.333 | 0.403 | 0.333 | 0.000 | 0.090 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `bm25` | not_ready | 0.368 | 0.327 | 0.327 | 0.419 | 0.327 | 0.000 | 0.090 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid-rerank` | not_ready | 0.368 | 0.333 | 0.333 | 0.400 | 0.333 | 0.000 | 0.090 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid-rerank` | not_ready | 0.368 | 0.333 | 0.333 | 0.400 | 0.333 | 0.000 | 0.090 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `dense-vector` | not_ready | 0.364 | 0.313 | 0.313 | 0.424 | 0.313 | 0.000 | 0.104 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `dense-vector` | not_ready | 0.363 | 0.307 | 0.307 | 0.424 | 0.307 | 0.000 | 0.119 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `dense-vector` | not_ready | 0.361 | 0.307 | 0.307 | 0.418 | 0.307 | 0.000 | 0.119 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `pageindex-oss` | not_ready | 0.360 | 0.307 | 0.307 | 0.414 | 0.307 | 0.000 | 0.119 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `pageindex-oss` | not_ready | 0.360 | 0.307 | 0.307 | 0.414 | 0.307 | 0.000 | 0.119 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid-rerank` | not_ready | 0.359 | 0.313 | 0.313 | 0.403 | 0.313 | 0.000 | 0.104 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `pageindex-oss` | not_ready | 0.359 | 0.300 | 0.300 | 0.414 | 0.300 | 0.000 | 0.134 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `pageindex-oss` | not_ready | 0.359 | 0.300 | 0.300 | 0.414 | 0.300 | 0.000 | 0.134 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `dense-vector` | not_ready | 0.359 | 0.307 | 0.307 | 0.418 | 0.307 | 0.000 | 0.104 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `dense-vector` | not_ready | 0.359 | 0.307 | 0.307 | 0.418 | 0.307 | 0.000 | 0.104 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `pageindex-oss` | not_ready | 0.358 | 0.300 | 0.300 | 0.411 | 0.300 | 0.000 | 0.134 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `dense-vector` | not_ready | 0.355 | 0.300 | 0.300 | 0.418 | 0.300 | 0.000 | 0.104 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `parent-child` | not_ready | 0.355 | 0.320 | 0.320 | 0.343 | 0.320 | 0.000 | 0.134 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `pageindex-oss` | not_ready | 0.354 | 0.300 | 0.300 | 0.411 | 0.300 | 0.000 | 0.104 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid-rerank` | not_ready | 0.353 | 0.307 | 0.307 | 0.400 | 0.307 | 0.000 | 0.090 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `hybrid-rerank` | not_ready | 0.353 | 0.307 | 0.307 | 0.400 | 0.307 | 0.000 | 0.090 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `parent-child` | not_ready | 0.340 | 0.293 | 0.293 | 0.343 | 0.293 | 0.000 | 0.134 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | financebench-open-source | `parent-child` | not_ready | 0.333 | 0.293 | 0.293 | 0.343 | 0.293 | 0.000 | 0.090 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, financebench_calculation first. |
| benchmark | general-docs | `pageindex-oss` | pilot_candidate | 0.889 | 0.850 | 0.850 | 0.945 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `pageindex-oss` | pilot_candidate | 0.889 | 0.850 | 0.850 | 0.945 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `pageindex-oss` | pilot_candidate | 0.889 | 0.850 | 0.850 | 0.945 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `dense-vector` | pilot_candidate | 0.886 | 0.850 | 0.850 | 0.935 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `dense-vector` | pilot_candidate | 0.886 | 0.850 | 0.850 | 0.935 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `dense-vector` | pilot_candidate | 0.886 | 0.850 | 0.850 | 0.935 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `hybrid` | pilot_candidate | 0.886 | 0.850 | 0.850 | 0.935 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `hybrid` | pilot_candidate | 0.886 | 0.850 | 0.850 | 0.935 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `hybrid-rerank` | pilot_candidate | 0.886 | 0.850 | 0.850 | 0.935 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `hybrid-rerank` | pilot_candidate | 0.886 | 0.850 | 0.850 | 0.935 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `hybrid-rerank` | pilot_candidate | 0.886 | 0.850 | 0.850 | 0.935 | 0.850 | 0.000 | 1.000 | Close to production; review citation_validity before rollout. |
| benchmark | general-docs | `hybrid` | not_ready | 0.848 | 0.800 | 0.800 | 0.910 | 0.800 | 0.000 | 1.000 | Do not use as production default yet; improve citation_validity first. |
| benchmark | general-docs | `pageindex-oss` | not_ready | 0.834 | 0.850 | 0.850 | 0.895 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `pageindex-oss` | not_ready | 0.834 | 0.850 | 0.850 | 0.895 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `pageindex-oss` | not_ready | 0.834 | 0.850 | 0.850 | 0.895 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `pageindex-oss` | not_ready | 0.834 | 0.850 | 0.850 | 0.895 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `pageindex-oss` | not_ready | 0.834 | 0.850 | 0.850 | 0.895 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `pageindex-oss` | not_ready | 0.834 | 0.850 | 0.850 | 0.895 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `dense-vector` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `dense-vector` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `dense-vector` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `dense-vector` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `dense-vector` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `dense-vector` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid-rerank` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid-rerank` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid-rerank` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid-rerank` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid-rerank` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid-rerank` | not_ready | 0.831 | 0.850 | 0.850 | 0.885 | 0.900 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid` | not_ready | 0.792 | 0.800 | 0.800 | 0.860 | 0.850 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `hybrid` | not_ready | 0.792 | 0.800 | 0.800 | 0.860 | 0.850 | 0.500 | 1.000 | Do not use as production default yet; improve no_answer_hallucination first. |
| benchmark | general-docs | `bm25` | not_ready | 0.667 | 0.600 | 0.600 | 0.710 | 0.600 | 0.000 | 1.000 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity first. |
| benchmark | general-docs | `parent-child` | not_ready | 0.623 | 0.550 | 0.550 | 0.660 | 0.550 | 0.000 | 1.000 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity first. |
| benchmark | general-docs | `bm25` | not_ready | 0.613 | 0.600 | 0.600 | 0.660 | 0.650 | 0.500 | 1.000 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, no_answer_hallucination first. |
| benchmark | general-docs | `bm25` | not_ready | 0.613 | 0.600 | 0.600 | 0.660 | 0.650 | 0.500 | 1.000 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, no_answer_hallucination first. |
| benchmark | general-docs | `parent-child` | not_ready | 0.568 | 0.550 | 0.550 | 0.610 | 0.600 | 0.500 | 1.000 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, no_answer_hallucination first. |
| benchmark | general-docs | `parent-child` | not_ready | 0.568 | 0.550 | 0.550 | 0.610 | 0.600 | 0.500 | 1.000 | Do not use as production default yet; improve pass_rate, answer_correctness, evidence_recall, citation_validity, no_answer_hallucination first. |

## Best By Axis

Product-stack ranking uses `exact-match-gold` as the canonical judge. Judge models are audited separately because they are measuring instruments, not deployable RAG components.

| Domain | Axis | Rank | Candidate | Score | Answer | Evidence | Failure | Reading |
|---|---|---:|---|---:|---:|---:|---:|---|
| finance | embedding | 1 | `e5-large-v2-proxy` | 0.724 | 0.741 | 0.987 | 0.259 | best embedding model |
| finance | embedding | 2 | `bge-m3-proxy` | 0.724 | 0.741 | 0.987 | 0.259 | best embedding model |
| finance | embedding | 3 | `finance-e5-proxy` | 0.712 | 0.728 | 0.974 | 0.272 | best embedding model |
| finance | generator | 1 | `reasoning-oss-llm` | 0.761 | 0.838 | 0.936 | 0.162 | best generator model |
| finance | generator | 2 | `balanced-oss-llm` | 0.671 | 0.680 | 0.936 | 0.320 | best generator model |
| finance | generator | 3 | `extractive-strict` | 0.622 | 0.590 | 0.936 | 0.410 | best generator model |
| finance | rag | 1 | `dense-vector` | 0.715 | 0.754 | 1.000 | 0.246 | best RAG system |
| finance | rag | 2 | `pageindex-oss` | 0.692 | 0.754 | 1.000 | 0.246 | best RAG system |
| finance | rag | 3 | `hybrid-rerank` | 0.690 | 0.754 | 1.000 | 0.246 | best RAG system |
| financebench-open-source | embedding | 1 | `bge-m3-proxy` | 0.289 | 0.339 | 0.424 | 0.661 | best embedding model |
| financebench-open-source | embedding | 2 | `e5-large-v2-proxy` | 0.286 | 0.337 | 0.419 | 0.663 | best embedding model |
| financebench-open-source | embedding | 3 | `finance-e5-proxy` | 0.285 | 0.337 | 0.416 | 0.663 | best embedding model |
| financebench-open-source | generator | 1 | `reasoning-oss-llm` | 0.282 | 0.372 | 0.414 | 0.628 | best generator model |
| financebench-open-source | generator | 2 | `extractive-strict` | 0.266 | 0.324 | 0.414 | 0.676 | best generator model |
| financebench-open-source | generator | 3 | `balanced-oss-llm` | 0.251 | 0.312 | 0.414 | 0.688 | best generator model |
| financebench-open-source | rag | 1 | `hybrid` | 0.297 | 0.364 | 0.444 | 0.636 | best RAG system |
| financebench-open-source | rag | 2 | `bm25` | 0.281 | 0.351 | 0.419 | 0.649 | best RAG system |
| financebench-open-source | rag | 3 | `dense-vector` | 0.267 | 0.325 | 0.420 | 0.675 | best RAG system |
| general-docs | embedding | 1 | `bge-m3-proxy` | 0.770 | 0.850 | 0.904 | 0.150 | best embedding model |
| general-docs | embedding | 2 | `finance-e5-proxy` | 0.770 | 0.850 | 0.904 | 0.150 | best embedding model |
| general-docs | embedding | 3 | `e5-large-v2-proxy` | 0.760 | 0.838 | 0.898 | 0.163 | best embedding model |
| general-docs | generator | 1 | `extractive-strict` | 0.746 | 0.807 | 0.900 | 0.193 | best generator model |
| general-docs | generator | 2 | `balanced-oss-llm` | 0.726 | 0.807 | 0.850 | 0.193 | best generator model |
| general-docs | generator | 3 | `reasoning-oss-llm` | 0.720 | 0.807 | 0.850 | 0.193 | best generator model |
| general-docs | rag | 1 | `dense-vector` | 0.755 | 0.850 | 0.902 | 0.150 | best RAG system |
| general-docs | rag | 2 | `hybrid` | 0.742 | 0.833 | 0.893 | 0.167 | best RAG system |
| general-docs | rag | 3 | `hybrid-rerank` | 0.732 | 0.850 | 0.902 | 0.150 | best RAG system |

## Judge Model Audit

| Domain | Rank | Judge | Judge Score | Gold Delta | Agreement Proxy | False Accept Risk | False Reject Risk | Reading |
|---|---:|---|---:|---:|---:|---:|---:|---|
| finance | 1 | `exact-match-gold` | 0.882 | 0.000 | 0.920 | 0.020 | 0.100 | canonical factual label evaluator; use for stack ranking |
| finance | 2 | `llm-judge-balanced-proxy` | 0.663 | -0.053 | 0.860 | 0.080 | 0.060 | lenient LLM judge proxy; useful for paraphrase tolerance checks |
| finance | 3 | `citation-strict-judge-proxy` | 0.629 | -0.053 | 0.830 | 0.030 | 0.140 | strict citation judge proxy; useful for compliance-style risk checks |
| financebench-open-source | 1 | `exact-match-gold` | 0.882 | 0.000 | 0.920 | 0.020 | 0.100 | canonical factual label evaluator; use for stack ranking |
| financebench-open-source | 2 | `llm-judge-balanced-proxy` | 0.673 | -0.020 | 0.860 | 0.080 | 0.060 | lenient LLM judge proxy; useful for paraphrase tolerance checks |
| financebench-open-source | 3 | `citation-strict-judge-proxy` | 0.639 | -0.038 | 0.830 | 0.030 | 0.140 | strict citation judge proxy; useful for compliance-style risk checks |
| general-docs | 1 | `exact-match-gold` | 0.882 | 0.000 | 0.920 | 0.020 | 0.100 | canonical factual label evaluator; use for stack ranking |
| general-docs | 2 | `llm-judge-balanced-proxy` | 0.673 | 0.000 | 0.860 | 0.080 | 0.060 | lenient LLM judge proxy; useful for paraphrase tolerance checks |
| general-docs | 3 | `citation-strict-judge-proxy` | 0.639 | -0.076 | 0.830 | 0.030 | 0.140 | strict citation judge proxy; useful for compliance-style risk checks |

## Failure Breakdown

| Domain | RAG | Embedding | Generator | Failure Type | Count |
|---|---|---|---|---|---:|
| finance | `bm25` | none | balanced-oss-llm | context_bloat | 4 |
| finance | `bm25` | none | balanced-oss-llm | retrieval_miss | 7 |
| finance | `bm25` | none | extractive-strict | context_bloat | 3 |
| finance | `bm25` | none | extractive-strict | generation_hallucination | 1 |
| finance | `bm25` | none | extractive-strict | retrieval_miss | 7 |
| finance | `bm25` | none | reasoning-oss-llm | context_bloat | 1 |
| finance | `bm25` | none | reasoning-oss-llm | retrieval_miss | 7 |
| finance | `dense-vector` | bge-m3-proxy | balanced-oss-llm | context_bloat | 4 |
| finance | `dense-vector` | bge-m3-proxy | balanced-oss-llm | generation_hallucination | 1 |
| finance | `dense-vector` | bge-m3-proxy | extractive-strict | context_bloat | 5 |
| finance | `dense-vector` | bge-m3-proxy | extractive-strict | generation_hallucination | 2 |
| finance | `dense-vector` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `dense-vector` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 4 |
| finance | `dense-vector` | e5-large-v2-proxy | balanced-oss-llm | generation_hallucination | 1 |
| finance | `dense-vector` | e5-large-v2-proxy | extractive-strict | context_bloat | 5 |
| finance | `dense-vector` | e5-large-v2-proxy | extractive-strict | generation_hallucination | 2 |
| finance | `dense-vector` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `dense-vector` | finance-e5-proxy | balanced-oss-llm | context_bloat | 4 |
| finance | `dense-vector` | finance-e5-proxy | balanced-oss-llm | generation_hallucination | 1 |
| finance | `dense-vector` | finance-e5-proxy | extractive-strict | context_bloat | 5 |
| finance | `dense-vector` | finance-e5-proxy | extractive-strict | generation_hallucination | 2 |
| finance | `dense-vector` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `hybrid` | bge-m3-proxy | balanced-oss-llm | context_bloat | 4 |
| finance | `hybrid` | bge-m3-proxy | balanced-oss-llm | generation_hallucination | 1 |
| finance | `hybrid` | bge-m3-proxy | balanced-oss-llm | retrieval_miss | 1 |
| finance | `hybrid` | bge-m3-proxy | extractive-strict | context_bloat | 5 |
| finance | `hybrid` | bge-m3-proxy | extractive-strict | generation_hallucination | 2 |
| finance | `hybrid` | bge-m3-proxy | extractive-strict | retrieval_miss | 1 |
| finance | `hybrid` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `hybrid` | bge-m3-proxy | reasoning-oss-llm | retrieval_miss | 1 |
| finance | `hybrid` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 4 |
| finance | `hybrid` | e5-large-v2-proxy | balanced-oss-llm | generation_hallucination | 1 |
| finance | `hybrid` | e5-large-v2-proxy | balanced-oss-llm | retrieval_miss | 1 |
| finance | `hybrid` | e5-large-v2-proxy | extractive-strict | context_bloat | 5 |
| finance | `hybrid` | e5-large-v2-proxy | extractive-strict | generation_hallucination | 2 |
| finance | `hybrid` | e5-large-v2-proxy | extractive-strict | retrieval_miss | 1 |
| finance | `hybrid` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `hybrid` | e5-large-v2-proxy | reasoning-oss-llm | retrieval_miss | 1 |
| finance | `hybrid` | finance-e5-proxy | balanced-oss-llm | context_bloat | 4 |
| finance | `hybrid` | finance-e5-proxy | balanced-oss-llm | generation_hallucination | 1 |
| finance | `hybrid` | finance-e5-proxy | balanced-oss-llm | retrieval_miss | 2 |
| finance | `hybrid` | finance-e5-proxy | extractive-strict | context_bloat | 5 |
| finance | `hybrid` | finance-e5-proxy | extractive-strict | generation_hallucination | 2 |
| finance | `hybrid` | finance-e5-proxy | extractive-strict | retrieval_miss | 2 |
| finance | `hybrid` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `hybrid` | finance-e5-proxy | reasoning-oss-llm | retrieval_miss | 2 |
| finance | `hybrid-rerank` | bge-m3-proxy | balanced-oss-llm | context_bloat | 4 |
| finance | `hybrid-rerank` | bge-m3-proxy | balanced-oss-llm | generation_hallucination | 1 |
| finance | `hybrid-rerank` | bge-m3-proxy | extractive-strict | context_bloat | 5 |
| finance | `hybrid-rerank` | bge-m3-proxy | extractive-strict | generation_hallucination | 2 |
| finance | `hybrid-rerank` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `hybrid-rerank` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 4 |
| finance | `hybrid-rerank` | e5-large-v2-proxy | balanced-oss-llm | generation_hallucination | 1 |
| finance | `hybrid-rerank` | e5-large-v2-proxy | extractive-strict | context_bloat | 5 |
| finance | `hybrid-rerank` | e5-large-v2-proxy | extractive-strict | generation_hallucination | 2 |
| finance | `hybrid-rerank` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `hybrid-rerank` | finance-e5-proxy | balanced-oss-llm | context_bloat | 4 |
| finance | `hybrid-rerank` | finance-e5-proxy | balanced-oss-llm | generation_hallucination | 1 |
| finance | `hybrid-rerank` | finance-e5-proxy | extractive-strict | context_bloat | 5 |
| finance | `hybrid-rerank` | finance-e5-proxy | extractive-strict | generation_hallucination | 2 |
| finance | `hybrid-rerank` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `pageindex-oss` | bge-m3-proxy | balanced-oss-llm | context_bloat | 5 |
| finance | `pageindex-oss` | bge-m3-proxy | extractive-strict | context_bloat | 7 |
| finance | `pageindex-oss` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `pageindex-oss` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 5 |
| finance | `pageindex-oss` | e5-large-v2-proxy | extractive-strict | context_bloat | 7 |
| finance | `pageindex-oss` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `pageindex-oss` | finance-e5-proxy | balanced-oss-llm | context_bloat | 5 |
| finance | `pageindex-oss` | finance-e5-proxy | extractive-strict | context_bloat | 7 |
| finance | `pageindex-oss` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 2 |
| finance | `parent-child` | none | balanced-oss-llm | context_bloat | 4 |
| finance | `parent-child` | none | balanced-oss-llm | retrieval_miss | 6 |
| finance | `parent-child` | none | extractive-strict | context_bloat | 3 |
| finance | `parent-child` | none | extractive-strict | generation_hallucination | 1 |
| finance | `parent-child` | none | extractive-strict | retrieval_miss | 6 |
| finance | `parent-child` | none | reasoning-oss-llm | context_bloat | 1 |
| finance | `parent-child` | none | reasoning-oss-llm | retrieval_miss | 6 |
| financebench-open-source | `bm25` | none | balanced-oss-llm | context_bloat | 18 |
| financebench-open-source | `bm25` | none | balanced-oss-llm | retrieval_miss | 83 |
| financebench-open-source | `bm25` | none | extractive-strict | context_bloat | 16 |
| financebench-open-source | `bm25` | none | extractive-strict | retrieval_miss | 83 |
| financebench-open-source | `bm25` | none | reasoning-oss-llm | context_bloat | 9 |
| financebench-open-source | `bm25` | none | reasoning-oss-llm | retrieval_miss | 83 |
| financebench-open-source | `dense-vector` | bge-m3-proxy | balanced-oss-llm | context_bloat | 24 |
| financebench-open-source | `dense-vector` | bge-m3-proxy | balanced-oss-llm | generation_hallucination | 1 |
| financebench-open-source | `dense-vector` | bge-m3-proxy | balanced-oss-llm | retrieval_miss | 79 |
| financebench-open-source | `dense-vector` | bge-m3-proxy | extractive-strict | context_bloat | 21 |
| financebench-open-source | `dense-vector` | bge-m3-proxy | extractive-strict | generation_hallucination | 3 |
| financebench-open-source | `dense-vector` | bge-m3-proxy | extractive-strict | retrieval_miss | 79 |
| financebench-open-source | `dense-vector` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 15 |
| financebench-open-source | `dense-vector` | bge-m3-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| financebench-open-source | `dense-vector` | bge-m3-proxy | reasoning-oss-llm | retrieval_miss | 79 |
| financebench-open-source | `dense-vector` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 23 |
| financebench-open-source | `dense-vector` | e5-large-v2-proxy | balanced-oss-llm | generation_hallucination | 1 |
| financebench-open-source | `dense-vector` | e5-large-v2-proxy | balanced-oss-llm | retrieval_miss | 80 |
| financebench-open-source | `dense-vector` | e5-large-v2-proxy | extractive-strict | context_bloat | 21 |
| financebench-open-source | `dense-vector` | e5-large-v2-proxy | extractive-strict | generation_hallucination | 3 |
| financebench-open-source | `dense-vector` | e5-large-v2-proxy | extractive-strict | retrieval_miss | 80 |
| financebench-open-source | `dense-vector` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 15 |
| financebench-open-source | `dense-vector` | e5-large-v2-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| financebench-open-source | `dense-vector` | e5-large-v2-proxy | reasoning-oss-llm | retrieval_miss | 80 |
| financebench-open-source | `dense-vector` | finance-e5-proxy | balanced-oss-llm | context_bloat | 24 |
| financebench-open-source | `dense-vector` | finance-e5-proxy | balanced-oss-llm | generation_hallucination | 1 |
| financebench-open-source | `dense-vector` | finance-e5-proxy | balanced-oss-llm | retrieval_miss | 80 |
| financebench-open-source | `dense-vector` | finance-e5-proxy | extractive-strict | context_bloat | 22 |
| financebench-open-source | `dense-vector` | finance-e5-proxy | extractive-strict | generation_hallucination | 2 |
| financebench-open-source | `dense-vector` | finance-e5-proxy | extractive-strict | retrieval_miss | 80 |
| financebench-open-source | `dense-vector` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 15 |
| financebench-open-source | `dense-vector` | finance-e5-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| financebench-open-source | `dense-vector` | finance-e5-proxy | reasoning-oss-llm | retrieval_miss | 80 |
| financebench-open-source | `hybrid` | bge-m3-proxy | balanced-oss-llm | context_bloat | 23 |
| financebench-open-source | `hybrid` | bge-m3-proxy | balanced-oss-llm | retrieval_miss | 76 |
| financebench-open-source | `hybrid` | bge-m3-proxy | extractive-strict | context_bloat | 19 |
| financebench-open-source | `hybrid` | bge-m3-proxy | extractive-strict | generation_hallucination | 1 |
| financebench-open-source | `hybrid` | bge-m3-proxy | extractive-strict | retrieval_miss | 76 |
| financebench-open-source | `hybrid` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 14 |
| financebench-open-source | `hybrid` | bge-m3-proxy | reasoning-oss-llm | retrieval_miss | 76 |
| financebench-open-source | `hybrid` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 21 |
| financebench-open-source | `hybrid` | e5-large-v2-proxy | balanced-oss-llm | retrieval_miss | 78 |
| financebench-open-source | `hybrid` | e5-large-v2-proxy | extractive-strict | context_bloat | 18 |
| financebench-open-source | `hybrid` | e5-large-v2-proxy | extractive-strict | generation_hallucination | 1 |
| financebench-open-source | `hybrid` | e5-large-v2-proxy | extractive-strict | retrieval_miss | 78 |
| financebench-open-source | `hybrid` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 13 |
| financebench-open-source | `hybrid` | e5-large-v2-proxy | reasoning-oss-llm | retrieval_miss | 78 |
| financebench-open-source | `hybrid` | finance-e5-proxy | balanced-oss-llm | context_bloat | 19 |
| financebench-open-source | `hybrid` | finance-e5-proxy | balanced-oss-llm | retrieval_miss | 81 |
| financebench-open-source | `hybrid` | finance-e5-proxy | extractive-strict | context_bloat | 15 |
| financebench-open-source | `hybrid` | finance-e5-proxy | extractive-strict | generation_hallucination | 1 |
| financebench-open-source | `hybrid` | finance-e5-proxy | extractive-strict | retrieval_miss | 81 |
| financebench-open-source | `hybrid` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 9 |
| financebench-open-source | `hybrid` | finance-e5-proxy | reasoning-oss-llm | retrieval_miss | 81 |
| financebench-open-source | `hybrid-rerank` | bge-m3-proxy | balanced-oss-llm | context_bloat | 18 |
| financebench-open-source | `hybrid-rerank` | bge-m3-proxy | balanced-oss-llm | retrieval_miss | 86 |
| financebench-open-source | `hybrid-rerank` | bge-m3-proxy | extractive-strict | context_bloat | 14 |
| financebench-open-source | `hybrid-rerank` | bge-m3-proxy | extractive-strict | retrieval_miss | 86 |
| financebench-open-source | `hybrid-rerank` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 9 |
| financebench-open-source | `hybrid-rerank` | bge-m3-proxy | reasoning-oss-llm | retrieval_miss | 86 |
| financebench-open-source | `hybrid-rerank` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 18 |
| financebench-open-source | `hybrid-rerank` | e5-large-v2-proxy | balanced-oss-llm | retrieval_miss | 86 |
| financebench-open-source | `hybrid-rerank` | e5-large-v2-proxy | extractive-strict | context_bloat | 14 |
| financebench-open-source | `hybrid-rerank` | e5-large-v2-proxy | extractive-strict | retrieval_miss | 86 |
| financebench-open-source | `hybrid-rerank` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 9 |
| financebench-open-source | `hybrid-rerank` | e5-large-v2-proxy | reasoning-oss-llm | retrieval_miss | 86 |
| financebench-open-source | `hybrid-rerank` | finance-e5-proxy | balanced-oss-llm | context_bloat | 17 |
| financebench-open-source | `hybrid-rerank` | finance-e5-proxy | balanced-oss-llm | retrieval_miss | 86 |
| financebench-open-source | `hybrid-rerank` | finance-e5-proxy | extractive-strict | context_bloat | 13 |
| financebench-open-source | `hybrid-rerank` | finance-e5-proxy | extractive-strict | generation_hallucination | 1 |
| financebench-open-source | `hybrid-rerank` | finance-e5-proxy | extractive-strict | retrieval_miss | 86 |
| financebench-open-source | `hybrid-rerank` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 8 |
| financebench-open-source | `hybrid-rerank` | finance-e5-proxy | reasoning-oss-llm | retrieval_miss | 86 |
| financebench-open-source | `pageindex-oss` | bge-m3-proxy | balanced-oss-llm | context_bloat | 17 |
| financebench-open-source | `pageindex-oss` | bge-m3-proxy | balanced-oss-llm | generation_hallucination | 4 |
| financebench-open-source | `pageindex-oss` | bge-m3-proxy | balanced-oss-llm | retrieval_miss | 84 |
| financebench-open-source | `pageindex-oss` | bge-m3-proxy | extractive-strict | context_bloat | 15 |
| financebench-open-source | `pageindex-oss` | bge-m3-proxy | extractive-strict | generation_hallucination | 5 |
| financebench-open-source | `pageindex-oss` | bge-m3-proxy | extractive-strict | retrieval_miss | 84 |
| financebench-open-source | `pageindex-oss` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 9 |
| financebench-open-source | `pageindex-oss` | bge-m3-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| financebench-open-source | `pageindex-oss` | bge-m3-proxy | reasoning-oss-llm | retrieval_miss | 84 |
| financebench-open-source | `pageindex-oss` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 17 |
| financebench-open-source | `pageindex-oss` | e5-large-v2-proxy | balanced-oss-llm | generation_hallucination | 4 |
| financebench-open-source | `pageindex-oss` | e5-large-v2-proxy | balanced-oss-llm | retrieval_miss | 84 |
| financebench-open-source | `pageindex-oss` | e5-large-v2-proxy | extractive-strict | context_bloat | 15 |
| financebench-open-source | `pageindex-oss` | e5-large-v2-proxy | extractive-strict | generation_hallucination | 5 |
| financebench-open-source | `pageindex-oss` | e5-large-v2-proxy | extractive-strict | retrieval_miss | 84 |
| financebench-open-source | `pageindex-oss` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 9 |
| financebench-open-source | `pageindex-oss` | e5-large-v2-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| financebench-open-source | `pageindex-oss` | e5-large-v2-proxy | reasoning-oss-llm | retrieval_miss | 84 |
| financebench-open-source | `pageindex-oss` | finance-e5-proxy | balanced-oss-llm | context_bloat | 18 |
| financebench-open-source | `pageindex-oss` | finance-e5-proxy | balanced-oss-llm | generation_hallucination | 3 |
| financebench-open-source | `pageindex-oss` | finance-e5-proxy | balanced-oss-llm | retrieval_miss | 84 |
| financebench-open-source | `pageindex-oss` | finance-e5-proxy | extractive-strict | context_bloat | 16 |
| financebench-open-source | `pageindex-oss` | finance-e5-proxy | extractive-strict | generation_hallucination | 5 |
| financebench-open-source | `pageindex-oss` | finance-e5-proxy | extractive-strict | retrieval_miss | 84 |
| financebench-open-source | `pageindex-oss` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 10 |
| financebench-open-source | `pageindex-oss` | finance-e5-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| financebench-open-source | `pageindex-oss` | finance-e5-proxy | reasoning-oss-llm | retrieval_miss | 84 |
| financebench-open-source | `parent-child` | none | balanced-oss-llm | context_bloat | 11 |
| financebench-open-source | `parent-child` | none | balanced-oss-llm | retrieval_miss | 95 |
| financebench-open-source | `parent-child` | none | extractive-strict | context_bloat | 10 |
| financebench-open-source | `parent-child` | none | extractive-strict | generation_hallucination | 1 |
| financebench-open-source | `parent-child` | none | extractive-strict | retrieval_miss | 95 |
| financebench-open-source | `parent-child` | none | reasoning-oss-llm | context_bloat | 7 |
| financebench-open-source | `parent-child` | none | reasoning-oss-llm | retrieval_miss | 95 |
| general-docs | `bm25` | none | balanced-oss-llm | context_bloat | 3 |
| general-docs | `bm25` | none | balanced-oss-llm | generation_hallucination | 1 |
| general-docs | `bm25` | none | balanced-oss-llm | retrieval_miss | 4 |
| general-docs | `bm25` | none | extractive-strict | context_bloat | 4 |
| general-docs | `bm25` | none | extractive-strict | retrieval_miss | 4 |
| general-docs | `bm25` | none | reasoning-oss-llm | context_bloat | 3 |
| general-docs | `bm25` | none | reasoning-oss-llm | generation_hallucination | 1 |
| general-docs | `bm25` | none | reasoning-oss-llm | retrieval_miss | 4 |
| general-docs | `dense-vector` | bge-m3-proxy | balanced-oss-llm | context_bloat | 2 |
| general-docs | `dense-vector` | bge-m3-proxy | balanced-oss-llm | generation_hallucination | 1 |
| general-docs | `dense-vector` | bge-m3-proxy | extractive-strict | context_bloat | 3 |
| general-docs | `dense-vector` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 2 |
| general-docs | `dense-vector` | bge-m3-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| general-docs | `dense-vector` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 2 |
| general-docs | `dense-vector` | e5-large-v2-proxy | balanced-oss-llm | generation_hallucination | 1 |
| general-docs | `dense-vector` | e5-large-v2-proxy | extractive-strict | context_bloat | 3 |
| general-docs | `dense-vector` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 2 |
| general-docs | `dense-vector` | e5-large-v2-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| general-docs | `dense-vector` | finance-e5-proxy | balanced-oss-llm | context_bloat | 2 |
| general-docs | `dense-vector` | finance-e5-proxy | balanced-oss-llm | generation_hallucination | 1 |
| general-docs | `dense-vector` | finance-e5-proxy | extractive-strict | context_bloat | 3 |
| general-docs | `dense-vector` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 2 |
| general-docs | `dense-vector` | finance-e5-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid` | bge-m3-proxy | balanced-oss-llm | context_bloat | 2 |
| general-docs | `hybrid` | bge-m3-proxy | balanced-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid` | bge-m3-proxy | extractive-strict | context_bloat | 3 |
| general-docs | `hybrid` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 2 |
| general-docs | `hybrid` | bge-m3-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 3 |
| general-docs | `hybrid` | e5-large-v2-proxy | balanced-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid` | e5-large-v2-proxy | extractive-strict | context_bloat | 4 |
| general-docs | `hybrid` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 3 |
| general-docs | `hybrid` | e5-large-v2-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid` | finance-e5-proxy | balanced-oss-llm | context_bloat | 2 |
| general-docs | `hybrid` | finance-e5-proxy | balanced-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid` | finance-e5-proxy | extractive-strict | context_bloat | 3 |
| general-docs | `hybrid` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 2 |
| general-docs | `hybrid` | finance-e5-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid-rerank` | bge-m3-proxy | balanced-oss-llm | context_bloat | 2 |
| general-docs | `hybrid-rerank` | bge-m3-proxy | balanced-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid-rerank` | bge-m3-proxy | extractive-strict | context_bloat | 3 |
| general-docs | `hybrid-rerank` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 2 |
| general-docs | `hybrid-rerank` | bge-m3-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid-rerank` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 2 |
| general-docs | `hybrid-rerank` | e5-large-v2-proxy | balanced-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid-rerank` | e5-large-v2-proxy | extractive-strict | context_bloat | 3 |
| general-docs | `hybrid-rerank` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 2 |
| general-docs | `hybrid-rerank` | e5-large-v2-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid-rerank` | finance-e5-proxy | balanced-oss-llm | context_bloat | 2 |
| general-docs | `hybrid-rerank` | finance-e5-proxy | balanced-oss-llm | generation_hallucination | 1 |
| general-docs | `hybrid-rerank` | finance-e5-proxy | extractive-strict | context_bloat | 3 |
| general-docs | `hybrid-rerank` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 2 |
| general-docs | `hybrid-rerank` | finance-e5-proxy | reasoning-oss-llm | generation_hallucination | 1 |
| general-docs | `pageindex-oss` | bge-m3-proxy | balanced-oss-llm | context_bloat | 1 |
| general-docs | `pageindex-oss` | bge-m3-proxy | balanced-oss-llm | generation_hallucination | 2 |
| general-docs | `pageindex-oss` | bge-m3-proxy | extractive-strict | context_bloat | 2 |
| general-docs | `pageindex-oss` | bge-m3-proxy | extractive-strict | generation_hallucination | 1 |
| general-docs | `pageindex-oss` | bge-m3-proxy | reasoning-oss-llm | context_bloat | 1 |
| general-docs | `pageindex-oss` | bge-m3-proxy | reasoning-oss-llm | generation_hallucination | 2 |
| general-docs | `pageindex-oss` | e5-large-v2-proxy | balanced-oss-llm | context_bloat | 1 |
| general-docs | `pageindex-oss` | e5-large-v2-proxy | balanced-oss-llm | generation_hallucination | 2 |
| general-docs | `pageindex-oss` | e5-large-v2-proxy | extractive-strict | context_bloat | 2 |
| general-docs | `pageindex-oss` | e5-large-v2-proxy | extractive-strict | generation_hallucination | 1 |
| general-docs | `pageindex-oss` | e5-large-v2-proxy | reasoning-oss-llm | context_bloat | 1 |
| general-docs | `pageindex-oss` | e5-large-v2-proxy | reasoning-oss-llm | generation_hallucination | 2 |
| general-docs | `pageindex-oss` | finance-e5-proxy | balanced-oss-llm | context_bloat | 1 |
| general-docs | `pageindex-oss` | finance-e5-proxy | balanced-oss-llm | generation_hallucination | 2 |
| general-docs | `pageindex-oss` | finance-e5-proxy | extractive-strict | context_bloat | 2 |
| general-docs | `pageindex-oss` | finance-e5-proxy | extractive-strict | generation_hallucination | 1 |
| general-docs | `pageindex-oss` | finance-e5-proxy | reasoning-oss-llm | context_bloat | 1 |
| general-docs | `pageindex-oss` | finance-e5-proxy | reasoning-oss-llm | generation_hallucination | 2 |
| general-docs | `parent-child` | none | balanced-oss-llm | context_bloat | 2 |
| general-docs | `parent-child` | none | balanced-oss-llm | generation_hallucination | 2 |
| general-docs | `parent-child` | none | balanced-oss-llm | retrieval_miss | 5 |
| general-docs | `parent-child` | none | extractive-strict | context_bloat | 3 |
| general-docs | `parent-child` | none | extractive-strict | generation_hallucination | 1 |
| general-docs | `parent-child` | none | extractive-strict | retrieval_miss | 5 |
| general-docs | `parent-child` | none | reasoning-oss-llm | context_bloat | 2 |
| general-docs | `parent-child` | none | reasoning-oss-llm | generation_hallucination | 2 |
| general-docs | `parent-child` | none | reasoning-oss-llm | retrieval_miss | 5 |

## Category View

| Domain | Category | Best System | Best Answer | Hardest System Failure |
|---|---|---:|---:|---:|
| finance | calculation | `bm25` | 0.667 | `bm25` 1.000 |
| finance | direct_lookup | `dense-vector` | 1.000 | `bm25` 0.500 |
| finance | multi_section | `bm25` | 1.000 | `bm25` 0.000 |
| finance | no_answer | `bm25` | 1.000 | `bm25` 0.000 |
| finance | section_navigation | `dense-vector` | 1.000 | `bm25` 0.667 |
| finance | table_numeric | `dense-vector` | 1.000 | `bm25` 1.000 |
| financebench-open-source | calculation | `pageindex-oss` | 0.239 | `bm25` 0.925 |
| financebench-open-source | direct_lookup | `hybrid` | 0.737 | `pageindex-oss` 0.579 |
| financebench-open-source | section_navigation | `bm25` | 0.640 | `parent-child` 0.520 |
| financebench-open-source | table_numeric | `hybrid` | 0.286 | `bm25` 0.929 |
| general-docs | direct_lookup | `bm25` | 1.000 | `bm25` 0.000 |
| general-docs | global_summary | `pageindex-oss` | 0.000 | `bm25` 1.000 |
| general-docs | multi_document | `bm25` | 0.500 | `bm25` 0.500 |
| general-docs | multi_section | `dense-vector` | 1.000 | `bm25` 0.500 |
| general-docs | no_answer | `bm25` | 1.000 | `bm25` 0.500 |
| general-docs | section_navigation | `dense-vector` | 1.000 | `parent-child` 0.556 |
| general-docs | table_numeric | `bm25` | 1.000 | `bm25` 0.500 |

## Operational Guidance

### finance

- Recommended default: `dense-vector` (score=0.791; semantic similarity baseline).
- Best quality: `dense-vector` (answer=0.895, evidence=1.000).
- Lowest query cost: `parent-child` (cost=0.000015).
- Fastest query path: `bm25` (latency=0.02 ms).

### financebench-open-source

- Recommended default: `bm25` (score=0.376; fast exact-term baseline).
- Best quality: `hybrid` (answer=0.400, evidence=0.456).
- Lowest query cost: `dense-vector` (cost=0.000416).
- Fastest query path: `bm25` (latency=1.45 ms).

### general-docs

- Recommended default: `dense-vector` (score=0.780; semantic similarity baseline).
- Best quality: `pageindex-oss` (answer=0.850, evidence=0.945).
- Lowest query cost: `parent-child` (cost=0.000013).
- Fastest query path: `bm25` (latency=0.02 ms).


## Interpretation Warnings

- general-docs: at least one question needs 5 evidence items, but top_k=4.

## Notes

- `pageindex-oss` uses a local PageIndex-style tree adapter only; hosted PageIndex APIs are excluded.
- Embedding and generator comparisons use deterministic local profiles by default; plug in real model adapters before claiming model-leaderboard results.
- Judge comparisons are judge reliability audits. Do not rank product stacks with a judge until it is validated against human labels for the target domain.
- `retrieval-only` isolates evidence retrieval, `generator-oracle` isolates answer generation with gold context, and `end-to-end` combines the full stack.
- Add real corpora and human-graded questions before treating numbers as production proof.
