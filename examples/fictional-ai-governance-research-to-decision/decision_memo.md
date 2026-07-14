# Decision memo (fictional): pilot an AI procurement copilot in supplier onboarding

## Decision

> Should the team pilot the AI procurement copilot in the supplier-onboarding workflow?

## Decision body

Risk and Compliance Council (RCC), chaired by the Head of Procurement Operations.

## Evidence summary

- 18% rework on document completeness, mixing clean and unclear cases.
- LLM with retrieval gets 70% right on a 50-case synthetic set; the set is easy-leaning.
- RCC requires human-in-the-loop; operational meaning of "HITL" is contested.
- Public vendor case studies show 30–50% review-time reduction (selection-biased).
- Logging specs align with public NIST/OWASP guidance; storage cost un-scoped.

## Recommendation

Run a 60-day controlled pilot on a narrow document class only, with:

- per-decision audit log (input / context / output / human edit / sent email);
- weekly review by a named human reviewer;
- pre-agreed stop condition on review-time reduction and safety signals.

## What we forgo

- rolling out across all supplier onboarding before pilot evidence;
- automating any outbound message without human review.

## Open risks

- Selection bias in the evaluation set → mitigation: refresh set with unseen cases week 2.
- HITL disagreement → mitigation: agree operational definition in pilot kickoff.
- Log storage cost → mitigation: cap logging scope to required fields only.

## Review conditions

Re-open this decision after 8 weeks if review-time reduction is <10% or any safety finding appears.
