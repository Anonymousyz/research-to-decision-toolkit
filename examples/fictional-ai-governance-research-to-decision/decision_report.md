# Decision packet: Should the team pilot the fictional AI procurement copilot in supplier onboarding?

- **Decision:** Structurally ready for human decision meeting
- **Total:** 23/24 (95.8%)
- **Veto:** no

## Area scores

| Area | Score | Max | Gaps |
|---|---:|---:|---|
| Decision framing | 6 | 6 | none |
| Evidence quality | 6 | 6 | none |
| Decision review | 6 | 6 | none |
| Artifact and feedback | 5 | 6 | feedback log is not yet filled |

## Veto items

- None

## Top gaps

- feedback log is not yet filled

## Claims and source-check declarations

### The synthetic baseline records 18% rework on document completeness.
- Source: Synthetic 2025 operations review
- Source tier: synthetic
- Human checker: not applicable/not declared
- Checked at: not applicable/not declared
- Weakest link: The mixed document classes may hide variation.
- What would change the conclusion: A clean re-count below 8% would weaken the pilot case.

### A retrieval prototype answered 70% of a synthetic 50-case set correctly.
- Source: Synthetic proposer-built evaluation
- Source tier: synthetic
- Human checker: not applicable/not declared
- Checked at: not applicable/not declared
- Weakest link: The proposer selected the cases.
- What would change the conclusion: Accuracy below 50% on an unseen set would stop the pilot.

### Human approval is required before any supplier-facing action.
- Source: Synthetic council charter
- Source tier: internal
- Human checker: not applicable/not declared
- Checked at: not applicable/not declared
- Weakest link: Approval and full review are not yet distinguished.
- What would change the conclusion: An unresolved review definition would make acceptance criteria impossible.

### Risk review should cover context, impacts, measurement, and treatment rather than model accuracy alone.
- Source: https://www.nist.gov/itl/ai-risk-management-framework
- Source tier: primary
- Human checker: Fictional case author
- Checked at: 2026-07-15
- Weakest link: The framework does not prescribe this local workflow.
- What would change the conclusion: If the council cannot map the pilot to named controls, postpone it.

### The pilot must test sensitive-information disclosure and excessive agency risks.
- Source: https://genai.owasp.org/
- Source tier: primary
- Human checker: Fictional case author
- Checked at: 2026-07-15
- Weakest link: The taxonomy identifies risks but does not prove control effectiveness.
- What would change the conclusion: A critical disclosure or unauthorized action in testing would block the pilot.

## Argument quality gates

- Review method: human-with-ai-assistance
- Accountable reviewer: Fictional case author
- Reviewed at: 2026-07-16
- Concept gate: A pilot means a time-limited, restricted-document evaluation; it does not mean production deployment.
- Evidence gate: Synthetic operational and evaluation claims are separated from public-framework claims and their limitations are explicit.
- Action gate: The council can approve only a controlled pilot with named owners, stop conditions, and a manual fallback.

### Argument chain 1
- Claim: A controlled pilot is the strongest action currently supported.
- Evidence: The synthetic baseline reports rework and the synthetic prototype reports partial accuracy, while both remain unvalidated on an unseen set.
- Inference: The evidence supports learning under constraints but not broad deployment.
- Action: Run a restricted human-in-the-loop pilot only after unseen-case and control tests pass.
- Boundary: No autonomous procurement decision, supplier sanction, or supplier-facing action is permitted.
- Counterevidence: Accuracy below 50% on an unseen set or one critical disclosure or agency failure blocks the pilot.

### Argument chain 2
- Claim: Risk review must cover governance and operational controls, not accuracy alone.
- Evidence: NIST AI RMF and OWASP GenAI sources identify broader risk-management and security concerns.
- Inference: A locally accountable control map and test plan are needed before the council can act.
- Action: Map each pilot risk to an owner, test, evidence artifact, and stop condition.
- Boundary: The cited frameworks inform the review but do not validate this local workflow or prove control effectiveness.
- Counterevidence: If the council cannot map risks to named controls and accountable owners, postpone the pilot.

## Five-pass writing review

- Path: A
- Review method: human-with-ai-assistance
- Accountable reviewer: Fictional case author
- Reviewed at: 2026-07-16

### Judgment
- Finding: The evidence supports a bounded learning decision, not a production-readiness claim.
- Revision: Narrowed the recommendation to a controlled pilot and stated the default outcome.

### Evidence
- Finding: Synthetic results and public-framework guidance could be confused as equivalent proof.
- Revision: Separated source tiers, human-check declarations, weakest links, and decision-changing gaps.

### Structure
- Finding: The decision chain needed an explicit bridge from evidence to action.
- Revision: Added two claim-evidence-inference-action chains with boundaries and counterevidence.

### Clarity
- Finding: Pilot, approval, and deployment required sharper meanings.
- Revision: Defined pilot as restricted and time-limited and excluded autonomous supplier-facing action.

### Delivery
- Finding: The packet needed to survive the author and support a council review.
- Revision: Named the artifact owner, acceptance criteria, feedback channel, check-in date, and stop threshold.

## Method note

Author-designed, uncalibrated decision-support heuristic for structural workflow completeness; source checks are human declarations and URLs are not fetched or substantively verified by the CLI.
This output is not approval, source authentication, compliance advice, or authority to ship or commit.
