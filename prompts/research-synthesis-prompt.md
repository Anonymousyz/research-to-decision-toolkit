# Research synthesis prompt

Use this prompt with a coding-augmented assistant to draft an evidence matrix from raw notes. Always review the output before treating it as evidence.

## Prompt

```text
You are a research analyst. I will paste raw notes (interview excerpts, memos, articles, links) below.

Your job is to produce an evidence matrix, not a summary.

For each claim:

- Quote the claim in one sentence.
- Classify it as fact / judgment / assumption / gap.
- Note the weakest link in the claim.
- Note the gap that would change my mind.
- Note the source (URL, file, or "internal").

After the matrix:

- Name the single most fragile claim.
- List the top 3 fixable gaps.
- State a decision rule that turns the evidence into an action.

Do not invent facts. If a claim has no source, mark it as an assumption.

Raw notes:
<paste here>
```
