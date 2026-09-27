---
name: multi-agent
description: How to run other agents through Paseo - role profiles, starting and briefing agents, workspaces, waiting for and reading results, the standard scout/implement/validate/fix loop, committees, and replacing agents that died or hit a usage limit. Read it before starting any other agent.
---

# multi-agent

Paseo is the one multi-agent runtime. Every other agent is started through
Paseo, from any harness, with its MCP tools or the `paseo` CLI. The Paseo
skills `paseo` (full tool reference), `paseo-committee`, `paseo-advisor`, and
`paseo-handoff` are installed with it; this skill is the organization's way of
using them.

## Profiles are roles

`list_profiles` returns the configured profiles. The role profiles carry the
role's name, and the agent started under one follows the skill of that name:

| Profile | Role |
|---|---|
| `scout` | finds things out and answers |
| `implementer` | writes and changes things; the fix step |
| `validator` | checks another agent's work, returns a verdict |
| `advisor` | gives a recommendation |
| `orchestrator` | runs agent flows |
| `committee-openai`, `committee-claude` | the two committee members (below) |

Each profile fixes the harness, model, reasoning effort, and full-access mode.
Use the profile for the role; pick a different model only when the requester
asks for one.

## Start an agent

`create_agent` has no profile parameter. Materialize the profile into it:

- `provider` = the profile's `provider/model`
- `settings.modeId` = its `modeId`
- `settings.thinkingOptionId` = its `thinkingOptionId`
- `settings.features` = its `featureValues`

Title agents `[<role>] <task>`. The first line of every brief is
`You are the <role>. Read the <role> skill first.`, followed by a
self-contained assignment: goal, acceptance criteria, repository, branch and
pull request, relevant paths, and earlier agents' results. The new agent has
no other context.

CLI equivalent:
`paseo run --provider <provider/model> --thinking <id> --mode <modeId> --title "[<role>] <task>" "<brief>"`.

## Workspaces

- An implementer works in its own worktree: `create_workspace` with
  `isolation: "worktree"`, `mode: "branch-off"`, an explicit
  `baseBranch: "origin/main"` (or `origin/internal/main` in a fork), and a new
  branch; or `mode: "checkout-pr"` to continue a pull request.
- Scouts, validators, and advisors may share the caller's workspace or check
  out the pull request under review.
- One writer per branch.

## Wait and read results

- Agents take 10-30 minutes and more. `create_agent` and background
  `send_agent_prompt` notify you when the agent finishes, errors, or needs
  attention; continue other work meanwhile. Polling status is unnecessary.
- The agent's final message is its result. Follow-ups go to the same agent
  with `send_agent_prompt` (`paseo send <id> "..."`); a new question with a
  fresh context goes to a new agent.
- Archive agents whose work is finished.

## The standard loop

```text
scout -> implementer -> validator -> implementer (fix) -> validator -> ...
```

The `orchestrator` skill states how the loop runs and how its results are
reported.

## Committee

Use the `paseo-committee` skill when stuck, looping, or facing a hard design
or planning problem. The committee has exactly two members, from different
model families, each started with the `advisor` role:

- `committee-openai` — the top OpenAI model at reasoning effort `max`.
- `committee-claude` — Claude Opus 5.5 at reasoning effort `xhigh`.

Both get the same question; relay each member's arguments to the other until
they converge, then report the consensus and where they diverged.

## Died, interrupted, or usage-limited agents

An agent that died or was interrupted before returning is replaced by a fresh
agent with the same profile and the same brief; the new agent owns the work
already pushed on the branch. A Claude session that stalls or ends because of
a usage limit is never resumed: start a new one the same way; it gets a fresh
account.
