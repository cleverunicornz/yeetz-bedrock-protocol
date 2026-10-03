"""Check actual response shapes and fixture selection before heavy replay."""
import hashlib
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "contract/tool-examples"
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location("bedrock_replay", HERE / "replay.py")
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


class ReplayArgumentTests(unittest.TestCase):
    def test_stored_content_response_has_no_reference_field(self):
        markdown = "Observed fixture result.\n"
        answer = {"markdown": markdown, "version": "object-version", "sha256": hashlib.sha256(markdown.encode()).hexdigest(), "state": "stored"}
        replay.check_reference_response({"op": "reference.get", "id": "R-fixture"}, answer, {"state": "stored", "sha256_of": markdown})

    def test_pointer_response_checks_the_record_identity(self):
        answer = {"reference": "R-other", "state": "stored", "record": {}}
        with self.assertRaises(AssertionError):
            replay.check_reference_response({"op": "reference.get", "id": "R-fixture"}, answer, {"state": "stored"})

    def test_stored_content_refuses_missing_version_or_wrong_digest(self):
        markdown = "Observed fixture result.\n"
        for answer in ({"markdown": markdown, "sha256": hashlib.sha256(markdown.encode()).hexdigest(), "state": "stored"},
                       {"markdown": markdown, "version": "object-version", "sha256": "0" * 64, "state": "stored"}):
            with self.assertRaises(AssertionError):
                replay.check_reference_response({"op": "reference.get", "id": "R-fixture"}, answer, {"state": "stored", "sha256_of": markdown})

    def test_mutation_intent_uses_named_stipulate_fixture(self):
        arguments = replay.fixture_arguments("stipulate", {"scope": "fixture-scope", "run": "fixture-run"})
        self.assertEqual((arguments["op"], arguments["verb"]), ("act", "stipulate"))
        self.assertIn("invariant", arguments["payload"])


if __name__ == "__main__":
    unittest.main()
