from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

from .schema import validate
from .scoring import make_report, render_json, render_markdown


def _load(path: str) -> dict:
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON parse error: {exc}") from exc
    if not isinstance(doc, dict):
        raise ValueError("decision brief must be a JSON object")
    return doc


def _print_validation(errors: list[str], vetoes: list[str]) -> None:
    for item in errors:
        print(f"ERROR: {item}")
    for item in vetoes:
        print(f"VETO: {item}")


def _cmd_validate(path: str) -> int:
    try:
        doc = _load(path)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 3
    _, errors, vetoes = validate(doc)
    if errors:
        _print_validation(errors, vetoes)
        return 2
    if vetoes:
        print("Structurally valid decision brief, but veto items block readiness:")
        _print_validation([], vetoes)
        return 1
    print(f"Valid decision brief: {path}")
    return 0


def _cmd_score(path: str, fmt: str) -> int:
    try:
        doc = _load(path)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 3
    _, errors, vetoes = validate(doc)
    if errors:
        _print_validation(errors, vetoes)
        return 2
    report = make_report(doc)
    if fmt == "json":
        print(render_json(report))
    else:
        print(f"Decision: {report['decision']}")
        print(f"Total: {report['total']}/{report['maximum']}")
        print(f"Normalized: {report['normalized_pct']}%")
        print(f"Veto: {'yes' if report['veto'] else 'no'}")
        if report["top_gaps"]:
            print("Top gaps:")
            for gap in report["top_gaps"]:
                print(f"- {gap}")
    return 1 if report["veto"] or report["total"] < 18 else 0


def _same_file(left: Path, right: Path) -> bool:
    try:
        if left.exists() and right.exists() and left.samefile(right):
            return True
    except OSError:
        pass
    return left.resolve() == right.resolve()


def _cmd_report(path: str, output: str) -> int:
    source = Path(path)
    destination = Path(output)
    if _same_file(source, destination):
        print("Refusing to overwrite the source decision brief", file=sys.stderr)
        return 2
    try:
        doc = _load(path)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 3
    _, errors, vetoes = validate(doc)
    if errors:
        _print_validation(errors, vetoes)
        return 2
    report = make_report(doc)
    resolved_destination = destination.resolve()
    resolved_destination.parent.mkdir(parents=True, exist_ok=True)
    resolved_destination.write_text(render_markdown(doc, report), encoding="utf-8")
    print(f"Wrote {resolved_destination}")
    return 1 if report["veto"] or report["total"] < 18 else 0


def _cmd_init(output: str) -> int:
    packaged = Path(__file__).resolve().parent / "data" / "starter_decision_brief.json"
    source_tree = (
        Path(__file__).resolve().parents[2]
        / "examples"
        / "fictional-ai-governance-research-to-decision"
        / "decision_brief.json"
    )
    source = packaged if packaged.exists() else source_tree
    if not source.exists():
        print("Could not locate the packaged starter decision brief", file=sys.stderr)
        return 3
    destination = Path(output)
    if destination.exists():
        print(f"Refusing to overwrite existing file: {destination}", file=sys.stderr)
        return 2
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    print(f"Copied starter brief to {destination}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="r2d", description="Research-to-decision workflow toolkit")
    sub = parser.add_subparsers(dest="command", required=True)
    validate_parser = sub.add_parser("validate", help="Validate a decision brief")
    validate_parser.add_argument("path")
    score_parser = sub.add_parser("score", help="Score workflow completeness")
    score_parser.add_argument("path")
    score_parser.add_argument("--format", choices=("text", "json"), default="text")
    score_parser.add_argument("--json", action="store_true", help="Backward-compatible alias for --format json")
    report_parser = sub.add_parser("report", help="Write a Markdown decision packet")
    report_parser.add_argument("path")
    report_parser.add_argument("--output", "-o", required=True)
    init_parser = sub.add_parser("init", help="Copy the fictional starter brief")
    init_parser.add_argument("output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        return _cmd_validate(args.path)
    if args.command == "score":
        return _cmd_score(args.path, "json" if args.json else args.format)
    if args.command == "report":
        return _cmd_report(args.path, args.output)
    if args.command == "init":
        return _cmd_init(args.output)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
