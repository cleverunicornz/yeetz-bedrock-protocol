"""The root AGENTS.md repository block equals the published fixed text, byte for byte."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check-agents-md.py"
FIXED = (ROOT / "templates/repository-block.md").read_text()
PROTOCOL = "<bedrock-protocol>\nRuntime-delivered text, not checked here.\n</bedrock-protocol>\n"


class CheckAgentsMd(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.agents = Path(directory.name) / "AGENTS.md"

    def check(self, text):
        self.agents.write_bytes(text.encode())
        return subprocess.run([sys.executable, str(SCRIPT), "--agents", str(self.agents),
                               "--template", str(ROOT / "templates/repository-block.md")],
                              capture_output=True, text=True)

    def test_fixed_text_passes(self):
        result = self.check(FIXED)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_the_user_level_protocol_block_is_not_checked(self):
        for text in (PROTOCOL + "\n" + FIXED, FIXED + "\n" + PROTOCOL):
            with self.subTest(text=text[:20]):
                result = self.check(text)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_one_byte_differs(self):
        variants = {
            "word": FIXED.replace("critical reading", "critical  reading"),
            "trailing newline": FIXED.rstrip("\n"),
            "crlf": FIXED.replace("\n", "\r\n"),
            "added rule": FIXED.replace("</bedrock-repository>", "Run the tests first.\n</bedrock-repository>"),
            "old template": "<bedrock-repository>\nIdentity: example/parser\n</bedrock-repository>\n",
        }
        for name, text in variants.items():
            with self.subTest(variant=name):
                result = self.check(text)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("byte for byte", result.stderr)

    def test_missing_or_repeated_block_fails(self):
        for text in ("", PROTOCOL, FIXED + FIXED):
            with self.subTest(text=text[:20]):
                result = self.check(text)
                self.assertEqual(result.returncode, 1)
                self.assertIn("exactly one", result.stderr)

    def test_missing_agents_md_fails(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--agents", str(self.agents),
                                 "--template", str(ROOT / "templates/repository-block.md")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AGENTS.md", result.stderr)


if __name__ == "__main__":
    unittest.main()
