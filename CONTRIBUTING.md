# Contributing

Thanks for considering a contribution.

## How to contribute

1. Open an issue describing the change.
2. For new templates: include the artifact form (memo, scorecard, prompt) and a fictional example.
3. For new scoring rules: explain why a veto is appropriate, cite a public source.
4. Keep the JSON schema stable; non-breaking additions only.

## What we will not accept

- changes that require private organizational knowledge to understand;
- changes that introduce client, employer, or personally identifying examples;
- changes that lower the bar on evidence quality without a public rationale.

## Local checks

```bash
python -m pip install -e .
python tests/run_tests.py
```
