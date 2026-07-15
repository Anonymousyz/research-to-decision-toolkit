from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentationBoundaryTests(unittest.TestCase):
    def test_all_external_model_prompts_have_information_boundary(self):
        for path in (ROOT / "prompts").glob("*.md"):
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

    def test_package_versions_match(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8-sig")
        init = (ROOT / "src" / "r2d" / "__init__.py").read_text(encoding="utf-8-sig")
        p_ver = re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE).group(1)
        i_ver = re.search(r'__version__ = "([^"]+)"', init).group(1)
        self.assertEqual(p_ver, i_ver)
        self.assertEqual(p_ver, "0.5.0")

    def test_example_readme_matches_cli_verdict(self):
        text = (ROOT / "examples" / "fictional-ai-governance-research-to-decision" / "README.md").read_text(encoding="utf-8-sig")
        self.assertIn("Structurally ready for human decision meeting", text)
        self.assertIn("23/24", text)


if __name__ == "__main__":
    unittest.main()
