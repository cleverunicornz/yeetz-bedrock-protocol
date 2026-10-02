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
