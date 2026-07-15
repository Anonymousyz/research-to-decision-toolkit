from __future__ import annotations

from datetime import date
from typing import Any
from urllib.parse import urlparse

REQUIRED_TOP = [
    "decision",
    "decision_body",
    "default_outcome",
    "deadline",
    "claims",
    "uncertainties",
    "artifact",
    "feedback",
    "decision_review",
]
SOURCE_TIERS = {"primary", "secondary", "internal", "synthetic"}
CLAIM_TYPES = {"fact", "judgment", "assumption", "recommendation"}
RESERVED_HOSTS = {"example.com", "example.org", "example.net", "localhost"}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string(value: Any) -> bool:
    return isinstance(value, str)


def _list_of_nonempty_strings(value: Any, minimum: int = 0) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= minimum
        and all(_nonempty(item) for item in value)
    )


def _valid_url(value: Any) -> bool:
    if not _nonempty(value):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _reserved_or_local_url(value: str) -> bool:
    host = (urlparse(value).hostname or "").lower()
    return (
        host in RESERVED_HOSTS
        or host.endswith(".example")
        or host.endswith(".invalid")
        or host.endswith(".test")
        or host.endswith(".localhost")
        or host.startswith("127.")
        or host == "::1"
    )


def _valid_date(value: Any) -> bool:
    if not _nonempty(value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def _validate_claim(claim: Any, index: int, errors: list[str]) -> None:
    prefix = f"claims[{index}]"
    if not isinstance(claim, dict):
        errors.append(f"{prefix} must be an object")
        return
    for key in ("claim", "source", "weakest_link"):
        if not _nonempty(claim.get(key)):
            errors.append(f"{prefix}.{key} must be a non-empty string")
    if claim.get("type") not in CLAIM_TYPES:
        errors.append(f"{prefix}.type must be one of {sorted(CLAIM_TYPES)}")
    if not _string(claim.get("gap_that_changes_mind")):
        errors.append(f"{prefix}.gap_that_changes_mind must be a string")

    tier = claim.get("source_tier")
    if tier not in SOURCE_TIERS:
        errors.append(f"{prefix}.source_tier must be one of {sorted(SOURCE_TIERS)}")

    source_url = claim.get("source_url")
    if source_url not in (None, "") and not _valid_url(source_url):
        errors.append(f"{prefix}.source_url must be an http(s) URL when provided")
    if tier in {"primary", "secondary"}:
        if not _valid_url(source_url):
            errors.append(f"{prefix}.source_url is required for {tier} sources")
        elif _reserved_or_local_url(source_url):
            errors.append(f"{prefix}.source_url uses a reserved or local domain")
        if not _nonempty(claim.get("source_checked_by")):
            errors.append(f"{prefix}.source_checked_by must name the human checker")
        if claim.get("source_check_method") != "human":
            errors.append(f"{prefix}.source_check_method must be 'human'")
        if not _valid_date(claim.get("source_checked_at")):
            errors.append(f"{prefix}.source_checked_at must be an ISO date")


def validate(doc: Any) -> tuple[bool, list[str], list[str]]:
    errors: list[str] = []
    vetoes: list[str] = []
    if not isinstance(doc, dict):
        return False, ["document must be a JSON object"], []

    for key in REQUIRED_TOP:
        if key not in doc:
            errors.append(f"missing required field: {key}")

    if "decision" in doc and not _nonempty(doc.get("decision")):
        errors.append("decision must be a non-empty string")
    for key in ("decision_body", "default_outcome"):
        if key in doc and not _string(doc.get(key)):
            errors.append(f"{key} must be a string")
    if "deadline" in doc and not _nonempty(doc.get("deadline")):
        errors.append("deadline must be a non-empty string")

    claims = doc.get("claims")
    if not isinstance(claims, list):
        errors.append("claims must be a list")
        claims = []
    else:
        for i, claim in enumerate(claims):
            _validate_claim(claim, i, errors)

    uncertainties = doc.get("uncertainties")
    if not _list_of_nonempty_strings(uncertainties):
        errors.append("uncertainties must be a list of non-empty strings")

    artifact = doc.get("artifact")
    if not isinstance(artifact, dict):
        errors.append("artifact must be an object")
    else:
        for key in ("form", "survives_author", "owner", "acceptance_criteria"):
            if not _nonempty(artifact.get(key)):
                errors.append(f"artifact.{key} must be a non-empty string")
        if not _list_of_nonempty_strings(artifact.get("readers"), minimum=1):
            errors.append("artifact.readers must be a list of non-empty strings")
        if not _list_of_nonempty_strings(artifact.get("channels"), minimum=1):
            errors.append("artifact.channels must be a list of non-empty strings")

    feedback = doc.get("feedback")
    if not isinstance(feedback, dict):
        errors.append("feedback must be an object")
    else:
        if not _list_of_nonempty_strings(feedback.get("channels"), minimum=1):
            errors.append("feedback.channels must be a list of non-empty strings")
        if not isinstance(feedback.get("log_filled"), bool):
            errors.append("feedback.log_filled must be boolean")
        for key in ("next_move_threshold", "checkin_date", "owner", "review_question"):
            if not _nonempty(feedback.get(key)):
                errors.append(f"feedback.{key} must be a non-empty string")

    review = doc.get("decision_review")
    if not isinstance(review, dict):
        errors.append("decision_review must be an object")
    else:
        for key in ("alternatives", "decision_criteria", "affected_stakeholders"):
            if not _list_of_nonempty_strings(review.get(key), minimum=2):
                errors.append(f"decision_review.{key} must be a list with at least 2 non-empty strings")
        for key in ("reversibility", "key_cost_or_tradeoff", "premortem_failure"):
            if not _nonempty(review.get(key)):
                errors.append(f"decision_review.{key} must be a non-empty string")

    if _string(doc.get("decision_body")) and not doc["decision_body"].strip():
        vetoes.append("decision_body is empty")
    if _string(doc.get("default_outcome")) and not doc["default_outcome"].strip():
        vetoes.append("default_outcome is empty")
    if claims and all(
        isinstance(claim, dict)
        and _string(claim.get("gap_that_changes_mind"))
        and not claim["gap_that_changes_mind"].strip()
        for claim in claims
    ):
        vetoes.append("no claim states what evidence would change the conclusion")

    return not errors and not vetoes, errors, vetoes
