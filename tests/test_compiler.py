"""Physical CLI checks of the three-part compiler and duplication boundary."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CompilerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.org = Path(self.tmp.name) / "org"
        self.org.mkdir()
        (self.org / "VERSION").write_text("2.0.0\n")
        (self.org / "templates").mkdir(parents=True)
        (self.org / "skills/operate").mkdir(parents=True)
        (self.org / "templates/organization.md").write_text(
            '<bedrock-organization>\nUse organisation scope example-org.\nRead org/skills/operate/SKILL.md for operations.\n</bedrock-organization>\n')
        (self.org / "skills/operate/SKILL.md").write_text(
            '---\nname: operate\nverb: produce\ndescription: Perform operations.\n---\n# operate\nKeep observations with their coordinates.\n')
        entries = lambda paths: [{"path": p, "sha256": hashlib.sha256((self.org / p).read_bytes()).hexdigest()} for p in paths]
        (self.org / "manifest.json").write_text(json.dumps({"version": "2.0.0", "description": "fixture", "organization": entries(["templates/organization.md"])[0], "skills": entries(["skills/operate/SKILL.md"]), "organization_situation": []}))
        self.repo = Path(self.tmp.name) / "repository.json"
        self.repo.write_text(json.dumps({"identity": "example/parser", "ownership": "OWNED", "scope": "example-parser", "bootstrap": "Tool access is provided by the runtime."}))

    def run_compile(self, *extra, repository=True):
        repo = ["--repository", str(self.repo)] if repository else []
        return subprocess.run([sys.executable, str(ROOT / "compiler/compile.py"), "--protocol-root", str(ROOT), "--org-root", str(self.org), *repo, *extra], capture_output=True, text=True)

    def test_composes_short_axioms_and_pointers(self):
        result = self.run_compile()
        self.assertEqual(result.returncode, 0, result.stderr)
        for marker in ("bedrock-protocol", "bedrock-organization", "bedrock-repository"):
            self.assertIn("<" + marker + ">", result.stdout)
        self.assertEqual(result.stdout.count("A Promise is"), 1)
        self.assertIn("bedrock/skills/mint/SKILL.md", result.stdout)
        self.assertIn("A Plan is a group of Candidates, Promises and Gaps", result.stdout)
        self.assertNotIn("example/parser", result.stdout)
        self.assertLess(len(result.stdout.splitlines()), 85)
        self.assertNotIn("situation/ is canonical", result.stdout)

    def test_split_installation_does_not_copy_repository_into_user(self):
        user = self.run_compile("--part", "user")
        repo = self.run_compile("--part", "repository")
        self.assertEqual(user.returncode, 0, user.stderr)
        self.assertEqual(repo.returncode, 0, repo.stderr)
        self.assertNotIn("bedrock-repository", user.stdout)
        self.assertNotIn("A Promise is", repo.stdout)

    def test_repository_block_is_the_fixed_text_byte_for_byte(self):
        fixed = (ROOT / "templates/repository-block.md").read_text()
        self.assertTrue(fixed.startswith("<bedrock-repository>\nThis repository is operated through the organisation's situation graph."))
        self.assertNotIn("{{", fixed)
        for repository in (True, False):
            with self.subTest(repository_input=repository):
                result = self.run_compile("--part", "repository", repository=repository)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, fixed)

    def test_repository_input_is_optional_and_never_rendered(self):
        result = self.run_compile(repository=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn((ROOT / "templates/repository-block.md").read_text().strip(), result.stdout)
        with_input = self.run_compile()
        self.assertEqual(with_input.stdout, result.stdout)

    def test_rejects_unverified_org_bytes(self):
        (self.org / "templates/organization.md").write_text("Changed without a manifest update.")
        result = self.run_compile()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("digest", result.stderr.lower())

    def test_rejects_record_copies_in_repository_input(self):
        self.repo.write_text(json.dumps({"identity": "example/parser", "ownership": "OWNED", "scope": "example-parser", "promises": ["copied record"]}))
        result = self.run_compile()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("promises", result.stderr)

    def test_duplicate_sentence_cli_normalizes_soft_wrap_and_markdown(self):
        agents = Path(self.tmp.name) / "AGENTS.md"
        skill = Path(self.tmp.name) / "SKILL.md"
        agents.write_text("- Keep **observations** with\n  their coordinates.\n")
        skill.write_text("# procedure\nKeep observations with their coordinates.\n")
        result = subprocess.run([sys.executable, str(ROOT / "compiler/check_sentences.py"), "--agents", str(agents), "--skills", str(skill)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("duplicated", result.stderr.lower())
        self.assertIn("SKILL.md", result.stderr)

    def test_compiler_checks_the_paired_org_skills(self):
        (self.org / "templates/organization.md").write_text('<bedrock-organization>\nKeep observations with their coordinates.\n</bedrock-organization>\n')
        data = json.loads((self.org / "manifest.json").read_text())
        data["organization"]["sha256"] = hashlib.sha256((self.org / "templates/organization.md").read_bytes()).hexdigest()
        (self.org / "manifest.json").write_text(json.dumps(data))
        result = self.run_compile()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicated", result.stderr.lower())

    def check_duplicate_form(self, skill_text):
        agents = Path(self.tmp.name) / "AGENTS.md"
        skill = Path(self.tmp.name) / "SKILL.md"
        agents.write_text("Keep observations with their coordinates.\n")
        skill.write_text(skill_text)
        result = subprocess.run([sys.executable, str(ROOT / "compiler/check_sentences.py"), "--agents", str(agents), "--skills", str(skill)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("duplicated", result.stderr.lower())

    def test_table_cell_sentence_duplication(self):
        self.check_duplicate_form("| Rule | Procedure |\n|---|---|\n| Evidence | Keep observations with their coordinates. |\n")

    def test_front_matter_description_sentence_duplication(self):
        self.check_duplicate_form('---\nname: operate\nverb: produce\ndescription: "Keep observations with their coordinates."\n---\n# operate\nDifferent body.\n')

    def test_folded_front_matter_description_sentence_duplication(self):
        self.check_duplicate_form("---\nname: operate\nverb: produce\ndescription: >-\n  Keep observations with\n  their coordinates.\n---\n# operate\nDifferent body.\n")

    def test_markdown_front_matter_description_sentence_duplication(self):
        self.check_duplicate_form("---\nname: operate\nverb: produce\ndescription: Keep **observations** with their coordinates.\n---\n# operate\nDifferent body.\n")

    def test_manifest_publishes_procedure_and_decision_dependencies(self):
        def paths(value):
            if isinstance(value, dict):
                return ({value["path"]} if "path" in value else set().union(*(paths(v) for v in value.values())))
            if isinstance(value, list):
                return set().union(*(paths(v) for v in value))
            return set()
        published = paths(json.loads((ROOT / "manifest.json").read_text()))
        required = {"contract/tool-examples/calls.json", "contract/tool-examples/probe.py", "migrations/2.0.0-draft-to-2.0.0.md"}
        self.assertFalse(required - published, f"unpublished required inputs: {sorted(required - published)}")


if __name__ == "__main__":
    unittest.main()
