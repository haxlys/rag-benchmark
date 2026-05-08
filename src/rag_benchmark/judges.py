from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .schemas import AnswerTrace, JudgementTrace, Question, RetrievalTrace
from .text import token_count


@dataclass(frozen=True)
class JudgeProfile:
    model_id: str
    family: str
    input_cost_per_token: float
    base_latency_ms: float
    token_latency_ms: float
    human_agreement_proxy: float
    false_accept_risk: float
    false_reject_risk: float
    strict_citation: bool
    lenient_partial_credit: bool
    notes: str


JUDGE_PROFILES: dict[str, JudgeProfile] = {
    "exact-match-gold": JudgeProfile(
        model_id="exact-match-gold",
        family="deterministic_gold_label_evaluator",
        input_cost_per_token=0.0,
        base_latency_ms=0.0,
        token_latency_ms=0.0,
        human_agreement_proxy=0.92,
        false_accept_risk=0.02,
        false_reject_risk=0.10,
        strict_citation=False,
        lenient_partial_credit=False,
        notes="Gold exact-match evaluator. Strong for normalized factual labels, weak for paraphrases.",
    ),
    "llm-judge-balanced-proxy": JudgeProfile(
        model_id="llm-judge-balanced-proxy",
        family="balanced_llm_as_judge_profile",
        input_cost_per_token=0.00000035,
        base_latency_ms=40.0,
        token_latency_ms=0.006,
        human_agreement_proxy=0.86,
        false_accept_risk=0.08,
        false_reject_risk=0.06,
        strict_citation=False,
        lenient_partial_credit=True,
        notes="Local deterministic proxy for an LLM judge that accepts grounded paraphrases but may over-accept plausible answers.",
    ),
    "citation-strict-judge-proxy": JudgeProfile(
        model_id="citation-strict-judge-proxy",
        family="citation_first_llm_judge_profile",
        input_cost_per_token=0.00000045,
        base_latency_ms=52.0,
        token_latency_ms=0.008,
        human_agreement_proxy=0.83,
        false_accept_risk=0.03,
        false_reject_risk=0.14,
        strict_citation=True,
        lenient_partial_credit=False,
        notes="Local deterministic proxy for a strict citation judge. Better for compliance checks, harsher on weak citations.",
    ),
}


def judge_answer(
    question: Question,
    retrieval: RetrievalTrace,
    answer: AnswerTrace,
    judge_model: str,
) -> JudgementTrace:
    profile = profile_for(judge_model)
    gold_answer_correctness = exact_answer_correct(question, answer)
    citation_validity = validate_citations(question, retrieval, answer)
    answer_correctness = judged_answer_correctness(
        profile,
        question,
        retrieval,
        answer,
        gold_answer_correctness,
        citation_validity,
    )
    abstention_correctness = 1.0 if question.no_answer and answer.abstained else 0.0
    groundedness = 1.0 if answer_correctness and citation_validity else 0.0
    faithfulness = groundedness
    judge_input_tokens = (
        token_count(question.question)
        + token_count(question.answer)
        + token_count(answer.answer)
        + sum(token_count(context.chunk.text) for context in retrieval.contexts)
    )
    wall_time_ms = profile.base_latency_ms + profile.token_latency_ms * judge_input_tokens
    return JudgementTrace(
        judge_model=profile.model_id,
        answer_correctness=answer_correctness,
        gold_answer_correctness=gold_answer_correctness,
        faithfulness=faithfulness,
        groundedness=groundedness,
        citation_validity=citation_validity,
        abstention_correctness=abstention_correctness,
        human_agreement_proxy=profile.human_agreement_proxy,
        false_accept_risk=profile.false_accept_risk,
        false_reject_risk=profile.false_reject_risk,
        input_token_count=judge_input_tokens,
        wall_time_ms=wall_time_ms,
        estimated_cost=round(profile.input_cost_per_token * judge_input_tokens, 8),
    )


def profile_for(model_id: str) -> JudgeProfile:
    try:
        return JUDGE_PROFILES[model_id]
    except KeyError as exc:
        raise ValueError(f"Unknown judge model: {model_id}") from exc


def exact_answer_correct(question: Question, answer: AnswerTrace) -> float:
    if question.no_answer:
        return 1.0 if answer.abstained else 0.0
    if answer.abstained:
        return 0.0
    allowed = [question.answer, *question.answer_aliases]
    normalized = answer.answer.strip().lower()
    return 1.0 if any(item.strip().lower() == normalized for item in allowed) else 0.0


def validate_citations(question: Question, retrieval: RetrievalTrace, answer: AnswerTrace) -> float:
    if question.no_answer:
        return 1.0 if not answer.cited_chunk_ids else 0.0
    if not answer.cited_chunk_ids:
        return 0.0
    by_id = {context.chunk.chunk_id: context for context in retrieval.contexts}
    valid = 0
    for chunk_id in answer.cited_chunk_ids:
        context = by_id.get(chunk_id)
        if context and any(context.chunk.overlaps(evidence) for evidence in question.evidence):
            valid += 1
    return valid / len(answer.cited_chunk_ids)


def judged_answer_correctness(
    profile: JudgeProfile,
    question: Question,
    retrieval: RetrievalTrace,
    answer: AnswerTrace,
    gold_answer_correctness: float,
    citation_validity: float,
) -> float:
    if profile.model_id == "exact-match-gold":
        return gold_answer_correctness
    if question.no_answer:
        if answer.abstained:
            return 1.0
        return 0.0 if not false_accept(profile, question, answer) else 1.0
    if answer.abstained:
        return 0.0
    if gold_answer_correctness:
        if profile.strict_citation and citation_validity < 1.0:
            return 0.0
        if false_reject(profile, question, answer):
            return 0.0
        return 1.0
    if profile.lenient_partial_credit and literal_answer_supported(question, retrieval):
        return 1.0
    return 1.0 if false_accept(profile, question, answer) else 0.0


def literal_answer_supported(question: Question, retrieval: RetrievalTrace) -> bool:
    aliases = [question.answer, *question.answer_aliases]
    combined_context = "\n".join(context.chunk.text for context in retrieval.contexts).lower()
    return any(alias and alias.lower() in combined_context for alias in aliases)


def false_accept(profile: JudgeProfile, question: Question, answer: AnswerTrace) -> bool:
    return stable_score(f"accept:{profile.model_id}:{question.question_id}:{answer.answer}") < profile.false_accept_risk


def false_reject(profile: JudgeProfile, question: Question, answer: AnswerTrace) -> bool:
    return stable_score(f"reject:{profile.model_id}:{question.question_id}:{answer.answer}") < profile.false_reject_risk


def stable_score(value: str) -> float:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF
