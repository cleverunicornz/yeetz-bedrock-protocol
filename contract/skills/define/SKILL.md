---
name: define
verb: define
description: Bedrock verb `define` - make the Oracle that says how one Promise is judged - its inputs, when it holds, when it fails, and who or what applies it. Read it when a Promise needs its judgment rule, ideally before any Witness is produced.
---

# define

`define` makes an Oracle: the judgment rule for one Promise. It states the
inputs a judge uses, when the Promise holds, when it fails, and how the
judgment is arranged.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Oracle` |
| Inputs | `Promise` |
| Outputs | `Oracle` |
| Held by | `authority` `orchestrator` |

## When

A Promise needs its judgment rule. Best before `produce`; a retrospective
Oracle is ordinary and honest about its time.

## What it makes

- An Oracle with `title`, `judges` (exactly one Promise), `inputs`,
  `holds_when`, `fails_when`, `arrangement` (`human`, `agent`,
  `deterministic` or `mixed`) and an optional `executable` pointer. A wholly
  human Oracle is complete as it stands.
- Its state is `defined`. Defining an Oracle never moves the Promise's state.
- A judgment applies the Promise's Oracle that is neither superseded nor
  revoked.

## Refusals

- A field over its limit (`title` 256 characters; `inputs`, `holds_when` and
  `fails_when` 1024) is refused with the field, its size and the limit.

## Not this verb

- A stricter or corrected rule is a new Oracle that supersedes this one
  (`supersede`). Superseding an Oracle never removes assurance: the Promise
  stays assured until a newer judgment, under the new Oracle, says otherwise.
- Applying the rule is `judge`.

## Source

`contract/bedrock-v2.md` sections 3, 4 and 6; `contract/bedrock-v2.yaml`
`verbs.define` and `nouns.Oracle`.
