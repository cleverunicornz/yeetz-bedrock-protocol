---
name: ste100-review
verb: evaluate
description: Evaluate a proposed change to Bedrock STE100 Communication against an observed communication failure and independent counterexamples, before its owner decides.
---

# STE100 Convention Review

This skill specialises `evaluate`. Read `contract/skills/evaluate/SKILL.md`
for its inputs, outcomes and procedure. It produces findings that inform a
Decision. The convention is `contract/communication/ste100-writing.md`;
its source lineage is `contract/communication/asd-ste100-issue9.md`.

## Review question

Could applying the current convention, or a specific extension of it, have
prevented this failure? What useful expression, inference or behaviour
would that extension impair?

## Inputs

Read the Candidate, the original interaction and relevant context, the
observed interpretation or action, and the convention version in use.
Use References to retain the supporting material with its existing
visibility. Separate what happened from explanations inferred afterwards.

A review starts from assigned work. Its requester arranges a proposer and
a different agent to examine the proposal adversarially, using the
adopter's runtime and the roles in `contract/roles.md`. Both receive the
original case and exact proposal. Neither is instructed to reach a
predetermined outcome.

## Evaluation

1. Identify where expression or interpretation contributed to the failure.
   Check whether applying an existing convention addresses it. State what
   the evidence establishes and what remains unknown.
2. Examine the exact proposed wording and scope. Cite the applicable STE
   rule or mark the addition as a Bedrock adaptation. Show a rewritten
   example and explain how it could prevent the observed failure.
3. The independent agent tests that argument against concrete counterexamples.
   Look for changed meaning, lost useful inference, cumbersome expression,
   or ambiguity moved elsewhere. Assess the original case as well as the
   cases that count against the proposal.
4. Compare the supported benefits, costs and alternatives. Retain remaining
   disagreement and identify any evidence that would change the conclusion.
   Label hypothetical rewrites and predicted consequences as counterfactual;
   keep actual observations distinct.
5. Record the evaluation using its existing outcome: `favourable`,
   `unfavourable`, `mixed` or `inconclusive`. Findings are References. State
   the recommended wording and scope, strongest supported objection, and
   remaining uncertainty so the owner can decide which risk to accept.

## Place in the Bedrock loop

An encountered concern uses `declare` (a Gap); a possible response uses
`formulate` (a Candidate). Read `contract/skills/declare/SKILL.md` and
`contract/skills/formulate/SKILL.md` when doing those acts. The proposer and
the independent reviewer each use `evaluate` for their analyses. The owner
uses `decide` to accept or decline the Candidate, or to close or keep a Gap;
read `contract/skills/decide/SKILL.md` for those distinctions.

The owner may request a revision or further evidence before choosing.
There is no additional `revise` act. The author's eligible correction uses
`contract/structural-skills/amend/SKILL.md`. A changed claim after the edit
window is a newly formulated Candidate replacing its predecessor through
`contract/skills/supersede/SKILL.md`. Additional evidence without a changed
claim uses `contract/skills/refine/SKILL.md`, under its role guidance.

Evaluate the revised Candidate again. A decided Candidate's changed
proposal also needs a successor before evaluation. Each further pass names
the changed proposal, new evidence or unresolved question it addresses.
Keep arguments attached to the exact proposal reviewed. Continue until the
owner adopts a proposal, retains the current convention, or leaves a
specified question open. Agreement between reviewers does not replace the
owner's choice, and a review need not result in a convention change.

A selected commitment follows `contract/skills/mint/SKILL.md` and
`contract/skills/define/SKILL.md`. Actual qualification follows
`contract/skills/produce/SKILL.md` and `contract/skills/judge/SKILL.md`.
Changes to assured behaviour follow their existing supersession rules.
Changing the shared communication convention is a Bedrock-level choice;
runtime scheduling and tool access remain the adopter's responsibility.
