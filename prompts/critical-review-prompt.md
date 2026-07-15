# Critical-review prompt

Use only fictional, public, or explicitly authorized material. Do not paste confidential, personal, client, employer, privileged, or restricted information into an external model. AI output is adversarial drafting material, not independent review.

```text
Using only the supplied memo, generate a bounded critical-review draft:

1. Strongest supported point, quoting the memo.
2. Weakest supported point, quoting the memo.
3. Evidence that would flip the recommendation.
4. One plausible second-order risk, labeled inference.
5. A stakeholder who may disagree and the supplied basis for that view.
6. One revision that makes uncertainty or responsibility clearer.

Separate quoted evidence, inference, and speculation. Do not invent stakeholder views, reviewer identities, source checks, facts, or approvals. Do not recommend implementation. End with questions for an accountable human reviewer.

Memo:
<fictional, public, or authorized text only>
```

## Fictional output excerpt

> Quoted evidence: “The evaluation set contains 30 synthetic cases.”
>
> Inference: the reported threshold may be unstable outside the synthetic set.
>
> Human review question: what result on permission-cleared unseen data would stop the proposal?
