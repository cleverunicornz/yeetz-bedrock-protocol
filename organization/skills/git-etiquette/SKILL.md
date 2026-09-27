---
name: git-etiquette
description: The organization's git and pull-request rules for agents - working trunks and branch names (including forks), WIP autosave commits, forward-only history, branches are never deleted, pull requests stay open unless merging is explicitly authorized, and merges use merge commits. Read it before branching, committing, pushing, or touching a pull request.
---

# git-etiquette

## Trunks and branches

- An owned repository's working trunk is `main`. A fork's working trunk is
  `internal/main`; its `main` tracks the upstream.
- `main`, `master`, and `internal/main` change only through pull requests.
  All work happens on a branch cut from the working trunk
  (`origin/main`, or `origin/internal/main` in a fork).
- In a fork every branch is named `internal/<name>` or `upstream/<name>`; the
  organization rulesets admit no other name. Elsewhere use a short
  descriptive name (`fix/parser-overflow`, `feat/export-csv`).
- One writer per branch. Parallel agents get separate branches.

## Commits

- Commit meaningful units with messages that say what and why, and push as
  you go.
- **Autosave.** Every agent stop runs an autosave that commits all changes,
  untracked files included, as `wip(agent): auto-save <UTC> [skip ci]` and
  pushes the branch. It skips `main`, `master`, `internal/main`, and detached
  HEADs. WIP commits are ordinary history; keep working on top of them. After
  a restart the worktree is recreated from `origin/<branch>`.
- History moves forward only. Corrections are new commits; pushed commits
  stay as they are (no amend, rebase, reset, or force push of pushed work).
- To take in trunk changes, merge the trunk into your branch.

## Branches are never deleted

Pushed branches stay in place, merged or not; the organization ruleset
forbids deleting them. The operator removes branches.

## Pull requests

- Every trunk change lands through a pull request. Open it early, keep its
  description current: what changed, why, how it was verified (CI run URLs).
- CI runs on the pull request; WIP commits carry `[skip ci]`, so push a
  normal commit (or re-run the workflow) when you need a fresh CI result.
- Passing checks and reviews make a pull request mergeable; they do not
  authorize an agent to merge it. Leave it open unless your task explicitly
  authorizes merging that exact pull request.
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
