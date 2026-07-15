# Decision-meeting structure scorecard

Score each item **0 (absent)** or **1 (present and structurally reviewable)**. The CLI applies the same 24 checks. A total of 18/24 with no veto means only **structurally ready for an accountable human decision meeting**.

## A. Decision framing — 6 points

- [ ] Decision question is non-empty.
- [ ] Accountable decision body is named.
- [ ] Default outcome is explicit.
- [ ] Deadline or trigger is explicit.
- [ ] At least three structured claims are present.
- [ ] At least three decision-level uncertainties are present.

## B. Evidence quality — 6 points

- [ ] At least three claims are present.
- [ ] At least two distinct primary-source URLs have human-check declarations.
- [ ] Every claim names its weakest link.
- [ ] At least three uncertainties are present.
- [ ] Both boundaries and out-of-scope notes are non-empty.
- [ ] Every claim states what evidence would change the conclusion.

## C. Decision review — 6 points

- [ ] At least two alternatives are stated.
- [ ] At least two decision criteria are stated.
- [ ] At least two affected stakeholder groups are stated.
- [ ] Reversibility is described.
- [ ] The key cost or trade-off is described.
- [ ] A pre-mortem failure is described.

## D. Artifact and feedback — 6 points

- [ ] Artifact form is named.
- [ ] Artifact acceptance criteria are explicit.
- [ ] Artifact owner is named.
- [ ] At least one feedback channel is named.
- [ ] Feedback owner is named.
- [ ] Feedback log is explicitly marked filled.

## Structural vetoes

A veto overrides the total:

- `decision_body` is present but empty;
- `default_outcome` is present but empty;
- claims exist but none states evidence that would change the conclusion.

Missing required fields and malformed types are schema errors, not low-score substitutes.

## Result

- **18–24 with no veto:** structurally ready for an accountable human decision meeting;
- **0–17 with no veto:** revise before the meeting;
- **any total with veto:** resolve the veto before relying on the packet.

The score checks declared structure, not truth. Human source-check fields are attestations, not authentication; sources, conclusions, permissions, and consequences still require accountable domain review.
