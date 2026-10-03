---
name: stipulate
verb: stipulate
description: Bedrock verb `stipulate` - state a binding rule in a scope as an Invariant. Read it when a rule must bind everyone working in a scope, or when you read which rules bind a scope.
---

# stipulate

`stipulate` makes an Invariant: a binding rule in a scope. A Decision may be its
basis; an axiom needs none. The Invariant binds its scope and every scope that
belongs to it, until it is superseded or revoked.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Invariant` |
| Inputs | `basis` |
| Outputs | `Invariant` |
| Held by | `authority` |

## When

A binding rule is needed in a scope. `basis` is optional: a Decision, a
Reference, a Witness or another Invariant the rule rests on.

## What it makes

- An Invariant with `title`, `rule` and `priority` (`critical` or `standard`).
  The rule is short enough to stand alone; depth goes in a Reference it links.
- Its state is `stipulated`, the past tense of this verb.
- The Invariants that bind a scope are those `stipulated` for it and for every
  scope it belongs to (the `binds` query); a superseded or revoked Invariant
  binds nothing.

## Refusals

- A field over its limit (`title` 256 characters, `rule` 1024) is refused with
  the field, its size and the limit; nothing is cut.

## Not this verb

- A rule is changed by `supersede` (a successor Invariant, stipulated first)
  or withdrawn by `revoke`; either cites a Decision as basis.
- A choice between options is `decide`; a commitment about behaviour is `mint`.

## Source

`contract/bedrock-v2.md` sections 3, 4 and 10; `contract/bedrock-v2.yaml`
`verbs.stipulate` and `nouns.Invariant`.


## Executable procedure

Use the pinned receiver interface in `contract/tool-interface.md` and
`contract/tool-interface.json`. The JSON below is the exact client argument
shape after substitution. `${scope}` is the admitted scope; `${run}` is a
unique replay prefix. `${step.field}` binds a field from an earlier successful
response in `contract/tool-examples/calls.json`; these substitutions are
performed before sending, never by the receiver. Never guess allocated IDs.

The receiver stamps the actor and role; callers never supply
actor, role, principal, allocated IDs or recording time. Preserve the verb's
roles and meaning in the Contract table above.

```json
{
  "op": "act",
  "verb": "stipulate",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "invariant": {
      "title": "Fixture observations keep their source",
      "rule": "Every fixture observation points to its evidence.",
      "priority": "standard"
    }
  },
  "request_id": "${run}:stipulate"
}
```

The native request is `POST /v1/acts`. `${session}` is discovered caller
lineage added by the client, not a client argument. Its required envelope is:

```json
{
  "verb": "stipulate",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "invariant": {
      "title": "Fixture observations keep their source",
      "rule": "Every fixture observation points to its evidence.",
      "priority": "standard"
    }
  },
  "request_id": "${run}:stipulate",
  "session": "${session}"
}
```

Retain `act_id`, `made`, `seq`, `recorded_at`, `changes` and any edit-window fields. Bind the returned `made` before any dependent call. Read back using this exact query:

```json
{
  "op": "query",
  "name": "record",
  "params": {
    "id": "${stipulate.made}"
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
