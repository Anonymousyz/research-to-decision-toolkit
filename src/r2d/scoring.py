"""Transparent 24-point heuristic for decision briefs."""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from .schema import _nonempty, _public_url

AREA_MAX = 6
MAX_SCORE = 24
AREAS = ("Decision framing", "Evidence quality", "Artifact plan", "Feedback loop")


def _add(ok: bool, gap: str, total: int, gaps: list[str]) -> int:
    if ok:
        return total + 1
    gaps.append(gap)
    return total


def _decision_score(doc: Mapping[str, Any]) -> tuple[int, list[str]]:
    total = 0; gaps: list[str] = []
    decision = doc.get("decision")
    total = _add(_nonempty(decision), "decision question missing", total, gaps)
    total = _add(_nonempty(decision) and decision.strip().endswith("?"), "decision should be written as a question", total, gaps)
    total = _add(_nonempty(doc.get("decision_body")), "decision body missing", total, gaps)
    total = _add(_nonempty(doc.get("deadline")), "deadline or trigger missing", total, gaps)
    total = _add(_nonempty(doc.get("default_outcome")), "default outcome missing", total, gaps)
    total = _add(_nonempty(doc.get("why_now")), "why-now rationale missing", total, gaps)
    return total, gaps


def _evidence_score(doc: Mapping[str, Any]) -> tuple[int, list[str]]:
    total = 0; gaps: list[str] = []
    claims = [c for c in (doc.get("claims") or []) if isinstance(c, Mapping)]
    total = _add(len(claims) >= 5, f"only {len(claims)} structured claims; need 5+", total, gaps)
    total = _add(bool(claims) and all(_nonempty(c.get("weakest_link")) for c in claims), "some claims lack a weakest-link note", total, gaps)
    total = _add(bool(claims) and all(_nonempty(c.get("gap_that_changes_mind")) for c in claims), "some claims lack a gap-that-changes-mind", total, gaps)
    types = {c.get("type") for c in claims}
    total = _add({"fact", "judgment", "assumption"}.issubset(types), "evidence does not separate fact, judgment, and assumption", total, gaps)
    primary_urls = {c.get("source_url") for c in claims if c.get("source_tier") == "primary" and _public_url(c.get("source_url"))}
    total = _add(len(primary_urls) >= 2, f"only {len(primary_urls)} distinct primary-source URLs; need 2+", total, gaps)
    total = _add(len(doc.get("uncertainties") or []) >= 2, "fewer than 2 decision-level uncertainties", total, gaps)
    return total, gaps


def _artifact_score(doc: Mapping[str, Any]) -> tuple[int, list[str]]:
    total = 0; gaps: list[str] = []
    artifact = doc.get("artifact") if isinstance(doc.get("artifact"), Mapping) else {}
    total = _add(_nonempty(artifact.get("form")), "artifact form missing", total, gaps)
    total = _add(len(artifact.get("readers") or []) >= 3, "fewer than 3 named reader groups", total, gaps)
    total = _add(len(artifact.get("channels") or []) >= 2, "fewer than 2 distribution channels", total, gaps)
    total = _add(_nonempty(artifact.get("survives_author")), "what survives the author is unclear", total, gaps)
    total = _add(_nonempty(artifact.get("owner")), "artifact owner missing", total, gaps)
    total = _add(_nonempty(artifact.get("acceptance_criteria")), "artifact acceptance criteria missing", total, gaps)
    return total, gaps


def _feedback_score(doc: Mapping[str, Any]) -> tuple[int, list[str]]:
    total = 0; gaps: list[str] = []
    feedback = doc.get("feedback") if isinstance(doc.get("feedback"), Mapping) else {}
    total = _add(len(feedback.get("channels") or []) >= 2, "fewer than 2 feedback channels", total, gaps)
    total = _add(feedback.get("log_filled") is True, "feedback log is not yet filled", total, gaps)
    total = _add(_nonempty(feedback.get("next_move_threshold")), "next-move threshold missing", total, gaps)
    total = _add(_nonempty(feedback.get("checkin_date")), "check-in date missing", total, gaps)
    total = _add(_nonempty(feedback.get("owner")), "feedback owner missing", total, gaps)
    total = _add(_nonempty(feedback.get("review_question")), "feedback review question missing", total, gaps)
    return total, gaps


def vetoes(doc: Mapping[str, Any]) -> list[str]:
    result: list[str] = []
    if not _nonempty(doc.get("decision_body")):
        result.append("decision body not named")
    if not _nonempty(doc.get("default_outcome")):
        result.append("default outcome not stated")
    claims = doc.get("claims") or []
    if not any(_nonempty(c.get("gap_that_changes_mind")) for c in claims if isinstance(c, Mapping)):
        result.append("no gap-that-changes-mind declared")
    return result

# Backward-compatible spelling used in v0.3.
vetos = vetoes


def make_report(doc: Mapping[str, Any]) -> dict[str, Any]:
    area_results = []
    all_gaps: list[str] = []
    for name, scorer in zip(AREAS, (_decision_score, _evidence_score, _artifact_score, _feedback_score)):
        score, gaps = scorer(doc)
        area_results.append({"name": name, "score": score, "max": AREA_MAX, "gaps": gaps})
        all_gaps.extend(gaps)
    total = sum(area["score"] for area in area_results)
    veto = vetoes(doc)
    if veto:
        verdict = "Do not proceed: veto present"
    elif total >= 18:
        verdict = "Ready for decision meeting"
    elif total >= 14:
        verdict = "Revise before decision meeting"
    else:
        verdict = "Not decision-ready"
    return {
        "total": total,
        "max": MAX_SCORE,
        "normalized_pct": round(total / MAX_SCORE * 100, 1),
        "veto": veto,
        "decision": verdict,
        "top_gaps": all_gaps[:5],
        "areas": area_results,
        "method_status": "author-designed, uncalibrated decision-support heuristic",
    }
