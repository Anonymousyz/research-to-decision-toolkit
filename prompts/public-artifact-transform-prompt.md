# Public-artifact transform prompt

Use this prompt to convert a private memo into a public artifact.

## Prompt

```text
You are turning a private memo into a public artifact. Private memos protect the author; public artifacts protect the reader.

Take this memo and:

1. Strip personal, organizational, and contractual details.
2. Convert specific claims into reusable claims (replace specific numbers with thresholds where possible).
3. Add at least one named reader who would benefit.
4. Add a paragraph on what survives the author.
5. Add a feedback section: where to comment, where to fork, where to cite.

Do not:
- add marketing language;
- exaggerate certainty;
- add claims that are not in the original memo.

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
