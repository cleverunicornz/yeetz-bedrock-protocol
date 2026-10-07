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


class AdditiveRetractionTests(unittest.TestCase):
    """The pinned receiver vendors the 2.0 contract; 2.1 must be 2.0 plus exactly the declared additions."""

    BASELINE = "58ed6646c00726f877b66fab987d18f9719d1b5e"  # the v2.0.1 release commit

    def baseline(self, path):
        import subprocess
        return subprocess.run(["git", "-C", str(ROOT), "show", f"{self.BASELINE}:{path}"],
                              check=True, capture_output=True, text=True).stdout

    def test_retracting_the_2_1_additions_gives_the_2_0_contract_and_schema(self):
        import json
        import yaml
        local = yaml.safe_load((HERE.parent / "bedrock-v2.yaml").read_text())
        schema = json.loads((HERE.parent / "bedrock-v2.schema.json").read_text())
        base = yaml.safe_load(self.baseline("contract/bedrock-v2.yaml"))
        base_schema = json.loads(self.baseline("contract/bedrock-v2.schema.json"))
        local, schema = replay.retract_additions(local, schema)
        for contract in (base, local):
            contract.pop("bedrock")
        for s in (base_schema, schema):
            s["properties"]["protocol"].pop("const", None)
            s.pop("title", None)
        self.assertEqual(local, base)
        self.assertEqual(schema, base_schema)

    def test_retraction_does_not_hide_other_changes(self):
        import json
        import yaml
        local = yaml.safe_load((HERE.parent / "bedrock-v2.yaml").read_text())
        schema = json.loads((HERE.parent / "bedrock-v2.schema.json").read_text())
        local["nouns"]["Gap"]["states"].append("parked")
        retracted, _ = replay.retract_additions(local, schema)
        self.assertIn("parked", retracted["nouns"]["Gap"]["states"])


if __name__ == "__main__":
    unittest.main()
