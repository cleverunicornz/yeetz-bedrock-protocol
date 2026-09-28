---
name: git-etiquette
description: How agents use git and pull requests - working trunks and branch names (including forks), commits and the shape of WIP autosave commits, forward-only history, pull request descriptions and CI, merge commits, and fork contribution flow. Read it before branching, committing, pushing, or touching a pull request.
---

# git-etiquette

## Trunks and branches

- An owned repository's working trunk is `main`. A fork's working trunk is
  `internal/main`; its `main` tracks the upstream.
- The working trunks `main` and `internal/main` are always protected and
  change only through pull requests. The organization uses no `master`.
- Branches are cut from the working trunk (`origin/main`, or
  `origin/internal/main` in a fork).
- In a fork every branch is named `internal/<name>` or `upstream/<name>`; the
  organization rulesets admit no other name. Elsewhere use a short
  descriptive name (`fix/parser-overflow`, `feat/export-csv`).
- One writer per branch. Parallel agents get separate branches.

## Commits

- Commit meaningful units with messages that say what and why, and push as
  you go.
- **Autosave commits** are `wip(agent): auto-save <UTC> [skip ci]`, include
  untracked files, and skip detached HEADs. They are ordinary history; keep
  working on top of them. After a restart the worktree is recreated from
  `origin/<branch>`.
- In a repo pod every commit carries `Lineage-*` trailers (human, pod,
  harness, Paseo agent, session) added by the pod's git hooks; keep them. A
  fork's `upstream/*` branches get none.
- History moves forward only. Corrections are new commits; pushed commits
  stay as they are (no amend, rebase, reset, or force push of pushed work).
- To take in trunk changes, merge the trunk into your branch.

## Pull requests

- Open pull requests early and keep the description current: what changed,
  why, how it was verified (CI run URLs).
- End every pull request description with the line that `cvu-lineage
  pr-footer` prints in a repo pod (`Lineage: human … · pod … · harness … ·
  paseo-agent … · session …`), unchanged. Outside a repo pod, leave it out.
- CI runs on the pull request; WIP commits carry `[skip ci]`, so push a
  normal commit (or re-run the workflow) when you need a fresh CI result.
- An authorized merge uses a **merge commit**, never squash or rebase, so every
  commit on the branch stays reachable from the trunk.

## Forks

- Advancing a fork's `main`, including an upstream sync, needs approval from a
  human fork maintainer.
- Contributions travel outward: cherry-pick from `internal/main` onto an
  `upstream/<name>` branch cut from `main`, open the pull request into
  `main`, and from `main` open the pull request to the upstream. Keep
  repository-knowledge changes in separate commits from code so cherry-picks
  stay clean.
