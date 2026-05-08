from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass

from .schemas import AnswerTrace, Question, RetrievalTrace
from .text import token_count


ABSTAIN = "Insufficient evidence in retrieved context."
HALLUCINATION = "Unverified answer generated without supporting evidence."


@dataclass(frozen=True)
class GeneratorProfile:
    model_id: str
    family: str
    input_cost_per_token: float
    output_cost_per_token: float
    base_latency_ms: float
    token_latency_ms: float
    partial_recall_min: float
    capabilities: dict[str, float]


GENERATOR_PROFILES: dict[str, GeneratorProfile] = {
    "retrieval-probe": GeneratorProfile(
        model_id="retrieval-probe",
        family="retrieval_only",
        input_cost_per_token=0.0,
        output_cost_per_token=0.0,
        base_latency_ms=0.0,
        token_latency_ms=0.0,
        partial_recall_min=1.0,
        capabilities={},
    ),
    "extractive-strict": GeneratorProfile(
        model_id="extractive-strict",
        family="small_grounded_oss_llm_profile",
        input_cost_per_token=0.00000020,
        output_cost_per_token=0.00000040,
        base_latency_ms=18.0,
        token_latency_ms=0.004,
        partial_recall_min=1.0,
        capabilities={
            "direct_lookup": 0.98,
            "section_navigation": 0.90,
            "multi_section": 0.70,
            "multi_document": 0.62,
            "table_numeric": 0.55,
            "calculation": 0.42,
            "global_summary": 0.50,
            "no_answer": 0.92,
        },
    ),
    "balanced-oss-llm": GeneratorProfile(
        model_id="balanced-oss-llm",
        family="balanced_instruction_oss_llm_profile",
        input_cost_per_token=0.00000035,
        output_cost_per_token=0.00000070,
        base_latency_ms=32.0,
        token_latency_ms=0.006,
        partial_recall_min=0.67,
        capabilities={
            "direct_lookup": 0.97,
            "section_navigation": 0.92,
            "multi_section": 0.82,
            "multi_document": 0.78,
            "table_numeric": 0.76,
            "calculation": 0.66,
            "global_summary": 0.76,
            "no_answer": 0.88,
        },
    ),
    "reasoning-oss-llm": GeneratorProfile(
        model_id="reasoning-oss-llm",
        family="reasoning_table_oss_llm_profile",
        input_cost_per_token=0.00000055,
        output_cost_per_token=0.00000110,
        base_latency_ms=58.0,
        token_latency_ms=0.010,
        partial_recall_min=0.50,
        capabilities={
            "direct_lookup": 0.96,
            "section_navigation": 0.93,
            "multi_section": 0.90,
            "multi_document": 0.86,
            "table_numeric": 0.88,
            "calculation": 0.84,
            "global_summary": 0.84,
            "no_answer": 0.84,
        },
    ),
}


def generate_answer(question: Question, retrieval: RetrievalTrace, generator_model: str) -> AnswerTrace:
    """Deterministic answer-generation profile.

    The benchmark stays reproducible by using local capability profiles instead
    of stochastic LLM calls. This separates three things: whether retrieval found
    the evidence, whether an oracle context would let a generator answer, and
    whether the end-to-end combination works.
    """
    profile = profile_for(generator_model)
    start = time.perf_counter()

    if profile.model_id == "retrieval-probe":
        answer = retrieval_probe(question, retrieval)
    else:
        answer = profiled_answer(question, retrieval, profile)

    input_tokens = token_count(question.question) + sum(
        token_count(context.chunk.text) for context in retrieval.contexts
    )
    output_tokens = token_count(answer.answer)
    wall_time_ms = (time.perf_counter() - start) * 1000 + estimate_latency(
        profile,
        input_tokens,
        output_tokens,
    )
    return AnswerTrace(
        answer=answer.answer,
        cited_chunk_ids=answer.cited_chunk_ids,
        abstained=answer.abstained,
        generator_model=profile.model_id,
        input_token_count=input_tokens,
        output_token_count=output_tokens,
        wall_time_ms=wall_time_ms,
        estimated_cost=estimate_cost(profile, input_tokens, output_tokens),
    )


def profile_for(model_id: str) -> GeneratorProfile:
    try:
        return GENERATOR_PROFILES[model_id]
    except KeyError as exc:
        raise ValueError(f"Unknown generator model: {model_id}") from exc


def retrieval_probe(question: Question, retrieval: RetrievalTrace) -> AnswerTrace:
    if question.no_answer:
        return AnswerTrace(answer=ABSTAIN, cited_chunk_ids=[], abstained=True)
    matched_contexts, required, matched = matched_evidence(question, retrieval)
    if required and matched >= required:
        return AnswerTrace(
            answer=question.answer,
            cited_chunk_ids=[context.chunk.chunk_id for context in matched_contexts],
            abstained=False,
        )
    return AnswerTrace(answer=ABSTAIN, cited_chunk_ids=[], abstained=True)


def profiled_answer(
    question: Question,
    retrieval: RetrievalTrace,
    profile: GeneratorProfile,
) -> AnswerTrace:
    if question.no_answer:
        can_abstain = capability_pass(profile, question, "no_answer")
        return (
            AnswerTrace(answer=ABSTAIN, cited_chunk_ids=[], abstained=True)
            if can_abstain
            else AnswerTrace(answer=HALLUCINATION, cited_chunk_ids=[], abstained=False)
        )

    matched_contexts, required, matched = matched_evidence(question, retrieval)
    recall = matched / required if required else 0.0
    aliases = [question.answer, *question.answer_aliases]
    combined_context = "\n".join(context.chunk.text for context in retrieval.contexts).lower()
    literal_answer_present = any(alias.lower() in combined_context for alias in aliases if alias)
    enough_context = required > 0 and matched >= required
    recoverable_partial = recall >= profile.partial_recall_min and literal_answer_present

    if (enough_context or recoverable_partial) and capability_pass(profile, question, question.category):
        cited_contexts = matched_contexts or retrieval.contexts[:1]
        return AnswerTrace(
            answer=question.answer,
            cited_chunk_ids=[context.chunk.chunk_id for context in cited_contexts],
            abstained=False,
        )

    return AnswerTrace(answer=ABSTAIN, cited_chunk_ids=[], abstained=True)


def matched_evidence(
    question: Question,
    retrieval: RetrievalTrace,
) -> tuple[list, int, int]:
    matched_contexts = []
    for context in retrieval.contexts:
        if any(context.chunk.overlaps(evidence) for evidence in question.evidence):
            matched_contexts.append(context)

    required_keys = {evidence.key() for evidence in question.evidence}
    matched_keys = {
        evidence.key()
        for evidence in question.evidence
        if any(context.chunk.overlaps(evidence) for context in retrieval.contexts)
    }
    return matched_contexts, len(required_keys), len(matched_keys)


def capability_pass(profile: GeneratorProfile, question: Question, category: str) -> bool:
    threshold = profile.capabilities.get(category, profile.capabilities.get("direct_lookup", 0.75))
    return stable_score(f"{profile.model_id}:{question.question_id}:{category}") <= threshold


def stable_score(value: str) -> float:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def estimate_latency(profile: GeneratorProfile, input_tokens: int, output_tokens: int) -> float:
    if profile.model_id == "retrieval-probe":
        return 0.0
    return profile.base_latency_ms + profile.token_latency_ms * (input_tokens + output_tokens)


def estimate_cost(profile: GeneratorProfile, input_tokens: int, output_tokens: int) -> float:
    return round(
        profile.input_cost_per_token * input_tokens
        + profile.output_cost_per_token * output_tokens,
        8,
    )
