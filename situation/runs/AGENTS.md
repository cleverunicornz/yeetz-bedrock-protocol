# Runs

Runs retain automation evidence: what each closure run observed, decided, and
changed, so results can be evaluated and prompts improved.

## Structure

Each run creates one directory:

```
runs/bedrock-<timestamp>-<head prefix>-<suffix>/
```

## Standard contents

- `closure-report.md` — what the closer observed and changed
- `validation-report.md` — what the validator found
- `correction-report.md` — what the corrector changed, when correction ran
- `result.json` — the structured terminal result

## Rules

- Run directories are append-only; a completed run is never edited.
- Reports state what happened, not a second derivation of the repository.
- Run evidence is for evaluation and audit; it is not repository law.

## Reference discipline

Files inside this repository are referenced by repository-root-relative
path. Files outside this repository are referenced only by full public URL.
Never reference a local clone, a private checkout, or a machine-local path.
Every reference must resolve for a reader on any machine.
