# Additive 2.1.0 commitment and judgment

## Promise

Under `migrations/v2.0.1-to-v2.1.0.md`, the package states one contract in
prose, YAML, schema, record templates and worked examples that keeps every
2.0.0 meaning and adds `Applies to`, Gaps as Plan members, records in the
domain with files as projections, and one fixed repository block. The compiler
admits stable `2.0.x` and `2.1.x` packages independently and renders the fixed
block byte for byte. The two published repository checks run only files from a
release verified against its `SHA256SUMS` and manifest; the AGENTS.md check
fails on any byte of difference in the repository block, and the projector
gives the same bytes for the same records, whatever is committed after them.

## Oracle

- `contract/check.py` agrees prose, YAML, schema, templates, skills and every
  worked example, including `18-plan-holds-a-gap`,
  `19-gap-member-still-waited-upon` and `20-applies-to-a-version` (binds
  returns the version's and the organisation's Invariants, not another
  version's).
- `tests/test_replay_arguments.py` retracts exactly the 2.1 additions and
  obtains the v2.0.1 contract and schema; native replay compares the pinned
  receiver against that retraction.
- `tests/test_compiler.py` and `tests/test_patch_compatibility.py`: the fixed
  block with and without repository input; admitted and refused versions.
- `tests/test_check_agents_md.py`: equal passes; a one-byte change, CRLF, an
  added rule, the old template, a missing or repeated block fail.
- `tests/test_situation_projection.py`: header, class order, id order,
  exclusions, link refusal, byte determinism, and project, commit, project again
  with the same bytes and the records commit in the header.
- `tests/test_repository_checks.py` runs the workflows' verification step
  against locally built assets: verified, tampered archive, tampered file with a
  matching archive checksum, and a checksum list without the archive.
- `tests/test_build_release.py` reproduces the published v2.0.1 assets byte for
  byte.
- CI lints both workflows with actionlint and shellcheck, projects this
  repository's `situation/` twice and compares the bytes.

## Qualification boundary

Source qualification proves the package, not a deployed receiver, a migrated
scope or a caller's run of the workflows. The receiver's support for the 2.1
additions and the first called runs after release are observed separately.
