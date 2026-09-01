# Bedrock Protocol Source

This repository is the source of the Bedrock knowledge protocol. It publishes
the standard nested `AGENTS.md` files and the manifest that adopting
repositories consume.

## What this repository represents

This repository represents the protocol definition and nothing more. Its
content classes are:

- the root `README.md`, a brief human-facing summary;
- this root `AGENTS.md`, the operating contract for authoring the protocol;
- `manifest.json`, the machine-readable list of published files and digests;
- `VERSION`, the current protocol version;
- `situation/AGENTS.md` and one `AGENTS.md` per namespace directory, which
  adopters copy byte-for-byte;
- `migrations/`, one note per release transition.

This repository does not contain application code, product documentation,
organization-specific material, credentials, automation workflows, or target
repository state. If a change requires private context to justify, it does
not belong here.

## Bedrock exemption

This repository does not adopt the Bedrock protocol itself. It has no
protocol lock, no closure workflow, and no situation records. Applying the
protocol to its own source would create circular authority; the exemption is
deliberate.

## Authoring rules

- Every namespace `AGENTS.md` is generic and domain-neutral. It must make
  sense to a public reader with no knowledge of any adopting organization.
- Never name organizations, hosts, domains, GitHub actors, model providers,
  credentials, or private repositories in any published file.
- Files are copied byte-for-byte by consumers. Any edit to a published file
  requires a version bump, a manifest regeneration, and a release.
- Each release is an immutable tag. Never move a tag.
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
5. Open a pull request; a human merges.
6. Tag the merge commit as `v<VERSION>` and publish a release.

## Manifest contract

`manifest.json` lists every published file with its SHA-256 digest relative
to the repository root. Consumers verify digests before copying. The
manifest is data, not an application; it contains no logic.
