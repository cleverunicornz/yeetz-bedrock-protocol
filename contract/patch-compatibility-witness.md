# Witness: finite stable patch compiler qualification

## Observed baseline

Before the implementation, the actual published `v2.0.0` archive at
`fa3c69eb8f22f226d1a1ecb178a63ec3a59f7b6d` rejected a frozen unpublished
organisation 2.0.1 source fixture with exit 1 and
`requires the paired 2.0.0 package`. The archive SHA256 was
`5be7e35e8390d1332bb660ace4b6233eef4c12b892f87cd504241d4baef2b9c2`;
its manifest SHA256 was
`914d4cb5fc2dd4cb024cf8c2cd10ac053d73127d2f5f8ea4dfb32078734be160`.
The organisation input was explicitly unpublished source, never a released
pair. Initial tests reported 17 failing assertions for independent patch
acceptance and ignored/mismatched VERSION files. A later test fixture was
corrected to keep its mismatch different from the new package's patch.

## Observed candidate

Candidate `fad785ba422dcdc327abdc3dbd551bca4df71c85` passed
https://github.com/cleverunicornz/yeetz-bedrock-protocol/actions/runs/37149411190
in compiler job
https://github.com/cleverunicornz/yeetz-bedrock-protocol/actions/runs/37149411190/job/111279892146.
All 302 job-log lines were read with pagination complete. The run checked
GitHub's merge tree of this head into unchanged `fa3c69e` main.

The same pinned published archive's refusal was reproduced with synthetic
organisation 2.0.1, then the manifest-only candidate package compiled full,
user and repository outputs successfully. Nineteen tests passed in 5.087s,
including independent patch combinations, unsupported/malformed versions,
VERSION agreement, output preservation on failure, path/digest guards and
sentence checks. Baseline and candidate source semantics passed; publication
manifest regeneration agreed byte for byte, and the finite example output
matched the existing compiled artifact.

## Limits and subsequent gates

This is finite producer compiler/package evidence under
`contract/patch-compatibility.md`, not an actual organisation release pair.
Native inputs were unchanged; the prior physical source replay remains
its retained bounded evidence and the additional native job was skipped.
No workbench calls ran after the stop order. This Witness does not claim
independent review, Base/observer disposition, publication, canary,
current-view qualification or live authority. Final candidate CI and review
must precede guarded merge and forward publication.

## Base review migration and workflow corrections

The first Base review identified an omitted-VERSION migration path and
coupled/custom CI selection. The selected guard was preserved. On the normal
workbench, the actual published organisation 2.0.0 archive SHA256
`6ac2f958b2770fb46d679c6f675afadab94feb73ddef54d78a0293dccbf01a5a`
and manifest SHA256
`d75352d45a1496d6d24b5645b55cbb07998c91a83774608d5e10f8260838aa5d`
were verified. Omitting its installed VERSION produced exit1; restoring only
that exact file from the SAME verified archive preserved the manifest and
every published byte and allowed all three compilation modes. The complete
probe exited0 in317ms. Documentation now assigns this repair to the consumer
installer, with no guessed or relabelled VERSION.

Both corrected workflow files parsed on the workbench in248ms. The native
job was structurally identical to the previously qualified job. Native
selection uses GitHub's workflow-level paths; the compiler job remains
unconditional. The published-archive check is independent, restores a cache
keyed by the immutable archive SHA, and still verifies the actual archive
and manifest on every check. No archive-host failure suppresses the native
or compiler job. Follow-up exact CI and review remain required.
