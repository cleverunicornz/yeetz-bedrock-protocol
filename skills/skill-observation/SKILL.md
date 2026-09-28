---
name: skill-observation
description: How to request skill observation on a pull request or issue, read the observer's comment, adjudicate every observation with the human you work for, and turn the actioned ones into changes - a repository skill, a new repository skill, a promotion to the organization, an organization skill, another target file, or a barrier - with the reply format the bookkeeping reads. Read it when your pull request is ready to merge, or when a human asks for skill observation on an issue.
---

# skill-observation

## What it is

The skill observer reads the recorded agent sessions linked to one pull
request or issue (their turns, commits, the review thread and CI) and reports
what the skills should have told those agents: a skill that is missing, a
skill to improve, or something to remove. It posts one comment as
`unicornz-integrity` and never edits anything. You and the human you work for
decide; you make the changes; a human merges them.

## Request it

- Post a comment whose whole text is
  `@unicornz-integrity skill observation requested` on the pull request, or on
  the issue a human names. Nothing else in that comment.
- Wait for the comment headed `## Skill observations`. Long ones arrive in
  numbered parts. If it says the record was not fresh or the run ended early,
  it says what it covered.
- Request it again only after substantial new work on the same pull request.
- Pull requests from `skill-observation/...` branches are not observed.

## Read the comment

- The header gives the scope (sessions and how they were linked), the counts
  per target, the observations that **need your input**, and the clusters that
  are one decision.
- Each observation `SO-nnnnnn` has a **Gap** (issue, relevance, evidence,
  impact) and a **Candidate** (suggested improvement, principle, targets,
  siblings checked, whether it extends an earlier observation or proposes a
  barrier). Its signal is `new`, `improve` or `simplify`; its type is
  `internal` (this repository's lane) or `open-source` (may land in the public
  protocol repository).
- Evidence cites turns as `<session>#<seq>` and links comments, commits and CI
  runs. Treat an observation as a proposal, not a finding: check the evidence
  you act on.

## Adjudicate with your human

- Show the human every observation. Never decide one that needs their input,
  and never decide for them what they did not answer: an unanswered
  observation stays open. A declined or ignored prompt is not approval.
- Reply on the same pull request or issue with one comment holding one line
  per observation you both decided, in exactly this form (the bookkeeping reads
  these lines; the latest line for an id wins):

  ```
  SO-000041: repo-skill
  SO-000042: org-skill
  SO-000043: decline "already covered by the ci-runners skill"
  SO-000044: park until "the second repository adopts the workbench"
  SO-000045: superseded by SO-000046
  ```

  Dispositions: `repo-skill`, `new-repo-skill`, `org-promotion`, `org-skill`,
  `target-file`, `barrier`, `decline "<why>"`, `park until "<condition>"`,
  `superseded by SO-nnnnnn`.
- A cluster is one decision: give its members the same disposition in the
  same reply, with one reason.

## Make the changes

| Disposition | Change | Where |
|---|---|---|
| `repo-skill` (fix or simplify, removals included) | edit `.agents/skills/<name>/SKILL.md` | this pull request when the skill lives in this repository; otherwise a follow-up pull request in that repository |
| `new-repo-skill` | add `.agents/skills/<name>/SKILL.md`; add the link `.claude/skills -> ../.agents/skills` if the repository has none | this pull request or a follow-up |
| `org-promotion` (the same lesson in two or more repositories) | a pull request in `cleverunicornz/yeetz-bedrock-protocol` adding `skills/<name>/SKILL.md`, then pull requests removing the repository copies | the removals merge only after the repo-pod image pins the protocol release that carries the skill |
| `org-skill` (fix or new) | a pull request in `cleverunicornz/yeetz-bedrock-protocol` with the skill change, the `VERSION` bump, the regenerated `manifest.json` digests and a migration note, as that repository's release process says | – |
| `target-file` | the named file: a repository block in `AGENTS.md`, the organization template, a situation invariant, a hook, a CI file | this pull request or a follow-up |
| `barrier` (the same rule broken a second time) | a hook, lint or CI check, admission rule or script: behaviour that can fail, never a rewording. In a repository with `situation/`, with its promise, oracle and a first witness | this pull request or a follow-up |

- A repository skill is a directory holding one `SKILL.md`: YAML front matter
  with `name` (equal to the directory) and `description`, then Markdown. No
  code files in a skill directory. Every file it references exists.
- An organization skill is changed only in the protocol repository, never in a
  repository copy. A skill someone else maintains (a vendor's) gets an issue
  upstream, not a local edit.
- Prefer fixing the system that owns the problem (code, configuration, CI)
  over adding a rule.
- Name follow-up branches `skill-observation/<SO-id>-<short-name>`.
- Put one line `Actions SO-nnnnnn` per observation in the body of every pull
  request that carries its change; the bookkeeping marks the observation
  actioned when that pull request merges.
- The protocol repository is public: keep repository names, GitHub logins,
  models and tools; never copy private content into it; cite private evidence
  only as `Private: owner/repo@<ref>#<path>`.

## Then

Leave the pull request for merge as your task allows. Recording decisions and
outcomes against the observations is automatic.
