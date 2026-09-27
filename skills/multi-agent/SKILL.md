---
name: multi-agent
description: How to run other agents through Paseo - choosing and materializing a profile, briefing, workspaces, waiting for and reading results, following up, and running a committee. Read it before starting any other agent.
---

# multi-agent

The mechanics of starting and working with other agents through Paseo's MCP
tools or the `paseo` CLI. The Paseo skills `paseo` (full tool reference),
`paseo-committee`, `paseo-advisor`, and `paseo-handoff` are installed with
Paseo.

## Profiles and roles

| Profile | Role skill | Use |
|---|---|---|
| `scout` | `scout` | find things out, with proof |
| `implementer` | `implementer` | write and fix code, test first |
| `validator` | `validator` | judge another agent's work |
| `advisor` | `advisor` | a second opinion |
| `orchestrator` | `orchestrator` | run a flow of agents |
| `security-implementer` | `implementer` | fallback only, see below |
| `security-validator` | `validator` | fallback only, see below |
| `committee-openai`, `committee-claude` | `advisor` | the committee |

- **Security fallback.** Implementation and validation always start under
  `implementer` and `validator`. When that model refuses the task on security
  grounds (defensive work such as authorization code), the same brief runs
  under `security-implementer` or `security-validator`.
- **Committee.** When work is stuck, looping, or faces a hard design or
  planning choice, `committee-openai` and `committee-claude` answer it
  together (see Run a committee).
- **Usage limits.** When a Claude agent stops on a usage limit, start a new
  agent with the same profile and brief; it gets a fresh account and
  continues from the pushed branch.

## Start an agent

`list_profiles` returns the configured profiles. `create_agent` has no
profile parameter; materialize the chosen profile into it:

- `provider` = the profile's `provider/model`
- `settings.modeId` = its `modeId`
- `settings.thinkingOptionId` = its `thinkingOptionId`
- `settings.features` = its `featureValues`

Use the profile for the role; pick a different model only when the requester
asks for one.

Title agents `[<profile>] <task>`. The first line of every brief is
`You are the <role>. Read the <role> skill first.`, where `<role>` is the
skill the profile follows. A self-contained assignment follows: goal,
acceptance criteria, repository, branch and pull request, relevant paths, and
earlier agents' results. The new agent has no other context.

CLI equivalent:
`paseo run --provider <provider/model> --thinking <id> --mode <modeId> --title "[<profile>] <task>" "<brief>"`.

## Workspaces

- An implementer works in its own worktree: `create_workspace` with
  `isolation: "worktree"`, `mode: "branch-off"`, an explicit
  `baseBranch: "origin/main"` (or `origin/internal/main` in a fork), and a new
  branch; or `mode: "checkout-pr"` to continue a pull request.
- Scouts, validators, and advisors may share the caller's workspace or check
  out the pull request under review.

## Wait and read results

- Agents take 10-30 minutes and more. `create_agent` and background
  `send_agent_prompt` notify you when the agent finishes, errors, or needs
  attention; continue other work meanwhile. Polling status is unnecessary.
- The agent's final message is its result. Follow-ups go to the same agent
  with `send_agent_prompt` (`paseo send <id> "..."`); a new question with a
  fresh context goes to a new agent.
- Archive agents whose work is finished.

## Run a committee

Follow the `paseo-committee` skill with the two committee profiles as its
members, each briefed as `advisor` with the same question. Relay each
member's arguments to the other until they converge, then report the
consensus and where they diverged.
