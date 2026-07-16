"""Tests for the r2d package."""
from copy import deepcopy
import json
import os
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
        self.assertEqual(self.doc.get("schema_version"), "0.6")
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

    def test_rejects_reserved_subdomains_trailing_dots_private_ips_and_legacy_hosts(self):
        for url in (
            "https://a.example.com/evidence",
            "https://example.org./evidence",
            "http://10.0.0.1/evidence",
            "http://192.168.1.1/evidence",
            "https://:443/missing-host",
            "http://2130706433/integer-loopback",
            "http://0x7f000001/hex-loopback",
            "http://127.1/short-loopback",
        ):
            with self.subTest(url=url):
                doc = deepcopy(self.doc)
                primary = next(claim for claim in doc["claims"] if claim["source_tier"] == "primary")
                primary["source_url"] = url
                ok, errors, _ = validate(doc)
                self.assertFalse(ok)
                self.assertTrue(any("source_url" in item for item in errors))

    def test_fragments_do_not_create_distinct_primary_sources(self):
        doc = deepcopy(self.doc)
        primary = [claim for claim in doc["claims"] if claim["source_tier"] == "primary"]
        self.assertGreaterEqual(len(primary), 2)
        primary[1]["source_url"] = primary[0]["source_url"] + "#different-fragment"
        report = make_report(doc)
        evidence = next(area for area in report["areas"] if area["name"] == "Evidence quality")
        self.assertIn("only 1 distinct human-checked primary-source URLs; need 2+", evidence["gaps"])

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

    def test_v06_requires_argument_quality_and_writing_review(self):
        doc = deepcopy(self.doc)
        doc["schema_version"] = "0.6"
        doc.pop("argument_quality", None)
        doc.pop("writing_review", None)
        ok, errors, _ = validate(doc)
        self.assertFalse(ok)
        self.assertTrue(any("argument_quality" in item for item in errors))
        self.assertTrue(any("writing_review" in item for item in errors))

    def test_rejects_unknown_or_non_string_schema_version(self):
        for version in ("9.9", 6, True, None):
            with self.subTest(version=version):
                doc = deepcopy(self.doc)
                doc["schema_version"] = version
                ok, errors, _ = validate(doc)
                self.assertFalse(ok)
                self.assertTrue(any("schema_version" in item for item in errors))

    def test_v06_rejects_incomplete_quality_review(self):
        doc = deepcopy(self.doc)
        doc.update({"schema_version": "0.6", "argument_quality": {}, "writing_review": {}})
        ok, errors, _ = validate(doc)
        self.assertFalse(ok)
        self.assertTrue(any("argument_quality.chain" in item for item in errors))
        self.assertTrue(any("writing_review.passes" in item for item in errors))

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

    def test_markdown_report_includes_v06_quality_review(self):
        output = render_markdown(self.doc, make_report(self.doc))
        self.assertIn("## Argument quality gates", output)
        self.assertIn("## Five-pass writing review", output)
        self.assertIn("human-with-ai-assistance", output)
        self.assertIn("counterevidence", output.lower())

    def test_cli_validate_score_report_and_init(self):
        self.assertEqual(main(["validate", str(EXAMPLE)]), 0)
        self.assertEqual(main(["score", str(EXAMPLE), "--json"]), 0)
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            starter = Path(tmp) / "starter.json"
            self.assertEqual(main(["report", str(EXAMPLE), "-o", str(report)]), 0)
            self.assertIn("# Decision packet", report.read_text(encoding="utf-8"))
            self.assertEqual(main(["init", str(starter)]), 0)
            self.assertEqual(json.loads(starter.read_text(encoding="utf-8")), self.doc)
            self.assertEqual(main(["init", str(starter)]), 2)

    def test_report_refuses_to_overwrite_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "brief.json"
            source.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
            original = source.read_bytes()
            with patch("sys.stderr"):
                self.assertEqual(main(["report", str(source), "--output", str(source)]), 2)
            self.assertEqual(source.read_bytes(), original)

    def test_report_refuses_hardlink_alias_of_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "brief.json"
            alias = Path(tmp) / "hardlink-report.md"
            source.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
            os.link(source, alias)
            original = source.read_bytes()
            with patch("sys.stderr"):
                self.assertEqual(main(["report", str(source), "--output", str(alias)]), 2)
            self.assertEqual(source.read_bytes(), original)

    def test_report_refuses_symlink_alias_of_source_when_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "brief.json"
            alias = Path(tmp) / "symlink-report.md"
            source.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
            try:
                os.symlink(source, alias)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symbolic links are not available in this environment: {exc}")
            original = source.read_bytes()
            with patch("sys.stderr"):
                self.assertEqual(main(["report", str(source), "--output", str(alias)]), 2)
            self.assertEqual(source.read_bytes(), original)

    def test_report_returns_one_for_valid_but_not_ready_brief(self):
        doc = deepcopy(self.doc)
        for claim in doc["claims"]:
            claim["gap_that_changes_mind"] = ""
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "brief.json"
            output = Path(tmp) / "report.md"
            source.write_text(json.dumps(doc), encoding="utf-8")
            self.assertEqual(main(["report", str(source), "--output", str(output)]), 1)
            self.assertTrue(output.exists())

    def test_cli_returns_input_error_for_bad_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"; path.write_text("{", encoding="utf-8")
            with patch("sys.stderr"):
                self.assertEqual(main(["validate", str(path)]), 3)


if __name__ == "__main__":
    unittest.main()
