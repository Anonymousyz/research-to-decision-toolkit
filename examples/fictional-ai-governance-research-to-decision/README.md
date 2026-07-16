# Fictional AI-governance research-to-decision example

A synthetic decision brief for an AI procurement-copilot pilot in a supplier-onboarding workflow. It demonstrates the local CLI and templates; it is not evidence of a real organization, deployment, outcome, or independent review.

## Files

- `decision_brief.json` — v0.6 structured brief with argument-quality and five-pass writing-review records
- `decision_memo.md` — fictional memo
- `evidence_matrix.md` — fictional evidence matrix
- `feedback_log.md` — intentionally unfilled feedback log
- `decision_report.md` — generated CLI report

Public source URLs are real references, while all case-specific claims, percentages, names, reviewer declarations, and outcomes are fictional. The CLI does not fetch those URLs or authenticate the declarations.

The quality-review records expose the case author's stated reasoning and revisions. They are not independent review, formal proof, or evidence that the fictional recommendation is correct.

## Run

```bash
r2d validate examples/fictional-ai-governance-research-to-decision/decision_brief.json
r2d score examples/fictional-ai-governance-research-to-decision/decision_brief.json
```

Expected output:

```text
Decision: Structurally ready for human decision meeting
Total: 23/24
Normalized: 95.8%
Veto: no
Top gaps:
- feedback log is not yet filled
```
