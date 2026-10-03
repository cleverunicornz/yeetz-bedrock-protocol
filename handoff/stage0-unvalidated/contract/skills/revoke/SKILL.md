---
name: revoke
verb: revoke
description: Bedrock verb `revoke` - withdraw a record or a Plan with its reason after its edit window; history stays. Read it when a record was mistaken, misattributed or no longer applies and has no successor, and before you think of deleting anything.
---

# revoke

`revoke` withdraws a record or a Plan, with a reason. Nothing is deleted: the
record and its history stay, and indexes hide it while lineage keeps it.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Invariant` `Gap` `Candidate` `Decision` `Promise` `Oracle` `Witness` `Reference` `Plan` |
| Inputs | `target` `basis` |
| Outputs | `revoked` |
| Held by | `authority` `orchestrator` `automation` |

## When

After the edit window, to withdraw a record with its reason. Within the
window the author corrects the record by amending it instead. After the
window an amendment is refused (`edit_window_closed`), and so is one by anyone
but the author (`not_author`); `revoke` and `supersede` are what remain.

## What it does

- The target becomes `revoked`. A `revoke` act always stands: revoking a
  successor does not restore what it superseded.
- It changes one step and never cascades:
  - revoking a Witness changes that Witness and its Promise's state (an
    assured Promise goes back to `asserted` unless an earlier `holds`
    judgment still stands and is again the latest);
  - revoking a Decision recomputes the subjects it decided (a Candidate back
    to `evaluated` or `formulated`, a Gap back to `declared`);
  - nothing else changes, and no act is generated.
- Revoking an assured Promise, a Decision or an Invariant cites a Decision as
  `basis`.
- Automation revokes only Candidates not yet `decided`.
- A Gap revoked by someone other than its declarer is a drift signal.

## Refusals

- Revoking a record that is already superseded or revoked is refused.

## Not this verb

- A replacement is `supersede`: withdraw and name the successor in one act.
- A better observation of a Promise is a new Witness by `refine`, not a
  revocation of the old one.

## Source

`contract/bedrock-v2.md` sections 4, 5 and 6; `contract/bedrock-v2.yaml`
`verbs.revoke`, `one_step` and `no_recursive_invalidation`.


## Executable procedure

Use the pinned receiver interface in `contract/tool-interface.md` and
`contract/tool-interface.json`. The JSON below is the exact client argument
shape after substitution. `${scope}` is the admitted scope; `${run}` is a
unique replay prefix. `${step.field}` binds a field from an earlier successful
response in `contract/tool-examples/calls.json`; these substitutions are
performed before sending, never by the receiver. Never guess allocated IDs.

Resolve `produce.made` from successful preceding responses. The receiver stamps the actor and role; callers never supply
actor, role, principal, allocated IDs or recording time. Preserve the verb's
roles and meaning in the Contract table above.

```json
{
  "op": "act",
  "verb": "revoke",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "target": "${produce.made}",
    "reason": "Withdraw the fixture observation to exercise assurance recomputation."
  },
  "request_id": "${run}:revoke"
}
```

The native request is `POST /v1/acts`. `${session}` is discovered caller
lineage added by the client, not a client argument. Its required envelope is:

```json
{
  "verb": "revoke",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "target": "${produce.made}",
    "reason": "Withdraw the fixture observation to exercise assurance recomputation."
  },
  "request_id": "${run}:revoke",
  "session": "${session}"
}
```

Retain `act_id`, `made`, `seq`, `recorded_at`, `changes` and any edit-window fields. This act makes no record; `made` is null. Read back using this exact query:

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
