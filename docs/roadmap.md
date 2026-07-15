# Roadmap

This repository is small on purpose. The roadmap prioritizes evidence, method clarity, and permission-safe reuse.

## v0.5 — current hardened alpha

- [x] `r2d init`, `validate`, `score`, JSON output, and Markdown report
- [x] Fixed four-area, 24-point structural contract
- [x] Decision-review area: alternatives, criteria, stakeholders, reversibility, trade-off, pre-mortem
- [x] Typed source, artifact, feedback, and human source-check declarations
- [x] Reserved/local source-domain rejection and malformed-field regression tests
- [x] Unified report renderer and documented exit codes
- [x] Fictional end-to-end example and inactive CI template under `docs/`

## v0.6 — validation and migration

- [ ] Add explicit schema-version and migration handling
- [ ] Compare two briefs across versions
- [ ] Test at least 20 fictional or permission-cleared briefs with multiple reviewers
- [ ] Measure item-level inter-rater agreement
- [ ] Add stale-source and contradictory-source fixtures
- [ ] Publish an active GitHub Actions workflow only with explicit workflow-scope authorization

## v1.0 — validated public method

- [ ] Stable CLI and JSON compatibility policy
- [ ] Published calibration results and known limitations
- [ ] Independent domain review
- [ ] Five or more permission-safe domain examples
- [ ] Multi-language quickstart

## Out of scope

- automatic fact verification or source authentication;
- automatic decision approval;
- project management or personal journaling;
- uploading confidential material to external models.

Version numbers record software and method maturity, not correctness, certification, or decision authority.
