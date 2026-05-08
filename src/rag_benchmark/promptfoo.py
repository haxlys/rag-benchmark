from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml

from .answer import generate_answer
from .datasets import (
    enabled_domains,
    enabled_mvp_embeddings,
    enabled_mvp_generators,
    enabled_mvp_judges,
    enabled_mvp_systems,
    enabled_tracks,
    load_domain,
)
from .evaluation import evaluate
from .judges import judge_answer
from .retrievers import build_retriever
from .retrievers.factory import uses_embedding
from .runner import load_config, oracle_retrieval
from .schemas import Question


DEFAULT_PROMPTFOO_SYSTEMS = ["bm25", "hybrid", "pageindex-oss"]
DEFAULT_PROMPTFOO_EMBEDDING = "bge-m3-proxy"
DEFAULT_PROMPTFOO_GENERATOR = "reasoning-oss-llm"
DEFAULT_PROMPTFOO_JUDGE = "exact-match-gold"
DEFAULT_PROMPTFOO_TRACK = "end-to-end"


@dataclass(frozen=True)
class PromptfooProviderVariant:
    track: str
    system_id: str
    embedding_model: str
    generator_model: str
    judge_model: str

    @property
    def label(self) -> str:
        parts = [
            self.track,
            self.system_id,
            self.embedding_model,
            self.generator_model,
            self.judge_model,
        ]
        return ":".join(part for part in parts if part and part != "none")


@dataclass(frozen=True)
class PromptfooExportSummary:
    output_dir: Path
    config_path: Path
    tests_path: Path
    provider_path: Path
    readme_path: Path
    readme_ko_path: Path
    providers: int
    tests: int
    model_graded: bool
    warnings: tuple[str, ...] = ()


def call_promptfoo_provider(prompt: str, options: dict, context: dict) -> dict:
    """Promptfoo Python provider entry point.

    The checked-in provider script delegates here after adding the repo's
    `src/` directory to `sys.path`.
    """
    config = options.get("config", {})
    root = resolve_provider_path(config.get("repoRoot", "../.."), config)
    config_path = resolve_provider_path(config.get("configPath", "configs/benchmark.yaml"), config, root)
    vars_ = context.get("vars", {}) if context else {}
    payload = run_promptfoo_case(
        root=root,
        config_path=config_path,
        prompt=prompt,
        vars_=vars_,
        provider_config=config,
    )
    output = json.dumps(payload, ensure_ascii=False)
    metrics = payload["metrics"]
    token_usage = {
        "total": int(metrics["generator_input_tokens"])
        + int(metrics["generator_output_tokens"])
        + int(metrics["judge_input_tokens"]),
        "prompt": int(metrics["generator_input_tokens"]) + int(metrics["judge_input_tokens"]),
        "completion": int(metrics["generator_output_tokens"]),
        "numRequests": 1,
    }
    latency_ms = (
        float(metrics["query_wall_time_ms"])
        + float(metrics["generator_wall_time_ms"])
        + float(metrics["judge_wall_time_ms"])
    )
    return {
        "output": output,
        "metadata": {
            "metrics": metrics,
            "retrieved_docs": [{"content": item["text"]} for item in payload["sources"]],
            "settings": payload["settings"],
        },
        "tokenUsage": token_usage,
        "cost": float(metrics["estimated_cost"]),
        "latencyMs": int(round(latency_ms)),
    }


def run_promptfoo_case(
    *,
    root: Path,
    config_path: Path,
    prompt: str,
    vars_: dict[str, Any],
    provider_config: dict[str, Any],
) -> dict[str, Any]:
    domain = str(vars_.get("domain") or provider_config.get("domain") or "general-docs")
    question = resolve_question(root, domain, vars_, prompt)
    documents, questions = load_domain(root, domain)
    question_by_id = {item.question_id: item for item in questions}
    question = question_by_id.get(question.question_id, question)

    track = str(provider_config.get("track", DEFAULT_PROMPTFOO_TRACK))
    system_id = str(provider_config.get("system", provider_config.get("system_id", "hybrid")))
    embedding_model = str(provider_config.get("embedding", provider_config.get("embedding_model", "none")))
    generator_model = str(provider_config.get("generator", provider_config.get("generator_model", DEFAULT_PROMPTFOO_GENERATOR)))
    judge_model = str(provider_config.get("judge", provider_config.get("judge_model", DEFAULT_PROMPTFOO_JUDGE)))
    top_k = int(provider_config.get("topK", provider_config.get("top_k", 4)))

    run_id = "promptfoo"
    if track == "generator-oracle":
        retrieval = oracle_retrieval(question, documents, top_k=top_k, run_id=run_id)
        system_id = "oracle-context"
        embedding_model = "gold-context"
    else:
        if track == "retrieval-only":
            generator_model = "retrieval-probe"
        retriever = build_retriever(
            system_id,
            documents,
            top_k=top_k,
            embedding_model=embedding_model,
        )
        retrieval = retriever.retrieve(question, top_k=top_k)

    answer = generate_answer(question, retrieval, generator_model)
    judgement = judge_answer(question, retrieval, answer, judge_model)
    result = evaluate(
        run_id=run_id,
        track=track,
        domain=domain,
        system_id=system_id,
        question=question,
        retrieval=retrieval,
        answer=answer,
        judgement=judgement,
    )
    sources = [
        {
            "chunk_id": context.chunk.chunk_id,
            "doc_id": context.chunk.doc_id,
            "title": context.chunk.title,
            "page_start": context.chunk.page_start,
            "page_end": context.chunk.page_end,
            "section_id": context.chunk.section_id,
            "score": context.score,
            "rank": context.rank,
            "text": context.chunk.text,
        }
        for context in retrieval.contexts
    ]
    return {
        "answer": answer.answer,
        "context": "\n\n".join(item["text"] for item in sources),
        "sources": sources,
        "metrics": result.model_dump(),
        "settings": {
            "track": track,
            "domain": domain,
            "system": system_id,
            "embedding": embedding_model,
            "generator": generator_model,
            "judge": judge_model,
            "top_k": top_k,
        },
    }


def export_promptfoo_bundle(
    *,
    root: Path,
    config_path: Path,
    output_dir: Path,
    domains: Iterable[str] | None = None,
    systems: Iterable[str] | None = None,
    embeddings: Iterable[str] | None = None,
    generators: Iterable[str] | None = None,
    judges: Iterable[str] | None = None,
    tracks: Iterable[str] | None = None,
    top_k: int = 4,
    max_questions_per_domain: int | None = 25,
    include_model_graded: bool = False,
    grader_provider: str | None = None,
) -> PromptfooExportSummary:
    config = load_config(config_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    provider_path = output_dir / "rag_benchmark_provider.py"
    source_provider = root / "integrations" / "promptfoo" / "rag_benchmark_provider.py"
    if source_provider.resolve() != provider_path.resolve():
        shutil.copyfile(source_provider, provider_path)

    selected_domains = list(domains) if domains else enabled_domains(config)
    variants = build_promptfoo_variants(
        config=config,
        systems=list(systems) if systems else None,
        embeddings=list(embeddings) if embeddings else None,
        generators=list(generators) if generators else None,
        judges=list(judges) if judges else None,
        tracks=list(tracks) if tracks else None,
    )
    tests = build_promptfoo_tests(
        root=root,
        domains=selected_domains,
        max_questions_per_domain=max_questions_per_domain,
    )
    repo_root_value = relative_or_absolute(root, output_dir)
    config_path_value = relative_or_absolute(config_path, output_dir)
    python_executable = default_python_executable(root, output_dir)
    promptfoo_config = {
        "description": "RAG benchmark quality gate generated from haxlys/rag-benchmark.",
        "prompts": ["{{query}}"],
        "providers": [
            {
                "id": "file://./rag_benchmark_provider.py",
                "label": variant.label,
                "config": {
                    "repoRoot": repo_root_value,
                    "configPath": config_path_value,
                    "track": variant.track,
                    "system": variant.system_id,
                    "embedding": variant.embedding_model,
                    "generator": variant.generator_model,
                    "judge": variant.judge_model,
                    "topK": top_k,
                    **({"pythonExecutable": python_executable} if python_executable else {}),
                },
            }
            for variant in variants
        ],
        "defaultTest": {
            "assert": build_promptfoo_assertions(include_model_graded, grader_provider),
        },
        "derivedMetrics": [
            {
                "name": "rag_quality",
                "value": "answer_correctness * 0.5 + evidence_recall * 0.3 + context_precision * 0.2",
            },
            {
                "name": "ops_score",
                "value": "rag_quality * 0.8 + citation_validity * 0.2",
            },
        ],
        "tests": "file://./tests.yaml",
    }
    if include_model_graded and grader_provider:
        promptfoo_config["defaultTest"]["options"] = {"provider": grader_provider}

    config_output = output_dir / "promptfooconfig.yaml"
    tests_output = output_dir / "tests.yaml"
    readme_output = output_dir / "README.md"
    readme_ko_output = output_dir / "README.ko.md"
    write_yaml(config_output, promptfoo_config)
    write_yaml(tests_output, tests)
    readme_output.write_text(build_promptfoo_readme(include_model_graded, grader_provider), encoding="utf-8")
    readme_ko_output.write_text(build_promptfoo_readme_ko(include_model_graded, grader_provider), encoding="utf-8")

    warnings = []
    if include_model_graded and not grader_provider:
        warnings.append(
            "Model-graded assertions were enabled without --grader-provider; promptfoo may use its own default grader."
        )
    return PromptfooExportSummary(
        output_dir=output_dir,
        config_path=config_output,
        tests_path=tests_output,
        provider_path=provider_path,
        readme_path=readme_output,
        readme_ko_path=readme_ko_output,
        providers=len(variants),
        tests=len(tests),
        model_graded=include_model_graded,
        warnings=tuple(warnings),
    )


def build_promptfoo_variants(
    *,
    config: dict,
    systems: list[str] | None,
    embeddings: list[str] | None,
    generators: list[str] | None,
    judges: list[str] | None,
    tracks: list[str] | None,
) -> list[PromptfooProviderVariant]:
    selected_tracks = tracks or [DEFAULT_PROMPTFOO_TRACK]
    enabled_track_set = set(enabled_tracks(config))
    selected_tracks = [track for track in selected_tracks if track in enabled_track_set]
    selected_judges = judges or [DEFAULT_PROMPTFOO_JUDGE]
    enabled_judge_set = set(enabled_mvp_judges(config))
    selected_judges = [judge for judge in selected_judges if judge in enabled_judge_set]
    selected_generators = generators or default_generator(config)
    enabled_generator_set = set(enabled_mvp_generators(config))
    selected_generators = [generator for generator in selected_generators if generator in enabled_generator_set]
    selected_systems = systems or default_systems(config)
    enabled_system_set = set(enabled_mvp_systems(config))
    selected_systems = [system for system in selected_systems if system in enabled_system_set]
    selected_embeddings = embeddings or default_embeddings(config)
    enabled_embedding_set = set(enabled_mvp_embeddings(config))
    selected_embeddings = [embedding for embedding in selected_embeddings if embedding in enabled_embedding_set]

    variants: list[PromptfooProviderVariant] = []
    for track in selected_tracks:
        for judge in selected_judges:
            if track == "generator-oracle":
                for generator in selected_generators:
                    variants.append(
                        PromptfooProviderVariant(
                            track=track,
                            system_id="oracle-context",
                            embedding_model="gold-context",
                            generator_model=generator,
                            judge_model=judge,
                        )
                    )
                continue
            if track == "retrieval-only":
                for system in selected_systems:
                    for embedding in embeddings_for_system(system, selected_embeddings):
                        variants.append(
                            PromptfooProviderVariant(
                                track=track,
                                system_id=system,
                                embedding_model=embedding,
                                generator_model="retrieval-probe",
                                judge_model=judge,
                            )
                        )
                    continue
                continue
            for system in selected_systems:
                for embedding in embeddings_for_system(system, selected_embeddings):
                    for generator in selected_generators:
                        variants.append(
                            PromptfooProviderVariant(
                                track=track,
                                system_id=system,
                                embedding_model=embedding,
                                generator_model=generator,
                                judge_model=judge,
                            )
                        )
    return variants


def build_promptfoo_tests(
    *,
    root: Path,
    domains: list[str],
    max_questions_per_domain: int | None,
) -> list[dict]:
    tests = []
    for domain in domains:
        _, questions = load_domain(root, domain)
        selected_questions = questions
        if max_questions_per_domain and max_questions_per_domain > 0:
            selected_questions = questions[:max_questions_per_domain]
        for question in selected_questions:
            tests.append(
                {
                    "description": f"{domain}:{question.question_id}",
                    "vars": {
                        "query": question.question,
                        "question_id": question.question_id,
                        "domain": question.domain,
                        "category": question.category,
                        "expected_answer": question.answer,
                        "expected_aliases": question.answer_aliases,
                        "no_answer": question.no_answer,
                    },
                    "metadata": {
                        "domain": question.domain,
                        "category": question.category,
                        "question_id": question.question_id,
                    },
                }
            )
    return tests


def build_promptfoo_assertions(
    include_model_graded: bool,
    grader_provider: str | None,
) -> list[dict]:
    assertions = [
        {"type": "is-json", "metric": "response_json"},
        {
            "type": "javascript",
            "metric": "answer_correctness",
            "threshold": 0.5,
            "value": "JSON.parse(output).metrics.answer_correctness",
        },
        {
            "type": "javascript",
            "metric": "evidence_recall",
            "threshold": 0.5,
            "value": "JSON.parse(output).metrics.evidence_recall",
        },
        {
            "type": "javascript",
            "metric": "context_precision",
            "threshold": 0.1,
            "value": "JSON.parse(output).metrics.context_precision",
        },
        {
            "type": "javascript",
            "metric": "citation_validity",
            "threshold": 0.5,
            "value": "JSON.parse(output).metrics.citation_validity",
        },
        {
            "type": "javascript",
            "metric": "failure_free",
            "threshold": 1.0,
            "value": "JSON.parse(output).metrics.failure_type === null ? 1 : 0",
        },
    ]
    if include_model_graded:
        graded_assertions = [
            {
                "type": "factuality",
                "metric": "promptfoo_factuality",
                "value": "{{expected_answer}}",
                "transform": "JSON.parse(output).answer",
                "threshold": 0.7,
            },
            {
                "type": "answer-relevance",
                "metric": "promptfoo_answer_relevance",
                "transform": "JSON.parse(output).answer",
                "threshold": 0.7,
            },
            {
                "type": "context-recall",
                "metric": "promptfoo_context_recall",
                "value": "{{expected_answer}}",
                "transform": "JSON.parse(output).answer",
                "contextTransform": "JSON.parse(output).context || 'No retrieved context'",
                "threshold": 0.7,
            },
            {
                "type": "context-relevance",
                "metric": "promptfoo_context_relevance",
                "contextTransform": "JSON.parse(output).context || 'No retrieved context'",
                "threshold": 0.5,
            },
            {
                "type": "context-faithfulness",
                "metric": "promptfoo_context_faithfulness",
                "transform": "JSON.parse(output).answer",
                "contextTransform": "JSON.parse(output).context || 'No retrieved context'",
                "threshold": 0.7,
            },
        ]
        if grader_provider:
            for assertion in graded_assertions:
                assertion["provider"] = grader_provider
        assertions.extend(graded_assertions)
    return assertions


def resolve_question(root: Path, domain: str, vars_: dict[str, Any], prompt: str) -> Question:
    _, questions = load_domain(root, domain)
    question_id = vars_.get("question_id")
    for question in questions:
        if question.question_id == question_id:
            return question
    query = str(vars_.get("query") or prompt)
    for question in questions:
        if question.question == query:
            return question
    return Question(
        question_id=str(question_id or "promptfoo-ad-hoc"),
        domain=domain,
        category=str(vars_.get("category") or "promptfoo"),
        question=query,
        answer=str(vars_.get("expected_answer") or ""),
        answer_aliases=list(vars_.get("expected_aliases") or []),
        no_answer=bool(vars_.get("no_answer", False)),
    )


def resolve_provider_path(value: str | Path, config: dict, root: Path | None = None) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    if root:
        return (root / path).resolve()
    base_path = Path(config.get("basePath", "."))
    return (base_path / path).resolve()


def default_systems(config: dict) -> list[str]:
    enabled = enabled_mvp_systems(config)
    return [system for system in DEFAULT_PROMPTFOO_SYSTEMS if system in enabled] or enabled[:1]


def default_embeddings(config: dict) -> list[str]:
    enabled = enabled_mvp_embeddings(config)
    if DEFAULT_PROMPTFOO_EMBEDDING in enabled:
        return [DEFAULT_PROMPTFOO_EMBEDDING]
    return enabled[:1]


def default_generator(config: dict) -> list[str]:
    enabled = enabled_mvp_generators(config)
    if DEFAULT_PROMPTFOO_GENERATOR in enabled:
        return [DEFAULT_PROMPTFOO_GENERATOR]
    return enabled[:1]


def default_python_executable(root: Path, output_dir: Path) -> str | None:
    candidates = [
        root / ".venv" / "bin" / "python",
        root / ".venv" / "bin" / "python3",
        root / ".venv" / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return relative_or_absolute(candidate, output_dir)
    return None


def embeddings_for_system(system_id: str, embeddings: list[str]) -> list[str]:
    return embeddings if uses_embedding(system_id) else ["none"]


def relative_or_absolute(path: Path, base: Path) -> str:
    target = path.absolute()
    start = base.absolute()
    try:
        return Path(os.path.relpath(target, start=start)).as_posix()
    except ValueError:
        return str(target)


def write_yaml(path: Path, data: Any) -> None:
    rendered = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)
    path.write_text(
        "# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json\n" + rendered,
        encoding="utf-8",
    )


def build_promptfoo_readme(include_model_graded: bool, grader_provider: str | None) -> str:
    grader_line = (
        f"Model-graded assertions are enabled with `{grader_provider}`."
        if include_model_graded and grader_provider
        else "The default config uses deterministic assertions only, so it does not call an external grader."
    )
    return f"""# Promptfoo Integration

This directory lets promptfoo call the local `rag-benchmark` harness as a custom Python provider.

{grader_line}
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
"""


def build_promptfoo_readme_ko(include_model_graded: bool, grader_provider: str | None) -> str:
    grader_line = (
        f"Model-graded assertion은 `{grader_provider}`를 사용하도록 켜져 있습니다."
        if include_model_graded and grader_provider
        else "기본 설정은 결정론적 assertion만 사용하므로 외부 grader를 호출하지 않습니다."
    )
    return f"""# Promptfoo 통합

이 디렉터리는 promptfoo가 로컬 `rag-benchmark` harness를 custom Python provider로 호출하게 해줍니다.

{grader_line}
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
"""
