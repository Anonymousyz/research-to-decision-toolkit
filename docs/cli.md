# Research-to-Decision CLI

A small validator and scorer for a decision-brief JSON file. The intent is operational, not pedantic: catch missing fields, surface weak spots, and produce a short report that can live next to a memo.

## Install

```bash
python -m pip install -e .
```

## Files

```text
research-to-decision-toolkit/
├── src/r2d/
│   ├── __init__.py
│   ├── cli.py
│   ├── scoring.py
│   └── schema.py
├── tests/test_r2d.py
└── examples/fictional-ai-governance-research-to-decision/decision_brief.json
```

## Commands

### Validate

```bash
r2d validate path/to/decision_brief.json
```

Confirms required fields and minimal structure. Exits 0 if valid.

### Score

```bash
r2d score path/to/decision_brief.json
```

Outputs a total score and a short list of gaps.

Example:

```text
Decision: Ready to ship
Total: 18/24
Normalized: 18/24 (75.0%)
Veto: no
Top gaps:
- No external reviewer named
- Feedback plan is implicit
```

## What the score actually measures

The scorer uses a 4-area rubric:

| Area | Weight | What we look for |
|---|---|---|
| Decision framing | 0–6 | Real decision, named decision body, deadline, default outcome |
| Evidence quality | 0–6 | Mix of facts / judgments / assumptions, gaps listed, weakest claim flagged |
| Artifact plan | 0–6 | Named artifact form, named readers, what survives the work |
| Feedback loop | 0–6 | Named channels, log template in place, threshold for next move |

A *veto* triggers when:

- no decision body is named;
- no default outcome if nothing happens;
- no gap is declared anywhere.

These are not opinions about the decision itself. They are blocking quality issues for the format.

## Why a CLI, not a notebook

The point is that the same JSON format can be:

- edited by hand;
- produced by an LLM;
- reviewed by someone else;
- archived next to the memo.

If the format is in a Jupyter notebook, none of that is easy.
