---
name: formulate
verb: formulate
description: Bedrock verb `formulate` - derive a possible response from evidence and record it as a Candidate, a brief hypothesis that commits no one. Read it when evidence suggests a response to a Gap, Witness, Decision, Reference or another Candidate.
---

# formulate

`formulate` makes a Candidate: a brief hypothesis, a possible response derived
from evidence. A Candidate is not a commitment; it becomes one only when a
Decision accepts it and a Promise is minted from it.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Candidate` |
| Inputs | `responds_to` |
| Outputs | `Candidate` |
| Held by | `authority` `orchestrator` `scout` `implementer` `advisor` `automation` |

## When

Evidence suggests a possible response. Walk the scope first: when a Candidate
already says it, add your evidence to it as a sighting (`refine`) or replace it
(`supersede`) instead of writing a duplicate.

## What it makes

- A Candidate with `title` and `hypothesis`, and at least one `responds_to`
  link: a Gap, Witness, Decision, Reference or Candidate. Depth goes in
  References it links.
- Its state is `formulated`; `evaluate` may move it to `evaluated`, and
  `decide` to `decided`.

## Refusals

- A Candidate without a `responds_to` link is refused: it is formulated from
  the evidence it responds to.
- A field over its limit (`title` 256 characters, `hypothesis` 1024) is
  refused with the field, its size and the limit; nothing is cut.

## Not this verb

- Investigating a Candidate is `evaluate`; accepting or declining it is
  `decide`; committing to it is `mint`.

## Source

`contract/bedrock-v2.md` sections 3 and 4; `contract/bedrock-v2.yaml`
`verbs.formulate` and `nouns.Candidate`.


## Executable procedure

Use the pinned receiver interface in `contract/tool-interface.md` and
`contract/tool-interface.json`. The JSON below is the exact client argument
shape after substitution. `${scope}` is the admitted scope; `${run}` is a
unique replay prefix. `${step.field}` binds a field from an earlier successful
response in `contract/tool-examples/calls.json`; these substitutions are
performed before sending, never by the receiver. Never guess allocated IDs.

Resolve `declare.made` from successful preceding responses. The receiver stamps the actor and role; callers never supply
actor, role, principal, allocated IDs or recording time. Preserve the verb's
roles and meaning in the Contract table above.

```json
{
  "op": "act",
  "verb": "formulate",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "responds_to": [
      "${declare.made}"
    ],
    "candidate": {
      "title": "Run the empty-list probe",
      "hypothesis": "Parsing the fixture empty JSON list produces an empty list."
    }
  },
  "request_id": "${run}:formulate"
}
```

The native request is `POST /v1/acts`. `${session}` is discovered caller
lineage added by the client, not a client argument. Its required envelope is:

```json
{
  "verb": "formulate",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "responds_to": [
      "${declare.made}"
    ],
    "candidate": {
      "title": "Run the empty-list probe",
      "hypothesis": "Parsing the fixture empty JSON list produces an empty list."
    }
  },
  "request_id": "${run}:formulate",
  "session": "${session}"
}
```

Retain `act_id`, `made`, `seq`, `recorded_at`, `changes` and any edit-window fields. Bind the returned `made` before any dependent call. Read back using this exact query:

```json
{
  "op": "query",
  "name": "record",
  "params": {
    "id": "${formulate.made}"
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
