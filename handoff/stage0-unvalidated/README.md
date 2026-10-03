# Stage 0 stopped handoff: unvalidated drafts

The operator's 2026-10-03 11:21Z access instruction stops source implementation
in this repository pod. These files preserve the existing child drafts for
the console implementer. They are unpublished, outside the manifest, and do
not change the active contract, templates, skills, version or distribution.

Assignment: https://github.com/cleverunicornz/yeetz-bedrock-protocol/issues/40.
Publication blocker: https://github.com/cleverunicornz/infra-v2/issues/618.
Baseline: main `757905749f8cfb3176983cc0eec936ff190ffe97`.

## Collected work

- `handoff/stage0-unvalidated/contract/skills/`: all thirteen draft verb
  skills, preserving meanings and adding client calls and native requests.
- `handoff/stage0-unvalidated/contract/tool-interface.md` and
  `handoff/stage0-unvalidated/contract/tool-interface.json`: native API and
  client schema pins, payload projection, ID binding, response and refusal
  behavior. Public client refusals raise sanitized exceptions; they are not
  native HTTP refusal response bodies.
- `handoff/stage0-unvalidated/contract/tool-examples/`: sequential fixtures,
  call checker, actual API/client/projector scratch replay and probe draft.
- `handoff/stage0-unvalidated/prepare-verbs.py`: original temporary draft
  generator, retained as development material only.

Source pins: task-graph `ac91c8dda973281bcc2b732886bdac8abf6ee30b`;
runner-images `f4dad5ba6c989e5aaf0896b7dd1ccd8e49fd3c37`.
The replay uses an explicit test identity seam. It cannot establish production
registration, live MCP qualification or canary authority.

## Verification state

No tests ran. The required untouched `contract/check.py` baseline did not run;
the workbench remained queued at position 3. The repository has no existing
CI workflow or baseline run. No independent validator was started, no PR was
published by this pod, and no release or activation happened. The drafts have
not been schema-checked, compiled, executed or independently reviewed.

## Console continuation

1. Run the untouched baseline first, using the workbench or source-authored
   qualification CI. Read the CI runner skill before adding a workflow.
2. Inspect and integrate these drafts into the actual contract paths; adapt
   the checker to preserve semantic validation while permitting pinned tool
   procedures. Physically replay calls on isolated pinned PostgreSQL/AGE
   with the real source API and client. Bind only returned IDs.
3. Implement the protocol Decision, three-part compiler and templates,
   short compiled example, VERSION/manifest and release 2.0.0. None of those
   source changes were authored in this pod before the stop instruction.
4. Apply the operator's 11:16Z design: tool synopses for graph, memory and
   board; one axiom per noun; each verb points to its skill; no noun skills;
   no repeated skill sentences. Add sentence-duplication CI. The organisation
   part is only a few pointers; the repository part has identity and only
   bootstrap information the graph cannot represent.
5. Keep draft until complete tests/CI, self-review, independent Codex
   validation and physical proof. Coordinate the exact org package/compiler
   contract with clever-unicorn-org #10/#11 and source interfaces with
   task-graph #11 and runner-images #130. D5/I74 remain immutable.
6. Stage 1 is github-agent-mcp: 131 ID records, 70 References, 1.69 MB per
   the chosen inventory. Prove the tool works; every record, link, Reference
   and history agrees with Git; real repo-pod work reads and writes through
   the tool; invariants and open work surface; the situation freeze holds;
   fresh questioned agents correctly explain and use the tools, nouns and
   verbs, with retained transcripts. Fix and re-test every failing gate.
7. After Stage 1, stop and report before any Stage 2 or 3 activation. No
   blanket fleet pin or default activation. The 11:21Z access instruction
   withdraws all previous console endpoints: issue #40 is the handoff route.

The final local commit and clean-worktree receipt are posted to issue #40.
