# Runs

Runs retain automation evidence as a bounded Git event interval. Git commits,
not a parallel result database, are the authoritative event log.

## Structure

Each run creates one append-only directory:

```
runs/bedrock-<timestamp>-<head prefix>-<suffix>/
```

## Standard contents

- `opening.md` — immutable opening checkpoint metadata
- `closure-report.md` — what the closer observed and changed
- `validation-report.md` — what the validator found
- `correction-report.md` — present only when correction ran
- `completion.md` — immutable closing checkpoint metadata

No `result.json` exists. Stage commits and their ancestry are the result.

## Opening checkpoint commit

Subject:

```
bedrock: open closure <run-id>
```

Required trailers:

```
Bedrock-Run: <run-id>
Bedrock-Event: open
Bedrock-Operation: INITIALIZE | BACKPORT | DELTA
Bedrock-Ownership: OWNED | UPSTREAM_FORK
Bedrock-Trigger-Head: <sha>
Bedrock-Protocol: <sha>
```

The commit adds `opening.md` and nothing else.

## Stage commits

Closer stages, when changed:

```
bedrock: <run-id> records
bedrock: <run-id> agents-index
bedrock: <run-id> readme
```

Validator:

```
bedrock: <run-id> validation approved
bedrock: <run-id> validation correct
```

Corrector stages, only when its docket touches them:

```
bedrock: <run-id> correct records
bedrock: <run-id> correct agents-index
bedrock: <run-id> correct readme
```

Every stage commit carries `Bedrock-Run`, `Bedrock-Event`, and
`Bedrock-Opening` trailers. Each stage is pushed before the next stage begins.

## Closing checkpoint commit

Subject:

```
bedrock: complete closure <run-id>
```

It adds `completion.md` and carries:

```
Bedrock-Run: <run-id>
Bedrock-Event: complete
Bedrock-Opening: <sha>
Bedrock-Operation: <operation>
Bedrock-Records: <sha or unchanged>
Bedrock-Agents-Index: <sha or unchanged>
Bedrock-README: <sha or unchanged>
Bedrock-Validation: <sha>
Bedrock-Correction: <sha or none>
Bedrock-Verdict: APPROVED | CORRECTED
Bedrock-Protocol: <sha>
```

## Recovery

An opening checkpoint without a matching closing checkpoint is an incomplete
run. A replacement orchestrator reads Git history, verifies stage subjects,
trailers, ancestry, and path scopes, then resumes from the last valid stage.
No session-local or external result state is required.

## Rules

- Opening and completion files are authored only by the orchestrator.
- Repository knowledge is authored only by closer/corrector stage commits.
- Each agent commits and pushes its own stages immediately.
- A pushed checkpoint or stage commit is immutable. Never amend, rebase,
  reset, or force-push it. A malformed stage is repaired by a new superseding
  stage commit; both SHAs and the reason are disclosed in run evidence.
- Before pushing, the author verifies the required subject and trailers from
  the commit object itself.
- Completed run directories are immutable.
- Re-running creates a new run ID and checkpoint pair.
