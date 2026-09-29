# I-000002 — CI is waited for in the background and read by summary

## Priority

standard

## Invariant

A CI run is waited for in the background with
`gh run watch <run-id> --exit-status` while work continues, and a failed run
is read with `actions_read` — `failure_summary`, then `job_log_tail` for one
job — never by downloading whole logs.

## Basis

- [D-000001](org/situation/decisions/D-000001-knowledge-in-records-skills-as-verbs.md)
