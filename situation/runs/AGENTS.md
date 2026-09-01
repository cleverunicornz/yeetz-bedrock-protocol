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
path. Files in external public repositories are referenced only by full
public URL. Files in external private repositories are referenced by
declared coordinate — `Private: owner/repo@<ref>#<path>` — never by an
unauthenticated URL, never undeclared. Never reference a local clone, a
private checkout, or a machine-local path.

A declared-private reference that cannot be fetched is expected, not an
error: never stop for one, never remove it, never invent its contents.
Content from a private reference never crosses into a public document.
