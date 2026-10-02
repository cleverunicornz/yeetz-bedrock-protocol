---
name: decide
verb: decide
description: Bedrock verb `decide` - collapse a choice into a Decision with its grounds, recording each subject's outcome (a Candidate accepted or declined, a Gap closed or kept). Read it when a choice must be made or recorded, and before you treat a Candidate or Gap as settled.
---

# decide

`decide` collapses a choice. It makes a Decision holding the grounds and
records an outcome for each subject it decides: a Candidate `accept` or
`decline`, a Gap `close` or `keep`. A Decision never mints: committing to an
accepted Candidate is a separate `mint`.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Decision` `Candidate` `Gap` |
| Inputs | `considered` |
| Outputs | `Decision` `outcomes` |
| Outcomes | `accept` `decline` `close` `keep` |
| Held by | `authority` |

## When

A choice collapses: a Candidate accepted or declined, a Gap closed or kept, or
any other recorded choice. `considered` links what was weighed.

## What it makes

- A Decision with `title`, `statement` and `why`, and optionally `rejected`
  (each alternative and why it lost) and `revisit_when`. Its state is
  `decided`.
- Each subject named in its outcomes is left `decided`, whatever the outcome.
  The outcome is recorded on the act and is never a state.
- A subject's outcome rests on its Decision: when the Decision is revoked, or
  superseded by one that does not decide that subject, the subject's state is
  recomputed one step (a Candidate back to `evaluated` or `formulated`, a Gap
  back to `declared`). Nothing else follows.

## Refusals

- An outcome that does not belong to its subject's noun is refused.
- Deciding a superseded or revoked subject is refused. A `decided` subject may
  be decided again by a later Decision.
- A field over its limit (`title` 256 characters, `statement`, `why` and
  `revisit_when` 1024) is refused with the field, its size and the limit.

## Not this verb

- Investigating before the choice is `evaluate`; it informs `decide` and
  never replaces it.
- Committing to an accepted Candidate is `mint`, citing this Decision as its
  basis.
- Changing a Decision is `supersede` (a successor Decision); withdrawing it is
  `revoke`, citing a Decision as basis.

## Source

`contract/bedrock-v2.md` sections 3, 4 and 5; `contract/bedrock-v2.yaml`
`verbs.decide`, `nouns.Decision` and `outcomes.decide`.
