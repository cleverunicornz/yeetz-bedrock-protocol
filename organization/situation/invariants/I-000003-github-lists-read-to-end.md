# I-000003 — A GitHub list is read to its end before it is used

## Priority

standard

## Invariant

A `github` MCP tool result with `pagination.complete: false` is continued
with its `continuation` until complete before it is used as the whole.

## Basis

- [D-000001](org/situation/decisions/D-000001-knowledge-in-records-skills-as-verbs.md)
