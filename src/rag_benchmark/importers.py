from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .schemas import Document, Evidence, Page, Question, Section


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
TRUTHY = {"1", "true", "yes", "y"}


@dataclass
class ImportSummary:
    path: Path
    rows_written: int
    warnings: list[str] = field(default_factory=list)


@dataclass
class Block:
    kind: str
    text: str
    level: int | None = None
    paragraph_index: int | None = None


@dataclass
class SectionBuilder:
    section_id: str
    title: str
    page_start: int
    page_end: int
    text_parts: list[str]
    parent_id: str | None = None

    def to_section(self) -> Section:
        text = "\n\n".join(part for part in self.text_parts if part).strip() or self.title
        return Section(
            section_id=self.section_id,
            title=self.title,
            page_start=self.page_start,
            page_end=max(self.page_end, self.page_start),
            text=text,
            parent_id=self.parent_id,
        )


def import_text_documents(
    *,
    source_dir: Path,
    output_dir: Path,
    domain: str,
    page_paragraphs: int = 4,
    overwrite: bool = True,
) -> ImportSummary:
    """Convert local markdown/text documents into the benchmark document schema."""
    files = sorted(
        path
        for path in source_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".markdown", ".txt"}
    )
    output_path = output_dir / "documents.jsonl"
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"{output_path} already exists")

    warnings = []
    documents = []
    for path in files:
        try:
            documents.append(parse_text_document(path, domain=domain, page_paragraphs=page_paragraphs))
        except ValueError as exc:
            warnings.append(f"{path}: {exc}")

    output_dir.mkdir(parents=True, exist_ok=True)
    write_models_jsonl(output_path, documents)
    return ImportSummary(path=output_path, rows_written=len(documents), warnings=warnings)


def parse_text_document(path: Path, *, domain: str, page_paragraphs: int = 4) -> Document:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("empty document")

    blocks = parse_blocks(text, markdown=path.suffix.lower() in {".md", ".markdown"})
    paragraphs = [block.text for block in blocks if block.kind == "paragraph"]
    if not paragraphs:
        paragraphs = [text]
    page_paragraphs = max(1, page_paragraphs)
    pages = make_pages(paragraphs, page_paragraphs=page_paragraphs)
    sections = make_sections(
        blocks=blocks,
        fallback_title=path.stem.replace("_", " ").replace("-", " ").strip().title(),
        page_paragraphs=page_paragraphs,
    )

    doc_id = stable_doc_id(path)
    return Document(
        doc_id=doc_id,
        domain=domain,
        title=path.stem.replace("_", " ").replace("-", " ").strip().title(),
        source=str(path),
        pages=pages,
        sections=sections,
    )


def import_questions(
    *,
    source_path: Path,
    output_dir: Path,
    domain: str,
    overwrite: bool = True,
) -> ImportSummary:
    """Convert JSONL/JSON/CSV question files into the benchmark question schema."""
    output_path = output_dir / "questions.jsonl"
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"{output_path} already exists")

    rows = read_question_rows(source_path)
    warnings = []
    questions = []
    for index, row in enumerate(rows, 1):
        try:
            questions.append(normalize_question_row(row, domain=domain, row_number=index))
        except (TypeError, ValueError) as exc:
            warnings.append(f"row {index}: {exc}")

    output_dir.mkdir(parents=True, exist_ok=True)
    write_models_jsonl(output_path, questions)
    return ImportSummary(path=output_path, rows_written=len(questions), warnings=warnings)


def import_financebench(
    *,
    source_path: Path,
    output_dir: Path,
    domain: str = "finance",
    limit: int | None = None,
    overwrite: bool = True,
) -> ImportSummary:
    """Import the open-source FinanceBench JSONL/HF schema.

    This importer builds evidence-page documents from FinanceBench evidence
    fields. It is useful for retrieval/orchestration comparisons without first
    downloading and parsing the full SEC filing PDFs.
    """
    documents_path = output_dir / "documents.jsonl"
    questions_path = output_dir / "questions.jsonl"
    if (documents_path.exists() or questions_path.exists()) and not overwrite:
        raise FileExistsError(f"{output_dir} already contains benchmark files")

    rows = read_question_rows(source_path)
    if limit is not None:
        rows = rows[:limit]

    page_text_by_doc: dict[str, dict[int, str]] = {}
    meta_by_doc: dict[str, dict[str, Any]] = {}
    questions: list[Question] = []
    warnings = [
        "FinanceBench import uses evidence pages only; full-PDF ingestion is needed for a harder production retrieval test."
    ]

    for index, row in enumerate(rows, 1):
        evidence_rows = financebench_evidence_rows(row)
        evidence = []
        for evidence_row in evidence_rows:
            doc_name = str(first_present(evidence_row, "doc_name", default=first_present(row, "doc_name")))
            if not doc_name or doc_name == "None":
                warnings.append(f"row {index}: missing doc_name in evidence")
                continue
            page = parse_financebench_page(first_present(evidence_row, "evidence_page_num", default=None))
            if page is None:
                warnings.append(f"row {index}: missing evidence_page_num for {doc_name}")
                continue
            text = str(
                first_present(
                    evidence_row,
                    "evidence_text_full_page",
                    "evidence_text",
                    default=first_present(row, "evidence_text_full_page", "evidence_text", default=""),
                )
                or ""
            ).strip()
            if not text:
                warnings.append(f"row {index}: missing evidence text for {doc_name} page {page}")
                continue
            page_text_by_doc.setdefault(doc_name, {})[page] = text
            meta_by_doc[doc_name] = {
                "company": first_present(row, "company", default=""),
                "doc_type": first_present(row, "doc_type", default=""),
                "doc_period": first_present(row, "doc_period", default=""),
                "doc_link": first_present(row, "doc_link", default="financebench"),
            }
            evidence.append(Evidence(doc_id=doc_name, page=page, section_id=f"page_{page}"))

        question_text = first_present(row, "question", "question_text", "query")
        answer = first_present(row, "answer", "answer_text", "gold_answer", default="")
        if not question_text or not answer:
            warnings.append(f"row {index}: skipped because question or answer is missing")
            continue

        questions.append(
            Question(
                question_id=str(first_present(row, "financebench_id", "question_id", "id", default=f"fb_{index:04d}")),
                domain=domain,
                category=financebench_category(row),
                question=str(question_text),
                answer=str(answer),
                answer_aliases=parse_financebench_aliases(str(answer)),
                evidence=evidence,
                notes=str(first_present(row, "justification", "notes", default="") or ""),
            )
        )

    documents = []
    for doc_id, pages_by_number in sorted(page_text_by_doc.items()):
        pages = [Page(page=page, text=text) for page, text in sorted(pages_by_number.items())]
        sections = [
            Section(
                section_id=f"page_{page.page}",
                title=f"{doc_id} evidence page {page.page}",
                page_start=page.page,
                page_end=page.page,
                text=page.text,
            )
            for page in pages
        ]
        meta = meta_by_doc.get(doc_id, {})
        documents.append(
            Document(
                doc_id=doc_id,
                domain=domain,
                title=f"{doc_id} {meta.get('doc_type', '')}".strip(),
                source=str(meta.get("doc_link") or source_path),
                pages=pages,
                sections=sections,
            )
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    write_models_jsonl(documents_path, documents)
    write_models_jsonl(questions_path, questions)
    return ImportSummary(path=output_dir, rows_written=len(questions), warnings=warnings)


def parse_blocks(text: str, *, markdown: bool) -> list[Block]:
    blocks: list[Block] = []
    paragraph_lines: list[str] = []
    paragraph_index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph_index
        if not paragraph_lines:
            return
        paragraph = "\n".join(paragraph_lines).strip()
        paragraph_lines.clear()
        if paragraph:
            paragraph_index += 1
            blocks.append(Block(kind="paragraph", text=paragraph, paragraph_index=paragraph_index))

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        heading = HEADING_RE.match(line) if markdown else None
        if heading:
            flush_paragraph()
            blocks.append(
                Block(kind="heading", text=heading.group(2).strip(), level=len(heading.group(1)))
            )
            continue
        if not line.strip():
            flush_paragraph()
            continue
        paragraph_lines.append(line)
    flush_paragraph()
    return blocks


def make_pages(paragraphs: list[str], *, page_paragraphs: int) -> list[Page]:
    pages = []
    for index in range(0, len(paragraphs), page_paragraphs):
        page_number = len(pages) + 1
        pages.append(Page(page=page_number, text="\n\n".join(paragraphs[index : index + page_paragraphs])))
    return pages or [Page(page=1, text="")]


def make_sections(
    *,
    blocks: list[Block],
    fallback_title: str,
    page_paragraphs: int,
) -> list[Section]:
    has_headings = any(block.kind == "heading" for block in blocks)
    if not has_headings:
        paragraphs = [block.text for block in blocks if block.kind == "paragraph"]
        text = "\n\n".join(paragraphs).strip()
        page_end = max(1, (len(paragraphs) + page_paragraphs - 1) // page_paragraphs)
        return [
            Section(
                section_id="body",
                title=fallback_title or "Document",
                page_start=1,
                page_end=page_end,
                text=text,
            )
        ]

    sections: list[Section] = []
    current: SectionBuilder | None = None
    heading_stack: list[tuple[int, str]] = []
    used_ids: set[str] = set()

    def close_current() -> None:
        nonlocal current
        if current is None:
            return
        sections.append(current.to_section())
        current = None

    for block in blocks:
        if block.kind == "heading":
            close_current()
            assert block.level is not None
            while heading_stack and heading_stack[-1][0] >= block.level:
                heading_stack.pop()
            parent_id = heading_stack[-1][1] if heading_stack else None
            section_id = unique_slug(block.text, used_ids)
            heading_stack.append((block.level, section_id))
            current = SectionBuilder(
                section_id=section_id,
                title=block.text,
                page_start=1,
                page_end=1,
                text_parts=[block.text],
                parent_id=parent_id,
            )
            continue

        page = paragraph_page(block.paragraph_index or 1, page_paragraphs=page_paragraphs)
        if current is None:
            section_id = unique_slug(fallback_title or "Document", used_ids)
            current = SectionBuilder(
                section_id=section_id,
                title=fallback_title or "Document",
                page_start=page,
                page_end=page,
                text_parts=[],
            )
        if current.text_parts == [current.title] and current.page_start == current.page_end == 1:
            current.page_start = page
            current.page_end = page
        else:
            current.page_start = min(current.page_start, page)
            current.page_end = max(current.page_end, page)
        current.text_parts.append(block.text)
    close_current()
    return sections


def paragraph_page(paragraph_index: int, *, page_paragraphs: int) -> int:
    return max(1, (paragraph_index - 1) // page_paragraphs + 1)


def read_question_rows(source_path: Path) -> list[dict[str, Any]]:
    suffix = source_path.suffix.lower()
    if suffix == ".jsonl":
        rows = []
        with source_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows
    if suffix == ".json":
        data = json.loads(source_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ("questions", "data", "rows"):
                if isinstance(data.get(key), list):
                    return data[key]
        raise ValueError("JSON must be a list or contain questions/data/rows")
    if suffix == ".csv":
        with source_path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    raise ValueError("questions must be .jsonl, .json, or .csv")


def normalize_question_row(row: dict[str, Any], *, domain: str, row_number: int) -> Question:
    question_text = first_present(row, "question", "question_text", "query")
    answer = first_present(row, "answer", "answer_text", "gold_answer", default="")
    category = first_present(row, "category", "type", default="direct_lookup")
    question_id = first_present(row, "question_id", "id", default="")
    no_answer = parse_bool(first_present(row, "no_answer", "unanswerable", default=False))

    if not question_text:
        raise ValueError("missing question")
    if not no_answer and not answer:
        raise ValueError("missing answer")

    if not question_id:
        question_id = f"{slugify(str(category))}_{row_number:04d}_{short_hash(str(question_text))}"

    aliases = parse_aliases(first_present(row, "answer_aliases", "aliases", default=[]))
    evidence = parse_evidence(first_present(row, "evidence", "evidence_json", "references", default=[]))

    return Question(
        question_id=str(question_id),
        domain=str(first_present(row, "domain", default=domain) or domain),
        category=str(category),
        question=str(question_text),
        answer=str(answer),
        answer_aliases=aliases,
        evidence=evidence,
        no_answer=no_answer,
        notes=str(first_present(row, "notes", "rationale", default="") or ""),
    )


def parse_aliases(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return [item.strip() for item in value.split("|") if item.strip()]
        return parse_aliases(parsed)
    return [str(value)]


def parse_evidence(value: Any) -> list[Evidence]:
    if value is None or value == "":
        return []
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            parts = [part.strip() for part in value.split("|") if part.strip()]
            rows = []
            for part in parts:
                doc_id, _, page = part.partition(":")
                rows.append({"doc_id": doc_id, "page": int(page) if page.isdigit() else None})
            value = rows
    if isinstance(value, dict):
        value = [value]
    if not isinstance(value, list):
        raise ValueError("evidence must be a list, object, JSON string, or doc_id:page string")
    return [Evidence.model_validate(item) for item in value]


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in TRUTHY


def financebench_evidence_rows(row: dict[str, Any]) -> list[dict[str, Any]]:
    evidence = row.get("evidence")
    if isinstance(evidence, str):
        try:
            evidence = json.loads(evidence)
        except json.JSONDecodeError:
            evidence = None
    if isinstance(evidence, dict):
        return [evidence]
    if isinstance(evidence, list):
        return [item for item in evidence if isinstance(item, dict)]
    return [
        {
            "doc_name": first_present(row, "doc_name", default=""),
            "evidence_page_num": first_present(row, "evidence_page_num", default=None),
            "evidence_text_full_page": first_present(row, "evidence_text_full_page", "evidence_text", default=""),
        }
    ]


def parse_financebench_page(value: Any) -> int | None:
    try:
        return int(value) + 1
    except (TypeError, ValueError):
        return None


def financebench_category(row: dict[str, Any]) -> str:
    reasoning = (
        f"{first_present(row, 'question_reasoning', default='')} "
        f"{first_present(row, 'question_type', default='')}"
    ).lower()
    if "calculation" in reasoning or "numerical" in reasoning:
        return "calculation"
    if "metric" in reasoning or "table" in reasoning:
        return "table_numeric"
    if "comparison" in reasoning:
        return "multi_section"
    if "extraction" in reasoning:
        return "direct_lookup"
    return "section_navigation"


def parse_financebench_aliases(answer: str) -> list[str]:
    aliases = {answer}
    compact = answer.replace(",", "")
    aliases.add(compact)
    if compact.startswith("$"):
        aliases.add(compact[1:])
    return sorted(alias for alias in aliases if alias and alias != answer)


def first_present(row: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return default


def stable_doc_id(path: Path) -> str:
    return f"{slugify(path.stem)}_{short_hash(str(path.resolve()))}"


def unique_slug(text: str, used: set[str]) -> str:
    base = slugify(text) or "section"
    candidate = base
    counter = 2
    while candidate in used:
        candidate = f"{base}_{counter}"
        counter += 1
    used.add(candidate)
    return candidate


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower()).strip("_")
    return slug[:80]


def short_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


def write_models_jsonl(path: Path, rows: list[Document] | list[Question]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row.model_dump(mode="json"), ensure_ascii=False) + "\n")
