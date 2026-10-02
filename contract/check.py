"""Check that the Bedrock v2 prose, machine-readable contract, JSON Schema and
worked examples agree.

Run from the repository root:

    uv run --no-project --with pyyaml --with jsonschema python contract/check.py

Exit 0 when everything agrees; otherwise every disagreement is printed and the
exit code is 1. The reference projector below replays each example's acts,
derives record states, and records every transition it applies, so the check
also proves that the transition table is consistent with the act rules and
that every listed transition is exercised by at least one example.
"""

from __future__ import annotations

import copy
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent
PROSE = ROOT / "bedrock-v2.md"
CONTRACT = ROOT / "bedrock-v2.yaml"
SCHEMA = ROOT / "bedrock-v2.schema.json"
EXAMPLES = ROOT / "examples"

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


# --------------------------------------------------------------------------
# Prose tables
# --------------------------------------------------------------------------


def prose_table(text: str, heading: str) -> list[list[str]]:
    """Rows of the first Markdown table after the given heading line."""
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        fail(f"prose: heading {heading!r} not found")
        return []
    rows: list[list[str]] = []
    in_table = False
    for line in lines[start + 1 :]:
        if line.startswith("#"):
            break
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not in_table:
                in_table = True  # header row
                continue
            if all(set(c) <= set("-: ") for c in cells):
                continue  # separator row
            rows.append(cells)
        elif in_table:
            break
    if not rows:
        fail(f"prose: no table rows under {heading!r}")
    return rows


def words(cell: str) -> list[str]:
    """Backticked words of a cell, in order."""
    return re.findall(r"`([^`]+)`", cell)


def check_prose(text: str, contract: dict) -> None:
    nouns = contract["nouns"]

    rows = prose_table(text, "### The nouns")
    prose_nouns = {r[0].strip("*"): r for r in rows}
    if list(prose_nouns) != list(nouns):
        fail(f"nouns: prose {list(prose_nouns)} != contract {list(nouns)}")
    for name, row in prose_nouns.items():
        spec = nouns.get(name)
        if not spec:
            continue
        if words(row[1]) != [spec["prefix"]]:
            fail(f"noun {name}: prose prefix {words(row[1])} != {spec['prefix']}")
        if words(row[2]) != spec["states"]:
            fail(f"noun {name}: prose states {words(row[2])} != {spec['states']}")
        if words(row[3]) != [spec["made_by"]]:
            fail(f"noun {name}: prose made-by {words(row[3])} != {spec['made_by']}")

    verbs = contract["verbs"]
    rows = prose_table(text, "### The thirteen verbs")
    prose_verbs = [words(r[1])[0] if words(r[1]) else r[1] for r in rows]
    if prose_verbs != list(verbs):
        fail(f"verbs: prose {prose_verbs} != contract {list(verbs)}")
    for row in rows:
        name = words(row[1])[0] if words(row[1]) else row[1]
        spec = verbs.get(name)
        if not spec:
            continue
        if row[2] != spec["kind"]:
            fail(f"verb {name}: prose kind {row[2]!r} != {spec['kind']!r}")
        if sorted(words(row[3])) != sorted(spec["acts_on"]):
            fail(f"verb {name}: prose acts-on {words(row[3])} != {spec['acts_on']}")
    if len(verbs) != 13:
        fail(f"verbs: contract lists {len(verbs)} verbs, not 13")

    rows = prose_table(text, "### Structural acts")
    prose_structural = [words(r[0])[0] for r in rows if words(r[0])]
    if prose_structural != list(contract["structural_acts"]):
        fail(f"structural acts: prose {prose_structural} != {list(contract['structural_acts'])}")

    rows = prose_table(text, "### Act nodes, verb by verb")
    seen = []
    for row in rows:
        name = words(row[0])[0] if words(row[0]) else row[0]
        seen.append(name)
        spec = verbs.get(name)
        if not spec:
            fail(f"act table: unknown verb {name}")
            continue
        if sorted(words(row[1])) != sorted(spec["inputs"]):
            fail(f"act {name}: prose inputs {words(row[1])} != {spec['inputs']}")
        if sorted(words(row[2])) != sorted(spec["outputs"]):
            fail(f"act {name}: prose outputs {words(row[2])} != {spec['outputs']}")
        if sorted(words(row[3])) != sorted(spec["roles"]):
            fail(f"act {name}: prose roles {words(row[3])} != {spec['roles']}")
    performed = [v for v, s in verbs.items() if s["kind"] == "act"]
    if seen != performed:
        fail(f"act table: prose verbs {seen} != performed verbs {performed}")

    rows = prose_table(text, "### Transitions")
    prose_tr = []
    for r in rows:
        noun, frm, to, by = r[0], words(r[1]), words(r[2]), words(r[3])
        prose_tr.append((noun, tuple(frm), to[0] if to else None, tuple(by)))
    yaml_tr = [
        (t["noun"], tuple(t["from"]), t["to"], tuple(t["by"])) for t in contract["transitions"]
    ]
    if prose_tr != yaml_tr:
        missing = [t for t in yaml_tr if t not in prose_tr]
        extra = [t for t in prose_tr if t not in yaml_tr]
        fail(f"transitions: prose and contract differ; missing in prose {missing}; extra in prose {extra}")

    rows = prose_table(text, "### Roles and their verbs")
    prose_roles = {words(r[0])[0]: words(r[1]) for r in rows if words(r[0])}
    yaml_roles = {k: v["verbs"] for k, v in contract["roles"].items()}
    if prose_roles != yaml_roles:
        fail(f"roles: prose {prose_roles} != contract {yaml_roles}")
    for role, held in yaml_roles.items():
        for v in held:
            if v not in verbs or verbs[v]["kind"] != "act":
                fail(f"role {role}: holds {v}, which is not a performed verb")
    for v, spec in verbs.items():
        holders = sorted(r for r, held in yaml_roles.items() if v in held)
        if holders != sorted(spec["roles"]):
            fail(f"verb {v}: lists roles {spec['roles']}, but the roles holding it are {holders}")

    rows = prose_table(text, "### Levels")
    prose_levels = [words(r[0])[0] for r in rows if words(r[0])]
    if prose_levels != contract["levels"]["initial"]:
        fail(f"levels: prose {prose_levels} != {contract['levels']['initial']}")

    rows = prose_table(text, "### Reference kinds")
    prose_kinds = [words(r[0])[0] for r in rows if words(r[0])]
    if prose_kinds != list(contract["references"]["kinds"]):
        fail(f"reference kinds: prose {prose_kinds} != {list(contract['references']['kinds'])}")

    rows = prose_table(text, "### Field limits")
    prose_limits = {}
    for r in rows:
        nums = re.findall(r"\d[\d,]*", r[1])
        if words(r[0]) and nums:
            prose_limits[words(r[0])[0]] = int(nums[0].replace(",", ""))
    if prose_limits != contract["limits"]:
        fail(f"limits: prose {prose_limits} != {contract['limits']}")

    rows = prose_table(text, "### The fixed queries")
    prose_queries = [words(r[0])[0] for r in rows if words(r[0])]
    if prose_queries != list(contract["queries"]):
        fail(f"queries: prose {prose_queries} != {list(contract['queries'])}")

    window = contract["parameters"]["edit_window_seconds"]
    if window != 600 or "10 minutes" not in text:
        fail(f"edit window: contract {window}s; prose must say 10 minutes")

    version = (ROOT.parent / "VERSION").read_text().strip()
    if contract["bedrock"] != version:
        fail(f"version: contract {contract['bedrock']} != VERSION {version}")
    if f"Version {version}" not in text:
        fail(f"version: prose does not state 'Version {version}'")


# --------------------------------------------------------------------------
# Schema against contract
# --------------------------------------------------------------------------


def check_schema(schema: dict, contract: dict) -> None:
    jsonschema.Draft202012Validator.check_schema(schema)
    defs = schema["$defs"]
    verbs = [v for v, s in contract["verbs"].items() if s["kind"] == "act"]
    act_names = verbs + list(contract["structural_acts"])
    if defs["verb"]["enum"] != act_names:
        fail(f"schema verb enum {defs['verb']['enum']} != contract acts {act_names}")
    for name, spec in contract["nouns"].items():
        enum = defs["state"]["properties"].get(name, {}).get("enum")
        if enum != spec["states"]:
            fail(f"schema states for {name} {enum} != {spec['states']}")
    for field, limit in contract["limits"].items():
        got = defs.get(field, {}).get("maxLength")
        if got != limit:
            fail(f"schema limit {field} {got} != contract {limit}")
    if defs["level"]["examples"] != contract["levels"]["initial"]:
        fail("schema level examples != contract initial levels")
    if defs["reference"]["properties"]["kind"]["enum"] != list(contract["references"]["kinds"]):
        fail("schema reference kinds != contract reference kinds")
    if schema["properties"]["protocol"]["const"] != contract["bedrock"]:
        fail("schema protocol const != contract version")
    for verb in act_names:
        if f"payload_{verb}" not in defs:
            fail(f"schema has no payload definition for {verb}")
    for noun, spec in contract["nouns"].items():
        if spec["prefix"] and not re.match(defs[f"id_{noun}"]["pattern"], f"{spec['prefix']}-1"):
            fail(f"schema id pattern for {noun} does not admit {spec['prefix']}-1")


# --------------------------------------------------------------------------
# Reference projector
# --------------------------------------------------------------------------


class Refused(Exception):
    def __init__(self, code: str, msg: str):
        super().__init__(msg)
        self.code = code


def noun_of(record_id: str, contract: dict) -> str:
    for name, spec in contract["nouns"].items():
        if record_id.startswith(spec["prefix"] + "-"):
            return name
    if record_id.startswith(contract["group"]["Plan"]["prefix"] + "-"):
        return "Plan"
    raise Refused("unknown_id", f"unknown record id {record_id}")


class Projector:
    def __init__(self, contract: dict):
        self.c = contract
        self.state: dict[str, str] = {}
        self.record: dict[str, dict] = {}
        self.author: dict[str, tuple[str, datetime]] = {}  # record -> (agent, created)
        self.acts: dict[str, dict] = {}
        self.applied: set[tuple] = set()
        self.allowed = {
            (t["noun"], f, t["to"], v)
            for t in contract["transitions"]
            for v in t["by"]
            for f in (t["from"] or [None])
        }

    def move(self, rid: str, to: str, by: str) -> None:
        noun = noun_of(rid, self.c)
        frm = self.state.get(rid)
        key = (noun, frm, to, by)
        if key not in self.allowed:
            raise Refused("transition_not_allowed", f"{noun} {rid}: {frm} -> {to} by {by}")
        self.applied.add(key)
        self.state[rid] = to

    def create(self, rec: dict, noun: str, state: str, by: str, act: dict) -> None:
        rid = rec["id"]
        if noun_of(rid, self.c) != noun:
            raise Refused("wrong_noun", f"{rid} is not a {noun}")
        if rid in self.state:
            raise Refused("duplicate_id", f"{rid} exists")
        self.move(rid, state, by)
        self.record[rid] = rec
        self.author[rid] = (act["actor"]["agent"], when(act))

    def need(self, rid: str, noun: str) -> dict:
        if rid not in self.record or noun_of(rid, self.c) != noun:
            raise Refused("missing_input", f"{rid} is not a recorded {noun}")
        return self.record[rid]

    def oracles_in_force(self, pid: str) -> list[str]:
        return [
            r for r, rec in self.record.items()
            if r.startswith("O-") and rec["judges"] == pid and self.state[r] == "in_force"
        ]

    def witnesses_of(self, pid: str) -> list[str]:
        return [
            r for r, rec in self.record.items()
            if r.startswith("W-") and rec["observes"] == pid and self.state[r] != "revoked"
        ]

    def maybe_assuring(self, pid: str, by: str) -> None:
        if self.state.get(pid) == "asserted" and self.oracles_in_force(pid) and self.witnesses_of(pid):
            self.move(pid, "assuring", by)

    def apply(self, act: dict) -> None:
        v, p = act["verb"], act["payload"]
        self.acts[act["id"]] = act
        if v == "stipulate":
            for b in p.get("basis", []):
                self.need(b, noun_of(b, self.c))
            self.create(p["invariant"], "Invariant", "in_force", v, act)
        elif v == "declare":
            if "arose_in" in p and p["arose_in"] not in self.acts:
                raise Refused("missing_input", f"arose_in {p['arose_in']} is not a recorded act")
            self.create(p["gap"], "Gap", "open", v, act)
        elif v == "formulate":
            for r in p["responds_to"]:
                self.need(r, noun_of(r, self.c))
            self.create(p["candidate"], "Candidate", "formulated", v, act)
            for r in p["responds_to"]:
                if r.startswith("G-") and self.state[r] == "open":
                    self.move(r, "addressing", v)
        elif v == "evaluate":
            cid = p["candidate"]
            self.need(cid, "Candidate")
            if p["phase"] == "begun":
                self.move(cid, "evaluating", v)
            else:
                self.move(cid, "evaluated", v)
        elif v == "decide":
            for r in p.get("considered", []):
                self.need(r, noun_of(r, self.c))
            self.create(p["decision"], "Decision", "in_force", v, act)
            for o in p.get("outcomes", []):
                subj, out = o["subject"], o["outcome"]
                noun = noun_of(subj, self.c)
                self.need(subj, noun)
                target = self.c["decision_outcomes"].get(noun, {}).get(out)
                if target is None and out not in self.c["decision_outcomes"].get(noun, {}):
                    raise Refused("bad_outcome", f"{out} is not an outcome for a {noun}")
                if target:
                    self.move(subj, target, v)
        elif v == "mint":
            basis = p["basis"]
            if "decision" in basis:
                self.need(basis["decision"], "Decision")
            else:
                self.need(basis["instruction"], "Reference")
            if "from_candidate" in p:
                if "decision" not in basis:
                    raise Refused("missing_input", "a Promise minted from a Candidate cites the Decision")
                self.need(p["from_candidate"], "Candidate")
                if self.state[p["from_candidate"]] != "accepted":
                    raise Refused("missing_input", "the Candidate was not accepted")
            self.create(p["promise"], "Promise", "asserted", v, act)
            for g in p.get("addresses", []):
                self.need(g, "Gap")
                if self.state[g] == "open":
                    self.move(g, "addressing", v)
        elif v == "define":
            o = p["oracle"]
            self.need(o["judges"], "Promise")
            self.create(o, "Oracle", "in_force", v, act)
            self.maybe_assuring(o["judges"], v)
        elif v == "produce":
            w = p["witness"]
            self.need(w["observes"], "Promise")
            for e in w["evidence"]:
                self.need(e, "Reference")
            self.create(w, "Witness", "produced", v, act)
            self.maybe_assuring(w["observes"], v)
        elif v == "refine":
            t = p["target"]
            noun = noun_of(t, self.c)
            self.need(t, noun)
            if noun == "Witness":
                w = p.get("witness")
                if not w or w["observes"] != self.record[t]["observes"]:
                    raise Refused("missing_input", "refining a Witness produces a new Witness of the same Promise")
                if self.state[t] == "revoked":
                    raise Refused("witness_revoked", f"{t} is revoked; produce a new Witness instead")
                for e in w["evidence"]:
                    self.need(e, "Reference")
                self.create(w, "Witness", "produced", v, act)
            elif noun in ("Gap", "Candidate"):
                if "sighting" not in p:
                    raise Refused("missing_input", "refining a Gap or Candidate adds a sighting")
                for e in p["sighting"].get("evidence", []):
                    self.need(e, "Reference")
            else:
                raise Refused("not_refinable", f"a {noun} is not refined")
        elif v == "judge":
            pid, oid, wid = p["promise"], p["oracle"], p["witness"]
            self.need(pid, "Promise")
            o = self.need(oid, "Oracle")
            w = self.need(wid, "Witness")
            if o["judges"] != pid or w["observes"] != pid:
                raise Refused("mismatched_inputs", "the Oracle and Witness must concern the judged Promise")
            if self.state[oid] != "in_force":
                raise Refused("oracle_not_in_force", f"{oid} is {self.state[oid]}")
            if self.state[wid] == "revoked":
                raise Refused("witness_revoked", f"{wid} is revoked")
            if p["verdict"] == "does_not_hold" and not p.get("failure_evidence"):
                raise Refused("missing_input", "does_not_hold cites the demonstrated in-scope failure")
            if self.state[wid] == "produced":
                self.move(wid, "judged", v)
            if p["verdict"] == "holds" and self.state[pid] == "assuring":
                self.move(pid, "assured", "assure")
        elif v in ("revoke", "supersede"):
            t = p["target"]
            noun = noun_of(t, self.c)
            if noun == "Plan":
                raise Refused("not_a_record", "a Plan is retired with regroup")
            self.need(t, noun)
            if v == "supersede":
                s = p["successor"]
                if noun_of(s, self.c) != noun:
                    raise Refused("wrong_noun", "a successor is the same noun")
                self.need(s, noun)
                if self.state[s] in ("superseded", "revoked"):
                    raise Refused("successor_not_current", f"{s} is {self.state[s]}")
            self.move(t, "revoked" if v == "revoke" else "superseded", v)
        elif v == "store":
            self.create(p["reference"], "Reference", "current", v, act)
        elif v == "group":
            plan = p["plan"]
            for m in plan["members"]:
                if noun_of(m, self.c) not in self.c["group"]["Plan"]["members"]:
                    raise Refused("bad_member", f"{m} cannot be a Plan member")
                self.need(m, noun_of(m, self.c))
            if plan["id"] in self.state:
                raise Refused("duplicate_id", plan["id"])
            self.state[plan["id"]] = "open"
            self.record[plan["id"]] = copy.deepcopy(plan)
            self.author[plan["id"]] = (act["actor"]["agent"], when(act))
        elif v == "regroup":
            plan = self.record.get(p["plan"])
            if plan is None:
                raise Refused("missing_input", f"{p['plan']} is not a Plan")
            for m in p.get("add_members", []):
                self.need(m, noun_of(m, self.c))
                plan["members"].append(m)
            for m in p.get("remove_members", []):
                plan["members"].remove(m)
            if p.get("retire"):
                self.state[p["plan"]] = "retired"
        elif v == "relate":
            for r in (p["from"], p["to"]):
                if not r.startswith("scope:"):
                    self.need(r, noun_of(r, self.c))
        elif v == "amend":
            target = self.acts.get(p["target_act"])
            if target is None:
                raise Refused("missing_input", f"{p['target_act']} is not a recorded act")
            if target["actor"]["agent"] != act["actor"]["agent"]:
                raise Refused("not_author", "only the author amends within the edit window")
            window = self.c["parameters"]["edit_window_seconds"]
            if (when(act) - when(target)).total_seconds() > window:
                raise Refused("edit_window_closed", "the edit window has closed; supersede or revoke")
        else:
            raise Refused("unknown_verb", v)


def when(act: dict) -> datetime:
    return datetime.fromisoformat(act["recorded_at"].replace("Z", "+00:00"))


def merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def check_examples(schema: dict, contract: dict) -> set[tuple]:
    validator = jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER
    )
    exercised: set[tuple] = set()
    files = sorted(EXAMPLES.glob("*.yaml"))
    if not files:
        fail("examples: none found")
    for path in files:
        ex = yaml.safe_load(path.read_text())
        name = path.name
        proj = Projector(contract)
        refused = None
        for i, raw in enumerate(ex["acts"]):
            act = merge(ex.get("defaults", {}), raw)
            for err in validator.iter_errors(act):
                fail(f"{name} act {i} ({act.get('id')}): schema: {err.message} at {list(err.absolute_path)}")
            try:
                proj.apply(act)
            except Refused as r:
                refused = (i, r)
                break
        expect = ex["expect"]
        if "refused" in expect:
            want = expect["refused"]
            if refused is None:
                fail(f"{name}: expected refusal {want} but every act applied")
            elif refused[1].code != want["code"] or refused[0] != want["act_index"]:
                fail(f"{name}: expected refusal {want}, got act {refused[0]} {refused[1].code}: {refused[1]}")
        elif refused is not None:
            fail(f"{name}: act {refused[0]} refused: {refused[1].code}: {refused[1]}")
        for rid, st in expect.get("states", {}).items():
            if proj.state.get(rid) != st:
                fail(f"{name}: {rid} expected {st}, projected {proj.state.get(rid)}")
        exercised |= proj.applied
    return exercised


def check_manifest() -> None:
    import hashlib

    manifest = json.loads((ROOT.parent / "manifest.json").read_text())
    listed = {e["path"]: e["sha256"] for e in manifest.get("contract", [])}
    for p in (PROSE, CONTRACT, SCHEMA):
        rel = str(p.relative_to(ROOT.parent))
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        if listed.get(rel) != digest:
            fail(f"manifest: {rel} digest {listed.get(rel)} != file {digest}")
    version = (ROOT.parent / "VERSION").read_text().strip()
    if manifest.get("version") != version:
        fail(f"manifest: version {manifest.get('version')} != VERSION {version}")


def main() -> int:
    for p in (PROSE, CONTRACT, SCHEMA):
        if not p.exists():
            fail(f"missing {p.relative_to(ROOT.parent)}")
    if errors:
        return report()
    text = PROSE.read_text()
    contract = yaml.safe_load(CONTRACT.read_text())
    schema = json.loads(SCHEMA.read_text())
    check_prose(text, contract)
    check_schema(schema, contract)
    check_manifest()
    exercised = check_examples(schema, contract)
    for t in contract["transitions"]:
        for v in t["by"]:
            keys = {(t["noun"], f, t["to"], v) for f in (t["from"] or [None])}
            if not keys & exercised:
                fail(f"transition {t['noun']} {t['from']} -> {t['to']} by {v} is exercised by no example")
    return report()


def report() -> int:
    if errors:
        for e in errors:
            print("FAIL", e)
        print(f"{len(errors)} disagreement(s)")
        return 1
    print("OK: prose, contract, schema and examples agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
