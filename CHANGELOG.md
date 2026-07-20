# Changelog

## Unreleased

- Published the active GitHub Actions validation workflow from the documented template (Python 3.9/3.11/3.12 matrix) now that a workflow-scope credential is available, and added the workflow badge to the README.
- Added a full Chinese README (`README.zh-CN.md`) and two Mermaid diagrams to both languages: the stage-by-stage workflow map and the 24-point/veto scoring flow.
- Added a Cursor cloud-agent environment definition (`.cursor/environment.json`) so hosted agents install the package before working.
- Documented the previously implicit exit code 1 for `validate` on structurally valid briefs that carry veto items.
- Guarded `python -m r2d` module execution against import-time exit and shipped `py.typed` so downstream type checkers can use the annotations.
- Added an `AGENTS.md` that binds coding agents to the frozen 24-point/three-veto contract, the zero-dependency policy, and the docs-backed-by-tests discipline.

## v0.6.0 — 2026-07-16

- Added an opt-in, backward-compatible `schema_version: "0.6"` contract for argument-quality and judgment-writing records; explicit null and other unsupported version values now fail closed.
- Added concept, evidence, and action gates plus explicit claim→evidence→inference→action chains with boundaries and counterevidence.
- Added Path A/B and an ordered five-pass writing review covering judgment, evidence, structure, clarity, and delivery; `path` now has explicit current-disposition semantics.
- Rendered both records in Markdown decision packets without changing the canonical 24-point score or 18-point threshold.
- Upgraded the packaged fictional starter, completed the source distribution with documented repository assets, and documented that the new records are structural, uncalibrated, and human-accountable.
- Hardened report output against direct, normalized, symbolic-link, and hard-link aliases of the source brief and aligned documented report exit codes with the CLI.
- Rejected reserved-domain subdomains, trailing-dot aliases, non-global IP source URLs, missing hosts, legacy numeric/hex/short IPv4 spellings, and fragment-only duplicates so the two-primary-source threshold cannot be bypassed.
- Added authorization and confidentiality gates to every external-model prompt, including the nested decision-review module.
- Separated the supplementary 16-point and qualitative worksheets from the canonical 24-point CLI contract.
- Added regression tests for schema versions, source protection, packaged initialization, prompt coverage, report readiness status, distribution completeness, and method boundaries.

## v0.5.2 — 2026-07-16

- Added machine-readable citation metadata and complete package-discovery links.
- Added release, license, and supported-Python badges to the public entry point.
- Kept the v0.5 decision-packet contract, thresholds, and CLI behavior unchanged.

## v0.5.1 — 2026-07-16

- Expanded the README with professional decision-packet context for research, policy analysis, product discovery, and AI deployment.
- Added a clear four-layer explanation of decision framing, evidence, decision review, and artifact/feedback.
- Preserved the v0.5 structural scoring and source-declaration contract; this patch changes presentation and package metadata, not the decision threshold.

## v0.5.0 — 2026-07-15

- Reframed the 24-point result as structural workflow readiness for a human decision meeting, not decision quality.
- Added a six-point decision-review area covering alternatives, criteria, stakeholders, reversibility, trade-offs, and pre-mortem failure.
- Required typed artifact/feedback fields and human-declared source checks for primary and secondary evidence.
- Rejected reserved/example source domains and malformed nested field types.
- Separated schema errors from structural vetoes and made CLI exit codes reflect invalid, vetoed, and not-ready inputs.
- Unified duplicate Markdown report implementations and preserved `init`, `--json`, and `-o` compatibility.
- Added an AI-deployment handoff guide that distinguishes prototype readiness from a separate human decision packet.

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
