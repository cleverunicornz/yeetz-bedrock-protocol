---
name: assure
verb: assure
description: Bedrock verb `assure` - the transition by which a Promise becomes `assured` when its latest standing judgment is `holds`; no one performs it. Read it when you need to know whether a Promise is assured, why, or what can remove its assurance.
---

# assure

`assure` is one of the thirteen verbs but not an act: it is the state
transition by which a Promise becomes `assured`. No one performs it and it
has no act node of its own. It is recorded as the state change of the `judge`
act whose verdict is `holds`, or of the `revoke` after which a `holds`
judgment is again the latest standing one.

## Contract

| Field | Value |
|---|---|
| Kind | `transition` |
| Acts on | `Promise` |
| Inputs | `judge` |
| Outputs | `assured` |
| Held by | none: no role performs it |

## When

A Promise is `assured` while its latest standing judgment is `holds`, and
`asserted` otherwise. `inconclusive` verdicts do not count: they are verdicts
on the Witness.

## What can change it

- **Removes assurance:** a later `does_not_hold` verdict, or revoking the
  Witness behind the assurance (unless an earlier `holds` judgment still
  stands and is again the latest).
- **Does not remove assurance:** superseding the Oracle or a Reference. The
  Promise stays assured until a newer judgment says otherwise; such Promises
  are listed by the `assured_under_earlier_oracle` query.
- `define` and `produce` never move a Promise.
- Recomputing assurance goes one step and creates no work.

## Refusals

- There is no `assure` act to record: an agent never sets a Promise
  `assured`. Assurance comes only from a judgment.

## Not this verb

- The judgment that causes it is `judge`. The standing judge act, Oracle and
  Witness behind an assured Promise are answered by the `assured_by` query.

## Source

`contract/bedrock-v2.md` sections 4, 5 and 6; `contract/bedrock-v2.yaml`
`verbs.assure`, `state_rule` and `no_recursive_invalidation`.


## Executable procedure

Use the pinned receiver interface in `contract/tool-interface.md` and
`contract/tool-interface.json`. The JSON below is the exact client argument
shape after substitution. `${scope}` is the admitted scope; `${run}` is a
unique replay prefix. `${step.field}` binds a field from an earlier successful
response in `contract/tool-examples/calls.json`; these substitutions are
performed before sending, never by the receiver. Never guess allocated IDs.

Resolve `mint.made` from the successful mint response. The receiver stamps the actor and role; callers never supply
actor, role, principal, allocated IDs or recording time. Preserve the verb's
roles and meaning in the Contract table above.

```json
{
  "op": "query",
  "name": "assured_by",
  "params": {
    "promise": "${mint.made}"
  }
}
```

The native request is `POST /v1/query`. `${session}` is discovered caller
lineage added by the client, not a client argument. Its required envelope is:

```json
{
  "name": "assured_by",
  "params": {
    "promise": "${mint.made}"
  }
}
```

Read `state`, `standing` and `since`. An assured Promise has `state` equal to `assured` and a standing holds judgment. No assure act is submitted. Read back using this exact query:

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
