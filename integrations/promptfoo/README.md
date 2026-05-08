# Promptfoo Integration

This directory lets promptfoo call the local `rag-benchmark` harness as a custom Python provider.

The default config uses deterministic assertions only, so it does not call an external grader.
The generated provider config points promptfoo at `.venv/bin/python` when that interpreter exists.

## Run

```bash
cd integrations/promptfoo
npx promptfoo@latest eval -c promptfooconfig.yaml --output promptfoo-results.html --output promptfoo-results.json --no-share
```

Open the HTML output:

```text
integrations/promptfoo/promptfoo-results.html
```

## Regenerate

```bash
uv run rag-benchmark export-promptfoo
```

Useful options:

```bash
uv run rag-benchmark export-promptfoo --domain finance --domain general-docs
uv run rag-benchmark export-promptfoo --system hybrid --system pageindex-oss --embedding bge-m3-proxy
uv run rag-benchmark export-promptfoo --include-model-graded --grader-provider ollama:chat:llama3.1
```

## Interpretation

- Use promptfoo here as a CI quality gate and external eval view.
- Keep `results/dashboard.html` as the canonical operations benchmark dashboard.
- Use model-graded assertions only after choosing an OSS/local grader if the run must stay OSS-only.
