"""Tests for r2d package."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
if str(ROOT / 'src') not in sys.path:
    sys.path.insert(0, str(ROOT / 'src'))

from r2d.schema import validate
from r2d.scoring import make_report, vetos

EX = ROOT / "examples" / "fictional-ai-governance-research-to-decision" / "decision_brief.json"

class R2DTests(unittest.TestCase):
    def test_load_example_validates(self):
        self.assertTrue(EX.exists(), f"missing example file at {EX}")
        doc = json.loads(EX.read_text(encoding="utf-8"))
        ok, errs, veto = validate(doc)
        self.assertTrue(ok, f"expected valid example; got errs={errs} veto={veto}")

    def test_scorecard_max_is_24(self):
        doc = json.loads(EX.read_text(encoding="utf-8"))
        rep = make_report(doc)
        self.assertEqual(rep["max"], 24)
        self.assertGreaterEqual(rep["total"], 0)

    def test_veto_items_is_list(self):
        doc = json.loads(EX.read_text(encoding="utf-8"))
        v = vetos(doc)
        self.assertIsInstance(v, list)

if __name__ == '__main__':
    unittest.main()
