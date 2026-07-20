# Agent instructions

This repository is a local-first CLI (`r2d`) plus templates that turn research evidence into a decision packet accountable people can review. Documentation honesty is the product: README numbers are locked by tests.

## Setup and verification

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
r2d validate examples/fictional-ai-governance-research-to-decision/decision_brief.json
```

All tests must pass before any commit. The suite runs in under a second.

## Hard rules

- Zero runtime dependencies. Do not add packages to `[project.dependencies]`.
- The canonical contract is frozen: four areas of six points each (24 total), the 18/24 readiness threshold, and the three structural vetoes in `src/r2d/schema.py`. Changing any of these requires the owner's explicit approval.
- The packaged starter brief (`src/r2d/data/starter_decision_brief.json`) must stay identical to the example brief; a test asserts equality.
- Every README claim (23/24 expected output, verdict strings, version numbers) must stay backed by a test. If you change behavior, update README, `README.zh-CN.md`, `docs/cli.md`, and the tests together.
- External-model prompts must keep their authorization/confidentiality/human-accountability clauses; a test enforces this.
- Examples are fictional. Never add real client, employer, or personal data. Never commit secrets.
- Record notable changes under `## Unreleased` in `CHANGELOG.md`. Do not create release tags or GitHub releases; releases are owner ceremonies.
