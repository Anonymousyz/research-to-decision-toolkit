# Quickstart

Use fictional, public, or explicitly authorized material. Do not paste confidential, personal, client, employer, privileged, or restricted information into an external model.

## 1. Name the decision

Answer five questions:

1. What is the real decision?
2. Who decides?
3. When is it due or what triggers it?
4. What happens by default if no decision is made?
5. Why is it needed now?

If these are not explicit, use [`problem-framing-canvas.md`](../templates/problem-framing-canvas.md) before continuing.

## 2. Build reviewable claims

Use [`evidence-matrix.md`](../templates/evidence-matrix.md). For each claim record:

- type: fact, judgment, assumption, or recommendation;
- source tier and source reference;
- weakest link;
- evidence that would change the conclusion.

For primary and secondary sources, the CLI requires a direct non-reserved HTTP(S) URL plus human checker and date declarations. Those declarations are not source authentication.

## 3. Add decision review

Record at least two alternatives, two criteria, two affected stakeholder groups, reversibility, key trade-off, and one pre-mortem failure.

## 4. Define artifact and feedback

Choose a permission-cleared artifact, owner, acceptance criteria, feedback channel, review question, and check-in date. Anonymization alone does not authorize publication.

## 5. Validate and score structure

```bash
r2d validate examples/fictional-ai-governance-research-to-decision/decision_brief.json
r2d score examples/fictional-ai-governance-research-to-decision/decision_brief.json
```

The threshold is 18/24 with no veto. It means only “structurally ready for an accountable human decision meeting.”

## 6. Circulate and learn

Use an appropriate authorized internal or public channel. Record feedback after circulation and revise the brief when evidence changes. AI-generated challenge drafts are not evidence or independent review.
