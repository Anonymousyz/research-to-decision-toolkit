from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentationBoundaryTests(unittest.TestCase):
    def test_all_external_model_prompts_have_information_boundary(self):
        paths = list((ROOT / "prompts").glob("*.md"))
        paths += [path for path in (ROOT / "modules").rglob("*.md") if "prompts" in path.parts]
        self.assertTrue(paths)
        for path in paths:
            text = path.read_text(encoding="utf-8-sig").lower()
            self.assertIn("authorized", text, path.name)
            self.assertIn("confidential", text, path.name)
            self.assertIn("human", text, path.name)

    def test_public_transform_does_not_treat_anonymization_as_permission(self):
        for name in ("public-artifact-transform-prompt.md", "feedback-porting-prompt.md"):
            text = (ROOT / "prompts" / name).read_text(encoding="utf-8-sig").lower()
            self.assertIn("anonymization", text)
            self.assertIn("not", text)
            self.assertIn("permission", text)

    def test_scorecard_matches_four_current_area_names(self):
        text = (ROOT / "scorecards" / "decision-readiness-scorecard.md").read_text(encoding="utf-8-sig")
        for heading in ("Decision framing", "Evidence quality", "Decision review", "Artifact and feedback"):
            self.assertIn(heading, text)
        self.assertNotIn("Artifact plan — 6 points", text)
        self.assertNotIn("Feedback loop — 6 points", text)

    def test_package_and_citation_versions_match_release(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8-sig")
        init = (ROOT / "src" / "r2d" / "__init__.py").read_text(encoding="utf-8-sig")
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8-sig")
        p_ver = re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE).group(1)
        i_ver = re.search(r'__version__ = "([^"]+)"', init).group(1)
        c_ver = re.search(r'^version: ([^\s]+)', citation, re.MULTILINE).group(1)
        self.assertEqual((p_ver, i_ver, c_ver), ("0.6.0", "0.6.0", "0.6.0"))

    def test_supplementary_scorecards_do_not_claim_the_cli_scale(self):
        decision_review = (ROOT / "modules" / "decision-review" / "scorecards" / "decision-quality-scorecard.md").read_text(encoding="utf-8-sig").lower()
        evidence = (ROOT / "scorecards" / "research-evidence-scorecard.md").read_text(encoding="utf-8-sig").lower()
        self.assertIn("supplementary 16-point manual review aid", decision_review)
        self.assertIn("not part of the cli's canonical 24-point", decision_review)
        self.assertIn("does not use the cli's canonical 24-point scale", evidence)

    def test_example_readme_matches_cli_verdict(self):
        text = (ROOT / "examples" / "fictional-ai-governance-research-to-decision" / "README.md").read_text(encoding="utf-8-sig")
        self.assertIn("Structurally ready for human decision meeting", text)
        self.assertIn("23/24", text)

    def test_ai_deployment_handoff_guide_is_bounded_and_linked(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
        guide = (ROOT / "docs" / "using_r2d_after_ai_prototype_review.md").read_text(encoding="utf-8-sig").lower()
        self.assertIn("docs/using_r2d_after_ai_prototype_review.md", readme)
        self.assertIn("prototype-to-production-toolkit", guide)
        self.assertIn("neither cli passes an assessment automatically", guide)
        self.assertIn("does not verify the source material", guide)

    def test_v06_quality_modules_are_linked_and_bounded(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
        for module in ("argument-quality", "judgment-writing"):
            path = ROOT / "modules" / module / "README.md"
            self.assertTrue(path.exists(), module)
            text = path.read_text(encoding="utf-8-sig").lower()
            self.assertIn(f"modules/{module}/", readme)
            self.assertIn("human", text)
            self.assertIn("not", text)

    def test_release_distribution_and_current_path_contract(self):
        manifest = (ROOT / "MANIFEST.in").read_text(encoding="utf-8-sig")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8-sig")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8-sig")
        argument_doc = (ROOT / "modules" / "argument-quality" / "README.md").read_text(encoding="utf-8-sig").lower()
        writing_doc = (ROOT / "modules" / "judgment-writing" / "README.md").read_text(encoding="utf-8-sig").lower()
        example = json.loads((ROOT / "examples" / "fictional-ai-governance-research-to-decision" / "decision_brief.json").read_text(encoding="utf-8"))
        packaged = json.loads((ROOT / "src" / "r2d" / "data" / "starter_decision_brief.json").read_text(encoding="utf-8"))
        for required in (
            "recursive-include docs",
            "recursive-include modules",
            "recursive-include examples",
            "recursive-include prompts",
            "recursive-include scorecards",
            "recursive-include templates",
            "include CITATION.cff",
            "include .gitignore",
        ):
            self.assertIn(required, manifest)
        self.assertNotIn("## v0.5.3", changelog)
        self.assertIn('license = "MIT"', pyproject)
        self.assertNotIn("License :: OSI Approved :: MIT License", pyproject)
        self.assertIn("free-text", argument_doc)
        self.assertIn("does not parse", argument_doc)
        self.assertIn("current disposition", writing_doc)
        self.assertEqual(example["writing_review"]["path"], "A")
        self.assertEqual(example, packaged)


if __name__ == "__main__":
    unittest.main()
