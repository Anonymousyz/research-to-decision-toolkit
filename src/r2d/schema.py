"""Validation for decision-brief JSON documents."""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlparse

REQUIRED = ["decision", "decision_body", "deadline", "default_outcome", "claims", "artifact", "feedback"]
CLAIM_TYPES = {"fact", "judgment", "assumption"}
SOURCE_TIERS = {"primary", "secondary", "internal", "synthetic"}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _public_url(value: Any) -> bool:
    if not _nonempty(value):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate(doc: Any) -> tuple[bool, list[str], list[str]]:
    errors: list[str] = []
    vetoes: list[str] = []
    if not isinstance(doc, Mapping):
        return False, ["document must be a JSON object"], ["decision brief is not structurally reviewable"]

    for key in REQUIRED:
        if key not in doc:
            errors.append(f"missing required field: {key}")
    for key in ("decision", "decision_body", "deadline", "default_outcome"):
        if key in doc and not _nonempty(doc[key]):
            errors.append(f"{key} must be a non-empty string")

    claims = doc.get("claims")
    if not isinstance(claims, list):
        errors.append("claims must be a list")
        claims = []
    elif len(claims) < 5:
        errors.append("need at least 5 claims for this heuristic scorecard")
    for index, claim in enumerate(claims):
        if not isinstance(claim, Mapping):
            errors.append(f"claims[{index}] must be an object")
            continue
        for field in ("claim", "source", "weakest_link", "gap_that_changes_mind"):
            if not _nonempty(claim.get(field)):
                errors.append(f"claims[{index}].{field} must be a non-empty string")
        if claim.get("type") not in CLAIM_TYPES:
            errors.append(f"claims[{index}].type must be one of: {', '.join(sorted(CLAIM_TYPES))}")
        if claim.get("source_tier") not in SOURCE_TIERS:
            errors.append(f"claims[{index}].source_tier must be one of: {', '.join(sorted(SOURCE_TIERS))}")
        if claim.get("source_url") and not _public_url(claim["source_url"]):
            errors.append(f"claims[{index}].source_url must be an http(s) URL")

    for field in ("artifact", "feedback"):
        if field in doc and not isinstance(doc[field], Mapping):
            errors.append(f"{field} must be an object")

    if not _nonempty(doc.get("decision_body")):
        vetoes.append("decision_body must be named")
    if not _nonempty(doc.get("default_outcome")):
        vetoes.append("default_outcome must be stated")
    if not any(_nonempty(c.get("gap_that_changes_mind")) for c in claims if isinstance(c, Mapping)):
        vetoes.append("no gap-that-changes-mind declared in claims")

    return not errors and not vetoes, errors, vetoes
