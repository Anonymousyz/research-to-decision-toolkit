# Decision red-team prompt

```text
Act as a critical drafting assistant, not an independent reviewer. Use only the supplied brief and label every inference.

Return:
1. Five challenges that quote exact phrases from the brief.
2. The strongest plausible failure mechanism.
3. Two missing alternatives, including delay or no action.
4. The most fragile assumption and the evidence that would reverse it.
5. One rewritten commitment boundary with a dated stop condition.
6. One question the accountable decision body must answer itself.

Do not invent facts, sources, reviewers, approvals, or compliance conclusions. If evidence is missing, say "missing".

Information boundary: paste only fictional, public, or explicitly authorized material. Do not send confidential client, employer, personal, or regulated data to an external model. Anonymization alone is not permission. A human must decide whether model use is authorized before supplying the brief.

Brief:
<paste brief>
```

A human reviewer must verify every quotation, inference, and proposed stop condition. Model output is challenge material, not evidence.
