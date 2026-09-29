# Organization operating layer

How agents work in this organization, whatever the harness. Each rule names
what you do and the skill you must read before doing it; the skill holds the
detail. These rules follow the protocol block and supersede any
`bedrock-organization` block a repository still carries.

## Agents

- **Paseo is the organization's agent runtime.** Every other agent — a
  sub-agent, a parallel worker, a reviewer, a committee — runs through Paseo
  (MCP tools or the `paseo` CLI) under a Paseo profile. Your harness's
  built-in sub-agents are off. Before you start, brief, or wait for another
  agent, you must read `multi-agent`.
- **When you are told to orchestrate or run a multi-agent workflow**, you
  must read `orchestrator` and `multi-agent`.
- **A profile is a role.** When you were started under a profile or your
  brief names a role, you must read and follow that role's skill: `scout`,
  `implementer`, `validator`, `advisor`, or `orchestrator`.
- **When a model refuses work on security grounds, or work is stuck or
  looping**, you must read `multi-agent`: it has the security fallback
  profiles and the committee.
- **A Claude session stopped by a usage limit is never resumed.** Start a new
  session with the same role and assignment; it continues from the pushed
  branch.
- **Agents have full tool access.** The container is the boundary.

## Work

- **When you compile, test, run a server, Docker, or a browser**, you must
  read `workbench` and run it on the repository's workbench.
- **When you write or change a GitHub Actions workflow, or a CI job is killed
  or queued**, you must read `ci-runners`.
- **When you branch, commit, push, or touch a pull request**, you must read
  `git-etiquette`. Your work autosaves as a pushed WIP commit whenever you
  stop. Remote branches are never deleted; local branches may be. Pull
  requests stay open unless your task explicitly authorizes merging that
  exact pull request.
- **Pull requests, reviews, issues, projects and CI results go through the
  `github` MCP tools.** Before you read or change any of them, or wait for or
  read CI, you must read `github`.
- **When you open a pull request**, assign it to the human you work for: the
  GitHub login in `$CVU_HUMAN_GITHUB_LOGIN` (set in every repo pod).
- **When your pull request is ready to merge**, you must read
  `skill-observation`: post the whole comment
  `@unicornz-integrity skill observation requested`, wait for the observation
  comment, adjudicate every observation with the human you work for, apply the
  actioned ones as `skill-observation` describes, then leave the pull request
  for merge.
- **When you write integration tests or deployment manifests, or need a staging,
  test or production environment**, you must read `environments`. Budgets are
  set by a human and recorded in the repository's AGENTS.md; never choose them
  yourself.
- **Security findings stay in the security vault, never in a repository.** A
  fix for one lands in one pull request together with its property-level
  Promise and Oracle: the property the code keeps, never the attack, a payload,
  reproduction steps, severity or "is vulnerable". This holds in every
  repository, public and private; the finding, its Candidate and the full
  Decision stay in the vault (a private repository may cite its opaque vault
  ID, a public one never does).
- **When you work with secure material** (anything from the security vault:
  our own known vulnerabilities, their details, exploitability, affected code
  paths), use it freely and never represent it in a public repository — code,
  comments, commits, branches, issues, pull requests, reviews or comments.
  Public CVE and CWE references are fine anywhere.
- **When infrastructure is broken, missing or blocking you**, open an issue in
  `cleverunicornz/infra-v2` saying what you needed and what failed, and link it from your work.
  Do not work around the platform.
- **Web search and fetch use the Exa MCP tools.**
- **Secret values stay unread and unprinted.** Consuming services validate
  them.
