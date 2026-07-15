# Changelog

## v0.5.0 — 2026-07-15

- Reframed the 24-point result as structural workflow readiness for a human decision meeting, not decision quality.
- Added a six-point decision-review area covering alternatives, criteria, stakeholders, reversibility, trade-offs, and pre-mortem failure.
- Required typed artifact/feedback fields and human-declared source checks for primary and secondary evidence.
- Rejected reserved/example source domains and malformed nested field types.
- Separated schema errors from structural vetoes and made CLI exit codes reflect invalid, vetoed, and not-ready inputs.
- Unified duplicate Markdown report implementations and preserved `init`, `--json`, and `-o` compatibility.

## v0.4.1 — 2026-07-15

- Restored the complete SPDX-standard MIT license text so GitHub can identify the repository license correctly.

## v0.4.0 — 2026-07-15

- Corrected the score model so four six-point areas sum transparently to 24.
- Replaced source-name heuristics with explicit source tiers and distinct primary-source URLs.
- Added `r2d init`, `r2d report`, JSON output, `python -m r2d`, and documented exit codes.
- Expanded unit and CLI coverage to ten tests.
- Added an explicit method boundary and validation roadmap.
- Integrated the decision-review module: alternatives, fragile assumptions, pre-mortem, red-team prompt, and scorecard.
- Updated the fictional case to cite authoritative public sources without implying real deployment evidence.

## v0.3.0

- Initial public draft.
- Added templates, prompts, scorecard, fictional example, and local CLI.
- License: MIT.
