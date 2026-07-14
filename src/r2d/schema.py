
"""Schema for decision_brief.json files used by r2d."""
from typing import Any, Dict, List, Tuple

REQUIRED = ["decision", "decision_body", "deadline", "default_outcome",
            "claims", "artifact", "feedback"]

def _is_str_nonempty(x):
    return isinstance(x, str) and x.strip() != ""

def validate(doc):
    errs = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing required field: {k}")
    if "claims" in doc and not isinstance(doc["claims"], list):
        errs.append("claims must be a list")
    elif doc.get("claims") and len(doc["claims"]) < 5:
        errs.append("need at least 5 claims for scorecard purposes")
    veto = []
    if not _is_str_nonempty(doc.get("decision_body", "")):
        veto.append("decision_body must be named")
    if not _is_str_nonempty(doc.get("default_outcome", "")):
        veto.append("default_outcome must be stated")
    claims = doc.get("claims") or []
    has_gap = any(_is_str_nonempty(c.get("gap_that_changes_mind", "")) for c in claims if isinstance(c, dict))
    if not has_gap:
        veto.append("no gap declared anywhere in claims")
    ok = (len(errs) == 0 and len(veto) == 0)
    return ok, errs, veto
