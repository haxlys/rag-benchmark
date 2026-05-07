from __future__ import annotations

import math
from collections import Counter

from rag_benchmark.datasets import page_chunks
from rag_benchmark.retrievers.base import Retriever, RetrieverStats
from rag_benchmark.schemas import CorpusChunk, Document, Question, RetrievedContext
from rag_benchmark.text import counter_cosine, tokenize, token_count, weighted_counter


class DenseVectorRetriever(Retriever):
    system_id = "dense-vector"

    def build(self, documents: list[Document]) -> RetrieverStats:
        self.chunks = page_chunks(documents)
        token_lists = [tokenize(chunk.text, semantic=True) for chunk in self.chunks]
        df: Counter[str] = Counter()
        for tokens in token_lists:
            df.update(set(tokens))
        total = max(len(token_lists), 1)
        self.idf = {token: math.log(1 + total / (1 + count)) for token, count in df.items()}
        self.vectors = [weighted_counter(tokens, self.idf) for tokens in token_lists]
        embedding_tokens = sum(token_count(chunk.text) for chunk in self.chunks)
        index_size = sum(len(vector) * 16 for vector in self.vectors)
        return RetrieverStats(embedding_tokens=embedding_tokens, index_size_bytes=index_size)

    def retrieve_contexts(self, question: Question, *, top_k: int) -> list[RetrievedContext]:
        query_vector = weighted_counter(tokenize(question.question, semantic=True), self.idf)
        scored = score_dense(self.chunks, self.vectors, query_vector)
        return [
            RetrievedContext(chunk=chunk, score=score, rank=rank, retriever=self.system_id)
            for rank, (chunk, score) in enumerate(scored[:top_k], 1)
            if score > 0
        ]


def score_dense(
    chunks: list[CorpusChunk],
    vectors: list[Counter[str]],
    query_vector: Counter[str],
) -> list[tuple[CorpusChunk, float]]:
    scored = [(chunk, counter_cosine(vector, query_vector)) for chunk, vector in zip(chunks, vectors)]
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored

