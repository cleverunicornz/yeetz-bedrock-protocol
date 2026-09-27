# Organization operating layer

These are the organization's operating rules for every agent, whatever its
harness. They follow the protocol block, which governs repository knowledge,
and they supersede any `bedrock-organization` block a repository still
carries.

## Agents and roles

- **Paseo runs every other agent.** Start, brief, wait for, and read other
  agents through Paseo (MCP tools or the `paseo` CLI) under a Paseo profile;
  `multi-agent` has the mechanics.
- **A profile name is a role.** An agent started under `scout`,
  `implementer`, `validator`, `advisor`, or `orchestrator` is that role and
  follows the skill of the same name. `security-implementer` follows
  `implementer`, `security-validator` follows `validator`, and
  `committee-openai` / `committee-claude` follow `advisor`.
- **Security fallback.** Implementation and validation always start under
  `implementer` and `validator`. When that model refuses the task on security
  grounds — defensive work such as authorization code — the same brief runs
  under `security-implementer` or `security-validator`.
- **Committee.** When work is stuck, looping, or faces a hard design or
  planning choice, a committee of two answers it: `committee-openai` (the top
  OpenAI model at reasoning effort `max`) and `committee-claude` (Claude Opus
  5.5 at `xhigh`).
- **Usage-limited Claude sessions end.** A Claude session that stalls or ends
  because of a usage limit is never resumed. A new session starts with the
  same role and assignment; it gets a fresh account and continues from the
  pushed branch.
- **Full access.** Agents run with full tool access; the container is the
  boundary. Role skills give guidance on what the role delivers.

## Work

- **Work autosaves.** Every agent stop commits all changes as a WIP commit and
  pushes the branch. Work happens on a branch: `main`, `master`, and
  `internal/main` are protected and receive changes only through pull
  requests.
- **Branches are never deleted.** Pushed branches stay, merged or not; the
  operator removes them.
- **Pull requests stay open.** An agent opens or updates a pull request and
  leaves it open unless its task explicitly authorizes merging that exact
  pull request.
- **Heavy work runs on the workbench.** Builds, tests, servers, Docker, and
  browsers run on the repository's workbench, where each command has a
  3-minute cap. Longer work runs on the GitHub test runners through CI.
- **CI runners** (runner group `ci`): `automation-test-s` for tests, lint, and
  small builds (the default); `automation-test-l` for heavy tests;
  `automation-test-xl` for test suites running many Docker containers;
  `build-native` for native builds without Docker; `build-docker` for image
  builds and jobs needing a Docker daemon.
- **Web search and fetch use the Exa MCP tools.**
- **Secret values stay unread and unprinted.** Consuming services validate
  them.

## Which skill to read

| When | Skill |
|---|---|
| You were started under a role profile | the role's skill (above) |
| You start, brief, or wait for other agents, or convene a committee | `multi-agent` |
| You compile, test, run a server, Docker, or a browser | `workbench` |
| You write or change a GitHub Actions workflow, or a CI job is killed or queued | `ci-runners` |
| You branch, commit, push, open or merge a pull request, or work in a fork | `git-etiquette` |
