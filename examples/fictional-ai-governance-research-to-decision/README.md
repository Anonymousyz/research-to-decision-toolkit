# Fictional AI governance: research-to-decision example

A fictional, synthetic decision brief for an "AI procurement copilot" pilot in a supplier-onboarding workflow. Used to demonstrate the toolkit's templates end to end.

## Files

- `decision_brief.json` — the structured brief (used by `r2d score`)
- `decision_memo.md` — a memo generated from the brief
- `evidence_matrix.md` — an evidence matrix generated from the brief
- `feedback_log.md` — an empty feedback log to be filled after pilot

## Why fictional

All claims, percentages, and organization names in this directory are fictional. No real organization, customer, or person is referenced.

## How to use

```bash
r2d validate examples/fictional-ai-governance-research-to-decision/decision_brief.json
r2d score   examples/fictional-ai-governance-research-to-decision/decision_brief.json
```

Expected output:

```text
Decision: Ready for decision meeting
Total: 23/24
Normalized: 95.8%
Veto: no
Top gaps:
- feedback log is not yet filled
```
