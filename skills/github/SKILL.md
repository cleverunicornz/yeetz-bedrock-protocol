---
name: github
verb: observe
description: When you read or change a pull request, review, issue or GitHub project, or wait for or read CI - use the github MCP tools (github-agent-mcp), read every list to its end, wait for a run with gh run watch in the background, and read a failed run with actions_read.
---

# github

## Procedure

1. Call the `github` MCP tool for the object — pull request, review, issue,
   project, or Actions run — with `method` and that method's arguments (NOOA:
   `self.github`). Commit and push with `git`; use `gh` only to wait on a run
   or for what the tools do not cover.
2. While a result says `pagination.complete: false`, pass its `continuation`
   back; use the list only when complete.
3. On an `error` with a `required_permission`, stop that call and report it as
   infrastructure blocking you.
4. After a push, find the run with `actions_read` `list_runs` (`pullNumber`,
   `sha` or `branch`), then wait in the background and keep working:
   `gh run watch <run-id> --exit-status`.
5. On failure, read `actions_read` `failure_summary` with `run_id`; for more
   of one job, `job_log_tail` with `job_id`, `tail_lines` and a `filter`.
6. For a check from another app, read the pull request page or ask the human
   you work for.
7. A merge follows `git-etiquette`.

## Records

- `org/situation/invariants/I-000001-github-through-mcp-tools.md` — the tools,
  calls, and blind spots: `org/situation/references/I-000001/github-mcp-tools.md`
- `org/situation/invariants/I-000002-ci-waited-in-background.md` — finding,
  waiting for, and reading runs: `org/situation/references/I-000002/github-ci-runs.md`
- `org/situation/invariants/I-000003-github-lists-read-to-end.md` — results,
  paging, and errors: `org/situation/references/I-000003/github-mcp-results.md`
