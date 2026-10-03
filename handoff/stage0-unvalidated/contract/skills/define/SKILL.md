---
name: define
verb: define
description: Bedrock verb `define` - make the Oracle that says how one Promise is judged - its inputs, when it holds, when it fails, and who or what applies it. Read it when a Promise needs its judgment rule, ideally before any Witness is produced.
---

# define

`define` makes an Oracle: the judgment rule for one Promise. It states the
inputs a judge uses, when the Promise holds, when it fails, and how the
judgment is arranged.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Oracle` |
| Inputs | `Promise` |
| Outputs | `Oracle` |
| Held by | `authority` `orchestrator` |

## When

A Promise needs its judgment rule. Best before `produce`; a retrospective
Oracle is ordinary and honest about its time.

## What it makes

- An Oracle with `title`, `judges` (exactly one Promise), `inputs`,
  `holds_when`, `fails_when`, `arrangement` (`human`, `agent`,
  `deterministic` or `mixed`) and an optional `executable` pointer. A wholly
  human Oracle is complete as it stands.
- Its state is `defined`. Defining an Oracle never moves the Promise's state.
- A judgment applies the Promise's Oracle that is neither superseded nor
  revoked.

## Refusals

- A field over its limit (`title` 256 characters; `inputs`, `holds_when` and
  `fails_when` 1024) is refused with the field, its size and the limit.

## Not this verb

- A stricter or corrected rule is a new Oracle that supersedes this one
  (`supersede`). Superseding an Oracle never removes assurance: the Promise
  stays assured until a newer judgment, under the new Oracle, says otherwise.
- Applying the rule is `judge`.

## Source

`contract/bedrock-v2.md` sections 3, 4 and 6; `contract/bedrock-v2.yaml`
`verbs.define` and `nouns.Oracle`.


## Executable procedure

Use the pinned receiver interface in `contract/tool-interface.md` and
`contract/tool-interface.json`. The JSON below is the exact client argument
shape after substitution. `${scope}` is the admitted scope; `${run}` is a
unique replay prefix. `${step.field}` binds a field from an earlier successful
response in `contract/tool-examples/calls.json`; these substitutions are
performed before sending, never by the receiver. Never guess allocated IDs.

Resolve `mint.made` from successful preceding responses. The receiver stamps the actor and role; callers never supply
actor, role, principal, allocated IDs or recording time. Preserve the verb's
roles and meaning in the Contract table above.

```json
{
  "op": "act",
  "verb": "define",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "oracle": {
      "title": "Check the empty-list probe",
      "judges": "${mint.made}",
      "inputs": "The fixture probe result and pinned source.",
      "holds_when": "The result is an empty list.",
      "fails_when": "The result differs from an empty list.",
      "arrangement": "deterministic"
    }
  },
  "request_id": "${run}:define"
}
```

The native request is `POST /v1/acts`. `${session}` is discovered caller
lineage added by the client, not a client argument. Its required envelope is:

```json
{
  "verb": "define",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "oracle": {
      "title": "Check the empty-list probe",
      "judges": "${mint.made}",
      "inputs": "The fixture probe result and pinned source.",
      "holds_when": "The result is an empty list.",
      "fails_when": "The result differs from an empty list.",
      "arrangement": "deterministic"
    }
  },
  "request_id": "${run}:define",
  "session": "${session}"
}
```

Retain `act_id`, `made`, `seq`, `recorded_at`, `changes` and any edit-window fields. Bind the returned `made` before any dependent call. Read back using this exact query:

```json
{
  "op": "query",
  "name": "record",
  "params": {
    "id": "${define.made}"
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
