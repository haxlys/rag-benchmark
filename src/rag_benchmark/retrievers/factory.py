from __future__ import annotations

from rag_benchmark.retrievers.base import Retriever
from rag_benchmark.retrievers.bm25 import BM25Retriever
from rag_benchmark.retrievers.dense import DenseVectorRetriever
from rag_benchmark.retrievers.hybrid import HybridRetriever
from rag_benchmark.retrievers.hybrid_rerank import HybridRerankRetriever
from rag_benchmark.retrievers.pageindex_oss import PageIndexOSSRetriever
from rag_benchmark.retrievers.parent_child import ParentChildRetriever
from rag_benchmark.schemas import Document


RETRIEVERS: dict[str, type[Retriever]] = {
    "bm25": BM25Retriever,
    "dense-vector": DenseVectorRetriever,
    "hybrid": HybridRetriever,
    "hybrid-rerank": HybridRerankRetriever,
    "parent-child": ParentChildRetriever,
    "pageindex-oss": PageIndexOSSRetriever,
}


def build_retriever(system_id: str, documents: list[Document], *, top_k: int) -> Retriever:
    try:
        retriever_cls = RETRIEVERS[system_id]
    except KeyError as exc:
        raise ValueError(f"Unknown retriever system: {system_id}") from exc
    return retriever_cls(documents, top_k=top_k)

