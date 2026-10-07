"""The two reusable repository checks: pinned to a protocol release, verified before use.

The release-verification step is executed exactly as the workflows carry it,
against release assets built by scripts/build-release.py and served from a
local directory. CI also lints both workflows with actionlint and shellcheck.
"""
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ("check-agents-md.yml", "situation-projection.yml")
spec = importlib.util.spec_from_file_location("build_release", ROOT / "scripts/build-release.py")
build_release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_release)


def workflow(name):
    return yaml.safe_load((ROOT / ".github/workflows" / name).read_text())


def step(name, title):
    [job] = workflow(name)["jobs"].values()
    return next(s for s in job["steps"] if s.get("name") == title)


class Shape(unittest.TestCase):
    def test_called_with_a_pinned_protocol_version(self):
        for name in WORKFLOWS:
            with self.subTest(workflow=name):
                text = (ROOT / ".github/workflows" / name).read_text()
                call = workflow(name)[True]["workflow_call"]  # YAML reads the key `on` as True
                self.assertEqual(call["inputs"]["version"], {
                    "description": call["inputs"]["version"]["description"], "required": True, "type": "string"})
                self.assertIn("releases/download/v${{ inputs.version }}", text)
                self.assertIn(f"uses: cleverunicornz/yeetz-bedrock-protocol/.github/workflows/{name}@v2.1.0", text)
                for uses in re.findall(r"(?m)^\s+(?:- )?uses: (\S+)", text):
                    self.assertRegex(uses, r"@[0-9a-f]{40}$", "actions are pinned by commit")

    def test_verification_steps_are_identical(self):
        title = "Fetch and verify the protocol release"
        self.assertEqual(step(WORKFLOWS[0], title)["run"], step(WORKFLOWS[1], title)["run"])

    def test_agents_check_runs_the_published_checker(self):
        run = step("check-agents-md.yml", "AGENTS.md repository block equals the fixed text")["run"]
        self.assertIn("bedrock/scripts/check-agents-md.py --agents repository/AGENTS.md --template bedrock/templates/repository-block.md", run)

    def test_projection_commits_to_the_head_and_refuses_forks_with_instructions(self):
        text = (ROOT / ".github/workflows/situation-projection.yml").read_text()
        [job] = workflow("situation-projection.yml")["jobs"].values()
        self.assertEqual(job["if"], "github.event_name == 'pull_request' && !github.event.repository.private")
        self.assertIn("push_token", workflow("situation-projection.yml")[True]["workflow_call"]["secrets"])
        self.assertIn("bedrock/scripts/situation-projection.py --root repository", text)
        self.assertIn("github.event.pull_request.head.sha", text)
        self.assertIn("comes from a fork, so it cannot be committed here", text)
        self.assertIn("git push origin", text)
        self.assertIn("--check", text)
        self.assertNotIn("[skip ci]", text)

    def test_public_neutral_wording(self):
        for name in WORKFLOWS + ("../../scripts/situation-projection.py", "../../scripts/check-agents-md.py"):
            text = (ROOT / ".github/workflows" / name).read_text()
            for private in ("clever-unicorn-org", "infra-v2", "org_read_token", "Paseo", "I-0000"):
                self.assertNotIn(private, text, name)


class ReleaseVerification(unittest.TestCase):
    """Run the workflows' verification step against a locally served release."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.tmp = Path(directory.name)
        self.version = (ROOT / "VERSION").read_text().strip()
        self.assets = build_release.build(ROOT, self.tmp / "assets")
        self.script = step("check-agents-md.yml", "Fetch and verify the protocol release")["run"]

    def verify(self, version=None):
        work = self.tmp / "work"
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir()
        env = {**os.environ, "VERSION": version or self.version, "RELEASE_BASE": self.assets.resolve().as_uri()}
        return subprocess.run(["bash", "-c", self.script], cwd=work, env=env, capture_output=True, text=True), work

    def test_verified_release_supplies_the_published_files(self):
        result, work = self.verify()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"verified protocol release v{self.version}", result.stdout)
        self.assertEqual((work / "bedrock/templates/repository-block.md").read_bytes(),
                         (ROOT / "templates/repository-block.md").read_bytes())
        agents = subprocess.run(["python3", "bedrock/scripts/check-agents-md.py", "--agents",
                                 str(ROOT / "templates/repository-block.md"), "--template",
                                 "bedrock/templates/repository-block.md"], cwd=work, capture_output=True, text=True)
        self.assertEqual(agents.returncode, 0, agents.stderr)

    def test_archive_not_matching_its_checksum_is_refused(self):
        archive = self.assets / f"bedrock-{self.version}.tar.gz"
        archive.write_bytes(archive.read_bytes() + b"\0")
        result, _ = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAILED", result.stdout + result.stderr)

    def test_file_not_matching_the_manifest_is_refused_even_with_a_matching_checksum(self):
        archive = self.assets / f"bedrock-{self.version}.tar.gz"
        members = []
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                data = tar.extractfile(member).read()
                if member.name == "bedrock/templates/repository-block.md":
                    data = data.replace(b"critical reading", b"optional reading")
                    member.size = len(data)
                members.append((member, data))
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
            for member, data in members:
                tar.addfile(member, io.BytesIO(data))
        archive.write_bytes(buffer.getvalue())
        sums = (self.assets / "SHA256SUMS").read_text().splitlines()
        sums[0] = f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}"
        (self.assets / "SHA256SUMS").write_text("\n".join(sums) + "\n")
        result, _ = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("templates/repository-block.md differs from its manifest digest", result.stderr)

    def test_checksum_list_without_the_archive_is_refused(self):
        (self.assets / "SHA256SUMS").write_text("0" * 64 + "  manifest.json\n")
        result, _ = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not name", result.stdout)


if __name__ == "__main__":
    unittest.main()
