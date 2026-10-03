"""Actual observation used only by the isolated executable-call fixture."""
import json


def observe() -> str:
    value = json.loads("[]")
    if value != []:
        raise AssertionError("empty-list probe differed from the fixture expectation")
    return "Parsing [] produced an empty list."
