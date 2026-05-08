from __future__ import annotations

from rag_benchmark.retrievers.base import Retriever, RetrieverStats
from rag_benchmark.retrievers.bm25 import BM25Retriever
from rag_benchmark.retrievers.dense import DenseVectorRetriever
from rag_benchmark.schemas import Document, Question, RetrievedContext


class HybridRetriever(Retriever):
    system_id = "hybrid"

    def build(self, documents: list[Document]) -> RetrieverStats:
        self.bm25 = BM25Retriever(documents, top_k=max(self.top_k * 4, 12))
        self.dense = DenseVectorRetriever(
            documents,
            top_k=max(self.top_k * 4, 12),
            embedding_model=self.embedding_model,
        )
        return RetrieverStats(
            embedding_tokens=self.dense.stats.embedding_tokens,
            index_size_bytes=self.bm25.stats.index_size_bytes + self.dense.stats.index_size_bytes,
        )

    def retrieve_contexts(self, question: Question, *, top_k: int) -> list[RetrievedContext]:
        broad_k = max(top_k * 4, 12)
        bm25 = self.bm25.retrieve_contexts(question, top_k=broad_k)
        dense = self.dense.retrieve_contexts(question, top_k=broad_k)
        fused = reciprocal_rank_fusion([bm25, dense], self.system_id)
        return fused[:top_k]


def reciprocal_rank_fusion(
    result_sets: list[list[RetrievedContext]],
    retriever: str,
    *,
    k: int = 60,
) -> list[RetrievedContext]:
    by_chunk: dict[str, tuple[RetrievedContext, float]] = {}
    for result_set in result_sets:
        for item in result_set:
            current = by_chunk.get(item.chunk.chunk_id, (item, 0.0))
            by_chunk[item.chunk.chunk_id] = (item, current[1] + 1 / (k + item.rank))
    ranked = sorted(by_chunk.values(), key=lambda item: item[1], reverse=True)
    return [
        RetrievedContext(chunk=item.chunk, score=score, rank=rank, retriever=retriever)
        for rank, (item, score) in enumerate(ranked, 1)
    ]
