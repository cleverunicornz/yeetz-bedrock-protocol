---
name: evaluate
verb: evaluate
description: Bedrock verb `evaluate` - investigate a Candidate and record the findings and an outcome that feeds a decision, without deciding. Read it when you are asked to investigate, assess or advise on a possible response before someone decides it.
---

# evaluate

`evaluate` investigates a Candidate. Its findings are References; its outcome
says what the investigation concluded. The outcome feeds `decide`; the
evaluator does not decide. Whoever asked for the evaluation keeps the choice.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Candidate` |
| Inputs | `Candidate` |
| Outputs | `findings` `outcome` |
| Outcomes | `favourable` `unfavourable` `mixed` `inconclusive` |
| Held by | `orchestrator` `scout` `advisor` |

## When

A Candidate needs investigation before a decision. The act is recorded once
the investigation is done, with its outcome; an act has no phases, and work in
progress shows on the evaluator's board, not in the Candidate's state.

## What it means

- Every finding cites what it rests on: a stored artifact, a file at a
  commit, or a retrieved web page, each a Reference. What could not be
  established is said to be unknown, with where it was looked for, and may be
  declared as a Gap.
- Commit to an outcome. `mixed` names what favours and what disfavours;
  `inconclusive` names the evidence that would settle it.
- The Candidate becomes `evaluated`. The outcome is recorded on the act and is
  never a state.

## Refusals

- Evaluating a `decided` Candidate is refused: the transitions allow
  `evaluate` only on a `formulated` or `evaluated` Candidate. A later Decision
  may decide it again.
- Evaluating a superseded or revoked Candidate is refused.

## Not this verb

- Accepting or declining the Candidate is `decide`, held by the authority.
- A new possible response found while evaluating is `formulate`; a concern is
  `declare`.

## Source

`contract/bedrock-v2.md` sections 3, 4 and 5; `contract/bedrock-v2.yaml`
`verbs.evaluate` and `outcomes.evaluate`.


## Executable procedure

Use the pinned receiver interface in `contract/tool-interface.md` and
`contract/tool-interface.json`. The JSON below is the exact client argument
shape after substitution. `${scope}` is the admitted scope; `${run}` is a
unique replay prefix. `${step.field}` binds a field from an earlier successful
response in `contract/tool-examples/calls.json`; these substitutions are
performed before sending, never by the receiver. Never guess allocated IDs.

Resolve `evidence.made`, `formulate.made` from successful preceding responses. The receiver stamps the actor and role; callers never supply
actor, role, principal, allocated IDs or recording time. Preserve the verb's
roles and meaning in the Contract table above.

```json
{
  "op": "act",
  "verb": "evaluate",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "candidate": "${formulate.made}",
    "outcome": "favourable",
    "findings": [
      "${evidence.made}"
    ],
    "note": "The fixture probe supplies a concrete result."
  },
  "request_id": "${run}:evaluate"
}
```

The native request is `POST /v1/acts`. `${session}` is discovered caller
lineage added by the client, not a client argument. Its required envelope is:

```json
{
  "verb": "evaluate",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "candidate": "${formulate.made}",
    "outcome": "favourable",
    "findings": [
      "${evidence.made}"
    ],
    "note": "The fixture probe supplies a concrete result."
  },
  "request_id": "${run}:evaluate",
  "session": "${session}"
}
```

Retain `act_id`, `made`, `seq`, `recorded_at`, `changes` and any edit-window fields. This act makes no record; `made` is null. Read back using this exact query:

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
