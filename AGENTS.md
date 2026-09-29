# Bedrock Protocol Source

This repository is the governance layer for the whole agent runtime. It is
the source of the Bedrock knowledge protocol — the standard nested
`AGENTS.md` files and the manifest that adopting repositories consume — and of
the organization operating layer every agent runs under.

## Layers

Agent instructions come from two levels, each with one source:

1. **User level** — the protocol block and the organization layer, baked into
   the agent container image one level above every repository and shipped
   with each container release (canary, then rollout). Every agent in every
   repository runs under it, whatever its harness. Its `AGENTS.md` is composed
   from `templates/root-protocol.md` followed by `templates/organization.md` —
   never from a repository's root `AGENTS.md` — and the skills under
   `skills/` are installed beside it.
2. **Repository level** — a repository's own root `AGENTS.md` holds only its
   repository block (`templates/repository-block.md`): that repository's
   situational state. `.agents/skills/` and `paseo.json` add repository
   tooling.

Earlier Bedrock releases put an organization block, `bedrock-organization`,
into each repository's root `AGENTS.md`. The organization layer replaces it and
supersedes any such block a repository still carries; organization rules are
never written into a repository.

## What this repository represents

Its content classes are:

- the root `README.md`, a brief human-facing summary;
- this root `AGENTS.md`, the operating contract for authoring the protocol;
- `manifest.json`, the machine-readable list of published files and digests;
- `VERSION`, the current protocol version;
- `situation/AGENTS.md` and one `AGENTS.md` per namespace directory, which
  adopters copy byte-for-byte;
- `templates/root-protocol.md`, the protocol block: the Bedrock protocol and
  how agents engage with it;
- `templates/organization.md`, the organization operating layer: runtime,
  roles, and working rules that are not protocol;
- `templates/repository-block.md`, the required shape of the repository block,
  the only content of a repository's root `AGENTS.md`;
- `skills/<name>/SKILL.md`, the role and organization skills installed at
  user level beside the composed `AGENTS.md`;
- `migrations/`, one note per release transition.

Organization-specific material lives only in `templates/organization.md` and
`skills/`. This
repository does not contain application code, product documentation,
credentials, automation workflows, or target repository state. If a change
requires private context to justify, it does not belong here.

## Bedrock exemption

This repository does not adopt the Bedrock protocol itself. It has no
protocol lock, no closure workflow, and no situation records. Applying the
protocol to its own source would create circular authority; the exemption is
deliberate.

## Authoring rules

- Every namespace `AGENTS.md` is generic and domain-neutral. It must make
  sense to a public reader with no knowledge of any adopting organization.
- Never name organizations, hosts, domains, GitHub actors, model providers,
  credentials, or private repositories in any protocol file: the namespace
  files, `templates/root-protocol.md`, and `templates/repository-block.md`.
- Each template has one job. `templates/root-protocol.md` states the Bedrock
  protocol and how to engage with it, and nothing about runtimes, runners,
  harnesses, models, or git and pull-request practice.
  `templates/organization.md` states organization operating rules and
  restates no protocol concept. Each fact lives in exactly one place:
  `templates/organization.md` states the rule, a skill carries the procedure
  and details and never restates the rule.
- `templates/organization.md` and `skills/` state the organization's own
  operating rules and procedures. This repository is public and that is intended: model
  names, repository names, runner labels, harnesses, and tools are all
  published freely. The one exclusion is personally identifying information:
  never name the operator's machines, local folder paths, or usernames other
  than GitHub usernames.
- Critical invariant: this repository is public, so secure material — our
  own known vulnerabilities from the security vault, their details,
  exploitability and affected code paths — is never represented in it, its
  branches, issues, pull requests, reviews or comments. Public CVE and CWE
  references are fine.
- A skill is a directory `skills/<name>/` holding one `SKILL.md` with `name`
  and `description` front matter; the directory name equals `name`. Skills
  are installed at user level and never copied into repositories.
- Reference discipline is law in every published file: repository files are
  referenced by repository-root-relative path; external public files by
  full public URL; external private files by declared coordinate
  (`Private: owner/repo@<ref>#<path>`). A declared-private reference that
  is unreachable is expected and never halts work. Never reference a local
  clone, a private checkout, or a machine-local path.
- Reference discipline is stated once, in `situation/AGENTS.md`. Every other
  published file points to that statement rather than restating it.
- Files are copied byte-for-byte by consumers. Any edit to a published file
  requires a version bump, a manifest regeneration, and a release.
- Quantitative protocol claims identify their source path and are derived
  mechanically where possible; one protocol record is never treated as the
  authority for another record's count.
- Each release is an immutable tag. Never move a tag.
- Pull-request review requirements and authority to execute a merge are
  independent. An agent opens or updates a pull request and leaves it open
  unless the active task explicitly authorizes that agent to merge that exact
  pull request.
- Add a migration note under `migrations/` when a release changes published
  files.
- Update `manifest.json` and `VERSION` in the same commit as the file
  changes they describe.

## Release process

1. Author changes to published files.
2. Run the manifest generator to rebuild `manifest.json` with current
   SHA-256 digests.
3. Bump `VERSION` using semantic versioning.
4. Write `migrations/<old>-to-<new>.md` when published files changed.
5. Open a pull request; absent explicit agent authority to merge that exact
   pull request, a human merges it.
6. Tag the merge commit as `v<VERSION>` and publish a release.

## Manifest contract

`manifest.json` lists every published file with its SHA-256 digest relative
to the repository root: the namespace files under `files`, the root protocol
block under `root_protocol`, the repository block template under
`repository_block`, the organization template under `organization`, and the
skills under `skills`. Consumers verify digests before copying. The manifest is
data, not an application; it contains no logic.
