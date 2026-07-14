
"""Scoring logic for decision_brief.json."""
AREAS = [
    ("Decision framing", ["decision", "decision_body", "deadline", "default_outcome"]),
    ("Evidence quality", ["claims_present", "weakest_named", "gaps_listed", "primary_sources"]),
    ("Artifact plan", ["artifact_form", "named_readers", "channels", "survives_author"]),
    ("Feedback loop", ["channels_named", "log_filled", "next_move_threshold", "checkin"]),
]

def _score(doc):
    total = 0
    notes = []
    d = doc.get("decision", "")
    if d:
        total += 1
        if isinstance(d, str) and d.strip().endswith("?"):
            total += 1
        else:
            notes.append("decision question should end with '?'")
    else:
        notes.append("decision question missing")
    if doc.get("decision_body"):
        total += 1
    else:
        notes.append("decision body missing")
    if doc.get("deadline"):
        total += 1
    else:
        notes.append("deadline/trigger missing")
    if doc.get("default_outcome"):
        total += 1
    else:
        notes.append("default outcome missing")

    claims = doc.get("claims") or []
    if len(claims) >= 5:
        total += 1
    else:
        notes.append(f"only {len(claims)} claims; need 5+")
    if any(c.get("weakest_link") for c in claims if isinstance(c, dict)):
        total += 1
    else:
        notes.append("no claim has a weakest-link note")
    if any(c.get("gap_that_changes_mind") for c in claims if isinstance(c, dict)):
        total += 1
    else:
        notes.append("no claim has a gap-that-changes-mind note")
    sources = sum(1 for c in claims if isinstance(c, dict) and c.get("source") and "internal" not in str(c.get("source", "")).lower())
    if sources >= 2:
        total += 1
    else:
        notes.append(f"only {sources} primary sources cited; need 2+")

    art = doc.get("artifact") or {}
    if art.get("form"):
        total += 1
    readers = art.get("readers") or []
    if len(readers) >= 3:
        total += 1
    else:
        notes.append(f"only {len(readers)} named readers; need 3+")
    channels = art.get("channels") or []
    if len(channels) >= 2:
        total += 1
    else:
        notes.append(f"only {len(channels)} channels; need 2+")
    if art.get("survives_author"):
        total += 1
    else:
        notes.append("'what survives the author' is empty")

    fb = doc.get("feedback") or {}
    fb_channels = fb.get("channels") or []
    if len(fb_channels) >= 2:
        total += 1
    else:
        notes.append(f"only {len(fb_channels)} feedback channels; need 2+")
    if fb.get("log_filled"):
        total += 1
    else:
        notes.append("feedback log is not filled")
    if fb.get("next_move_threshold"):
        total += 1
    else:
        notes.append("next-move threshold is empty")
    if fb.get("checkin_date"):
        total += 1
    else:
        notes.append("30-day check-in date is empty")
    return total, notes

def vetos(doc):
    veto = []
    if not (doc.get("decision_body") or "").strip():
        veto.append("decision body not named")
    if not (doc.get("default_outcome") or "").strip():
        veto.append("default outcome not stated")
    claims = doc.get("claims") or []
    if not any((c.get("gap_that_changes_mind") or "") for c in claims if isinstance(c, dict)):
        veto.append("no gap declared anywhere")
    return veto

def make_report(doc):
    total, notes = _score(doc)
    v = vetos(doc)
    decision = "Ready to ship" if (total >= 16 and not v) else "Not ready"
    return {
        "total": total,
        "max": 24,
        "normalized_pct": round(total / 24 * 100, 1),
        "veto": v,
        "decision": decision,
        "top_gaps": notes[:3],
        "areas": [{"name": n, "weight": 6} for n, _ in AREAS],
    }
