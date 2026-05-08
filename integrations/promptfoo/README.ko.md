# Promptfoo 통합

이 디렉터리는 promptfoo가 로컬 `rag-benchmark` harness를 custom Python provider로 호출하게 해줍니다.

기본 설정은 결정론적 assertion만 사용하므로 외부 grader를 호출하지 않습니다.
생성된 provider config는 `.venv/bin/python`이 있으면 promptfoo가 그 Python을 사용하도록 지정합니다.

## 실행

```bash
cd integrations/promptfoo
npx promptfoo@latest eval -c promptfooconfig.yaml --output promptfoo-results.html --output promptfoo-results.json --no-share
```

HTML 결과:

```text
integrations/promptfoo/promptfoo-results.html
```

## 재생성

```bash
uv run rag-benchmark export-promptfoo
```

자주 쓰는 옵션:

```bash
uv run rag-benchmark export-promptfoo --domain finance --domain general-docs
uv run rag-benchmark export-promptfoo --system hybrid --system pageindex-oss --embedding bge-m3-proxy
uv run rag-benchmark export-promptfoo --include-model-graded --grader-provider ollama:chat:llama3.1
```

## 해석

- 여기서 promptfoo는 CI 품질 게이트와 외부 평가 화면으로 사용합니다.
- 운영 판단의 canonical dashboard는 `results/dashboard.html`입니다.
- OSS-only 실행이 필요하면 model-graded assertion을 켤 때 반드시 로컬/OSS grader를 지정하세요.
