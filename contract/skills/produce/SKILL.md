---
name: produce
verb: produce
description: Bedrock verb `produce` - retain an observation of one real run of a Promise's subject as a Witness, with its evidence and no verdict. Read it when you have changed or run the subject of a Promise and must show what actually happened, and when you answer a judgment's findings.
---

# produce

`produce` makes a Witness: one observation from one real run, retained before
and independent of any verdict. Whoever makes the subject deliver a Promise
also owns showing it: the producer retains the observation; someone else
judges it.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Witness` |
| Inputs | `Promise` `evidence` |
| Outputs | `Witness` |
| Held by | `implementer` |

## When

A real run observed the Promise's subject: a test run, a deployment, a
measurement, a person trying it. Domain work changes the subject; `produce`
retains what a run of it showed.

## What it makes

- A Witness with `title`, `observes` (one Promise), `observed_at`,
  `coordinate` (what was run: a commit, a release, a draft, any version
  coordinate), `result` and `evidence` (at least one Reference).
- `result` says what was observed, never a verdict: "the run exited 0 and
  wrote 12 rows", not "it works".
- Its state is `produced`; a judgment makes it `judged`. Producing a Witness
  never moves the Promise's state.
- A Witness is immutable and never superseded.

## Answering a judgment

- A Gap a judge declared is binding as a finding; the producer never
  dismisses it.
- A fix is domain work, shown by a new Witness of a run after the fix, which
  is judged like any other.
- Disagreement is evidence: a Witness or Reference that whoever decides the
  Gap can weigh.

## Refusals

- A Witness without at least one evidence Reference is refused.
- A field over its limit (`title` and `coordinate` 256 characters, `result`
  512) is refused with the field, its size and the limit.

## Not this verb

- The verdict is `judge`, by someone other than the producer above board
  level; a judge act by the producer of the judged Witness is a drift signal.
- A better observation after an `inconclusive` verdict is `refine`. A
  misattributed Witness is withdrawn by `revoke`.

## Source

`contract/bedrock-v2.md` sections 3, 4, 6 and 7; `contract/bedrock-v2.yaml`
`verbs.produce` and `nouns.Witness`.


## Executable procedure

Use the pinned receiver interface in `contract/tool-interface.md` and
`contract/tool-interface.json`. The JSON below is the exact client argument
shape after substitution. `${scope}` is the admitted scope; `${run}` is a
unique replay prefix. `${step.field}` binds a field from an earlier successful
response in `contract/tool-examples/calls.json`; these substitutions are
performed before sending, never by the receiver. Never guess allocated IDs.

Resolve `evidence.made`, `mint.made` from successful preceding responses. The receiver stamps the actor and role; callers never supply
actor, role, principal, allocated IDs or recording time. Preserve the verb's
roles and meaning in the Contract table above.

```json
{
  "op": "act",
  "verb": "produce",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "witness": {
      "title": "Empty-list fixture observation",
      "observes": "${mint.made}",
      "observed_at": "${observed_at}",
      "coordinate": "${fixture_commit}",
      "result": "${probe_result}",
      "evidence": [
        "${evidence.made}"
      ]
    }
  },
  "request_id": "${run}:produce"
}
```

The native request is `POST /v1/acts`. `${session}` is discovered caller
lineage added by the client, not a client argument. Its required envelope is:

```json
{
  "verb": "produce",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "witness": {
      "title": "Empty-list fixture observation",
      "observes": "${mint.made}",
      "observed_at": "${observed_at}",
      "coordinate": "${fixture_commit}",
      "result": "${probe_result}",
      "evidence": [
        "${evidence.made}"
      ]
    }
  },
  "request_id": "${run}:produce",
  "session": "${session}"
}
```

Retain `act_id`, `made`, `seq`, `recorded_at`, `changes` and any edit-window fields. Bind the returned `made` before any dependent call. Read back using this exact query:

```json
{
  "op": "query",
  "name": "record",
  "params": {
    "id": "${produce.made}"
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

`${observed_at}`, `${fixture_commit}` and `${probe_result}` are actual probe
values supplied by the isolated replay. For real work use its actual run
time, artifact coordinate, result and previously stored evidence References.
A fixture observation is never a qualification of the deployed receiver.
