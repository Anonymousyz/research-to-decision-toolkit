"""Human-readable reporting for r2d."""
from __future__ import annotations
from typing import Any, Mapping


def render_markdown(doc: Mapping[str, Any], report: Mapping[str, Any]) -> str:
    lines = [
        f"# Decision-readiness report", "",
        f"- **Decision:** {doc.get('decision', 'not specified')}",
        f"- **Verdict:** {report['decision']}",
        f"- **Score:** {report['total']}/{report['max']} ({report['normalized_pct']}%)",
        f"- **Veto:** {'yes' if report['veto'] else 'no'}", "",
        "## Area scores", "", "| Area | Score | Max |", "|---|---:|---:|",
    ]
    for area in report["areas"]:
        lines.append(f"| {area['name']} | {area['score']} | {area['max']} |")
    lines.extend(["", "## Vetoes", ""])
    lines.extend((f"- {item}" for item in report["veto"]) if report["veto"] else ["No veto was triggered."])
    lines.extend(["", "## Priority gaps", ""])
    lines.extend((f"- {item}" for item in report["top_gaps"]) if report["top_gaps"] else ["No scorecard gap was detected."])
    lines.extend(["", "## Method note", "", "This is an author-designed, uncalibrated decision-support heuristic. It does not validate the truth of claims or replace domain, legal, security, or compliance review."])
    return "\n".join(lines) + "\n"
