# CLI

Install from a local clone:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

Create a starter brief:

```bash
r2d init decision_brief.json
```

Validate, score, and report:

```bash
r2d validate decision_brief.json
r2d score decision_brief.json
r2d score decision_brief.json --json
r2d report decision_brief.json --output decision_report.md
python -m r2d --help
```

Exit codes:

| Code | Meaning |
|---:|---|
| 0 | Command completed and no veto was triggered |
| 1 | Report produced but at least one veto was triggered |
| 2 | Schema/validation failure or protected output file |
| 3 | File or JSON input error |

The CLI validates structure and computes a transparent heuristic. It does not verify source content or authorize a decision.
