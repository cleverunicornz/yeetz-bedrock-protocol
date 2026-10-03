---
name: mint
verb: mint
description: Bedrock verb `mint` - make a Promise, a falsifiable commitment, directly on a Decision or an accepted instruction, or from a Candidate a Decision accepted. Read it when a commitment is accepted and must become something that can be judged.
---

# mint

`mint` makes a Promise: a falsifiable commitment, "we want this to be true".
A minted Promise is `asserted`; it becomes `assured` only through a judgment
that holds.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Promise` |
| Inputs | `basis` `from_candidate` `addresses` |
| Outputs | `Promise` |
| Held by | `authority` `orchestrator` |

## When

A commitment is accepted.

- **Directly:** `basis` is a Decision (the grounds) or a Reference holding the
  accepted instruction or specification.
- **From a Candidate:** `from_candidate` names it and `basis` is the Decision
  that accepted it. The Candidate's latest standing outcome must be `accept`;
  it stays a Candidate after minting.
- `addresses` optionally names the Gaps the Promise answers.

## What it makes

- A Promise with `title`, `statement`, `scope` and an optional `residual`
  (what it knowingly leaves out). The statement is falsifiable within its
  scope.
- Its state is `asserted`. Making the subject deliver it is domain work, not
  a verb; that work is shown by Witnesses (`produce`) and judged (`judge`)
  against its Oracle (`define`).
- An assured Promise is invariant behaviour. Changing it is a superseding
  Promise, minted with its own Oracle and new Witnesses, with a Decision as
  basis.

## Refusals

- `wrong_basis`: a Promise minted from a Candidate cites the Decision that
  accepted that Candidate; any other Decision is refused.
- Minting from a Candidate whose latest standing outcome is not `accept` is
  refused.
- A field over its limit (`title` 256 characters, `statement`, `scope` and
  `residual` 1024) is refused with the field, its size and the limit.

## Not this verb

- The choice itself is `decide`; a Decision never mints.
- How the Promise is judged is `define`.

## Source

`contract/bedrock-v2.md` sections 3, 4 and 5; `contract/bedrock-v2.yaml`
`verbs.mint`, `nouns.Promise` and `refusals.wrong_basis`.


## Executable procedure

Use the pinned receiver interface in `contract/tool-interface.md` and
`contract/tool-interface.json`. The JSON below is the exact client argument
shape after substitution. `${scope}` is the admitted scope; `${run}` is a
unique replay prefix. `${step.field}` binds a field from an earlier successful
response in `contract/tool-examples/calls.json`; these substitutions are
performed before sending, never by the receiver. Never guess allocated IDs.

Resolve `decide.made`, `declare.made`, `formulate.made` from successful preceding responses. The receiver stamps the actor and role; callers never supply
actor, role, principal, allocated IDs or recording time. Preserve the verb's
roles and meaning in the Contract table above.

```json
{
  "op": "act",
  "verb": "mint",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "basis": {
      "decision": "${decide.made}"
    },
    "from_candidate": "${formulate.made}",
    "addresses": [
      "${declare.made}"
    ],
    "promise": {
      "title": "The fixture empty list parses",
      "statement": "Parsing [] produces an empty list.",
      "scope": "The isolated fixture probe."
    }
  },
  "request_id": "${run}:mint"
}
```

The native request is `POST /v1/acts`. `${session}` is discovered caller
lineage added by the client, not a client argument. Its required envelope is:

```json
{
  "verb": "mint",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "basis": {
      "decision": "${decide.made}"
    },
    "from_candidate": "${formulate.made}",
    "addresses": [
      "${declare.made}"
    ],
    "promise": {
      "title": "The fixture empty list parses",
      "statement": "Parsing [] produces an empty list.",
      "scope": "The isolated fixture probe."
    }
  },
  "request_id": "${run}:mint",
  "session": "${session}"
}
```

Retain `act_id`, `made`, `seq`, `recorded_at`, `changes` and any edit-window fields. Bind the returned `made` before any dependent call. Read back using this exact query:

```json
{
  "op": "query",
  "name": "record",
  "params": {
    "id": "${mint.made}"
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
