from __future__ import annotations

import math

from .schemas import AnswerTrace, EvaluationResult, Question, RetrievalTrace


def evaluate(
    *,
    run_id: str,
    track: str,
    domain: str,
    system_id: str,
    question: Question,
    retrieval: RetrievalTrace,
    answer: AnswerTrace,
) -> EvaluationResult:
    relevant_flags = [
        any(context.chunk.overlaps(evidence) for evidence in question.evidence)
        for context in retrieval.contexts
    ]
    unique_evidence = {evidence.key() for evidence in question.evidence}
    matched_evidence = {
        evidence.key()
        for evidence in question.evidence
        if any(context.chunk.overlaps(evidence) for context in retrieval.contexts)
    }
    evidence_recall = (
        len(matched_evidence) / len(unique_evidence)
        if unique_evidence
        else 1.0 if answer.abstained else 0.0
    )
    context_precision = (
        sum(1 for flag in relevant_flags if flag) / len(relevant_flags)
        if relevant_flags
        else 1.0 if question.no_answer else 0.0
    )
    mrr = reciprocal_rank(relevant_flags)
    ndcg = ndcg_at_k(relevant_flags)
    answer_correctness = answer_correct(question, answer)
    citation_validity = validate_citations(question, retrieval, answer)
    groundedness = 1.0 if answer_correctness and citation_validity else 0.0
    faithfulness = groundedness
    abstention_correctness = 1.0 if question.no_answer and answer.abstained else 0.0
    hit_rate = 1.0 if evidence_recall > 0 or abstention_correctness else 0.0
    failure_type = classify_failure(question, evidence_recall, context_precision, answer_correctness)

    return EvaluationResult(
        run_id=run_id,
        track=track,
        domain=domain,
        system_id=system_id,
        rag_method=retrieval.rag_method,
        embedding_model=retrieval.embedding_model,
        reranker_model=retrieval.reranker_model,
        generator_model=answer.generator_model,
        question_id=question.question_id,
        category=question.category,
        hit_rate=hit_rate,
        evidence_recall=evidence_recall,
        context_precision=context_precision,
        mrr=mrr,
        ndcg=ndcg,
        answer_correctness=answer_correctness,
        faithfulness=faithfulness,
        groundedness=groundedness,
        citation_validity=citation_validity,
        abstention_correctness=abstention_correctness,
        retrieved_token_count=retrieval.retrieved_token_count,
        query_wall_time_ms=retrieval.query_wall_time_ms,
        generator_wall_time_ms=answer.wall_time_ms,
        index_wall_time_ms=retrieval.index_wall_time_ms,
        embedding_tokens=retrieval.embedding_tokens,
        generator_input_tokens=answer.input_token_count,
        generator_output_tokens=answer.output_token_count,
        reranker_calls=retrieval.reranker_calls,
        tool_calls=retrieval.tool_calls,
        estimated_cost=retrieval.estimated_cost + answer.estimated_cost,
        failure_type=failure_type,
    )


def answer_correct(question: Question, answer: AnswerTrace) -> float:
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


def reciprocal_rank(relevant_flags: list[bool]) -> float:
    for index, flag in enumerate(relevant_flags, 1):
        if flag:
            return 1 / index
    return 0.0


def ndcg_at_k(relevant_flags: list[bool]) -> float:
    if not relevant_flags:
        return 0.0
    dcg = sum((1.0 if flag else 0.0) / math.log2(index + 1) for index, flag in enumerate(relevant_flags, 1))
    ideal_relevant = sorted(relevant_flags, reverse=True)
    idcg = sum((1.0 if flag else 0.0) / math.log2(index + 1) for index, flag in enumerate(ideal_relevant, 1))
    return dcg / idcg if idcg else 0.0


def classify_failure(
    question: Question,
    evidence_recall: float,
    context_precision: float,
    answer_correctness: float,
) -> str | None:
    if answer_correctness == 1.0:
        return None
    if question.no_answer:
        return "generation_hallucination"
    if evidence_recall == 0.0:
        return "retrieval_miss"
    if context_precision < 0.34:
        return "context_bloat"
    return "generation_hallucination"
