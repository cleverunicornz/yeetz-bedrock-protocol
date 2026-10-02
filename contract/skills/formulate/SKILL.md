---
name: formulate
verb: formulate
description: Bedrock verb `formulate` - derive a possible response from evidence and record it as a Candidate, a brief hypothesis that commits no one. Read it when evidence suggests a response to a Gap, Witness, Decision, Reference or another Candidate.
---

# formulate

`formulate` makes a Candidate: a brief hypothesis, a possible response derived
from evidence. A Candidate is not a commitment; it becomes one only when a
Decision accepts it and a Promise is minted from it.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Candidate` |
| Inputs | `responds_to` |
| Outputs | `Candidate` |
| Held by | `authority` `orchestrator` `scout` `implementer` `advisor` `automation` |

## When

Evidence suggests a possible response. Walk the scope first: when a Candidate
already says it, add your evidence to it as a sighting (`refine`) or replace it
(`supersede`) instead of writing a duplicate.

## What it makes

- A Candidate with `title` and `hypothesis`, and at least one `responds_to`
  link: a Gap, Witness, Decision, Reference or Candidate. Depth goes in
  References it links.
- Its state is `formulated`; `evaluate` may move it to `evaluated`, and
  `decide` to `decided`.

## Refusals

- A Candidate without a `responds_to` link is refused: it is formulated from
  the evidence it responds to.
- A field over its limit (`title` 256 characters, `hypothesis` 1024) is
  refused with the field, its size and the limit; nothing is cut.

## Not this verb

- Investigating a Candidate is `evaluate`; accepting or declining it is
  `decide`; committing to it is `mint`.

## Source

`contract/bedrock-v2.md` sections 3 and 4; `contract/bedrock-v2.yaml`
`verbs.formulate` and `nouns.Candidate`.
