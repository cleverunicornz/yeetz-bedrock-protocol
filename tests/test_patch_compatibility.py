"""Finite CLI compatibility checks against manifest-only package inputs."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

import test_compiler as fixture

ROOT = fixture.ROOT


def entries(value):
    if isinstance(value, dict):
        if "path" in value:
            yield value
        else:
            for child in value.values():
                yield from entries(child)
    elif isinstance(value, list):
        for child in value:
            yield from entries(child)


class PatchCompatibilityTests(unittest.TestCase):
    setUp = fixture.CompilerTests.setUp

    def package(self):
        root = Path(self.tmp.name) / "bedrock"
        root.mkdir()
        for entry in entries(json.loads((ROOT / "manifest.json").read_text())):
            target = root / entry["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / entry["path"], target)
        for name in ("VERSION", "manifest.json"):
            shutil.copyfile(ROOT / name, root / name)
        return root

    def version(self, root, version):
        manifest = json.loads((root / "manifest.json").read_text())
        manifest["version"] = version
        (root / "manifest.json").write_text(json.dumps(manifest))
        (root / "VERSION").write_text(str(version) + "\n")

    def compile(self, protocol, part="full", output=None):
        cmd = [sys.executable, str(protocol / "compiler/compile.py"),
               "--protocol-root", str(protocol), "--org-root", str(self.org),
               "--repository", str(self.repo), "--part", part]
        if output:
            cmd.extend(["--output", str(output)])
        return subprocess.run(cmd, capture_output=True, text=True)

    def test_independent_stable_patches_compile_manifest_only_in_all_modes(self):
        protocol = self.package()
        for pv, ov in (("2.0.0", "2.0.1"), ("2.0.1", "2.0.0"), ("2.0.1", "2.0.37"),
                       ("2.1.0", "2.0.1"), ("2.1.0", "2.0.37"), ("2.1.3", "2.1.0"), ("2.0.1", "2.1.0")):
            self.version(protocol, pv)
            self.version(self.org, ov)
            for part in ("full", "user", "repository"):
                with self.subTest(protocol=pv, organization=ov, part=part):
                    result = self.compile(protocol, part)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("<bedrock-", result.stdout)

    def test_invalid_versions_fail_closed_for_each_package(self):
        protocol = self.package()
        invalid = ("1.0.1", "2.2.0", "2.10.0", "3.0.0", "2.0.01", "2.1.01", "2.01.0", "02.0.1", "2.00.1",
                   "2.0.1-rc.1", "2.0.1+build", "2.0", "v2.0.1", "2.0.1\n", "", None, 2, ["2.0.1"])
        self.version(self.org, "2.0.0")
        for root in (protocol, self.org):
            for version in invalid:
                with self.subTest(package=root.name, version=version):
                    self.version(root, version)
                    result = self.compile(protocol)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(result.stdout, "")
            self.version(root, "2.0.0")

    def test_each_package_requires_matching_version_file_before_output(self):
        protocol = self.package()
        self.version(protocol, "2.0.0")
        self.version(self.org, "2.0.0")
        output = Path(self.tmp.name) / "output.md"
        output.write_text("existing output\n")
        for root in (protocol, self.org):
            for content in (None, "2.0.1\n", "2.0.0-rc.1\n", " 2.0.0\n"):
                with self.subTest(package=root.name, version_file=content):
                    if content is None:
                        (root / "VERSION").unlink()
                    else:
                        (root / "VERSION").write_text(content)
                    result = self.compile(protocol, output=output)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(result.stdout, "")
                    self.assertEqual(output.read_text(), "existing output\n")
            self.version(root, "2.0.0")

    def test_patch_admission_never_bypasses_path_or_digest_checks(self):
        protocol = self.package()
        self.version(self.org, "2.0.1")
        manifest_path = self.org / "manifest.json"
        original = manifest_path.read_text()
        for mutation in ("digest", "escape", "absolute", "duplicate"):
            with self.subTest(mutation=mutation):
                manifest = json.loads(original)
                entry = manifest["organization"]
                if mutation == "digest":
                    entry["sha256"] = "0" * 64
                elif mutation == "escape":
                    entry["path"] = "../repository.json"
                elif mutation == "absolute":
                    entry["path"] = str(self.repo)
                else:
                    manifest["skills"].append(dict(entry))
                manifest["accepted_versions"] = ["2.0.1"]
                manifest_path.write_text(json.dumps(manifest))
                result = self.compile(protocol)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
