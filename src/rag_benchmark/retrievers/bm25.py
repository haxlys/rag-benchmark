from __future__ import annotations

import math
from collections import Counter

from rag_benchmark.datasets import page_chunks
from rag_benchmark.retrievers.base import Retriever, RetrieverStats
from rag_benchmark.schemas import CorpusChunk, Document, Question, RetrievedContext
from rag_benchmark.text import tokenize


class BM25Retriever(Retriever):
    system_id = "bm25"

    def build(self, documents: list[Document]) -> RetrieverStats:
        self.chunks = page_chunks(documents)
        self.chunk_tokens = [tokenize(chunk.text) for chunk in self.chunks]
        self.doc_freq: Counter[str] = Counter()
        for tokens in self.chunk_tokens:
            self.doc_freq.update(set(tokens))
        self.avgdl = sum(len(tokens) for tokens in self.chunk_tokens) / max(len(self.chunk_tokens), 1)
        self.idf = {
            token: math.log(1 + (len(self.chunks) - df + 0.5) / (df + 0.5))
            for token, df in self.doc_freq.items()
        }
        index_size = sum(len(chunk.text.encode("utf-8")) for chunk in self.chunks)
        return RetrieverStats(index_size_bytes=index_size)

    def retrieve_contexts(self, question: Question, *, top_k: int) -> list[RetrievedContext]:
        query_tokens = tokenize(question.question)
        scored = score_bm25(self.chunks, self.chunk_tokens, self.idf, self.avgdl, query_tokens)
        return [
            RetrievedContext(chunk=chunk, score=score, rank=rank, retriever=self.system_id)
            for rank, (chunk, score) in enumerate(scored[:top_k], 1)
            if score > 0
        ]


def score_bm25(
    chunks: list[CorpusChunk],
    chunk_tokens: list[list[str]],
    idf: dict[str, float],
    avgdl: float,
    query_tokens: list[str],
) -> list[tuple[CorpusChunk, float]]:
    k1 = 1.5
    b = 0.75
    scored = []
    for chunk, tokens in zip(chunks, chunk_tokens):
        counts = Counter(tokens)
        dl = len(tokens) or 1
        score = 0.0
        for token in query_tokens:
            tf = counts.get(token, 0)
            if not tf:
                continue
            denom = tf + k1 * (1 - b + b * dl / max(avgdl, 1e-9))
            score += idf.get(token, 0.0) * (tf * (k1 + 1)) / denom
        scored.append((chunk, score))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored

