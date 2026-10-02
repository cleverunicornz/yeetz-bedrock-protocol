---
name: refine
verb: refine
description: Bedrock verb `refine` - add without changing a claim - a better Witness after an inconclusive verdict, or a further sighting on an existing Gap or Candidate. Read it when you have new evidence for something already recorded, before you write a duplicate.
---

# refine

`refine` adds evidence without changing a claim. On a Witness it makes a new
Witness linked to the earlier one; on a Gap or a Candidate it adds a
sighting: a note and optional References.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Witness` `Gap` `Candidate` |
| Inputs | `target` `evidence` |
| Outputs | `Witness` `sighting` |
| Held by | `implementer` `automation` |

## When

- After an `inconclusive` verdict, when a better observation can settle it.
- When a Gap or Candidate already recorded is met again: add the sighting to
  it instead of declaring or formulating a duplicate. Independent sightings
  count as further evidence for it.

## What it makes

- **On a Witness:** a new Witness of the same Promise, with a `refines` link
  to the earlier one, which stays as it was. The new Witness is `produced`
  and is judged like any other.
- **On a Gap or Candidate:** a sighting. It gives no state; the record keeps
  its claim and its state.

## Refusals

- Refining a revoked Witness is refused; produce a new Witness instead.
- Refining any other noun is refused.

## Not this verb

- A Witness is never superseded; `refine` is how a better observation
  arrives.
- Changing what a Gap or Candidate claims is `supersede` (a successor record)
  or, within the edit window, the author's own amendment.

## Source

`contract/bedrock-v2.md` sections 3, 4 and 6; `contract/bedrock-v2.yaml`
`verbs.refine`.
