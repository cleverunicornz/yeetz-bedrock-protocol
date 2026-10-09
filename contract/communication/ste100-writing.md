# Bedrock STE100 Communication

Profile 1, introduced by `migrations/v2.1.0-to-v2.1.1.md`. Source: ASD-STE100,
Issue 9, 2025-01-15; edition, rule coordinates and adaptations are retained in
`contract/communication/asd-ste100-issue9.md`.

This is Bedrock's shared writing convention. Apply it to agent-authored
records, handoffs and general communication in every Bedrock setting,
including personal use. Human input remains natural. Organisations and
repositories inherit this baseline and may add domain terminology.

## Writing

1. Write short sentences, usually with one main point or instruction. Use
   20 words for instructions and 25 for descriptions as editing targets.
2. Use active voice when the actor is known. Name the actor where its
   identity matters; leave an unknown actor or cause unknown.
3. Use simple tenses appropriate to the statement: present for stated
   behaviour, past for observations, and explicit wording for possibilities
   and intended behaviour. Preserve a record's stated lifecycle status.
4. Put relevant conditions before instructions. Keep dependencies,
   exceptions and actions that occur together connected.
5. Use the same term for the same concept. Preserve Bedrock meanings and
   technical names. Prefer familiar words over unnecessary synonyms.
6. Preserve meaning when simplifying: scope, uncertainty, negation,
   quantities, permission and commitment. Keep code, commands, identifiers,
   quotations and retained evidence exact.
7. Give each paragraph one topic. Connect related statements explicitly;
   use lists when they clarify steps or alternatives.

These conventions are normal authoring practice. Exercise judgment where a
convention would distort useful meaning. An observed communication failure
can inform a review; it does not by itself assign a convention change.

## Vocabulary and progressive disclosure

Nouns: **Invariant, Gap, Candidate, Decision, Promise, Oracle, Witness,
Reference**. Their definitions are in `contract/bedrock-v2.md`, section 3.

Verbs: **stipulate, declare, formulate, evaluate, decide, mint, define,
produce, refine, judge, assure, revoke, supersede**. Each has its procedure
at `contract/skills/<verb>/SKILL.md`; `assure` names a transition.

**Plan** groups work. Structural acts **store, group, regroup, relate,
amend** have procedures at `contract/structural-skills/<act>/SKILL.md`.

Read the definitions and individual skills relevant to the assigned work.
Role guidance is in `contract/roles.md`. These paths start at the published
protocol root; installed verb and structural skills are also exposed under
`bedrock/skills/` as specified in `compiler/README.md`.

For an assigned review of a communication failure or proposed convention
change, read `contract/communication/ste100-review/SKILL.md`.
