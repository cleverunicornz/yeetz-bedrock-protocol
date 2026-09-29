# The github MCP tools

Owned by [I-000001](org/situation/invariants/I-000001-github-through-mcp-tools.md).

Every harness in a repo pod has the `github` MCP server (github-agent-mcp).
Its nine tools act as the pod's GitHub identity: they can do what its token
permits.

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

## Calls

- Every call takes `method` and that method's arguments; the tool's
  description lists both. Comment bodies are passed as arguments.
- NOOA has the same tools as async methods of `self.github`, for example
  `await self.github.pr_read(method="get", owner="cleverunicornz", repo="<repo>", pullNumber=12)`.
- The tools never wait; waiting on a run is `gh`'s
  ([github-ci-runs](org/situation/references/I-000002/github-ci-runs.md)).

## What the tools cannot see

- Check runs of other apps. The token cannot read check runs, so
  `pr_workspace` `get_check_runs` and `assemble_review_context` serve the head
  commit's Actions runs instead (`source: "actions_runs"`). A third-party
  app's check (external CI, code scanning) is not visible there; the pull
  request page shows it.
- Issue types need an organization permission the token may lack; the error
  says so
  ([github-mcp-results](org/situation/references/I-000003/github-mcp-results.md)).
