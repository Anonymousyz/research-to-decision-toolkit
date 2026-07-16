from __future__ import annotations

from datetime import date
from ipaddress import ip_address
import re
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
REVIEW_METHODS = {"human", "human-with-ai-assistance"}
WRITING_PASS_ORDER = ["judgment", "evidence", "structure", "clarity", "delivery"]
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


def _parse_legacy_ipv4(host: str):
    """Parse inet-style numeric IPv4 spellings so they can be rejected."""
    parts = host.split(".")
    if not 1 <= len(parts) <= 4:
        return None
    values = []
    for part in parts:
        if not part or re.fullmatch(r"(?:0[xX][0-9a-fA-F]+|[0-9]+)", part) is None:
            return None
        try:
            if part.lower().startswith("0x"):
                value = int(part, 16)
            elif len(part) > 1 and part.startswith("0"):
                value = int(part, 8)
            else:
                value = int(part, 10)
        except ValueError:
            return None
        values.append(value)
    limits = {
        1: (0xFFFFFFFF,),
        2: (0xFF, 0xFFFFFF),
        3: (0xFF, 0xFF, 0xFFFF),
        4: (0xFF, 0xFF, 0xFF, 0xFF),
    }[len(values)]
    if any(value > limit for value, limit in zip(values, limits)):
        return None
    if len(values) == 1:
        packed = values[0]
    elif len(values) == 2:
        packed = (values[0] << 24) | values[1]
    elif len(values) == 3:
        packed = (values[0] << 24) | (values[1] << 16) | values[2]
    else:
        packed = (values[0] << 24) | (values[1] << 16) | (values[2] << 8) | values[3]
    return ip_address(packed)


def _valid_url(value: Any) -> bool:
    if not _nonempty(value):
        return False
    parsed = urlparse(value)
    try:
        parsed.port
    except ValueError:
        return False
    return (
        parsed.scheme in {"http", "https"}
        and bool(parsed.hostname)
        and parsed.username is None
        and parsed.password is None
    )


def _reserved_or_local_url(value: str) -> bool:
    host = (urlparse(value).hostname or "").lower().rstrip(".")
    try:
        address = ip_address(host)
    except ValueError:
        address = None
    if address is None and _parse_legacy_ipv4(host) is not None:
        return True
    if address is not None:
        return not address.is_global
    return (
        host in RESERVED_HOSTS
        or any(host.endswith(f".{reserved}") for reserved in RESERVED_HOSTS)
        or host.endswith(".example")
        or host.endswith(".invalid")
        or host.endswith(".test")
        or host.endswith(".localhost")
        or host.endswith(".local")
    )


def _valid_date(value: Any) -> bool:
    if not _nonempty(value) or re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is None:
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


def _validate_review_metadata(value: dict, prefix: str, errors: list[str]) -> None:
    if not _nonempty(value.get("reviewed_by")):
        errors.append(f"{prefix}.reviewed_by must name the accountable human")
    if not _valid_date(value.get("reviewed_at")):
        errors.append(f"{prefix}.reviewed_at must be an ISO date")
    if value.get("review_method") not in REVIEW_METHODS:
        errors.append(f"{prefix}.review_method must be one of {sorted(REVIEW_METHODS)}")


def _validate_argument_quality(value: Any, errors: list[str]) -> None:
    prefix = "argument_quality"
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object")
        return
    _validate_review_metadata(value, prefix, errors)
    gates = value.get("gates")
    if not isinstance(gates, dict):
        errors.append(f"{prefix}.gates must be an object")
    else:
        for name in ("concept", "evidence", "action"):
            if not _nonempty(gates.get(name)):
                errors.append(f"{prefix}.gates.{name} must be a non-empty string")
    chain = value.get("chain")
    if not isinstance(chain, list) or not chain:
        errors.append(f"{prefix}.chain must be a non-empty list")
        return
    for index, item in enumerate(chain):
        item_prefix = f"{prefix}.chain[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_prefix} must be an object")
            continue
        for key in ("claim", "evidence", "inference", "action", "boundary", "counterevidence"):
            if not _nonempty(item.get(key)):
                errors.append(f"{item_prefix}.{key} must be a non-empty string")


def _validate_writing_review(value: Any, errors: list[str]) -> None:
    prefix = "writing_review"
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object")
        return
    _validate_review_metadata(value, prefix, errors)
    if value.get("path") not in {"A", "B"}:
        errors.append(f"{prefix}.path must be 'A' or 'B'")
    passes = value.get("passes")
    if not isinstance(passes, list) or len(passes) != len(WRITING_PASS_ORDER):
        errors.append(f"{prefix}.passes must contain exactly five ordered passes")
        return
    names = [item.get("name") if isinstance(item, dict) else None for item in passes]
    if names != WRITING_PASS_ORDER:
        errors.append(f"{prefix}.passes must use this order: {WRITING_PASS_ORDER}")
    for index, item in enumerate(passes):
        item_prefix = f"{prefix}.passes[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_prefix} must be an object")
            continue
        for key in ("finding", "revision"):
            if not _nonempty(item.get(key)):
                errors.append(f"{item_prefix}.{key} must be a non-empty string")


def validate(doc: Any) -> tuple[bool, list[str], list[str]]:
    errors: list[str] = []
    vetoes: list[str] = []
    if not isinstance(doc, dict):
        return False, ["document must be a JSON object"], []

    for key in REQUIRED_TOP:
        if key not in doc:
            errors.append(f"missing required field: {key}")

    if "schema_version" in doc:
        version = doc["schema_version"]
        if version != "0.6":
            errors.append("schema_version must be '0.6' when provided")
    else:
        version = None

    if version == "0.6":
        for key in ("argument_quality", "writing_review"):
            if key not in doc:
                errors.append(f"missing required field for schema 0.6: {key}")
        if "argument_quality" in doc:
            _validate_argument_quality(doc["argument_quality"], errors)
        if "writing_review" in doc:
            _validate_writing_review(doc["writing_review"], errors)

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
