from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .datasets import load_domain
from .schemas import Document, Question


@dataclass
class ValidationReport:
    domain: str
    documents: int
    questions: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_domain_data(root: Path, domain: str, *, top_k: int | None = None) -> ValidationReport:
    documents, questions = load_domain(root, domain)
    report = ValidationReport(domain=domain, documents=len(documents), questions=len(questions))
    validate_documents(documents, report)
    validate_questions(documents, questions, report, top_k=top_k)
    return report


def validate_documents(documents: list[Document], report: ValidationReport) -> None:
    seen_doc_ids: set[str] = set()
    for doc in documents:
        if doc.doc_id in seen_doc_ids:
            report.errors.append(f"duplicate document id: {doc.doc_id}")
        seen_doc_ids.add(doc.doc_id)
        if not doc.pages:
            report.errors.append(f"{doc.doc_id}: no pages")
        page_numbers = {page.page for page in doc.pages}
        if len(page_numbers) != len(doc.pages):
            report.errors.append(f"{doc.doc_id}: duplicate page numbers")
        section_ids = {section.section_id for section in doc.sections}
        for section in doc.sections:
            if section.page_start > section.page_end:
                report.errors.append(f"{doc.doc_id}/{section.section_id}: invalid page range")
            if section.parent_id and section.parent_id not in section_ids:
                report.warnings.append(
                    f"{doc.doc_id}/{section.section_id}: parent_id {section.parent_id} not found"
                )


def validate_questions(
    documents: list[Document],
    questions: list[Question],
    report: ValidationReport,
    *,
    top_k: int | None = None,
) -> None:
    doc_by_id = {doc.doc_id: doc for doc in documents}
    question_ids: set[str] = set()
    for question in questions:
        if question.question_id in question_ids:
            report.errors.append(f"duplicate question id: {question.question_id}")
        question_ids.add(question.question_id)
        if question.domain != report.domain:
            report.warnings.append(
                f"{question.question_id}: question domain {question.domain} differs from {report.domain}"
            )
        if not question.no_answer and not question.evidence:
            report.warnings.append(f"{question.question_id}: answerable question has no evidence labels")
        if top_k is not None and len(question.evidence) > top_k:
            report.warnings.append(
                f"{question.question_id}: has {len(question.evidence)} evidence labels but top_k={top_k}"
            )
        for evidence in question.evidence:
            doc = doc_by_id.get(evidence.doc_id)
            if doc is None:
                report.errors.append(
                    f"{question.question_id}: evidence references missing doc {evidence.doc_id}"
                )
                continue
            if evidence.page is not None and not any(page.page == evidence.page for page in doc.pages):
                report.errors.append(
                    f"{question.question_id}: evidence page {evidence.page} missing in {doc.doc_id}"
                )
            if evidence.section_id is not None and not any(
                section.section_id == evidence.section_id for section in doc.sections
            ):
                report.errors.append(
                    f"{question.question_id}: evidence section {evidence.section_id} missing in {doc.doc_id}"
                )
