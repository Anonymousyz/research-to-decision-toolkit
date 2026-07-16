# Decision-review module

Use this module after the evidence brief is coherent but before commitment. It adds four checks: alternatives, fragile assumptions, pre-mortem failure causes, and an independent red-team pass.

## Sequence

1. Record alternatives and reversibility in [`templates/decision-brief-review.md`](templates/decision-brief-review.md).
2. Track fragile assumptions in [`templates/assumption-ledger.md`](templates/assumption-ledger.md).
3. Run a pre-mortem with [`templates/pre-mortem.md`](templates/pre-mortem.md).
4. Use the [`decision red-team prompt`](prompts/decision-red-team-prompt.md) as a drafting aid, then require human review.
5. Apply the [`decision-quality scorecard`](scorecards/decision-quality-scorecard.md).

AI output is not evidence and cannot be the independent reviewer. The decision body remains accountable for source quality, challenge handling, and the final choice.

## CLI boundary

The module is a supplementary human-review path. The CLI's six-point `Decision review` area checks alternatives, criteria, stakeholders, reversibility, trade-offs, and one pre-mortem statement; it does not score the full assumption ledger, dated stop-condition workflow, or independent-human response in this module. Do not present the module's 16-point manual scorecard as part of the canonical CLI total.
