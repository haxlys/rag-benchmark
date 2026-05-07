from __future__ import annotations

from .schemas import AnswerTrace, Question, RetrievalTrace


ABSTAIN = "Insufficient evidence in retrieved context."


def generate_answer(question: Question, retrieval: RetrievalTrace) -> AnswerTrace:
    """Deterministic extractive answerer for retrieval-focused benchmarking.

    If the retrieved context covers the gold evidence, return the gold answer.
    Otherwise abstain. This keeps the first benchmark reproducible and makes
    failures easy to attribute to retrieval rather than to a stochastic LLM.
    """
    if question.no_answer:
        return AnswerTrace(answer=ABSTAIN, cited_chunk_ids=[], abstained=True)

    matched_contexts = []
    for context in retrieval.contexts:
        if any(context.chunk.overlaps(evidence) for evidence in question.evidence):
            matched_contexts.append(context)

    required = len({evidence.key() for evidence in question.evidence})
    matched_keys = {
        evidence.key()
        for evidence in question.evidence
        if any(context.chunk.overlaps(evidence) for context in retrieval.contexts)
    }

    if required and len(matched_keys) >= required:
        return AnswerTrace(
            answer=question.answer,
            cited_chunk_ids=[context.chunk.chunk_id for context in matched_contexts],
            abstained=False,
        )

    # Secondary check for cases where the chunk contains a literal answer alias
    # but the page/section metadata is imperfect.
    combined_context = "\n".join(context.chunk.text for context in retrieval.contexts).lower()
    aliases = [question.answer, *question.answer_aliases]
    if aliases and any(alias.lower() in combined_context for alias in aliases):
        return AnswerTrace(
            answer=question.answer,
            cited_chunk_ids=[context.chunk.chunk_id for context in retrieval.contexts[:1]],
            abstained=False,
        )

    return AnswerTrace(answer=ABSTAIN, cited_chunk_ids=[], abstained=True)

