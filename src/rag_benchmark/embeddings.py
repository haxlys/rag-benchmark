from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from .text import tokenize


@dataclass(frozen=True)
class EmbeddingProfile:
    model_id: str
    model_ref: str
    family: str
    dimension: int
    lexical_weight: float
    semantic_weight: float
    title_weight: float
    finance_weight: float
    numeric_weight: float
    cost_per_token: float
    notes: str


FINANCE_CONCEPTS = {
    "assets",
    "backlog",
    "capital_expenditure",
    "cash",
    "contract_liability",
    "debt",
    "debt_covenant",
    "ebitda",
    "income",
    "liability",
    "liquidity",
    "margin_bridge",
    "restructuring",
    "return_on_assets",
    "revenue",
}

NUMERIC_RE = re.compile(r"\$[0-9,.]+|\b\d+(?:\.\d+)?%?")

PROFILES: dict[str, EmbeddingProfile] = {
    "none": EmbeddingProfile(
        model_id="none",
        model_ref="none",
        family="not-applicable",
        dimension=0,
        lexical_weight=0.0,
        semantic_weight=0.0,
        title_weight=0.0,
        finance_weight=0.0,
        numeric_weight=0.0,
        cost_per_token=0.0,
        notes="No embedding model is used by this retrieval method.",
    ),
    "e5-large-v2-proxy": EmbeddingProfile(
        model_id="e5-large-v2-proxy",
        model_ref="intfloat/e5-large-v2",
        family="general_dense",
        dimension=1024,
        lexical_weight=0.35,
        semantic_weight=1.0,
        title_weight=0.20,
        finance_weight=0.10,
        numeric_weight=0.15,
        cost_per_token=0.000000015,
        notes="Deterministic local proxy for a general E5-style embedding model.",
    ),
    "bge-m3-proxy": EmbeddingProfile(
        model_id="bge-m3-proxy",
        model_ref="BAAI/bge-m3",
        family="hybrid_multifunction",
        dimension=1024,
        lexical_weight=0.70,
        semantic_weight=0.95,
        title_weight=0.35,
        finance_weight=0.18,
        numeric_weight=0.25,
        cost_per_token=0.000000018,
        notes="Deterministic local proxy for a BGE-M3-style dense+sparse retrieval model.",
    ),
    "finance-e5-proxy": EmbeddingProfile(
        model_id="finance-e5-proxy",
        model_ref="FinanceMTEB/Fin-e5-tokenizer",
        family="finance_domain_dense",
        dimension=1024,
        lexical_weight=0.45,
        semantic_weight=1.05,
        title_weight=0.30,
        finance_weight=0.75,
        numeric_weight=0.40,
        cost_per_token=0.000000018,
        notes="Deterministic local proxy for a finance-adapted E5-style embedding model.",
    ),
}


def profile_for(model_id: str | None) -> EmbeddingProfile:
    if not model_id:
        return PROFILES["none"]
    try:
        return PROFILES[model_id]
    except KeyError as exc:
        raise ValueError(f"Unknown embedding model: {model_id}") from exc


def embedding_counter(
    text: str,
    model_id: str,
    *,
    title: str | None = None,
) -> Counter[str]:
    profile = profile_for(model_id)
    if profile.model_id == "none":
        return Counter()

    counter: Counter[str] = Counter()
    add_tokens(counter, tokenize(text), profile.lexical_weight)
    semantic_tokens = tokenize(text, semantic=True)
    add_tokens(counter, semantic_tokens, profile.semantic_weight)
    add_tokens(counter, numeric_tokens(text), profile.numeric_weight)

    if profile.finance_weight:
        finance_tokens = [
            token
            for token in semantic_tokens
            if token in FINANCE_CONCEPTS or token.replace("finance:", "") in FINANCE_CONCEPTS
        ]
        add_tokens(counter, finance_tokens, profile.finance_weight)

    if title and profile.title_weight:
        add_tokens(counter, tokenize(title, semantic=True), profile.title_weight)

    return counter


def add_tokens(counter: Counter[str], tokens: list[str], weight: float) -> None:
    if weight <= 0:
        return
    for token in tokens:
        counter[token] += weight


def numeric_tokens(text: str) -> list[str]:
    tokens = []
    for match in NUMERIC_RE.finditer(text):
        raw = match.group(0).lower().replace(",", "")
        if raw.startswith("$"):
            tokens.append("currency_amount")
        elif raw.endswith("%"):
            tokens.append("percentage")
        else:
            tokens.append("number")
    return tokens


def apply_idf(counter: Counter[str], idf: dict[str, float]) -> Counter[str]:
    return Counter({token: value * idf.get(token, 1.0) for token, value in counter.items()})


def embedding_query_cost(model_id: str, tokens: int) -> float:
    return profile_for(model_id).cost_per_token * tokens
