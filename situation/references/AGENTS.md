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
- Donor material retained for historical value lives here, never in
  namespace folders.
- Any content type is acceptable: markdown, images, data, diagrams.

## Reference discipline

Files inside this repository are referenced by repository-root-relative
path. Files outside this repository are referenced only by full public URL.
Never reference a local clone, a private checkout, or a machine-local path.
Every reference must resolve for a reader on any machine.
