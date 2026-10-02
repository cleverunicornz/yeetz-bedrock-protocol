---
name: produce
verb: produce
description: Bedrock verb `produce` - retain an observation of one real run of a Promise's subject as a Witness, with its evidence and no verdict. Read it when you have changed or run the subject of a Promise and must show what actually happened, and when you answer a judgment's findings.
---

# produce

`produce` makes a Witness: one observation from one real run, retained before
and independent of any verdict. Whoever makes the subject deliver a Promise
also owns showing it: the producer retains the observation; someone else
judges it.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Witness` |
| Inputs | `Promise` `evidence` |
| Outputs | `Witness` |
| Held by | `implementer` |

## When

A real run observed the Promise's subject: a test run, a deployment, a
measurement, a person trying it. Domain work changes the subject; `produce`
retains what a run of it showed.

## What it makes

- A Witness with `title`, `observes` (one Promise), `observed_at`,
  `coordinate` (what was run: a commit, a release, a draft, any version
  coordinate), `result` and `evidence` (at least one Reference).
- `result` says what was observed, never a verdict: "the run exited 0 and
  wrote 12 rows", not "it works".
- Its state is `produced`; a judgment makes it `judged`. Producing a Witness
  never moves the Promise's state.
- A Witness is immutable and never superseded.

## Answering a judgment

- A Gap a judge declared is binding as a finding; the producer never
  dismisses it.
- A fix is domain work, shown by a new Witness of a run after the fix, which
  is judged like any other.
- Disagreement is evidence: a Witness or Reference that whoever decides the
  Gap can weigh.

## Refusals

- A Witness without at least one evidence Reference is refused.
- A field over its limit (`title` and `coordinate` 256 characters, `result`
  512) is refused with the field, its size and the limit.

## Not this verb

- The verdict is `judge`, by someone other than the producer above board
  level; a judge act by the producer of the judged Witness is a drift signal.
- A better observation after an `inconclusive` verdict is `refine`. A
  misattributed Witness is withdrawn by `revoke`.

## Source

`contract/bedrock-v2.md` sections 3, 4, 6 and 7; `contract/bedrock-v2.yaml`
`verbs.produce` and `nouns.Witness`.
