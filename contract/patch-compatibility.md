# Stable patch compilation commitment and judgment

## Promise

Under `migrations/2.0.0-to-2.0.1.md`, the compiler accepts independently
versioned stable protocol and organisation `2.0.x` packages after verifying
each package's own VERSION agreement and every manifest path and digest.
It rejects unsupported major/minor versions, prerelease/build metadata,
malformed versions and altered package bytes before writing output.
Full, user and repository compilation and all supplied skill sentence
checks preserve the fixed protocol semantics and short instruction layout.

## Oracle

First reproduce the failure using the actual unchanged published 2.0.0
archive with an independently versioned organisation 2.0.1 input. Retain
the archive/manifest hashes and compiler failure. Then run focused CLI tests
for compatible patch combinations, invalid versions, VERSION disagreement,
missing VERSION, path escape and digest mutation. Build only manifest-listed
files plus VERSION/manifest and compile that package in all three modes.
Run source semantics and sentence checks, verify manifest regeneration,
and obtain independent Codex validation of the exact candidate before READY.
Exact-head CI, Base review and adjudicated observation precede guarded merge
and forward publication. Confirm release archive and manifest digests by
reading the published assets back.

## Qualification boundary

An optional frozen unpublished organisation source fixture is producer input,
never proof of an organisation release. Consumers qualify the actual new
published tuple afterwards. Existing native source replay remains its bounded
retained evidence: this version predicate introduces no tool/API behavior,
production authority or canary claim. SO117 remains unresolved.
