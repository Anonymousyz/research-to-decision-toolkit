# Critical review prompt

Use this prompt to stress-test a draft memo.

## Prompt

```text
You are a critical reviewer. Read the following decision memo and produce a one-page review with these sections:

1. What is the strongest part?
2. What is the weakest part?
3. What evidence would flip the recommendation?
4. What second-order risk is the memo ignoring?
5. Who would disagree with this memo, and why?
6. What single change most improves this memo?

Rules:
- Be specific. Quote phrases from the memo.
- Be honest. Comfort is not the goal.
- Suggest tradeoffs, not just criticism.

Memo:
<paste here>
```


## Why this prompt

Specificity produces specific output. The prompt gives the model a specific identity, a specific brief, and a specific output schema.

## Worked example I/O

*Input*: A 5-page internal memo describing a pilot decision.
*Expected output*:

> sharpest challenge quoting phrases, strongest prediction, one-paragraph rewrite, one embarrassing question, one good-faith concession.

## Reviewing the output

Ask: did the challenges quote phrases? Did the rewrite change the brief, or just paraphrase it?
## Worked example I/O (fictional)

*Input*: A 5-page internal memo describing a pilot decision.

*Expected output*:

> 1. Sharpest challenge: "The pilot scope assumes retrieval accuracy > 90%. The eval set has 30 cases. The claim collapses under pressure."
> 2. Strongest prediction: "Six months in, the team will want to expand scope and lose the stop condition."
> 3. One-paragraph rewrite: tightened brief with explicit stop condition.
> 4. Embarrassing question: "Why is the legal review the only place where the scope was actually tightened?"
> 5. Concession: "A reviewer could not find evidence for claim 4; treat as assumption."

## When to use vs. not to use

Use when the artifact must survive an honest third-party challenge. Do not use to rubber-stamp an existing narrative.
