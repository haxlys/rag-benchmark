from __future__ import annotations

import json
from pathlib import Path

from .schemas import CorpusChunk, Document, Question


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_domain(root: Path, domain: str) -> tuple[list[Document], list[Question]]:
    domain_dir = root / "data" / "fixtures" / domain
    documents = [Document.model_validate(row) for row in read_jsonl(domain_dir / "documents.jsonl")]
    questions = [Question.model_validate(row) for row in read_jsonl(domain_dir / "questions.jsonl")]
    return documents, questions


def enabled_domains(config: dict) -> list[str]:
    return [name for name, item in config.get("domains", {}).items() if item.get("enabled")]


def enabled_mvp_systems(config: dict) -> list[str]:
    systems = config.get("systems", {})
    return [
        name
        for name, item in systems.items()
        if item.get("enabled") and item.get("stage") == "mvp"
    ]


def enabled_mvp_embeddings(config: dict) -> list[str]:
    embeddings = config.get("embeddings", {})
    return [
        name
        for name, item in embeddings.items()
        if item.get("enabled") and item.get("stage") == "mvp"
    ]


def enabled_mvp_generators(config: dict) -> list[str]:
    generators = config.get("generators", {})
    return [
        name
        for name, item in generators.items()
        if item.get("enabled") and item.get("stage") == "mvp"
    ]


def enabled_tracks(config: dict) -> list[str]:
    tracks = config.get("experiment_tracks", {})
    return [name for name, item in tracks.items() if item.get("enabled")]


def page_chunks(documents: list[Document]) -> list[CorpusChunk]:
    chunks = []
    for doc in documents:
        for page in doc.pages:
            section = next(
                (
                    section
                    for section in doc.sections
                    if section.page_start <= page.page <= section.page_end
                ),
                None,
            )
            chunks.append(
                CorpusChunk(
                    chunk_id=f"{doc.doc_id}:page:{page.page}",
                    doc_id=doc.doc_id,
                    domain=doc.domain,
                    title=doc.title,
                    text=page.text,
                    page_start=page.page,
                    page_end=page.page,
                    section_id=section.section_id if section else None,
                    section_title=section.title if section else None,
                )
            )
    return chunks


def section_chunks(documents: list[Document]) -> list[CorpusChunk]:
    chunks = []
    for doc in documents:
        for section in doc.sections:
            chunks.append(
                CorpusChunk(
                    chunk_id=f"{doc.doc_id}:section:{section.section_id}",
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
            )
    return chunks
