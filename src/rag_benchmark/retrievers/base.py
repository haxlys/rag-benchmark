from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from rag_benchmark.embeddings import embedding_query_cost
from rag_benchmark.schemas import Document, Question, RetrievedContext, RetrievalTrace
from rag_benchmark.text import token_count


@dataclass
class RetrieverStats:
    index_wall_time_ms: float = 0.0
    embedding_tokens: int = 0
    reranker_calls: int = 0
    tool_calls: int = 0
    index_size_bytes: int = 0
    warnings: list[str] = field(default_factory=list)


class Retriever(ABC):
    system_id: str

    def __init__(
        self,
        documents: list[Document],
        *,
        top_k: int = 4,
        embedding_model: str = "none",
        reranker_model: str = "none",
    ) -> None:
        self.documents = documents
        self.top_k = top_k
        self.embedding_model = embedding_model
        self.reranker_model = reranker_model
        start = time.perf_counter()
        self.stats = self.build(documents)
        self.stats.index_wall_time_ms = (time.perf_counter() - start) * 1000

    @abstractmethod
    def build(self, documents: list[Document]) -> RetrieverStats:
        """Build an index."""

    @abstractmethod
    def retrieve_contexts(self, question: Question, *, top_k: int) -> list[RetrievedContext]:
        """Return ranked contexts."""

    def retrieve(self, question: Question, *, top_k: int | None = None) -> RetrievalTrace:
        requested_top_k = top_k or self.top_k
        reranker_before = self.stats.reranker_calls
        tool_before = self.stats.tool_calls
        start = time.perf_counter()
        contexts = self.retrieve_contexts(question, top_k=requested_top_k)
        query_wall_time_ms = (time.perf_counter() - start) * 1000
        retrieved_token_count = sum(token_count(item.chunk.text) for item in contexts)
        embedding_tokens = token_count(question.question) if self.stats.embedding_tokens else 0
        reranker_calls = self.stats.reranker_calls - reranker_before
        tool_calls = self.stats.tool_calls - tool_before
        estimated_cost = estimate_cost(
            embedding_tokens=embedding_tokens,
            embedding_model=self.embedding_model,
            reranker_calls=reranker_calls,
            tool_calls=tool_calls,
            retrieved_token_count=retrieved_token_count,
        )
        return RetrievalTrace(
            system_id=self.system_id,
            rag_method=self.system_id,
            embedding_model=self.embedding_model,
            reranker_model=self.reranker_model,
            question_id=question.question_id,
            contexts=contexts,
            query_wall_time_ms=query_wall_time_ms,
            index_wall_time_ms=self.stats.index_wall_time_ms,
            retrieved_token_count=retrieved_token_count,
            embedding_tokens=embedding_tokens,
            reranker_calls=reranker_calls,
            tool_calls=tool_calls,
            estimated_cost=estimated_cost,
            warnings=self.stats.warnings,
        )


def estimate_cost(
    *,
    embedding_tokens: int,
    embedding_model: str,
    reranker_calls: int,
    tool_calls: int,
    retrieved_token_count: int,
) -> float:
    """Small normalized cost estimate for relative operations comparison."""
    return round(
        embedding_query_cost(embedding_model, embedding_tokens)
        + reranker_calls * 0.00002
        + tool_calls * 0.00001
        + retrieved_token_count * 0.00000001,
        8,
    )
