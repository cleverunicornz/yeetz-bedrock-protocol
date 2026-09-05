<bedrock-protocol>
## Repository knowledge protocol

This repository operates under the Bedrock knowledge protocol. These policies
are repository law: follow them as written; do not readjudicate them during
ordinary work.

Before changing code, behavior, architecture, repository policy, documentation,
or planned work:

1. Read `situation/AGENTS.md`.
2. Read the relevant situation records, related open Gaps, and qualifying
   Candidates.
3. Read the nested `AGENTS.md` governing every situation namespace you will
   modify.
4. Update affected records in the same work as the repository change.
5. Treat `situation/` as canonical repository knowledge. README is human-facing
   orientation; neither README, comments, plans, nor pretrained assumptions
   override situation records.

The record classes are:

- **Promises** state falsifiable behavior and carry lifecycle state.
- **Oracles** define how Promises are judged.
- **Witnesses** retain immutable observations from actual runs.
- **Decisions** preserve why choices were selected or rejected.
- **Invariants** state binding repository rules.
- **Gaps** record bounded, repository-relevant absences.
- **Candidates** record evidence-derived possibilities, not commitments.
- **Plans** group Candidates and Promises into work without restating them.
- **References** retain supporting depth.

Git is the run's append-only event log. A run performs one closure on one pull
request branch, bounded by an opening checkpoint commit and a closing checkpoint
commit on that branch. Agents commit and push completed units of work promptly;
corrections are new forward commits. Published history is never amended,
rebased, reset, or force-pushed. Only opening and closing checkpoints define the
run container; interior commit count and shape are not prescribed.

Run reports — closer summary, validator docket, corrector summary — are pull
request comments, never repository files. Agent transcripts are archived outside
the repository; both checkpoint commits carry the archive URI in a
`Bedrock-Transcript` trailer alongside their other trailers. The checkpoint
commits are the only writers of the closure state in `situation/context.md`.

A failed run is never resumed. An opening checkpoint with no closing checkpoint
marks a failed closure: the pull request is closed with a pointer to its rerun,
and the rerun starts on a new branch from the head admitted before the failed
run. The failed branch and its comments remain the record.

Records created or changed inside the current closure interval, on the open pull
request, may be corrected in place by a forward commit. Immutability begins at
the closing checkpoint.

Every assured Promise is invariant behavior. Changing it requires a superseding
Promise, a Decision explaining the change, a replacement Oracle, and new
Witnesses.

Gaps record what relevant capability, evidence, decision, implementation, or
instrument is absent. Candidates are possible responses derived from evidence.
A Candidate becomes behavior only through a Decision that promotes it into a
falsifiable Promise with an Oracle. Plans qualify Candidates and implement or
assure Promises.

The learning loop is:

```text
Promise -> implementation -> Oracle -> Witness -> disposition
        -> Gap -> Candidates -> Plan -> Decision
        -> promoted Promise + Oracle -> implementation
```

Repository files are referenced by repository-root-relative path. Historical
repository bytes use `<commit>:<path>`. External public files use full URLs.
External private files use declared `Private: owner/repo@<ref>#<path>`
coordinates; inability to fetch a declared-private reference is expected and
never grounds to stop, remove it, or invent its contents.

When repository orientation identifies an upstream fork, upstream
synchronization and contribution are outside Bedrock. Invoke the exact
`fork-operations` skill; do not infer or recreate that procedure from repository
records.

Root `AGENTS.md` carries three tagged blocks in this order: the protocol block
`bedrock-protocol`, the organization block `bedrock-organization`, and the
repository block `bedrock-repository`. The organization block is
organization-owned and synchronized by the closure automation; it is optional,
and adopters whose automation supplies none carry the other two blocks.

This protocol block is protocol-owned and the organization block is
organization-owned: agents must not edit any byte inside either. Agents edit
only the repository block, which holds all repository-specific orientation in
the required shape given by the protocol template
`templates/repository-block.md`.
</bedrock-protocol>
