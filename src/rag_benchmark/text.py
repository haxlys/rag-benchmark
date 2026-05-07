from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable

TOKEN_RE = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9.$%_-]*")

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}

SEMANTIC_ALIASES = {
    "cash": "liquidity",
    "money": "liquidity",
    "debt": "debt",
    "borrowings": "debt",
    "growth": "increase",
    "grew": "increase",
    "increase": "increase",
    "retention": "retention",
    "keep": "retention",
    "stored": "retention",
    "delete": "deletion",
    "deletion": "deletion",
    "remove": "deletion",
    "incident": "incident",
    "outage": "incident",
    "recovery": "recovery",
    "rto": "recovery",
    "rpo": "recovery",
    "limit": "rate_limit",
    "quota": "rate_limit",
    "throttle": "rate_limit",
    "ebitda": "ebitda",
    "adjusted": "adjusted",
    "restructuring": "restructuring",
    "revenue": "revenue",
    "sales": "revenue",
    "assets": "assets",
    "income": "income",
    "profit": "income",
    "roa": "return_on_assets",
    "return": "return",
    "api": "api",
    "backup": "backup",
    "backups": "backup",
    "refund": "refund",
    "sla": "sla",
    "enterprise": "enterprise",
}


def tokenize(text: str, *, semantic: bool = False, keep_stopwords: bool = False) -> list[str]:
    tokens = [match.group(0).lower().strip("._-") for match in TOKEN_RE.finditer(text)]
    cleaned = []
    for token in tokens:
        if not token:
            continue
        if not keep_stopwords and token in STOPWORDS:
            continue
        if semantic:
            token = SEMANTIC_ALIASES.get(token, token)
        cleaned.append(token)
    return cleaned


def token_count(text: str) -> int:
    return len(tokenize(text, keep_stopwords=True))


def counter_cosine(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    numerator = sum(a[token] * b.get(token, 0.0) for token in a)
    a_norm = math.sqrt(sum(value * value for value in a.values()))
    b_norm = math.sqrt(sum(value * value for value in b.values()))
    if a_norm == 0 or b_norm == 0:
        return 0.0
    return numerator / (a_norm * b_norm)


def weighted_counter(tokens: Iterable[str], idf: dict[str, float] | None = None) -> Counter[str]:
    counts = Counter(tokens)
    if not idf:
        return counts
    return Counter({token: count * idf.get(token, 1.0) for token, count in counts.items()})


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]

