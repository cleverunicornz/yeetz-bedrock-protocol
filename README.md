# Bedrock 2.1

Bedrock defines a fixed act protocol: eight nouns, a Plan group, thirteen
verbs and five structural acts. Records are projected from a task-graph
act log. Memory retains what happened; a board outlines the session.

This package publishes the fixed contract, executable procedures, the
record templates, a compiler for short agent instructions and two reusable
repository checks. Organisation operating policy is a separate paired
package. See compiler/README.md for exact paths and CLI, contract/stage0.md
for the source commitment and its verification, and
migrations/2.0.0-draft-to-2.0.0.md and migrations/v2.0.1-to-v2.1.0.md for the
protocol Decisions.

Bedrock STE100 Communication applies to records, handoffs and agent prose,
including personal use. Read `contract/communication/ste100-writing.md` for
the compact convention and vocabulary pointers. Its `ste100-review` skill
evaluates proposed changes through existing Bedrock acts, with independent
counterarguments. Source lineage and the protocol Decision are retained in
`contract/communication/asd-ste100-issue9.md` and
`migrations/v2.1.0-to-v2.1.1.md`.

## Using it in a repository

Records live in the situation domain; files are projections (contract
section 8). A repository under the protocol keeps its root `AGENTS.md`
repository block equal to `templates/repository-block.md`, and calls the two
checks pinned to the protocol version it adopts:

```yaml
on: pull_request
jobs:
  agents-md:
    uses: cleverunicornz/yeetz-bedrock-protocol/.github/workflows/check-agents-md.yml@v2.1.0
    with:
      version: 2.1.0
  situation:
    permissions:
      contents: write
    uses: cleverunicornz/yeetz-bedrock-protocol/.github/workflows/situation-projection.yml@v2.1.0
    with:
      version: 2.1.0
    secrets:
      push_token: ${{ secrets.SITUATION_PUSH_TOKEN }}
```

Both accept an optional `runs-on` input (JSON) for the runner; it defaults
to `"ubuntu-latest"`. The projection runs only on pull requests of public
repositories; a private repository carries no `SITUATION.md`, and a pull
request from a fork is refused. A fork's repository follows its upstream's
`AGENTS.md` and does not call the AGENTS.md check.

## Qualification boundary

The source examples and pinned API/client replay preserve the meanings in
contract/bedrock-v2.yaml. They use returned IDs, standing judgments and
explicit reference pins. Source qualification does not prove live platform
identity, a deployed board or a migrated scope.

Releasing 2.1.0 activates nothing by itself. A scope changes authority after
reconciliation and its qualification receipt; existing Git history remains.
Stage0 and the Stage1 canary proceed when qualified. After all six canary
gates, stop and report before Stage2 or Stage3. Historical namespace and
organisation source remains in Git, outside the new publication manifest.
