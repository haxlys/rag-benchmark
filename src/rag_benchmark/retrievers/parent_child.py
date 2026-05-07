from __future__ import annotations

import math
from collections import Counter

from rag_benchmark.retrievers.base import Retriever, RetrieverStats
from rag_benchmark.retrievers.bm25 import score_bm25
from rag_benchmark.schemas import CorpusChunk, Document, Question, RetrievedContext
from rag_benchmark.text import split_sentences, tokenize


class ParentChildRetriever(Retriever):
    system_id = "parent-child"

    def build(self, documents: list[Document]) -> RetrieverStats:
        self.child_chunks: list[CorpusChunk] = []
        self.parent_chunks: dict[str, CorpusChunk] = {}
        for doc in documents:
            for section in doc.sections:
                parent = CorpusChunk(
                    chunk_id=f"{doc.doc_id}:parent:{section.section_id}",
                    doc_id=doc.doc_id,
                    domain=doc.domain,
                    title=doc.title,
                    text=section.text,
                    page_start=section.page_start,
                    page_end=section.page_end,
                    section_id=section.section_id,
                    section_title=section.title,
                    parent_id=section.parent_id,
                )
                self.parent_chunks[parent.chunk_id] = parent
                for index, sentence in enumerate(split_sentences(section.text), 1):
                    self.child_chunks.append(
                        CorpusChunk(
                            chunk_id=f"{doc.doc_id}:child:{section.section_id}:{index}",
                            doc_id=doc.doc_id,
                            domain=doc.domain,
                            title=doc.title,
                            text=sentence,
                            page_start=section.page_start,
                            page_end=section.page_end,
                            section_id=section.section_id,
                            section_title=section.title,
                            parent_id=parent.chunk_id,
                        )
                    )
        self.child_tokens = [tokenize(chunk.text) for chunk in self.child_chunks]
        df: Counter[str] = Counter()
        for tokens in self.child_tokens:
            df.update(set(tokens))
        total = max(len(self.child_chunks), 1)
        self.idf = {token: math.log(1 + (total - count + 0.5) / (count + 0.5)) for token, count in df.items()}
        self.avgdl = sum(len(tokens) for tokens in self.child_tokens) / max(total, 1)
        index_size = sum(len(chunk.text.encode("utf-8")) for chunk in self.child_chunks)
        return RetrieverStats(index_size_bytes=index_size)

    def retrieve_contexts(self, question: Question, *, top_k: int) -> list[RetrievedContext]:
        query_tokens = tokenize(question.question)
        child_scored = score_bm25(
            self.child_chunks,
            self.child_tokens,
            self.idf,
            self.avgdl,
            query_tokens,
        )
        parent_scores: dict[str, float] = {}
        for child, score in child_scored:
            if score <= 0 or not child.parent_id:
                continue
            parent_scores[child.parent_id] = max(parent_scores.get(child.parent_id, 0.0), score)
        ranked = sorted(parent_scores.items(), key=lambda item: item[1], reverse=True)
        return [
            RetrievedContext(
                chunk=self.parent_chunks[parent_id],
                score=score,
                rank=rank,
                retriever=self.system_id,
            )
            for rank, (parent_id, score) in enumerate(ranked[:top_k], 1)
        ]

