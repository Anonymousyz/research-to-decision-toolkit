# Feedback porting prompt

Use this prompt to convert real feedback signals from private channels into public artifacts.

## Prompt

```text
You are helping me turn private feedback into a public artifact.

I will paste one feedback entry: a comment, a message, or a short note from a peer.

Produce:

1. A one-paragraph anonymized version (no names, no organization).
2. A one-line public "what this means".
3. A specific suggestion to update a public artifact (template, scorecard, prompt, or example).
4. A flag if anything in the feedback should NOT be made public.

Rules:
- Never invent facts.
- Never name the source.
- If the feedback reveals a personal detail, mark it private-only and stop.
```


## Why this prompt

Specificity produces specific output. The prompt gives the model a specific identity, a specific brief, and a specific output schema.

## Worked example I/O

*Input*: A 5-page internal memo describing a pilot decision.
*Expected output*:

> sharpest challenge quoting phrases, strongest prediction, one-paragraph rewrite, one embarrassing question, one good-faith concession.

## Reviewing the output

Ask: did the challenges quote phrases? Did the rewrite change the brief, or just paraphrase it?
