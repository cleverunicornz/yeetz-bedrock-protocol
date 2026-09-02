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

Every reference carries a visibility class so a reader never has to guess
whether a reference is broken or access-controlled.

- A file **inside this repository** is referenced by its repository-root-
  relative path: `situation/promises/P-000001-stable-identity.md`. Never a
  path that walks above the repository, never a machine-local path.
- Historical bytes from this repository are referenced as
  `<commit>:<repository-root-relative-path>` and resolved with `git show`.
  This is the canonical form when a BACKPORT later rewrites the live file.
- A file **in an external public repository** is referenced only by its
  full public URL, including the exact path to the file.
- A file **in an external private repository** is referenced by its
  coordinate — `Private: owner/repo@<ref>#<path>` — with a short access
  note. Never by an unauthenticated URL, never undeclared.
- Never reference a local clone of a public project as if other machines
  could access it. If the material matters, it is either committed into
  this repository (usually under `references/`) or linked by public URL.

## Private reference behavior

A declared-private reference that cannot be fetched is a normal, expected
state — not an error, not a missing file, and never grounds to stop work,
remove the reference, or invent its contents. Access to private
repositories is environment-dependent: a failed API call does not mean a
credentialed clone will not work. Agents use whatever access method their
environment provides; when the material is unreachable, they record the
need and proceed with available evidence. Content from a private reference
is never copied into a public document.

An undeclared reference that cannot be resolved is a defect. A declared
private reference that cannot be resolved is expected.

## Quantitative and provenance discipline

Every numeric claim names the exact repository-root-relative path or public
source it was counted from. Counts are re-derived from that source rather
than copied from another record. Words such as `donor`, `legacy`, `current`,
or `generated` always resolve to a named path, tree, commit, or URL.

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

## Bedrock operation

Repository phase and closure operation are separate classifications:

- `INITIALIZE` — no substantive donor or implementation; install the
  substrate and minimal orientation without inventing behavior.
- `BACKPORT` — substantive existing documentation/code, no completed Bedrock
  adoption; establish records from existing behavior and preserve already
  collapsed choices as Decisions.
- `DELTA` — a completed adoption exists; inspect only the pull-request diff
  and records it directly affects. Never re-derive unchanged donors.

Every run records its operation in the opening checkpoint.

Git checkpoint/stage history is the sole processing receipt. A file handled by
a stage commit inside a completed closure interval is already processed. DELTA
compares that stage to the current head and reviews only the changed lines. No
parallel donor registry or copied donor snapshot exists.

## Repository ownership

- `OWNED` — normal repository; the operational trunk is its default branch.
- `UPSTREAM_FORK` — `main` mirrors upstream; `internal/main` is the
  Bedrock-enabled operational trunk. Normal work branches from
  `internal/main`; only selected upstream contribution branches target
  `main`; `internal/main` never merges into `main`.

Every run records ownership and, for forks, upstream coordinates and trunk
roles in `context.md` and root `AGENTS.md`.

## README lifecycle

README is human-facing orientation and is always considered after records and
root `AGENTS.md` stabilize:

- `INITIALIZE` — minimal purpose and pointers; no invented behavior.
- `BACKPORT` — replace dense canonical detail with concise human orientation
  and pointers into `situation/`; retain donor depth through references.
- `DELTA` — update only when the delta changes human-facing purpose, usage,
  setup, or capabilities; otherwise leave it unchanged.

README never overrides records under `situation/`.
When multiple root human orientations exist (for example `README.md` and
`README.zh.md`), BACKPORT/DELTA keeps their purpose, status, branch topology,
and situation pointers consistent across languages.
