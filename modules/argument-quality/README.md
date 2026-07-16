# Argument Quality Module

This module adds a reviewable bridge between evidence and action:

```text
concept gate → evidence gate → action gate
claim → evidence → inference → action → boundary → counterevidence
```

It is an author-designed operational synthesis for decision packets. It is **not** a new formal logic, proof system, truth engine, fact checker, or substitute for domain review.

## Three gates

1. **Concept gate** — define the terms whose ambiguity could change the decision.
2. **Evidence gate** — separate the claim, source, inference, uncertainty, and contrary evidence.
3. **Action gate** — state, in one reviewer-authored free-text declaration, the strongest action supported now and address its owner, boundary, stop condition, and fallback.

The runtime checks that each gate is non-empty. It **does not parse or independently verify** that a free-text action declaration actually contains every component or that those components are sound; that remains a human review responsibility.

A packet can pass the schema while the underlying reasoning remains wrong. The CLI checks structure only; an accountable human must inspect the sources, inference, counterevidence, and consequences.

## Minimal chain

Each v0.6 `argument_quality.chain` item records:

- `claim` — the proposition under review;
- `evidence` — the material actually offered in support;
- `inference` — why the evidence is said to support the claim;
- `action` — the bounded next move;
- `boundary` — what the claim does not authorize;
- `counterevidence` — the observation that would weaken or reverse the move.

Use one main chain per important commitment. Do not stack methods merely to appear rigorous.

## Review metadata

`reviewed_by`, `reviewed_at`, and `review_method` make responsibility visible. Allowed methods are `human` and `human-with-ai-assistance`. AI-generated objections may help drafting, but they do not count as independent review or evidence.

## Manual template

Use [`templates/argument-quality-review.md`](templates/argument-quality-review.md) when JSON is unnecessary. The fictional end-to-end case demonstrates the machine-readable form.

## Failure modes

- defined terms that do not resolve the actual ambiguity;
- URLs mistaken for evidence that supports the claim;
- inference omitted between evidence and recommendation;
- token counterarguments that cannot change the action;
- action without an owner, boundary, stop condition, or fallback;
- the proposer naming themselves as an “independent” reviewer.

The canonical 24-point score remains unchanged in v0.6. This module is a required structural extension only for documents declaring `schema_version: "0.6"`; it is not a fifth scored area and is not calibrated.
