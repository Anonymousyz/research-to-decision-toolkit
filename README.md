# Research-to-Decision Toolkit

> **Open research → evidence → decision → artifact → feedback.**

A public toolkit for turning open research into evidence-backed decisions, reusable artifacts, and public feedback loops.

```text
problem → evidence → judgment → artifact → feedback → iteration
```

This toolkit is for researchers, policy analysts, consulting practitioners, product owners, independent builders, and forward-deployed engineers who want to make their research visibly useful to strangers — not only useful inside their own organization.

It is **not**:

- a personal productivity system;
- a journaling system;
- a project management tool;
- a substitute for domain expertise.

It **is**:

- a small set of reusable canvases, templates, and prompts;
- a way to separate evidence from judgment from excitement;
- a way to publish research into assets other people can copy;
- a way to run a public feedback loop without relying on closed networks.

---

## 30-second value proposition

When someone says:

> I did a lot of research but I am not sure what decision it supports, what artifact it should become, or whether anyone else even cares.

Use this toolkit to:

1. Frame the real decision before collecting more evidence.
2. Organize what you know into an evidence matrix.
3. Separate facts from assumptions from judgments.
4. Decide whether the result should be a memo, a template, a tool, or a publication.
5. Ship a public artifact and log the feedback signals that come back.

---

## Repository map

| Area | Files | Purpose |
|---|---|---|
| Philosophy | [`MANIFESTO.md`](MANIFESTO.md) | Why research needs an artifact, and artifacts need feedback |
| Frame the decision | [`templates/problem-framing-canvas.md`](templates/problem-framing-canvas.md) | Turn a vague topic into a real decision question |
| Organize evidence | [`templates/evidence-matrix.md`](templates/evidence-matrix.md) | Sort claims into facts, judgments, assumptions, gaps |
| Decide the move | [`templates/decision-memo.md`](templates/decision-memo.md) | A short memo that produces a real decision |
| Decide the artifact | [`templates/public-artifact-brief.md`](templates/public-artifact-brief.md) | Decide whether the result becomes a repo, an article, a tool, or a workshop |
| Capture feedback | [`templates/feedback-log.md`](templates/feedback-log.md) | Record public feedback signals without overfitting |
| Score the readiness | [`scorecards/decision-readiness-scorecard.md`](scorecards/decision-readiness-scorecard.md) | A 0/1/2 score that decides whether to ship |
| AI prompts | [`prompts/research-synthesis-prompt.md`](prompts/research-synthesis-prompt.md), [`prompts/critical-review-prompt.md`](prompts/critical-review-prompt.md), [`prompts/public-artifact-transform-prompt.md`](prompts/public-artifact-transform-prompt.md) | Use AI to draft, stress-test, and transform |
| Example | [`examples/fictional-ai-governance-research-to-decision.md`](examples/fictional-ai-governance-research-to-decision.md) | A fictional end-to-end case |
| CLI | [`src/r2d`](src/r2d), [`docs/cli.md`](docs/cli.md) | Validate and score a decision brief locally |
| Tests | [`tests/test_r2d.py`](tests/test_r2d.py) | Small test surface for the validator |
| Quickstart | [`docs/quickstart.md`](docs/quickstart.md) | 10 minutes to first decision brief |
| Sources | [`SOURCES.md`](SOURCES.md) | Where the method comes from |
| Roadmap | [`docs/roadmap.md`](docs/roadmap.md) | What this repo will become next |

---

## Quick start

### Option A — manual

1. Open [`templates/problem-framing-canvas.md`](templates/problem-framing-canvas.md) and write down the real decision question.
2. Move claims into [`templates/evidence-matrix.md`](templates/evidence-matrix.md).
3. Use [`templates/decision-memo.md`](templates/decision-memo.md) to produce a memo.
4. Use [`templates/public-artifact-brief.md`](templates/public-artifact-brief.md) to choose the artifact form.
5. Use [`scorecards/decision-readiness-scorecard.md`](scorecards/decision-readiness-scorecard.md) to decide whether to ship.
6. After shipping, log feedback in [`templates/feedback-log.md`](templates/feedback-log.md).

### Option B — CLI

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e .
r2d validate examples/fictional-ai-governance-research-to-decision/decision_brief.json
r2d score   examples/fictional-ai-governance-research-to-decision/decision_brief.json
```

Expected output:

```text
Decision: Ready to ship
Total: 18/24
Normalized: 18/24 (75.0%)
Veto: no
Top gaps:
- No external reviewer named
- Feedback plan is implicit
```

See [`docs/cli.md`](docs/cli.md).

---

## How to read this repository

If you only have 5 minutes:

1. Read this README.
2. Read [`MANIFESTO.md`](MANIFESTO.md).
3. Skim [`examples/fictional-ai-governance-research-to-decision.md`](examples/fictional-ai-governance-research-to-decision.md).

If you have 30 minutes:

1. Read the manifesto, the quickstart, and the road map.
2. Walk through one template end to end with your own material.

If you have 2 hours:

1. Reproduce the fictional example from scratch.
2. Adapt each template to your own domain.
3. Try the CLI.

---

## What this toolkit is not

- not a substitute for legal, security, compliance, or medical advice;
- not a guarantee of correctness for any specific decision;
- not a project management or task tracking tool;
- not a content calendar.

It is a structured starting point for moving research from private thoughts to public artifacts and feedback.

---

## License

MIT. See [`LICENSE`](LICENSE).
