# D-000001 — Organization knowledge lives in records; skills are verbs

## Status

accepted

## Date

2026-09-29

## Context

Organization skills carried their knowledge inline: the `github` skill held
the tool catalogue, result and error shapes, and what the tools cannot see
beside the steps to follow. Knowledge copied into a procedure drifts from
every other place that needs it, and a skill's body is loaded only when the
skill is. The protocol's record classes already name every kind of knowledge,
and its verbs name every act.

## Evidence

None: a preference of the organization's human authority, stated on
2026-09-29, not an evidence-derived choice.

## Decision

The organization keeps its knowledge once, as records in its own situation
(`org/situation/`), in the same schema, layout, and namespace rules as a
repository's `situation/`: mostly Invariants and References. A skill is a
verb: its `description` is the trigger (when it applies), its body is the
procedure only (steps and checks), and it points by path to the records it
relies on, declaring its verb in `verb` front matter.

The `github` skill is the first worked example. Its bounding rules became
[I-000001](org/situation/invariants/I-000001-github-through-mcp-tools.md),
[I-000002](org/situation/invariants/I-000002-ci-waited-in-background.md), and
[I-000003](org/situation/invariants/I-000003-github-lists-read-to-end.md); its
descriptive knowledge became
[github-mcp-tools](org/situation/references/I-000001/github-mcp-tools.md),
[github-ci-runs](org/situation/references/I-000002/github-ci-runs.md), and
[github-mcp-results](org/situation/references/I-000003/github-mcp-results.md).
The skill declares `observe`.

## Why

A harness keeps each skill's name and description in the agent's context and
loads the body at the moment of action, so the description is the trigger
that must be right, and the body is best spent on steps. Knowledge written
once as records is read by every procedure that needs it and changes in one
place.

## Rejected alternatives

- Knowledge kept inline in skills: each copy drifts, and none is citable as a
  record.
- A separate schema for organization knowledge: a second schema to learn and
  maintain; the repository schema already fits.

## Consequences

- The organization layer installs `org/situation/` beside `org/AGENTS.md` and
  `org/skills/`; the source is `organization/situation/` in the protocol
  repository.
- Other organization skills move their knowledge into records only after the
  operator reviews this example.

## Revisit when

The worked example shows agents failing to follow a pointer they needed, or a
harness stops surfacing skill descriptions ahead of their bodies.
