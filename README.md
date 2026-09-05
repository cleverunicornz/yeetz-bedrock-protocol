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

The protocol files explain, in each namespace directory, what that record
class is and how to author one:

- **Promises** state falsifiable behavior and carry a lifecycle state.
- **Oracles** define the judgment rule for a promise.
- **Witnesses** retain immutable observations from real runs.
- **Decisions** record why a choice collapsed and must not be relitigated.
- **Invariants** state binding repository rules; critical ones surface in the
  root `AGENTS.md`.
- **Gaps** retain bounded, repository-relevant absences.
- **Candidates** retain evidence-derived possibilities before commitment.
- **Plans** are thin containers grouping promises into a delivery effort.
- **References** hold retained depth linked from records.

Two templates complete an installation: `templates/root-protocol.md`, the
protocol-owned block that opens the adopter's root `AGENTS.md`, and
`templates/repository-block.md`, the required shape of the repository-owned
block that closes it.

## What this is not

This repository contains no application code, no organization-specific
information, no credentials, no automation runtime, and no Bedrock closure of
its own. It is exempt by design: the protocol source does not consume itself.

## Usage

Reference a release tag (for example `v1.0.0`) and copy the files listed in
`manifest.json` into the adopting repository. Install the root protocol block
byte-for-byte at the top of the adopter's root `AGENTS.md`; the repository
block template is the shape the closer fills in, not a file to copy. Store the
resolved commit SHA and file digests in the adopter's
`situation/protocol-lock.json`. See the Bedrock closure workflow documentation
in the consuming repository for the synchronization contract.
