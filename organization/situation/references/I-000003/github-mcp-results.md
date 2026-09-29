# github MCP results, paging and errors

Owned by [I-000003](org/situation/invariants/I-000003-github-lists-read-to-end.md).

## Results

A result is JSON `{"coverage", "data"}`. A list that stops at a bound says
`pagination.complete: false` in its coverage and gives a `continuation`;
passing the `continuation` back to the same method reads on.

## Errors

A failure is `{"error": {kind, operation, status, message, hint,
required_permission}}`. A `required_permission` names a permission the pod's
token lacks: the token's limit, not the caller's, and not something the
caller can grant.
