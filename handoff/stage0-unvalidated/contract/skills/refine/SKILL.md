---
name: refine
verb: refine
description: Bedrock verb `refine` - add without changing a claim - a better Witness after an inconclusive verdict, or a further sighting on an existing Gap or Candidate. Read it when you have new evidence for something already recorded, before you write a duplicate.
---

# refine

`refine` adds evidence without changing a claim. On a Witness it makes a new
Witness linked to the earlier one; on a Gap or a Candidate it adds a
sighting: a note and optional References.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Witness` `Gap` `Candidate` |
| Inputs | `target` `evidence` |
| Outputs | `Witness` `sighting` |
| Held by | `implementer` `automation` |

## When

- After an `inconclusive` verdict, when a better observation can settle it.
- When a Gap or Candidate already recorded is met again: add the sighting to
  it instead of declaring or formulating a duplicate. Independent sightings
  count as further evidence for it.

## What it makes

- **On a Witness:** a new Witness of the same Promise, with a `refines` link
  to the earlier one, which stays as it was. The new Witness is `produced`
  and is judged like any other.
- **On a Gap or Candidate:** a sighting. It gives no state; the record keeps
  its claim and its state.

## Refusals

- Refining a revoked Witness is refused; produce a new Witness instead.
- Refining any other noun is refused.

## Not this verb

- A Witness is never superseded; `refine` is how a better observation
  arrives.
- Changing what a Gap or Candidate claims is `supersede` (a successor record)
  or, within the edit window, the author's own amendment.

## Source

`contract/bedrock-v2.md` sections 3, 4 and 6; `contract/bedrock-v2.yaml`
`verbs.refine`.


## Executable procedure

Use the pinned receiver interface in `contract/tool-interface.md` and
`contract/tool-interface.json`. The JSON below is the exact client argument
shape after substitution. `${scope}` is the admitted scope; `${run}` is a
unique replay prefix. `${step.field}` binds a field from an earlier successful
response in `contract/tool-examples/calls.json`; these substitutions are
performed before sending, never by the receiver. Never guess allocated IDs.

Resolve `declare.made`, `evidence.made` from successful preceding responses. The receiver stamps the actor and role; callers never supply
actor, role, principal, allocated IDs or recording time. Preserve the verb's
roles and meaning in the Contract table above.

```json
{
  "op": "act",
  "verb": "refine",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "target": "${declare.made}",
    "sighting": {
      "note": "The independent fixture replay sees the same coverage need.",
      "evidence": [
        "${evidence.made}"
      ]
    }
  },
  "request_id": "${run}:refine"
}
```

The native request is `POST /v1/acts`. `${session}` is discovered caller
lineage added by the client, not a client argument. Its required envelope is:

```json
{
  "verb": "refine",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "target": "${declare.made}",
    "sighting": {
      "note": "The independent fixture replay sees the same coverage need.",
      "evidence": [
        "${evidence.made}"
      ]
    }
  },
  "request_id": "${run}:refine",
  "session": "${session}"
}
```

Retain `act_id`, `made`, `seq`, `recorded_at`, `changes` and any edit-window fields. The sighting form makes no record; `made` is null. Read back using this exact query:

```json
{
  "op": "query",
  "name": "record",
  "params": {
    "id": "${declare.made}"
  }
}
```

Query answers carry `watermark` and `head`; check that projection has passed
the returned act sequence before interpreting the state. A lagging or absent
projection is not a refusal. On an uncertain write outcome, retain and repeat
the identical arguments and original request key; never allocate a new key
for that intent. The pinned client suppresses native refusal messages and
raises an error containing the refusal code. Readback and replay limits are
listed in `contract/tool-interface.md`.

For a Witness, use the complete `refine_witness` invocation in
`contract/tool-examples/calls.json`: it makes a new Witness of the same Promise
and returns its `made` ID. For a Gap or Candidate the sighting invocation
above makes no record; `made` is null. Neither form rewrites the observation.
