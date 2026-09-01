# Oracles

An oracle defines the judgment rule for a promise. It states what inputs are
examined and what constitutes pass or fail. It does not execute itself; an
oracle may be designed before its executable implementation exists.

## File naming

```
O-<six digits>-<kebab-case-name>.md
```

## Required headings

- `State` — `designed` or `implemented`
- `Judges` — link to the promise
- `Inputs` — what evidence the oracle examines
- `Pass` — the condition that passes
- `Fail` — the condition that fails
- `Implementation` — present only when state is `implemented`

## States

`designed` — the judgment rule is stated but no executable check exists.

`implemented` — a test, workflow, or checker command exists and runs. The
Implementation section links it.

## Rules

- Pass and fail conditions must be decidable from the stated inputs.
- One oracle may judge one promise. When a judgment rule serves multiple
  promises, write one oracle per promise and link them in References.
- The oracle does not record results; witnesses do that.
- Changing a pass or fail condition after witnesses exist requires a new
  oracle superseding the old one.
