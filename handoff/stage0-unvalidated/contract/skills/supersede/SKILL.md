---
name: supersede
verb: supersede
description: Bedrock verb `supersede` - replace a record by a successor of the same noun, made first by its own verb; history stays. Read it when a record must change after its edit window, and before you change an assured Promise, a Decision or an Invariant.
---

# supersede

`supersede` replaces a record by a successor of the same noun. The successor
is made first by its own verb (a new Promise by `mint`, a new Oracle by
`define`, and so on); `supersede` then links the two and withdraws the old
one. History stays.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Invariant` `Gap` `Candidate` `Decision` `Promise` `Oracle` `Reference` |
| Inputs | `target` `successor` `basis` |
| Outputs | `superseded` |
| Held by | `authority` `orchestrator` `automation` |

## When

After the edit window, to replace a record by its successor. Within the
window the author corrects the record by amending it instead. After the
window an amendment is refused (`edit_window_closed`), and so is one by anyone
but the author (`not_author`); `revoke` and `supersede` are what remain.

## What it does

- The target becomes `superseded`. A `supersede` act always stands.
- It changes one step and never cascades: the target, and the subjects of a
  superseded Decision that its successor does not decide again (recomputed:
  a Candidate back to `evaluated` or `formulated`, a Gap back to `declared`).
- Superseding an Oracle or a Reference never removes assurance; the Promise
  stays assured until a newer judgment says otherwise.
- An assured Promise is invariant behaviour: changing it is a superseding
  Promise, minted with its own Oracle and new Witnesses, with a Decision as
  `basis`. Superseding a Decision or an Invariant also cites a Decision.
- Automation supersedes only Candidates not yet `decided`.
- References are immutable: a changed Reference is a new one that supersedes
  the old.

## Refusals

- A Witness is never superseded: a better observation is a new Witness made
  by `refine`; a misattributed one is revoked.
- A successor of another noun, or one already superseded or revoked, is
  refused.
- Superseding a record already superseded or revoked is refused.

## Not this verb

- Withdrawal without a successor is `revoke`.
- A Plan is changed by regrouping it, not superseded.

## Source

`contract/bedrock-v2.md` sections 3, 4, 5 and 6; `contract/bedrock-v2.yaml`
`verbs.supersede` and `one_step`.


## Executable procedure

Use the pinned receiver interface in `contract/tool-interface.md` and
`contract/tool-interface.json`. The JSON below is the exact client argument
shape after substitution. `${scope}` is the admitted scope; `${run}` is a
unique replay prefix. `${step.field}` binds a field from an earlier successful
response in `contract/tool-examples/calls.json`; these substitutions are
performed before sending, never by the receiver. Never guess allocated IDs.

Resolve `judgment_gap.made`, `successor.made` from successful preceding responses. The receiver stamps the actor and role; callers never supply
actor, role, principal, allocated IDs or recording time. Preserve the verb's
roles and meaning in the Contract table above.

```json
{
  "op": "act",
  "verb": "supersede",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "target": "${judgment_gap.made}",
    "successor": "${successor.made}",
    "reason": "The successor states the observed limit more precisely."
  },
  "request_id": "${run}:supersede"
}
```

The native request is `POST /v1/acts`. `${session}` is discovered caller
lineage added by the client, not a client argument. Its required envelope is:

```json
{
  "verb": "supersede",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "target": "${judgment_gap.made}",
    "successor": "${successor.made}",
    "reason": "The successor states the observed limit more precisely."
  },
  "request_id": "${run}:supersede",
  "session": "${session}"
}
```

Retain `act_id`, `made`, `seq`, `recorded_at`, `changes` and any edit-window fields. This act makes no record; `made` is null. Read back using this exact query:

```json
{
  "op": "query",
  "name": "record",
  "params": {
    "id": "${judgment_gap.made}"
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
