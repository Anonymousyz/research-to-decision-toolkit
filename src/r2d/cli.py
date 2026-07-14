
"""CLI entry point for r2d."""
import argparse, json, sys
from pathlib import Path
from .schema import validate
from .scoring import make_report

def _cmd_validate(path):
    text = Path(path).read_text(encoding="utf-8")
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as e:
        print("JSON parse error:", e)
        return 3
    ok, errs, veto = validate(doc)
    if ok:
        print("Valid decision brief:", path)
        return 0
    print("Validation failed:")
    for e in errs + [f"VETO: {v}" for v in veto]:
        print(" -", e)
    return 2

def _cmd_score(path):
    text = Path(path).read_text(encoding="utf-8")
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as e:
        print("JSON parse error:", e)
        return 3
    rep = make_report(doc)
    veto = rep["veto"]
    print("Decision:", rep["decision"])
    print(f"Total: {rep['total']}/{rep['max']}")
    print(f"Normalized: {rep['total']}/{rep['max']} ({rep['normalized_pct']}%)")
    print("Veto:", "yes" if veto else "no")
    if rep["top_gaps"]:
        print("Top gaps:")
        for g in rep["top_gaps"]:
            print(" -", g)
    return 0

def main(argv=None):
    p = argparse.ArgumentParser(prog="r2d")
    sub = p.add_subparsers(dest="cmd", required=True)
    pv = sub.add_parser("validate")
    pv.add_argument("path")
    ps = sub.add_parser("score")
    ps.add_argument("path")
    args = p.parse_args(argv)
    if args.cmd == "validate":
        return _cmd_validate(args.path)
    if args.cmd == "score":
        return _cmd_score(args.path)
    return 1

if __name__ == "__main__":
    sys.exit(main())
