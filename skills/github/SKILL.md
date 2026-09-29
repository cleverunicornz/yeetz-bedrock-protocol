---
name: github
description: How agents work with GitHub - the github MCP tools (github-agent-mcp) for pull requests, reviews, issues, projects and Actions results, waiting for CI with gh run watch in the background, reading a failed run with actions_read, paging, errors, and what the tools cannot see. Read it before reading or changing a pull request, review, issue or project, and before waiting for or reading CI.
---

# github

Every harness in a repo pod has the `github` MCP server (github-agent-mcp).
Its nine tools act as the pod's GitHub identity: they can do what its token
permits. `git` stays for commits and pushes; `gh` for waiting on a run and
for anything the tools do not cover.

## Tools

| Tool | For |
|---|---|
| `pr_read` | pull requests: get, list, search, diff, status, reviews, comments, review threads |
| `pr_workspace` | changed files, commits, the head commit's checks; `assemble_review_context` for a review |
| `pr_write` | create; title, body, state, draft, base, labels, assignees, reviewers, comments, branch update, merge |
| `pr_review_write` | reviews, review comments, replies, resolving threads |
| `issue_read`, `issue_write` | issues: get, list, search, comments, sub-issues, timeline, linked pull requests; create, edit, comment, label, close |
| `project_read`, `project_write` | GitHub Projects: projects, fields, items, views, status updates |
| `actions_read` | Actions results: `list_runs`, `failure_summary`, `job_log_tail` |

- Every call takes `method` and that method's arguments; the tool's
  description lists both. Comment bodies are passed as arguments.
- **NOOA**: the same tools as async methods of `self.github`, for example
  `await self.github.pr_read(method="get", owner="cleverunicornz", repo="<repo>", pullNumber=12)`.
- A merge follows `git-etiquette` and the organization layer.

## Results

- Results are JSON `{"coverage", "data"}`. A list that stops at a bound says
  `pagination.complete: false` and gives a `continuation`: pass it back to
  read on. Never treat an incomplete read as the whole.
- A failure is `{"error": {kind, operation, status, message, hint,
  required_permission}}`. A missing permission is the token's, not yours to
  work around: report it as the organization layer says.

## Wait for CI, then read it

1. Find the run: `actions_read` `list_runs` with `pullNumber`, `sha` or
   `branch`. A run appears a few seconds after the push.
2. Wait in the background and keep working:
   `gh run watch <run-id> --exit-status`. It returns when the run ends; its
   exit code is the result. The tools never wait.
3. On failure: `actions_read` `failure_summary` with `run_id` gives the failed
   and cancelled jobs, their failing steps and a short cleaned log tail each.
   For more of one job, `job_log_tail` with `job_id`, `tail_lines` and a
   `filter`. Do not download whole logs.

## What the tools cannot see

- Check runs of other apps. The token cannot read check runs, so
  `pr_workspace` `get_check_runs` and `assemble_review_context` serve the head
  commit's Actions runs instead (`source: "actions_runs"`). A third-party
  app's check (external CI, code scanning) is not visible there: look at the
  pull request page, or ask the human you work for.
- Issue types need an organization permission the token may lack; the error
  says so.
