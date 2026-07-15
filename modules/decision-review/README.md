# Decision-review module

Use this module after the evidence brief is coherent but before commitment. It adds four checks: alternatives, fragile assumptions, pre-mortem failure causes, and an independent red-team pass.

## Sequence

1. Record alternatives and reversibility in [`templates/decision-brief-review.md`](templates/decision-brief-review.md).
2. Track fragile assumptions in [`templates/assumption-ledger.md`](templates/assumption-ledger.md).
3. Run a pre-mortem with [`templates/pre-mortem.md`](templates/pre-mortem.md).
4. Use the [`decision red-team prompt`](prompts/decision-red-team-prompt.md) as a drafting aid, then require human review.
5. Apply the [`decision-quality scorecard`](scorecards/decision-quality-scorecard.md).

AI output is not evidence and cannot be the independent reviewer. The decision body remains accountable for source quality, challenge handling, and the final choice.
