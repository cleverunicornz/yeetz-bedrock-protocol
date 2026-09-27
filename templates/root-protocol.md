<bedrock-protocol>
## Repository knowledge protocol

A repository that carries a `situation/` directory keeps its knowledge under
the Bedrock knowledge protocol. In such a repository these policies are
repository law: follow them as written; do not readjudicate them during
ordinary work. A repository without `situation/` is outside the protocol.

Bedrock closure automation is not running. Agents do not request, open, or
perform closures, and record changes land in the pull request that makes the
repository change.

Before changing code, behavior, architecture, repository policy, documentation,
or planned work:

1. Read `situation/AGENTS.md`.
2. Read the relevant situation records, related Gaps, and qualifying Candidates.
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
- **Gaps** preserve encountered absences, concerns, and uncertainties.
- **Candidates** record evidence-derived possibilities, not commitments.
- **Plans** group Candidates and Promises into work without restating them.
- **References** retain supporting depth.

Record concerns and uncertainties encountered during the work as Gaps, even
when minor or tentative. Follow `situation/gaps/AGENTS.md` to relate them to
existing Gaps and supporting records. Surfacing a Gap does not assign its
investigation or resolution to this task; continue the assigned
Promise/Oracle/Witness work.

A change affecting claimed behavior repairs missing local Promise/Oracle/Witness
lineage in the same pull request; a Gap about unaffected behavior remains an
observation.

A record is immutable once merged into the working trunk. Until then, on the
open pull request, it may be corrected in place by a forward commit.
Gaps permit append-only observations and separately assigned State/Resolution
updates under `situation/gaps/AGENTS.md`; earlier observations remain unchanged.

Every assured Promise is invariant behavior. Changing it requires a superseding
Promise, a Decision explaining the change, a replacement Oracle, and new
Witnesses.

Candidates are possible responses derived from evidence. A Candidate becomes
behavior only through a Decision that promotes it into a falsifiable Promise
with an Oracle. Plans qualify Candidates and implement or assure Promises;
recording a Gap does not assign that subsequent work.
Detailed requirements may be adopted by reference from a pinned specification;
changing it follows the assured-promise path. A promoted Promise is the selected
commitment stating the accepted behavior; implementation never redefines it.

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
synchronization and contribution follow the organization's fork rules in the
organization layer. Bedrock records ownership and the upstream coordinate and
performs neither.

This protocol block is supplied at user level, outside every repository, and
is protocol-owned. A repository's root `AGENTS.md` holds only the repository
block `bedrock-repository`, which carries all repository-specific orientation
in the shape given by the repository block template published with the
protocol release. Agents edit only the repository block.
</bedrock-protocol>
