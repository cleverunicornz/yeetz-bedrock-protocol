"""Validate tool arguments and skill procedures; no runtime trust qualification.

Used by contract/check.py. Physical source HTTP replay lives in replay.py.
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve().parent
TOKEN = re.compile(r"\$\{([A-Za-z0-9_.]+)\}")
MADE = {"stipulate": "invariant", "declare": "gap", "formulate": "candidate",
        "decide": "decision", "mint": "promise", "define": "oracle", "produce": "witness",
        "store": "reference", "group": "plan"}


def substitute(value, values):
    """Resolve only known earlier responses; no allocation or server interpolation."""
    if isinstance(value, dict):
        return {k: substitute(v, values) for k, v in value.items()}
    if isinstance(value, list):
        return [substitute(v, values) for v in value]
    if isinstance(value, str):
        match = TOKEN.fullmatch(value)
        if match:
            return lookup(match[1], values)
        return TOKEN.sub(lambda m: str(lookup(m[1], values)), value)
    return value


def lookup(name, values):
    parts = name.split(".")
    out = values
    for part in parts:
        if not isinstance(out, dict) or part not in out:
            raise ValueError(f"unbound substitution {name}; predecessor must succeed first")
        out = out[part]
    if out is None:
        raise ValueError(f"substitution {name} is null")
    return out


def project(arguments, lineage):
    """Expected source projection, checked against the actual client by replay.py."""
    op = arguments["op"]
    if op == "query":
        return "/v1/query", {"name": arguments["name"], "params": arguments.get("params", {})}
    if op == "reference.get":
        return "/v1/references/" + arguments["id"], None
    if op == "act":
        body = {k: arguments[k] for k in ("verb", "level", "scope", "payload")}
        body.update(lineage)
        route = "/v1/acts"
    elif op == "reference.put":
        body = {**arguments["reference"], "level": arguments["level"], "scope": arguments["scope"]}
        body.update({k: v for k, v in lineage.items() if k != "repository"})
        if lineage.get("repository"):
            body["act_repository"] = lineage["repository"]
        route = "/v1/references"
    else:
        raise ValueError(f"unknown operation {op}")
    body["request_id"] = arguments["request_id"]
    return route, body


def validate_arguments(args, interface):
    jsonschema.validate(args, interface["client_tool"]["schema"])
    op = args["op"]
    if set(args) - set(interface["client_fields"][op]):
        raise ValueError(f"{op}: arguments outside operation fields")
    if not set(interface["client_required"][op]) <= set(args):
        raise ValueError(f"{op}: incomplete operation arguments")
    if op == "query" and args["name"] not in interface["queries"]:
        raise ValueError(f"unsupported pinned query {args['name']}")
    if "request_id" in args and not re.fullmatch(r"[A-Za-z0-9._:-]{1,200}", args["request_id"]):
        raise ValueError("request_id does not satisfy actual client validation")
    if op == "act" and args["verb"] == "assure":
        raise ValueError("assure is a transition, never an act")


def check(root, contract, schema, reference):
    """Return pinpointed disagreements; synthetic IDs are checker-local only."""
    failures = []
    interface = json.loads((root / "tool-interface.json").read_text())
    fixture = json.loads((root / "tool-examples/calls.json").read_text())
    values = {"scope": "fixture-scope", "run": "check-run", "session": "fixture:session",
              "fixture_commit": "1" * 40, "observed_at": "2026-10-03T12:00:00Z",
              "probe_result": "Parsing [] produced an empty list."}
    engine = reference.Projector(contract)
    prefixes = {k: v["prefix"] for k, v in contract["nouns"].items()}
    prefixes["Plan"] = contract["group"]["Plan"]["prefix"]
    seen = set()
    performed = set()
    for index, step in enumerate(fixture["steps"], 1):
        key = step["key"]
        try:
            if key in seen:
                raise ValueError("duplicate step key")
            seen.add(key)
            args = substitute(step["arguments"], values)
            validate_arguments(args, interface)
            if step["role"] not in contract["roles"]:
                raise ValueError("unknown receiver fixture role")
            route, body = project(args, {"session": values["session"]})
            if body is not None:
                op = interface["operations"][args["op"]]
                if set(body) - set(op["allowed"]) or not set(op["required"]) <= set(body):
                    raise ValueError("incomplete or excessive native envelope")
            if args["op"] in ("query", "reference.get"):
                if args["op"] == "query" and args["name"] == "assured_by":
                    if engine.state[args["params"]["promise"]] != step["check"]["state"]:
                        raise ValueError("assurance query expectation contradicts semantic replay")
                values[key] = {}
                continue
            if args["op"] == "reference.put":
                r = args["reference"]
                payload = {"reference": {"title": r["title"], "kind": r["kind"], "media_type": "text/markdown",
                    "visibility": "shared", "location": {k: r[k] for k in ("repository", "commit", "path")}}}
                verb = "store"
            else:
                verb, payload = args["verb"], copy.deepcopy(args["payload"])
                if verb in contract["verbs"]:
                    performed.add(verb)
                if verb in contract["verbs"] and step["role"] not in contract["verbs"][verb]["roles"]:
                    raise ValueError("fixture receiver role does not hold the verb")
            made_key = MADE.get(verb)
            if verb == "refine" and "witness" in payload:
                made_key = "witness"
            made = None
            if made_key:
                noun = "Plan" if made_key == "plan" else made_key.capitalize()
                made = f"{prefixes[noun]}-check{index}"
                payload[made_key]["id"] = made
            act = {"id": f"A-check{index}", "protocol": contract["bedrock"], "verb": verb,
                "level": args["level"], "scope": args["scope"], "recorded_at": f"2026-10-03T12:00:{index:02d}Z",
                "actor": {"kind": "agent", "agent": "fixture:" + step["role"], "role": step["role"]},
                "session": values["session"], "payload": payload}
            jsonschema.Draft202012Validator(schema, format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER).validate(act)
            engine.apply(act)
            values[key] = {"made": made, "act_id": act["id"], "seq": index}
            expected = step.get("check", {})
            subject = substitute(expected.get("subject", made), values)
            if subject and "state" in expected and engine.state[subject] != expected["state"]:
                raise ValueError(f"state {engine.state[subject]} != {expected['state']}")
        except (ValueError, KeyError, jsonschema.ValidationError, reference.Refused) as error:
            failures.append(f"contract/tool-examples/calls.json:{key}: {error}")
            # Dependent steps then fail at their own binding; never invent a response.
    want = {v for v, spec in contract["verbs"].items() if spec["kind"] == "act"}
    if performed != want:
        failures.append(f"executable fixture verbs {sorted(performed)} != fixed performed verbs {sorted(want)}")
    primary = {s["key"]: s for s in fixture["steps"]}
    for verb in contract["verbs"]:
        path = root / "skills" / verb / "SKILL.md"
        rel = f"contract/skills/{verb}/SKILL.md"
        try:
            text = path.read_text()
            if text.count("## Executable procedure") != 1:
                raise ValueError("exactly one executable procedure required")
            section = text.split("## Executable procedure", 1)[1]
            blocks = [json.loads(b) for b in re.findall(r"```json\n(.*?)\n```", section, re.S)]
            if len(blocks) != 3 or blocks[0] != primary[verb]["arguments"]:
                raise ValueError("procedure must match exact fixture arguments and contain native envelope/readback")
            _, expected = project(blocks[0], {"session": "${session}"})
            if blocks[1] != expected:
                raise ValueError("native envelope disagrees with pinned client projection")
            if blocks[2].get("op") != "query" or blocks[2].get("name") != "record":
                raise ValueError("record readback required")
            if "contract/tool-interface.md" not in section or "contract/tool-interface.json" not in section:
                raise ValueError("pinned interface pointers required")
            if verb == "assure" and blocks[0].get("name") != "assured_by":
                raise ValueError("assure only reads standing assurance")
        except (ValueError, KeyError, OSError) as error:
            failures.append(f"{rel}: {error}")
    return failures
