# References

References hold retained depth: research, long-form material, rejected
paths, historical context, and anything a record points to that is too large
to live inline.

## Structure

References are organized by the record that owns them:

```
references/P-000001/
references/O-000003/
references/D-000014/
```

A reference is a child of the record that links it.

## Rules

- A reference must be linked from at least one record; unowned files here
  are misplaced.
- References are depth, not law. They never override a promise, oracle,
  decision, or invariant.
- Git is the canonical store for historical donor bytes. Copy donor material
  here only when active human/agent retrieval needs an in-tree reference; any
  copy must be owned by and linked from a record.
- Any content type is acceptable: markdown, images, data, diagrams.

## Reference discipline

Files inside this repository are referenced by repository-root-relative
path. Files in external public repositories are referenced only by full
public URL. Files in external private repositories are referenced by
declared coordinate — `Private: owner/repo@<ref>#<path>` — never by an
unauthenticated URL, never undeclared. Never reference a local clone, a
private checkout, or a machine-local path.

A declared-private reference that cannot be fetched is expected, not an
error: never stop for one, never remove it, never invent its contents.
Content from a private reference never crosses into a public document.

## Donor provenance

Git is the donor receipt. BACKPORT's opening checkpoint identifies the exact
trigger tree. Do not copy donor snapshots or create donor registries.

On DELTA, `git diff <last closing checkpoint>..<trigger head>` is the complete
review surface. An empty diff means there is no closure work; a nonempty diff
bounds it. Historical donor bytes remain available through `git show`.
