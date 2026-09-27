# Bedrock Protocol

This repository publishes the Bedrock knowledge protocol: the standard
`AGENTS.md` files that adopting repositories install under their `situation/`
directory, the two root `AGENTS.md` block templates, and the manifest that
lists them.

## What this is

A consuming repository runs a deterministic synchronizer before its Bedrock
closure workflow. The synchronizer compares a pinned release of this
repository against the consumer's `situation/protocol-lock.json`. When the
release has changed, it copies the protocol-owned files byte-for-byte, writes
an explicit sync commit, and only then starts any agent work.

The closure workflow is not running at this time. Agents do not request,
open, or perform closures; repositories with `situation/` keep their records
current in the pull request that makes each change.

The protocol files explain, in each namespace directory, what that record
class is and how to author one:

- **Promises** state falsifiable behavior and carry a lifecycle state.
- **Oracles** define the judgment rule for a promise.
- **Witnesses** retain immutable observations from real runs.
- **Decisions** record why a choice collapsed and must not be relitigated.
- **Invariants** state binding repository rules; critical ones surface in the
  root `AGENTS.md`.
- **Gaps** preserve encountered absences, concerns, and uncertainties, with
  additive observations kept separate from qualification or resolution.
- **Candidates** retain evidence-derived possibilities before commitment.
- **Plans** are thin containers grouping promises into a delivery effort.
- **References** hold retained depth linked from records.

Three templates complete an installation, each with one job:

- `templates/root-protocol.md` — the Bedrock protocol and how agents engage
  with it;
- `templates/organization.md` — the organization operating layer: agent
  runtime, roles, and working rules that are not protocol;
- `templates/repository-block.md` — the required shape of the repository
  block, the only content of the adopter's root `AGENTS.md`.

The role and organization skills live in `skills/`.

## Layers

This repository is the governance layer for the whole agent runtime. Agent
instructions come from two levels:

| Level | Content | Where it lives | How it ships |
|---|---|---|---|
| User | protocol block + organization layer: `AGENTS.md` composed from `templates/root-protocol.md` then `templates/organization.md`, plus the skills under `skills/` | the agent container image, one level above every repository | each container release (canary, then rollout) |
| Repository | the repository's root `AGENTS.md`, holding only its repository block (`templates/repository-block.md`) — that repository's situational state — plus `.agents/skills/` and `paseo.json` | the repository | the repository's own pull requests |

**Composition rule:** the user-level `AGENTS.md` is exactly
`templates/root-protocol.md` followed by `templates/organization.md`. A
repository's root `AGENTS.md` is never part of it; the harness reads that file
separately, from the repository.

Earlier Bedrock releases put an organization block (`bedrock-organization`)
into every repository's root `AGENTS.md`. The organization layer replaces it
and supersedes any such block a repository still carries.

## What this is not

This repository contains no application code, no organization-specific
information outside `templates/organization.md` and `skills/`, no
credentials, no automation runtime, and no Bedrock closure of its own. It is exempt by design: the protocol source does not consume itself.

## Usage

Reference a release tag (for example `v1.0.0`) and copy the namespace files
listed under `files` in `manifest.json` into the adopting repository. The root
protocol block is provided byte-for-byte at user level by the agent container,
composed with the organization template as above; the adopter's root
`AGENTS.md` holds only the repository block, whose template is the shape the
closer fills in, not a file to copy. Store the resolved commit SHA and file digests in the adopter's
`situation/protocol-lock.json`. See the Bedrock closure workflow documentation
in the consuming repository for the synchronization contract.
