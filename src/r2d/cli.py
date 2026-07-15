"""CLI entry point for r2d."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
from .reporting import render_markdown
from .schema import validate
from .scoring import make_report


def _load(path: str) -> tuple[dict | None, str | None]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)
    return data, None


def _cmd_validate(path: str) -> int:
    doc, error = _load(path)
    if error:
        print(f"Input error: {error}", file=sys.stderr); return 3
    ok, errors, veto = validate(doc)
    if ok:
        print(f"Valid decision brief: {path}"); return 0
    print("Validation failed:")
    for item in errors + [f"VETO: {v}" for v in veto]:
        print(f" - {item}")
    return 2


def _cmd_score(path: str, as_json: bool = False) -> int:
    doc, error = _load(path)
    if error:
        print(f"Input error: {error}", file=sys.stderr); return 3
    ok, errors, _ = validate(doc)
    if errors:
        print("Validation errors must be fixed before scoring:", file=sys.stderr)
        for item in errors:
            print(f" - {item}", file=sys.stderr)
        return 2
    report = make_report(doc)
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Decision: {report['decision']}")
        print(f"Total: {report['total']}/{report['max']}")
        print(f"Normalized: {report['normalized_pct']}%")
        print(f"Veto: {'yes' if report['veto'] else 'no'}")
        if report["top_gaps"]:
            print("Top gaps:")
            for gap in report["top_gaps"]:
                print(f" - {gap}")
    return 1 if report["veto"] else 0


def _cmd_report(path: str, output: str) -> int:
    doc, error = _load(path)
    if error:
        print(f"Input error: {error}", file=sys.stderr); return 3
    ok, errors, _ = validate(doc)
    if errors:
        print("Validation errors must be fixed before reporting", file=sys.stderr); return 2
    report = make_report(doc)
    destination = Path(output); destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_markdown(doc, report), encoding="utf-8")
    print(f"Wrote {destination}")
    return 1 if report["veto"] else 0


def _cmd_init(output: str) -> int:
    source = Path(__file__).resolve().parents[2] / "examples" / "fictional-ai-governance-research-to-decision" / "decision_brief.json"
    destination = Path(output)
    if destination.exists():
        print(f"Refusing to overwrite existing file: {destination}", file=sys.stderr); return 2
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    print(f"Copied starter brief to {destination}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="r2d", description="Validate, score, and report a research-to-decision brief.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    validate_parser = sub.add_parser("validate"); validate_parser.add_argument("path")
    score_parser = sub.add_parser("score"); score_parser.add_argument("path"); score_parser.add_argument("--json", action="store_true")
    report_parser = sub.add_parser("report"); report_parser.add_argument("path"); report_parser.add_argument("--output", "-o", required=True)
    init_parser = sub.add_parser("init"); init_parser.add_argument("output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "validate": return _cmd_validate(args.path)
    if args.cmd == "score": return _cmd_score(args.path, args.json)
    if args.cmd == "report": return _cmd_report(args.path, args.output)
    if args.cmd == "init": return _cmd_init(args.output)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
