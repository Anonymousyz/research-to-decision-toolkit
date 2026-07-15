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
        self.assertEqual(report["decision"], "Structurally ready for human decision meeting")
        self.assertEqual(report["total"], 23)
        self.assertIn("feedback log is not yet filled", report["top_gaps"])

    def test_veto_overrides_high_score(self):
        doc = deepcopy(self.doc); doc["default_outcome"] = ""
        report = make_report(doc)
        self.assertTrue(vetoes(doc))
        self.assertEqual(report["decision"], "Not ready for human decision meeting: veto present")

    def test_rejects_non_object_document(self):
        ok, errors, veto = validate([])
        self.assertFalse(ok); self.assertIn("document must be a JSON object", errors); self.assertFalse(veto)

    def test_rejects_malformed_claim(self):
        doc = deepcopy(self.doc); doc["claims"][0]["type"] = "opinion"
        ok, errors, _ = validate(doc)
        self.assertFalse(ok); self.assertTrue(any("type must be one of" in item for item in errors))

    def test_primary_source_count_requires_urls(self):
        doc = deepcopy(self.doc)
        for claim in doc["claims"]:
            claim.pop("source_url", None)
        ok, errors, _ = validate(doc)
        self.assertFalse(ok)
        self.assertTrue(any("source_url is required for primary" in item for item in errors))

    def test_rejects_string_where_reader_list_is_required(self):
        doc = deepcopy(self.doc)
        doc["artifact"]["readers"] = "abc"
        ok, errors, _ = validate(doc)
        self.assertFalse(ok)
        self.assertTrue(any("artifact.readers must be a list" in item for item in errors))

    def test_rejects_reserved_domain_as_primary_source(self):
        doc = deepcopy(self.doc)
        primary = next(claim for claim in doc["claims"] if claim["source_tier"] == "primary")
        primary["source_url"] = "https://example.com/not-evidence"
        ok, errors, _ = validate(doc)
        self.assertFalse(ok)
        self.assertTrue(any("reserved or local domain" in item for item in errors))

    def test_requires_human_source_check_metadata_for_primary_sources(self):
        doc = deepcopy(self.doc)
        primary = next(claim for claim in doc["claims"] if claim["source_tier"] == "primary")
        primary.pop("source_checked_by", None)
        ok, errors, _ = validate(doc)
        self.assertFalse(ok)
        self.assertTrue(any("source_checked_by" in item for item in errors))

    def test_requires_decision_review_structure(self):
        doc = deepcopy(self.doc)
        doc.pop("decision_review", None)
        ok, errors, _ = validate(doc)
        self.assertFalse(ok)
        self.assertTrue(any("decision_review" in item for item in errors))

    def test_cli_scores_structural_veto_and_returns_one(self):
        doc = deepcopy(self.doc)
        doc["default_outcome"] = ""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "veto.json"
            path.write_text(json.dumps(doc), encoding="utf-8")
            self.assertEqual(main(["score", str(path)]), 1)

    def test_score_uses_decision_review_and_combined_artifact_feedback_area(self):
        report = make_report(self.doc)
        self.assertEqual(
            [area["name"] for area in report["areas"]],
            ["Decision framing", "Evidence quality", "Decision review", "Artifact and feedback"],
        )

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
            self.assertIn("# Decision packet", report.read_text(encoding="utf-8"))
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
