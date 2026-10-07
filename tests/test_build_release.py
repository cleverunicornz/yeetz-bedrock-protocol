"""The release assets are built deterministically from manifest-published files."""
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build-release.py"
spec = importlib.util.spec_from_file_location("build_release", SCRIPT)
build_release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_release)

# The published v2.0.1 release: its merge commit and its SHA256SUMS asset.
V201_COMMIT = "58ed6646c00726f877b66fab987d18f9719d1b5e"
V201_SUMS = ("e5b2a061d16f2d31195182f77646f4fbe56a17271dc26f3e7f7b64314befea91  bedrock-2.0.1.tar.gz\n"
             "6b921f05fc28c6869689743b434f6e8b2477c09336fbd35ee0b186ba235f1b26  manifest.json\n")


class BuildRelease(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.tmp = Path(directory.name)

    def test_reproduces_the_published_2_0_1_assets_byte_for_byte(self):
        source = self.tmp / "source"
        source.mkdir()
        archive = subprocess.run(["git", "-C", str(ROOT), "archive", V201_COMMIT], check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(source)], input=archive, check=True)
        build_release.build(source, self.tmp / "out")
        self.assertEqual((self.tmp / "out/SHA256SUMS").read_text(), V201_SUMS)

    def test_current_tree_builds_twice_to_the_same_bytes(self):
        first = build_release.build(ROOT, self.tmp / "one")
        second = build_release.build(ROOT, self.tmp / "two")
        version = (ROOT / "VERSION").read_text().strip()
        self.assertEqual(sorted(p.name for p in first.iterdir()), sorted([f"bedrock-{version}.tar.gz", "SHA256SUMS", "manifest.json"]))
        for name in ("SHA256SUMS", f"bedrock-{version}.tar.gz", "manifest.json"):
            self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())
        with tarfile.open(first / f"bedrock-{version}.tar.gz") as tar:
            names = tar.getnames()
        self.assertEqual(names, sorted(names))
        for required in ("bedrock/VERSION", "bedrock/manifest.json", "bedrock/templates/repository-block.md",
                         "bedrock/scripts/situation-projection.py", "bedrock/scripts/check-agents-md.py"):
            self.assertIn(required, names)

    def test_refuses_a_tree_whose_files_disagree_with_the_manifest(self):
        source = self.tmp / "source"
        source.mkdir()
        archive = subprocess.run(["git", "-C", str(ROOT), "archive", V201_COMMIT], check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(source)], input=archive, check=True)
        (source / "templates/repository-block.md").write_text("changed\n")
        with self.assertRaisesRegex(ValueError, "digest"):
            build_release.build(source, self.tmp / "out")


if __name__ == "__main__":
    unittest.main()
