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

    def current(self):
        import json
        import yaml
        return (yaml.safe_load((HERE.parent / "bedrock-v2.yaml").read_text()),
                json.loads((HERE.parent / "bedrock-v2.schema.json").read_text()))

    def test_a_change_inside_a_retracted_field_is_refused(self):
        """Each field the retraction rewrites must hold exactly the declared 2.1 value."""
        mutations = {
            "binds answers": lambda c, s: c["queries"]["binds"].__setitem__("answers", "Promises revoked only."),
            "plan members": lambda c, s: c["group"]["Plan"].__setitem__("members", ["Candidate", "Gap", "Promise"]),
            "plan members prose": lambda c, s: c["group"]["Plan"]["fields"].__setitem__("members", "any ids"),
            "plan member work": lambda c, s: c["group"]["Plan"]["member_work"]["Gap"].__setitem__("outcome", "judge"),
            "plan assigns": lambda c, s: c["group"]["Plan"].__setitem__("assigns", "the orchestrator"),
            "bad_member": lambda c, s: c["refusals"].__setitem__("bad_member", "anything goes"),
            "regroup members": lambda c, s: c["structural_acts"]["regroup"].__setitem__("members", ["Gap"]),
            "invariant field": lambda c, s: c["nouns"]["Invariant"]["fields"].__setitem__("applies_to", "text"),
            "promise field": lambda c, s: c["nouns"]["Promise"]["fields"].__setitem__("applies_to", "applies_to"),
            "applies_to section": lambda c, s: c["applies_to"].__setitem__("default", "agent-runtime/2"),
            "records section": lambda c, s: c["records"]["projection"].__setitem__("private_repository", "one"),
            "mismatch refusal": lambda c, s: c["refusals"].__setitem__("applies_to_mismatch", "never refused"),
            "schema member constraint": lambda c, s: s["$defs"]["id_plan_member"].__setitem__("maxLength", 8),
            "schema member set": lambda c, s: s["$defs"]["id_plan_member"]["anyOf"].append({"$ref": "#/$defs/id_Witness"}),
            "schema applies_to": lambda c, s: s["$defs"]["applies_to"]["anyOf"][1].__setitem__("maxLength", 9),
            "schema invariant ref": lambda c, s: s["$defs"]["invariant"]["properties"].__setitem__("applies_to", {"type": "string"}),
            "schema promise ref": lambda c, s: s["$defs"]["promise"]["properties"]["applies_to"].__setitem__("minLength", 3),
            "schema protocol": lambda c, s: s["properties"]["protocol"]["enum"].append("2.2.0"),
        }
        for name, mutate in mutations.items():
            with self.subTest(mutation=name):
                contract, schema = self.current()
                mutate(contract, schema)
                with self.assertRaisesRegex(AssertionError, "not the declared 2.1 addition"):
                    replay.retract_additions(contract, schema)

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
