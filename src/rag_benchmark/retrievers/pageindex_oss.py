from __future__ import annotations

from collections import Counter

from rag_benchmark.datasets import section_chunks
from rag_benchmark.retrievers.base import Retriever, RetrieverStats
from rag_benchmark.schemas import CorpusChunk, Document, Question, RetrievedContext
from rag_benchmark.text import counter_cosine, tokenize, token_count, weighted_counter


class PageIndexOSSRetriever(Retriever):
    """Deterministic OSS PageIndex-style adapter.

    The hosted PageIndex API is intentionally not used. This adapter models the
    open-source flow as a local tree of document sections, then performs
    tree-aware section selection and page-range fetches.
    """

    system_id = "pageindex-oss"

    def build(self, documents: list[Document]) -> RetrieverStats:
        self.section_nodes = section_chunks(documents)
        token_lists = [
            tokenize(f"{chunk.section_title or ''} {chunk.text}", semantic=True)
            for chunk in self.section_nodes
        ]
        df: Counter[str] = Counter()
        for tokens in token_lists:
            df.update(set(tokens))
        total = max(len(token_lists), 1)
        self.idf = {token: 1 + total / (1 + count) for token, count in df.items()}
        self.vectors = [weighted_counter(tokens, self.idf) for tokens in token_lists]
        tree_bytes = sum(len(node.model_dump_json().encode("utf-8")) for node in self.section_nodes)
        return RetrieverStats(
            index_size_bytes=tree_bytes,
            tool_calls=0,
            embedding_tokens=sum(token_count(node.text) for node in self.section_nodes),
        )

    def retrieve_contexts(self, question: Question, *, top_k: int) -> list[RetrievedContext]:
        self.stats.tool_calls += 2
        query_tokens = set(tokenize(question.question, semantic=True))
        query_vector = weighted_counter(query_tokens, self.idf)
        scored: list[tuple[CorpusChunk, float]] = []
        for chunk, vector in zip(self.section_nodes, self.vectors):
            title_tokens = set(tokenize(chunk.section_title or "", semantic=True))
            title_score = len(query_tokens & title_tokens) / max(len(query_tokens), 1)
            semantic_score = counter_cosine(vector, query_vector)
            structure_bonus = 0.08 if chunk.section_title else 0.0
            scored.append((chunk, semantic_score + 0.75 * title_score + structure_bonus))
        scored.sort(key=lambda item: item[1], reverse=True)
        selected = [(chunk, score) for chunk, score in scored if score > 0][:top_k]
        self.stats.tool_calls += len(selected)
        return [
            RetrievedContext(chunk=chunk, score=score, rank=rank, retriever=self.system_id)
            for rank, (chunk, score) in enumerate(selected, 1)
        ]

