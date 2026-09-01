# Witnesses

A witness retains one observation from one real run. It is immutable
evidence, not a living status. A witness proves an observation happened,
never that a behavior always holds.

## File naming

```
witnesses/P-<promise six digits>/W-<six digits>-<kebab-case-name>.md
```

Witnesses are grouped by the promise they observe.

## Required headings

- `Promise` — the observed promise
- `Oracle` — the oracle applied
- `Result` — `PASS`, `FAIL`, `INVALID`, or `BLOCKED`
- `Head` — the exact commit the observation ran against
- `Observed` — the date of the observation
- `Evidence` — URLs, digests, and artifact references

## Results

- `PASS` — the oracle passed on this observation.
- `FAIL` — the oracle failed; this is evidence, not garbage.
- `INVALID` — the observation could not exercise the oracle meaningfully.
- `BLOCKED` — the observation could not run to completion.

## Rules

- Never edit a witness after creation. Corrections are new witnesses.
- Evidence must be retained and retrievable: a workflow run URL, an
  artifact digest, or a committed result file.
- A failed witness explains how a promise's state changed; keep it.
- A witness observes one promise under one oracle at one head.

## Reference discipline

Files inside this repository are referenced by repository-root-relative
path. Files outside this repository are referenced only by full public URL.
Never reference a local clone, a private checkout, or a machine-local path.
Every reference must resolve for a reader on any machine.
