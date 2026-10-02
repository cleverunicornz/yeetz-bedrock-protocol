---
name: declare
verb: declare
description: Bedrock verb `declare` - record an absence, concern or uncertainty as a Gap, at its actual certainty, even when minor or tentative. Read it whenever you meet something missing, doubtful or unknown, and when a judgment finds a condition under which a Promise might not hold.
---

# declare

`declare` makes a Gap: an absence, concern or uncertainty, recorded at the
certainty the evidence supports. Declaring assigns nothing: it does not make
anyone responsible for investigating or resolving the Gap.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Gap` |
| Inputs | `about` `arose_in` |
| Outputs | `Gap` |
| Held by | `authority` `orchestrator` `scout` `implementer` `validator` `advisor` `automation` |

## When

Whenever an absence, concern or uncertainty is met, even minor or tentative.
`about` links the records it concerns; `arose_in` names the act during which it
arose, for example a judgment.

## What it makes

- A Gap with `title`, `statement` and an optional `impact`. Its state is
  `declared`.
- State exactly what the evidence shows and no more: "not found where I
  looked", with where you looked, rather than "does not exist". An inference
  is labelled as one, with the evidence it rests on.

## Gaps from a judgment

- A judge declares the conditions under which the Promise might not hold as
  separate `declare` acts with `arose_in` set to the judge act.
- Such a Gap is binding as a finding: recorded, visible, and decided only by
  `decide`. The producer of the judged work cannot dismiss it.
- It never gates assurance, and it is not a Promise anyone asserted. Turning
  it into work takes `formulate`, `decide` and `mint`.

## Refusals

- A field over its limit (`title` 256 characters, `statement` and `impact`
  1024) is refused with the field, its size and the limit; nothing is cut.

## Not this verb

- A further observation of a Gap already declared is a sighting added by
  `refine`, not a second Gap.
- A Gap is decided only by `decide` (outcome `close` or `keep`). A mistaken
  declaration is withdrawn by `revoke`; a Gap revoked by someone other than
  its declarer is a drift signal.
- A possible response to a Gap is `formulate`.

## Source

`contract/bedrock-v2.md` sections 3, 4 and 6; `contract/bedrock-v2.yaml`
`verbs.declare`, `nouns.Gap` and `judge_rule.gaps`.
