from __future__ import annotations

from rag_benchmark.retrievers.base import RetrieverStats
from rag_benchmark.retrievers.hybrid import HybridRetriever
from rag_benchmark.schemas import Document, Question, RetrievedContext
from rag_benchmark.text import tokenize


class HybridRerankRetriever(HybridRetriever):
    system_id = "hybrid-rerank"

    def build(self, documents: list[Document]) -> RetrieverStats:
        stats = super().build(documents)
        stats.reranker_calls = 0
        return stats

    def retrieve_contexts(self, question: Question, *, top_k: int) -> list[RetrievedContext]:
        candidates = super().retrieve_contexts(question, top_k=max(top_k * 4, 12))
        self.stats.reranker_calls += len(candidates)
        query_tokens = set(tokenize(question.question, semantic=True))
        reranked = []
        for item in candidates:
            text_tokens = set(tokenize(item.chunk.text, semantic=True))
            title_tokens = set(tokenize(item.chunk.section_title or item.chunk.title, semantic=True))
            overlap = len(query_tokens & text_tokens) / max(len(query_tokens), 1)
            title_overlap = len(query_tokens & title_tokens) / max(len(query_tokens), 1)
            score = item.score + 0.65 * overlap + 0.45 * title_overlap
            reranked.append((item, score))
        reranked.sort(key=lambda item: item[1], reverse=True)
        return [
            RetrievedContext(chunk=item.chunk, score=score, rank=rank, retriever=self.system_id)
            for rank, (item, score) in enumerate(reranked[:top_k], 1)
        ]

