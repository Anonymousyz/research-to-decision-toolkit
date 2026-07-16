from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from urllib.parse import urlparse

from .schema import validate


def vetoes(doc: dict) -> list[str]:
    """Return structural vetoes without treating them as schema errors."""
    return validate(doc)[2]


@dataclass(frozen=True)
class AreaScore:
    name: str
    score: int
    max: int
    gaps: list[str]


def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _decision_score(doc: dict) -> AreaScore:
    gaps: list[str] = []
    checks = [
        (_nonempty(doc.get("decision")), "decision is missing"),
        (_nonempty(doc.get("decision_body")), "decision body is missing"),
        (_nonempty(doc.get("default_outcome")), "default outcome is missing"),
        (_nonempty(doc.get("deadline")), "deadline is missing"),
        (len(doc.get("claims", [])) >= 3, "fewer than 3 claims"),
        (len(doc.get("uncertainties", [])) >= 3, "fewer than 3 uncertainties"),
    ]
    for ok, gap in checks:
        if not ok:
            gaps.append(gap)
    return AreaScore("Decision framing", sum(ok for ok, _ in checks), 6, gaps)


def _is_verified_primary(claim: dict) -> bool:
    if claim.get("source_tier") != "primary":
        return False
    url = claim.get("source_url")
    if not _nonempty(url):
        return False
    host = (urlparse(url).hostname or "").lower()
    reserved = host in {"example.com", "example.org", "example.net", "localhost"}
    return (
        not reserved
        and claim.get("source_check_method") == "human"
        and _nonempty(claim.get("source_checked_by"))
        and _nonempty(claim.get("source_checked_at"))
    )


def _source_identity(url: str) -> tuple[str, str, int | None, str, str]:
    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower().rstrip(".")
    try:
        port = parsed.port
    except ValueError:
        port = None
    if (scheme, port) in {("http", 80), ("https", 443)}:
        port = None
    path = parsed.path.rstrip("/") or "/"
    return scheme, host, port, path, parsed.query


def _evidence_score(doc: dict) -> AreaScore:
    claims = doc.get("claims", [])
    uncertainties = doc.get("uncertainties", [])
    verified_primary_urls = {
        _source_identity(claim.get("source_url"))
        for claim in claims
        if isinstance(claim, dict) and _is_verified_primary(claim)
    }
    checks = [
        (len(claims) >= 3, "fewer than 3 claims"),
        (len(verified_primary_urls) >= 2, f"only {len(verified_primary_urls)} distinct human-checked primary-source URLs; need 2+"),
        (bool(claims) and all(_nonempty(claim.get("weakest_link")) for claim in claims), "weakest link not named for every claim"),
        (len(uncertainties) >= 3, "fewer than 3 uncertainties"),
        (_nonempty(doc.get("boundaries")) and _nonempty(doc.get("out_of_scope")), "boundaries or out-of-scope note is missing"),
        (bool(claims) and all(_nonempty(claim.get("gap_that_changes_mind")) for claim in claims), "not every claim states what evidence would change the conclusion"),
    ]
    return AreaScore("Evidence quality", sum(ok for ok, _ in checks), 6, [gap for ok, gap in checks if not ok])


def _review_score(doc: dict) -> AreaScore:
    review = doc.get("decision_review", {})
    checks = [
        (isinstance(review.get("alternatives"), list) and len(review["alternatives"]) >= 2, "fewer than 2 alternatives"),
        (isinstance(review.get("decision_criteria"), list) and len(review["decision_criteria"]) >= 2, "fewer than 2 decision criteria"),
        (isinstance(review.get("affected_stakeholders"), list) and len(review["affected_stakeholders"]) >= 2, "fewer than 2 affected stakeholder groups"),
        (_nonempty(review.get("reversibility")), "reversibility is missing"),
        (_nonempty(review.get("key_cost_or_tradeoff")), "key cost or trade-off is missing"),
        (_nonempty(review.get("premortem_failure")), "pre-mortem failure is missing"),
    ]
    return AreaScore("Decision review", sum(ok for ok, _ in checks), 6, [gap for ok, gap in checks if not ok])


def _artifact_feedback_score(doc: dict) -> AreaScore:
    artifact = doc.get("artifact", {})
    feedback = doc.get("feedback", {})
    checks = [
        (_nonempty(artifact.get("form")), "artifact form is missing"),
        (_nonempty(artifact.get("acceptance_criteria")), "artifact acceptance criteria are missing"),
        (_nonempty(artifact.get("owner")), "artifact owner is missing"),
        (isinstance(feedback.get("channels"), list) and bool(feedback["channels"]), "feedback channels are missing"),
        (_nonempty(feedback.get("owner")), "feedback owner is missing"),
        (feedback.get("log_filled") is True, "feedback log is not yet filled"),
    ]
    return AreaScore("Artifact and feedback", sum(ok for ok, _ in checks), 6, [gap for ok, gap in checks if not ok])


def make_report(doc: dict) -> dict:
    _, errors, vetoes = validate(doc)
    if errors:
        raise ValueError("Invalid decision brief: " + "; ".join(errors))
    areas = [
        _decision_score(doc),
        _evidence_score(doc),
        _review_score(doc),
        _artifact_feedback_score(doc),
    ]
    total = sum(area.score for area in areas)
    maximum = sum(area.max for area in areas)
    if vetoes:
        verdict = "Not ready for human decision meeting: veto present"
    elif total >= 18:
        verdict = "Structurally ready for human decision meeting"
    else:
        verdict = "Revise before human decision meeting"
    return {
        "decision": verdict,
        "total": total,
        "max": maximum,
        "maximum": maximum,
        "normalized_pct": round(total / maximum * 100, 1),
        "veto": bool(vetoes),
        "veto_items": vetoes,
        "areas": [asdict(area) for area in areas],
        "top_gaps": [gap for area in areas for gap in area.gaps][:8],
        "method_boundary": "Author-designed, uncalibrated decision-support heuristic for structural workflow completeness; source checks are human declarations and URLs are not fetched or substantively verified by the CLI.",
    }


def render_markdown(doc: dict, report: dict) -> str:
    lines = [
        f"# Decision packet: {doc['decision']}",
        "",
        f"- **Decision:** {report['decision']}",
        f"- **Total:** {report['total']}/{report['max']} ({report['normalized_pct']}%)",
        f"- **Veto:** {'yes' if report['veto'] else 'no'}",
        "",
        "## Area scores",
        "",
        "| Area | Score | Max | Gaps |",
        "|---|---:|---:|---|",
    ]
    for area in report["areas"]:
        gaps = "; ".join(area["gaps"]) or "none"
        lines.append(f"| {area['name']} | {area['score']} | {area['max']} | {gaps} |")
    lines += ["", "## Veto items", ""]
    lines += [f"- {item}" for item in report["veto_items"]] or ["- None"]
    lines += ["", "## Top gaps", ""]
    lines += [f"- {item}" for item in report["top_gaps"]] or ["- None"]
    lines += ["", "## Claims and source-check declarations", ""]
    for claim in doc["claims"]:
        source = claim.get("source_url") or claim.get("source")
        lines += [
            f"### {claim['claim']}",
            f"- Source: {source}",
            f"- Source tier: {claim.get('source_tier', 'not declared')}",
            f"- Human checker: {claim.get('source_checked_by', 'not applicable/not declared')}",
            f"- Checked at: {claim.get('source_checked_at', 'not applicable/not declared')}",
            f"- Weakest link: {claim['weakest_link']}",
            f"- What would change the conclusion: {claim['gap_that_changes_mind']}",
            "",
        ]
    argument = doc.get("argument_quality")
    if isinstance(argument, dict):
        lines += [
            "## Argument quality gates",
            "",
            f"- Review method: {argument.get('review_method')}",
            f"- Accountable reviewer: {argument.get('reviewed_by')}",
            f"- Reviewed at: {argument.get('reviewed_at')}",
        ]
        for name in ("concept", "evidence", "action"):
            lines.append(f"- {name.title()} gate: {argument.get('gates', {}).get(name)}")
        for index, item in enumerate(argument.get("chain", []), start=1):
            lines += [
                "",
                f"### Argument chain {index}",
                f"- Claim: {item.get('claim')}",
                f"- Evidence: {item.get('evidence')}",
                f"- Inference: {item.get('inference')}",
                f"- Action: {item.get('action')}",
                f"- Boundary: {item.get('boundary')}",
                f"- Counterevidence: {item.get('counterevidence')}",
            ]
    writing = doc.get("writing_review")
    if isinstance(writing, dict):
        lines += [
            "",
            "## Five-pass writing review",
            "",
            f"- Path: {writing.get('path')}",
            f"- Review method: {writing.get('review_method')}",
            f"- Accountable reviewer: {writing.get('reviewed_by')}",
            f"- Reviewed at: {writing.get('reviewed_at')}",
        ]
        for item in writing.get("passes", []):
            lines += [
                "",
                f"### {item.get('name', '').title()}",
                f"- Finding: {item.get('finding')}",
                f"- Revision: {item.get('revision')}",
            ]
    lines += [
        "",
        "## Method note",
        "",
        report["method_boundary"],
        "This output is not approval, source authentication, compliance advice, or authority to ship or commit.",
    ]
    return "\n".join(lines) + "\n"


def render_json(report: dict) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)
