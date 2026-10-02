---
name: stipulate
verb: stipulate
description: Bedrock verb `stipulate` - state a binding rule in a scope as an Invariant. Read it when a rule must bind everyone working in a scope, or when you read which rules bind a scope.
---

# stipulate

`stipulate` makes an Invariant: a binding rule in a scope. A Decision may be its
basis; an axiom needs none. The Invariant binds its scope and every scope that
belongs to it, until it is superseded or revoked.

## Contract

| Field | Value |
|---|---|
| Kind | `act` |
| Acts on | `Invariant` |
| Inputs | `basis` |
| Outputs | `Invariant` |
| Held by | `authority` |

## When

A binding rule is needed in a scope. `basis` is optional: a Decision, a
Reference, a Witness or another Invariant the rule rests on.

## What it makes

- An Invariant with `title`, `rule` and `priority` (`critical` or `standard`).
  The rule is short enough to stand alone; depth goes in a Reference it links.
- Its state is `stipulated`, the past tense of this verb.
- The Invariants that bind a scope are those `stipulated` for it and for every
  scope it belongs to (the `binds` query); a superseded or revoked Invariant
  binds nothing.

## Refusals

- A field over its limit (`title` 256 characters, `rule` 1024) is refused with
  the field, its size and the limit; nothing is cut.

## Not this verb

- A rule is changed by `supersede` (a successor Invariant, stipulated first)
  or withdrawn by `revoke`; either cites a Decision as basis.
- A choice between options is `decide`; a commitment about behaviour is `mint`.

## Source

`contract/bedrock-v2.md` sections 3, 4 and 10; `contract/bedrock-v2.yaml`
`verbs.stipulate` and `nouns.Invariant`.
