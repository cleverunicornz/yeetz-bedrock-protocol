# Executable verb interface

This adapter pins implementation mechanics separately from the fixed Bedrock
meanings. `contract/bedrock-v2.yaml` and `contract/bedrock-v2.schema.json` own
nouns, verbs, states, outcomes and roles. The semantic baseline is protocol
source commit 7579057; release-coordinate changes do not change those meanings.
Reference discipline: `situation/AGENTS.md`.

## Sources and qualification

The declared private coordinates, full commit pins and SHA-256 digests of every consumed source
file are in `contract/tool-interface.json`. Native API/projector source:

- Private: cleverunicornz/task-graph@ac91c8dda973281bcc2b732886bdac8abf6ee30b#src/taskgraph/api.py
- Private: cleverunicornz/task-graph@ac91c8dda973281bcc2b732886bdac8abf6ee30b#src/taskgraph/queries.py
- Private: cleverunicornz/task-graph@ac91c8dda973281bcc2b732886bdac8abf6ee30b#src/taskgraph/identity.py

Actual single-tool client schema and projection:

- Private: cleverunicornz/runner-images@f4dad5ba6c989e5aaf0896b7dd1ccd8e49fd3c37#images/repo-pod/runtime/cvu_task_graph_mcp.py
- Private: cleverunicornz/runner-images@f4dad5ba6c989e5aaf0896b7dd1ccd8e49fd3c37#images/repo-pod/runtime/cvu_task_graph.py

Client source P-000063/O-000064 is qualified for opt-in mock HTTP and real stdio
transport by W-000158; it does not qualify deployment:
Private: cleverunicornz/runner-images@f4dad5ba6c989e5aaf0896b7dd1ccd8e49fd3c37#situation/witnesses/P-000063/W-000158-task-graph-final-source-assurance.md.
Native source P-000001 remains implementing at this pin:
Private: cleverunicornz/task-graph@ac91c8dda973281bcc2b732886bdac8abf6ee30b#situation/promises/P-000001-the-act-log-is-judged-appended-and-projected-by-one-writer.md.
No deployed authority, registration or installed-tool qualification is inferred.

## Calls and projection

The real MCP server is `task-graph`, with exactly one tool named `task-graph`.
Its four operations are `act`, `query`, `reference.put` and `reference.get`.
There are no thirteen named verb tools. The skill JSON is that tool's argument
shape, not an invented transport API. The replay can execute these arguments
through the pinned client against a scratch native HTTP service; it cannot
claim that the tool is available in a session where it is not installed.

For `act`, the client copies verb/level/scope/payload, adds discovered lineage
and the retained request_id, then POSTs /v1/acts. Session is required and
discovered; optional turn/tool_call/repository/paseo_agent_id/harness/model
are claims only. The optional act repository argument must match the discovered
checkout. No caller actor, role, principal, ID or recording time is admitted.
The native API stamps actor fields from its identity implementation.

For `query`, it POSTs {name, params} to /v1/query. For `reference.put`, it
flattens reference fields, adds level/scope and discovered lineage, uses
act_repository for the caller's repository, and POSTs /v1/references. Reference
repository is the pointed-to source, not the caller home. For `reference.get`,
it GETs /v1/references/<returned-id>. Repository-file retrieval is JSON with
reference/state/record; stored markdown retrieval carries
X-Reference-Version, X-Reference-Sha256 and X-Reference-State headers. The
client converts those headers into version/sha256/state plus markdown.

Native success is HTTP200 with seq, act_id, made (nullable), recorded_at,
changes and replayed; making acts also return edit-window fields. Success
through the client retains those fields and adds _client.lineage,
_client.missing_pointers and, for writes, _client.request_id.
Native semantic refusal is HTTP409 with refused.code/message and, for edit
window refusals, remaining_verbs. The client instead raises sanitized
ClientError containing the HTTP status and code, suppressing message and
remaining_verbs; the stdio wrapper turns this into a tool error. HTTP400/401,
transport failures and backend failures are distinct from semantic refusal.

## Sequential IDs and readback

`contract/tool-examples/calls.json` contains full public arguments. Its
${step.field} notation is a fixture substitution performed BEFORE a call. It
uses the actual earlier response; it is not a server batch feature. Parents
and dependencies are recorded first. No sequential IDs, preallocated IDs or
forward references are assumed. ${run} is a unique stable request prefix;
${scope} is the admitted scratch scope. Probe values come from
`contract/tool-examples/probe.py`; the fixture records no deployment promise.

Read a made or affected record through query record with params {id}. Act IDs
are not record IDs; for act provenance use transcript_behind with params
{act}, or how_did_we_get_here with params {id}. Every query result includes
watermark and head. For a write at seq S, wait until watermark >= S before
using the projected result. watermark == head proves catch-up at that snapshot,
not that no later write can occur. assure is only a transition: query
assured_by with params {promise}; never submit verb assure.

After an uncertain write, repeat IDENTICAL arguments with the original
request_id in the same retained client/session/endpoint context. The client
retains original body lineage. A confirmed replay returns the same act_id
and made, replayed true, with no extra append. Changed-body reuse is refused.
This baseline has no request-key-only query; a missing projection does not
prove absence. It also has no native board operation or compiler query.

## Checks and remaining gaps

`contract/check.py` checks fixed semantics and each executable procedure.
`contract/tool-examples/check_calls.py` checks envelopes, substitutions,
source-shaped client arguments, role metadata and semantic replay without
changing noun/verb/role authority. `contract/tool-examples/replay.py` runs the
actual pinned App/Store/Projector and client in an isolated PostgreSQL18.6/AGE
scratch store. Only its test identity seam supplies receiver stamps; it is
explicitly unqualified for live platform trust. It does not read production
credentials, modify a deployed database or activate a runtime.

Physical replay receipts are printed only after the run passes. A not-run or
failed scratch check remains a gap, never a qualification claim. Fixture
repository-file References test pointer roundtrips, not stored object versions
or S3 redaction. The qualified client source's broader mock suite covers its
own transport properties; those Witnesses are not reused as native service
qualification.

Upstream successor registration, original-key-only readback and runtime
distribution remain dependencies:
https://github.com/cleverunicornz/task-graph/issues/11#issuecomment-5968597913
and https://github.com/cleverunicornz/runner-images/issues/130#issuecomment-5968598002.
No profile-to-trust, human authority or cross-home mapping is inferred.
