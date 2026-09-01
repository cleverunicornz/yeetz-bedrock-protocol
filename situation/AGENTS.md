# Situation System

All repository knowledge records live under `situation/`. This file explains
the structure, identifier rules, and relationships between namespaces.

## Structure

- `invariants/` — binding repository rules, explicit and citable
- `promises/` — falsifiable behavior claims with a lifecycle state
- `oracles/` — judgment rules that decide whether a promise holds
- `witnesses/` — immutable observations from real runs
- `decisions/` — append-only records of why a choice collapsed
- `plans/` — thin containers grouping promises into a delivery effort
- `references/` — retained depth linked from records
- `runs/` — automation-run evidence folders
- `context.md` — repository identity, phase, and current/intended state

## Identifier rules

Every record class carries a repository-scoped numeric identifier:

```
I-000001  invariant
P-000001  promise
O-000001  oracle
W-000001  witness
D-000001  decision
PLAN-000001  plan
```

Identifiers are minimum six decimal digits, zero-padded, monotonically
allocated, never reused, never renumbered. Expansion beyond six digits is
allowed.

## Reference discipline

References must resolve for a reader on any machine. The rules are simple
and admit no exceptions:

- A file **inside this repository** is referenced by its repository-root-
  relative path: `situation/promises/P-000001-stable-identity.md`. Never a
  path that walks above the repository, never a machine-local path.
- A file **outside this repository** is referenced only by its full public
  URL, including the exact path to the file. Never a bare repository name,
  a local clone path, or a private checkout path.
- Never reference a local clone of a public project as if other machines
  could access it. If the material matters, it is either committed into
  this repository (usually under `references/`) or linked by public URL.

A reference that a reader on another machine cannot resolve is a defect,
not a style issue.

## Relationships

```
Promise -> Oracle -> Witness -> disposition in the Promise
Decision -> Invariant (basis)
Decision -> Decision (supersedes)
Plan -> Promise set
Reference -> owning record
Run -> automation evidence
```

A promise states behavior. An oracle states the judgment rule. A witness
retains one observation. The promise's state records the current disposition
after applying the oracle to available witnesses. A decision explains why a
path was accepted or rejected; an invariant states the binding rule that
results.

## Assured promises are invariant

Every promise in state `assured` is invariant behavior. Changing it requires
a new promise superseding the old one, a decision explaining why, a
replacement oracle, and new witnesses. The old record remains immutable
history.

## Repository phase

`context.md` states the repository's current phase: `INITIAL`, `PLANNING`,
`IMPLEMENTATION`, or `EVOLUTION`. Absence of implementation source is a
current-phase fact; it never implies the repository's purpose is
documentation. Future-facing records are valid when clearly represented as
intended rather than implemented.
