from __future__ import annotations

from pydantic import BaseModel, Field


class Page(BaseModel):
    page: int
    text: str


class Section(BaseModel):
    section_id: str
    title: str
    page_start: int
    page_end: int
    text: str
    parent_id: str | None = None


class Document(BaseModel):
    doc_id: str
    domain: str
    title: str
    source: str = "fixture"
    pages: list[Page]
    sections: list[Section] = Field(default_factory=list)


class Evidence(BaseModel):
    doc_id: str
    page: int | None = None
    section_id: str | None = None

    def key(self) -> tuple[str, int | None, str | None]:
        return (self.doc_id, self.page, self.section_id)


class Question(BaseModel):
    question_id: str
    domain: str
    category: str
    question: str
    answer: str
    answer_aliases: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    no_answer: bool = False
    notes: str = ""


class CorpusChunk(BaseModel):
    chunk_id: str
    doc_id: str
    domain: str
    title: str
    text: str
    page_start: int
    page_end: int
    section_id: str | None = None
    section_title: str | None = None
    parent_id: str | None = None
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)

    def overlaps(self, evidence: Evidence) -> bool:
        if self.doc_id != evidence.doc_id:
            return False
        if evidence.section_id and self.section_id == evidence.section_id:
            return True
        if evidence.page is not None and self.page_start <= evidence.page <= self.page_end:
            return True
        return False


class RetrievedContext(BaseModel):
    chunk: CorpusChunk
    score: float
    rank: int
    retriever: str


class RetrievalTrace(BaseModel):
    system_id: str
    rag_method: str
    embedding_model: str = "none"
    reranker_model: str = "none"
    question_id: str
    contexts: list[RetrievedContext]
    query_wall_time_ms: float
    index_wall_time_ms: float = 0.0
    retrieved_token_count: int = 0
    embedding_tokens: int = 0
    reranker_calls: int = 0
    tool_calls: int = 0
    estimated_cost: float = 0.0
    warnings: list[str] = Field(default_factory=list)


class AnswerTrace(BaseModel):
    answer: str
    cited_chunk_ids: list[str]
    abstained: bool
    generator_model: str = "extractive-strict"
    input_token_count: int = 0
    output_token_count: int = 0
    wall_time_ms: float = 0.0
    estimated_cost: float = 0.0


class EvaluationResult(BaseModel):
    run_id: str
    track: str
    domain: str
    system_id: str
    rag_method: str
    embedding_model: str
    reranker_model: str
    generator_model: str
    question_id: str
    category: str
    hit_rate: float
    evidence_recall: float
    context_precision: float
    mrr: float
    ndcg: float
    answer_correctness: float
    faithfulness: float
    groundedness: float
    citation_validity: float
    abstention_correctness: float
    retrieved_token_count: int
    query_wall_time_ms: float
    generator_wall_time_ms: float
    index_wall_time_ms: float
    embedding_tokens: int
    generator_input_tokens: int
    generator_output_tokens: int
    reranker_calls: int
    tool_calls: int
    estimated_cost: float
    failure_type: str | None
