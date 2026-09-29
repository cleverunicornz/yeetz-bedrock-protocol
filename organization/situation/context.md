# Organization situation

## Identity

The organization circle: the organization's own knowledge records, in the
same schema as a repository's `situation/`, installed read-only at user level
as `org/situation/` beside the organization layer's `AGENTS.md` and skills,
and versioned with the protocol release that ships them.

## Ownership

`OWNED`

## Phase

`INITIAL` — the first records carry GitHub work
([I-000001](org/situation/invariants/I-000001-github-through-mcp-tools.md),
[I-000002](org/situation/invariants/I-000002-ci-waited-in-background.md),
[I-000003](org/situation/invariants/I-000003-github-lists-read-to-end.md) and
their References), decomposed from the `github` skill under
[D-000001](org/situation/decisions/D-000001-knowledge-in-records-skills-as-verbs.md).
The other organization skills still hold their knowledge inline.

## Implementation map

- `org/AGENTS.md` — the protocol block and the organization layer: the rules,
  each naming the skill to read before acting.
- `org/skills/<name>/SKILL.md` — procedures; each declares its verb and
  points into this record set.
- `org/situation/` — this record set.

## Closure state

- Current run: none
- Last completed closure: none
- Transcript: none
