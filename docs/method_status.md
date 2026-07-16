# Method status and validation roadmap

## Current status

The R2D score is a fixed, author-designed, uncalibrated structural-workflow heuristic. It checks whether a brief contains reviewable components; it does **not** establish that claims are true, sources are sufficient, a checker is independent, or the decision is correct.

## Scoring model

Four areas carry six points each:

1. decision framing;
2. evidence quality;
3. decision review;
4. artifact and feedback.

The item-level contract is published in [`scorecards/decision-readiness-scorecard.md`](../scorecards/decision-readiness-scorecard.md). A total of 18/24 with no veto triggers “structurally ready for human decision meeting,” not “approved” or “ready to implement.”

## Source-check boundary

For primary and secondary evidence, the schema requires a non-reserved HTTP(S) URL plus `source_check_method: human`, checker, and date declarations. The CLI validates field structure only. It does not fetch the URL, authenticate the person, determine source authority, or test whether the source supports the claim.

## v0.6 quality-review boundary

The v0.6 extension records concept/evidence/action gates, an explicit argument chain, and an ordered five-pass writing review. These records make human reasoning and revision more inspectable. They are not formal proof, source authentication, independent review, or calibrated writing-quality measures, and they do not add points to the canonical 24-point score. Unversioned briefs retain legacy compatibility; any declared version other than the string `"0.6"` is rejected rather than guessed.

## Validation roadmap

- Have at least two independent reviewers score the same 20 permission-cleared or fictional briefs.
- Measure item-level agreement and revise ambiguous criteria.
- Test the structured source-declaration model against deliberately misleading and stale sources.
- Record which missing evidence actually changes later decisions.
- Publish threshold changes and migration notes.
- Seek domain review before applying the toolkit to regulated, medical, financial, employment, or other high-consequence decisions.

Until then, use the score to structure a meeting and expose gaps—not to replace judgment, permission, source authentication, or accountability.
