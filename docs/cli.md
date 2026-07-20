# CLI

The local `r2d` CLI validates a decision-brief structure, calculates four six-point structural areas, and renders a review packet. It does not fetch URLs, authenticate evidence, verify the identity or independence of a named checker, or authorize a decision.

## Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

## Commands

```bash
r2d init decision_brief.json
r2d validate decision_brief.json
r2d score decision_brief.json
r2d score decision_brief.json --json
r2d report decision_brief.json --output decision_report.md
python -m r2d --help
```

## Exit codes

| Code | Meaning |
|---:|---|
| 0 | `init` completed; `validate` found no errors and no vetoes; `score` or `report` reached 18/24 with no structural veto |
| 1 | `validate` found a structurally valid brief with veto items; `score` or `report` completed but the document is below 18/24 or has a structural veto |
| 2 | Schema/validation failure or refusal to overwrite a protected/source path |
| 3 | File or JSON input error |

A code of `0` is not approval, evidence authentication, compliance advice, or authority to implement.

## v0.6 quality-review extension

Documents that declare `schema_version: "0.6"` must include:

- `argument_quality`: concept/evidence/action gates plus at least one claim→evidence→inference→action chain with a boundary and counterevidence;
- `writing_review`: Path A or B plus the ordered judgment, evidence, structure, clarity, and delivery passes;
- accountable reviewer, date, and `human` or `human-with-ai-assistance` method declarations for both reviews.

The extension is structural and unscored. The canonical readiness score remains 24 points. Older documents with no `schema_version` remain valid under the legacy contract. If the field is present, only the string `"0.6"` is accepted; unknown versions and wrong types fail closed.

## Source declarations

Primary and secondary claims require:

- an HTTP(S) URL that is not local or a reserved example domain;
- `source_check_method: "human"`;
- a non-empty `source_checked_by` declaration;
- an ISO `source_checked_at` date.

These fields make responsibility reviewable. They do **not** prove that the human exists, visited the URL, interpreted it correctly, or that the source supports the claim.

## Report safety

`r2d report` refuses to overwrite its source file. Review generated Markdown before circulation and publish only fictional, public, or explicitly authorized material.

The starter copied by `r2d init` is included in the installed wheel; the command does not depend on a source checkout.
