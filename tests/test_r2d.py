"""Tests for the r2d package."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from r2d.cli import main
from r2d.reporting import render_markdown
from r2d.schema import validate
from r2d.scoring import make_report, vetoes

EXAMPLE = ROOT / "examples" / "fictional-ai-governance-research-to-decision" / "decision_brief.json"


class R2DTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_example_validates(self):
        ok, errors, veto = validate(self.doc)
        self.assertTrue(ok, f"errors={errors} veto={veto}")

    def test_scorecard_has_four_six_point_areas(self):
        report = make_report(self.doc)
        self.assertEqual(report["max"], 24)
        self.assertEqual(len(report["areas"]), 4)
        self.assertTrue(all(area["max"] == 6 for area in report["areas"]))
        self.assertEqual(sum(area["score"] for area in report["areas"]), report["total"])

    def test_example_is_ready_but_has_feedback_gap(self):
        report = make_report(self.doc)
        self.assertEqual(report["decision"], "Ready for decision meeting")
        self.assertEqual(report["total"], 23)
        self.assertIn("feedback log is not yet filled", report["top_gaps"])

    def test_veto_overrides_high_score(self):
        doc = deepcopy(self.doc); doc["default_outcome"] = ""
        report = make_report(doc)
        self.assertTrue(vetoes(doc))
        self.assertEqual(report["decision"], "Do not proceed: veto present")

    def test_rejects_non_object_document(self):
        ok, errors, veto = validate([])
        self.assertFalse(ok); self.assertIn("document must be a JSON object", errors); self.assertTrue(veto)

    def test_rejects_malformed_claim(self):
        doc = deepcopy(self.doc); doc["claims"][0]["type"] = "opinion"
        ok, errors, _ = validate(doc)
        self.assertFalse(ok); self.assertTrue(any("type must be one of" in item for item in errors))

    def test_primary_source_count_requires_urls(self):
        doc = deepcopy(self.doc)
        for claim in doc["claims"]:
            claim.pop("source_url", None)
        report = make_report(doc)
        evidence = next(area for area in report["areas"] if area["name"] == "Evidence quality")
        self.assertIn("only 0 distinct primary-source URLs; need 2+", evidence["gaps"])

    def test_markdown_report_discloses_method_boundary(self):
        output = render_markdown(self.doc, make_report(self.doc))
        self.assertIn("uncalibrated decision-support heuristic", output)
        self.assertIn("| Evidence quality |", output)

    def test_cli_validate_score_report_and_init(self):
        self.assertEqual(main(["validate", str(EXAMPLE)]), 0)
        self.assertEqual(main(["score", str(EXAMPLE), "--json"]), 0)
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            starter = Path(tmp) / "starter.json"
            self.assertEqual(main(["report", str(EXAMPLE), "-o", str(report)]), 0)
            self.assertIn("# Decision-readiness report", report.read_text(encoding="utf-8"))
            self.assertEqual(main(["init", str(starter)]), 0)
            self.assertTrue(starter.exists())
            self.assertEqual(main(["init", str(starter)]), 2)

    def test_cli_returns_input_error_for_bad_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"; path.write_text("{", encoding="utf-8")
            with patch("sys.stderr"):
                self.assertEqual(main(["validate", str(path)]), 3)


if __name__ == "__main__":
    unittest.main()
