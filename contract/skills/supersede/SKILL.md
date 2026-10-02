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
