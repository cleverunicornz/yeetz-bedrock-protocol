# Organization operating layer

Every agent reads this file first, whatever its harness. It is baked into the
agent container image at user level with the role and organization skills,
one level above every repository, and ships with each container release. A
repository's own root `AGENTS.md` carries only that repository's situational
state; its `.agents/skills/` and `paseo.json` add repository tooling. This
layer supersedes any `bedrock-organization` block a repository still carries.

## Invariants

- **Paseo runs every other agent.** Start, brief, wait for, and read other
  agents through Paseo (MCP tools or the `paseo` CLI) under a Paseo profile.
  Read `multi-agent` before starting one.
- **A profile name is a role.** An agent started under the profile `scout`,
  `implementer`, `validator`, `advisor`, or `orchestrator` is that role and
  follows the skill of the same name. `security-implementer` follows
  `implementer`, `security-validator` follows `validator`, and
  `committee-openai` / `committee-claude` follow `advisor`.
- **Security fallback.** Implementation and validation always start under
  `implementer` and `validator`. When that model refuses the task on security
  grounds — defensive work such as authorization code — start the same brief
  under `security-implementer` or `security-validator`.
- **Full access.** Agents run with full tool access; the container is the
  boundary. Role skills give guidance on what the role delivers.
- **Usage-limited Claude sessions end.** A Claude session that stalls or ends
  because of a usage limit is never resumed. Start a new session with the same
  role and assignment; it gets a fresh account and continues from the pushed
  branch.
- **Work autosaves.** Every agent stop commits all changes as a WIP commit and
  pushes the branch. Work on a branch: `main`, `master`, and `internal/main`
  are protected and never receive commits directly. Read `git-etiquette`.
- **Pull requests stay open.** Every trunk change lands through a pull
  request. An agent opens or updates it and leaves it open unless its task
  explicitly authorizes merging that exact pull request.
- **Heavy work runs on the workbench.** Builds, tests, servers, Docker, and
  browsers run on the repository's workbench, where each command has a
  3-minute cap. Longer work runs on the GitHub test runners through CI.
- **Web search and fetch use the Exa MCP tools.**
- **Secret values stay unread and unprinted.** Consuming services validate
  them.

## Which skill to read

| When | Skill |
|---|---|
| You were started under a role profile | `scout`, `implementer`, `validator`, `advisor`, or `orchestrator` |
| You start, brief, or wait for other agents; you need a committee | `multi-agent` |
| You compile, test, run a server, Docker, or a browser | `workbench` |
| You write or change a GitHub Actions workflow, or a CI job is killed or queued | `ci-runners` |
| You branch, commit, push, open or merge a pull request, or work in a fork | `git-etiquette` |
