# Waiting for and reading a CI run

Owned by [I-000002](org/situation/invariants/I-000002-ci-waited-in-background.md).

## Finding a run

`actions_read` `list_runs` takes `pullNumber`, `sha` or `branch`. A run
appears a few seconds after the push that triggers it.

## Waiting

`gh run watch <run-id> --exit-status` returns when the run ends; its exit
code is the run's result. Run in the background, it leaves the agent free to
keep working. The `github` MCP tools never wait.

## Reading a failure

- `actions_read` `failure_summary` with `run_id` gives the failed and
  cancelled jobs, their failing steps, and a short cleaned log tail for each.
- `actions_read` `job_log_tail` with `job_id`, `tail_lines` and a `filter`
  gives more of one job.
- A whole log is large and mostly noise; the two methods above return the
  part that explains the failure.
