# Public-artifact transformation prompt

Run this prompt only after a human has confirmed both external-model processing authorization and public-release authorization. Anonymization, summarization, or removal of names alone does not create permission.

Do not paste confidential, personal, client, employer, privileged, contract-restricted, or re-identifiable information into an external model.

```text
Using only the permission-cleared memo, draft a public artifact.

1. Preserve supported claims and their public sources.
2. Remove details already approved for omission; do not assume omission resolves re-identification risk.
3. Replace case-specific claims with reusable language only when the meaning remains supported.
4. State the intended reader and reusable artifact.
5. Add limitations, excluded claims, and unresolved evidence gaps.
6. Add authorized feedback channels.
7. Produce a release-risk checklist for human sign-off.

Do not invent facts, permissions, sources, outcomes, endorsements, or authorization. Do not output the source memo. If any permission or re-identification question is unresolved, return only: DO NOT PUBLISH — HUMAN AUTHORIZATION REQUIRED.

Memo:
<explicitly authorized text only>
```

A responsible human must compare the draft with the source, authorization record, contractual restrictions, and re-identification risk before publication.
