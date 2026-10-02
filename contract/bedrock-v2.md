# Bedrock v2: the contract

Version 2.0.0-draft. **Status: draft for review.** Nothing in this directory is in force. The v1 protocol
(`templates/root-protocol.md` and the namespace files under `situation/`) stays in force, unchanged, until a release
replaces it. The machine-readable form of this contract is `contract/bedrock-v2.yaml`; an act is validated by
`contract/bedrock-v2.schema.json`; `contract/check.py` proves that the prose, the YAML, the schema and the worked
examples in `contract/examples/` agree.

## 1. What Bedrock is

Bedrock is a protocol, the way a wire protocol is: a small fixed set of **nouns** (what a thing is), **verbs**
(how things are made and moved), **states**, and **acts** (one recorded use of a verb). It changes rarely, and only
when a need applies to everyone who uses it.

**The Bedrock rule.** Anything that defines or changes the nouns, the verbs, or what they mean and how they move is
a Bedrock change. Everything else is policy: an organisation's (two organisations may differ entirely) or a
repository's.

## 2. Principles

1. **Verbs carry the behaviour; nouns only say what a thing is.** A noun is its definition, fields and states. All
   procedure lives with the verb, so a misbehaving verb is tuned at the verb and the effect measured.
2. **Every act is a node.** An act has a verb, inputs, outputs, an actor, a time, a level and lineage pointers. A
   judgment, an evaluation and a decision share the one shape, so "how did this get assured" is a walk.
3. **The act log is authoritative.** Records, states and links are a projection of the log, rebuilt by one
   projector. States are never written directly: the verbs give the states.
4. **Brief records, heavy References.** A record is a thread, not a novel: enough meaning to stand alone, then
   links. Depth lives in References.
5. **Best effort with lineage.** Roles and their verbs are guidance carried by prompts and skills. Tools record
   lineage on every act and do not enforce roles. Drift is a measured signal, never a block.
6. **Positive space only.** A judge decides whether the Promise as stated holds within its scope. Conditions
   outside it are declared as Gaps; they never gate.
7. **One schema at every level.** The nouns and verbs are the same on an agent's board, in a repository, a system,
   an organisation and in Bedrock itself. Level is a property, not a hierarchy.
8. **Designed from the queries back.** Section 10 lists the fixed queries; every act and link exists to answer one.

## 3. Nouns

### The nouns

| Noun | Id prefix | States | Made by | What it is |
|---|---|---|---|---|
| **Invariant** | `I` | `in_force` `superseded` `revoked` | `stipulate` | A binding rule in a scope. |
| **Gap** | `G` | `open` `addressing` `closed` `tolerated` `superseded` `revoked` | `declare` | An absence, concern or uncertainty, at its actual certainty. |
| **Candidate** | `C` | `formulated` `evaluating` `evaluated` `accepted` `declined` `superseded` `revoked` | `formulate` | A brief hypothesis: a possible response, derived from evidence, not a commitment. |
| **Decision** | `D` | `in_force` `superseded` `revoked` | `decide` | A collapsed choice with its grounds. |
| **Promise** | `P` | `asserted` `assuring` `assured` `superseded` `revoked` | `mint` | A falsifiable commitment: "we want this to be true". |
| **Oracle** | `O` | `in_force` `superseded` `revoked` | `define` | How one Promise is judged: inputs, holds-when, fails-when, arrangement. |
| **Witness** | `W` | `produced` `judged` `revoked` | `produce` | One observation from one real run, retained before and independent of any verdict. |
| **Reference** | `R` | `current` `superseded` `revoked` | `store` | Pinned supporting depth: a stored artifact, a repository file at a commit, or a website extraction. |

Fields (limits in "Field limits" below; `?` marks optional):

- **Invariant:** `title`, `rule`, `priority` (`critical` or `standard`). Optional basis links.
- **Gap:** `title`, `statement`, `impact?`. Optional `about` links and `arose_in` (the act during which it arose,
  for example a judgment).
- **Candidate:** `title`, `hypothesis`. At least one `responds_to` link (a Gap, Witness, Decision, Reference or
  Candidate). Depth goes in References.
- **Decision:** `title`, `statement`, `why`, `rejected?` (alternative and why), `revisit_when?`. Optional
  `considered` links and per-subject `outcomes`.
- **Promise:** `title`, `statement`, `scope`, `residual?`. A `basis` (a Decision, or a Reference holding the
  accepted instruction or specification); optional `from_candidate` and `addresses` (Gaps).
- **Oracle:** `title`, `judges` (one Promise), `inputs`, `holds_when`, `fails_when`, `arrangement` (`human`,
  `agent`, `deterministic`, `mixed`), `executable?`. A wholly human Oracle is complete as it stands.
- **Witness:** `title`, `observes` (one Promise), `observed_at`, `coordinate` (what was run: a commit, a release, a
  draft, any version coordinate), `result` (what was observed, never a verdict), `evidence` (at least one
  Reference).
- **Reference:** see section 9.

### Plan: a group, not a noun

A **Plan** (`PLAN` prefix) groups Candidates and Promises, nothing more: `title`, `members`, and optional, loose
`waits_on` links between members (`member` waits upon `upon`). Order is never required up front. A Plan asserts
nothing; its progress is read from its members' states. It is made by the structural act `group`, changed and
retired by `regroup`, and is `open` or `retired`.

### Field limits

| Field | Limit | Used for |
|---|---|---|
| `title` | 120 characters | every record's title, a Witness coordinate, a rejected alternative |
| `text` | 800 characters (about 200 tokens) | statements, rules, hypotheses, why, scope, inputs, reasons, notes |
| `result` | 400 characters (about 100 tokens) | a Witness's observed result |

Limits are counted in characters. An oversized write is refused with the field, its size and the limit; nothing
is cut silently. Point, never copy: write the detail into a Reference and link it. A lower layer may tighten a
limit, never loosen it.

## 4. Verbs

### The thirteen verbs

| # | Verb | Kind | Makes or changes | Meaning |
|---|---|---|---|---|
| 1 | `stipulate` | act | `Invariant` | State a binding rule in a scope. A Decision is optional basis; an axiom needs none. |
| 2 | `declare` | act | `Gap` | Record an absence, concern or uncertainty. Assigns nothing. |
| 3 | `formulate` | act | `Candidate` `Gap` | Derive a possible response from evidence; a Gap it responds to becomes `addressing`. |
| 4 | `evaluate` | act | `Candidate` | Investigate a Candidate; findings are References; the outcome feeds `decide`. |
| 5 | `decide` | act | `Decision` `Candidate` `Gap` | Collapse a choice: record the disposition of each subject and the grounds. Never mints. |
| 6 | `mint` | act | `Promise` `Gap` | Make a commitment from an accepted instruction (direct) or an accepted Candidate (via its Decision). |
| 7 | `define` | act | `Oracle` `Promise` | Make the judgment rule for one Promise. |
| 8 | `produce` | act | `Witness` `Promise` | Retain an observation of a real run, with no verdict. |
| 9 | `refine` | act | `Witness` `Gap` `Candidate` | Add without changing a claim: a better Witness after an inconclusive verdict, or a sighting on a Gap or Candidate. |
| 10 | `judge` | act | `Witness` | Apply the Promise's Oracle in force to one Witness: `holds`, `does_not_hold` or `inconclusive`. |
| 11 | `assure` | transition | `Promise` | The Promise becomes `assured`. Not performed by anyone: the state change of a qualifying judgment. |
| 12 | `revoke` | act | `Invariant` `Gap` `Candidate` `Decision` `Promise` `Oracle` `Witness` `Reference` | Withdraw a record, with a reason. History stays. |
| 13 | `supersede` | act | `Invariant` `Gap` `Candidate` `Decision` `Promise` `Oracle` `Reference` | Replace a record by a successor of the same noun. History stays. |

### Where the draft list and the rulings pulled apart, and how this draft resolves it

1. **`assure` is one of the thirteen, but it is a state transition, not an act.** It keeps its name and its place
   in the list, with kind `transition`. No one performs it and it has no act node of its own; it is recorded as the
   state change of the `judge` act whose verdict is `holds` (section 6). The twelve other verbs are performed acts.
2. **`refine` is wider than "a better Witness".** Automation must add evidence to an existing Candidate instead of
   writing a duplicate, and a Gap collects further observations. Both are refinement: they add, and change no claim.
   On a Witness, `refine` makes a new Witness linked to the earlier one (a Witness is immutable); on a Gap or
   Candidate it adds a sighting (a note and optional References). Independent sightings feed scoring.
3. **Nothing in the thirteen makes a Reference or a Plan.** Both are made by **structural acts** (below): recorded
   with the same envelope and lineage as a verb, open to every role, but they make nothing true. A Reference is
   depth and asserts nothing; a Plan only groups. "Only a verb makes something true" holds.
4. **Witnesses are never superseded.** An observation happened; replacing it would rewrite history. An inadequate
   Witness is refined; a misattributed one is revoked with its reason.
5. **A Gap is closed only by `decide`.** A judge's declared Gap is binding as a finding and the implementer cannot
   dismiss it. `revoke` remains available on a Gap (a mistaken declaration); a Gap revoked by someone other than its
   declarer is a drift signal, not an error.
6. **v1's `challenge`, `test`, `promote`, `implement`, `bound`, `observe`, `surface`, `propose` and `plan`** map
   onto these verbs or leave the core (see `migrations/v1.18.2-to-v2.0.0-draft.md`). Implementation is domain work,
   not a verb.

### Structural acts

| Act | Makes or changes | Meaning |
|---|---|---|
| `store` | Reference | The tool stores the content (or pins the coordinate) and returns a Reference. |
| `group` | Plan | Make a Plan with its first members. |
| `regroup` | Plan | Add or remove members or `waits_on` links, or retire the Plan. |
| `relate` | an optional link | Add or remove `belongs_to` (scope to scope) or `about` (record to record). Never required up front. |
| `amend` | the author's own act | Correct one's own record within the edit window. |

## 5. Acts as nodes

### The act envelope

Every act, verb or structural, is a node with these fields:

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | The act's identity (`A-` prefix). |
| `protocol` | yes | The Bedrock version the act was recorded under. |
| `verb` | yes | One of the twelve performed verbs or a structural act. |
| `level`, `scope` | yes | Where it applies (section 8). |
| `recorded_at` | yes | Set by the tool. |
| `actor` | yes | `kind` (`human`, `agent`, `tool`) and `agent`; `role` and `principal` where known. |
| `session` | yes | Pointer to the session in the transcript store. |
| `turn`, `tool_call` | where known | Pointers to the turn and tool call in that session. |
| `repository` | where known | The repository the actor worked in. |
| `batch` | no | Acts submitted together share a batch id; each keeps its own node and meaning. |
| `edit_window_closes_at` | set by the tool | Section 5, "The edit window". |
| `payload` | yes | The verb's inputs and the record it makes. |

- **Role and principal are stamped, not claimed.** The runtime stamps the role from what executes the agent and the
  principal from the caller's key. An agent never sets its own role. Neither is enforced; both are lineage.
- **The task graph and the transcript store join only by these pointers**, through each service's interface. No
  transcript data is copied into the graph and no graph data into the transcript store. "Show me the transcript
  behind this decision" follows the act's pointers.
- **Outputs are derived.** The projector derives each act's outputs and state changes from the log; an act states
  only its inputs and the record it makes.

### Act nodes, verb by verb

| Verb | Inputs | Outputs | Who (guidance) | When |
|---|---|---|---|---|
| `stipulate` | `basis` (optional) | `Invariant` | `authority` | A binding rule is needed in a scope. |
| `declare` | `about`, `arose_in` (optional) | `Gap` | `authority` `orchestrator` `scout` `implementer` `validator` `advisor` `automation` | Whenever an absence, concern or uncertainty is met, even minor or tentative. |
| `formulate` | `responds_to` | `Candidate` | `authority` `orchestrator` `scout` `implementer` `advisor` `automation` | Evidence suggests a response. Walk the scope first: refine or supersede an existing Candidate rather than duplicate it. |
| `evaluate` | `Candidate` | `findings`, `outcome` | `orchestrator` `scout` `advisor` | A Candidate needs investigation before deciding. May be recorded `begun`, then `completed` (outcome `favourable`, `unfavourable`, `mixed`, `inconclusive`). |
| `decide` | `considered` | `Decision`, `outcomes` | `authority` | A choice collapses: an accept or decline press, a Gap closed or tolerated, any recorded choice. |
| `mint` | `basis`, `from_candidate`, `addresses` | `Promise` | `authority` `orchestrator` | A commitment is accepted. Direct: basis is the instruction's Reference. Via a Candidate: basis is the Decision that accepted it. |
| `define` | `Promise` | `Oracle` | `authority` `orchestrator` | Best before `produce`. A retrospective Oracle is ordinary and honest about its time. |
| `produce` | `Promise`, `evidence` | `Witness` | `implementer` | A real run observed the Promise's subject. |
| `refine` | `target`, `evidence` | `Witness`, `sighting` | `implementer` `automation` | After an inconclusive verdict; or a further independent sighting of a Gap or Candidate. |
| `judge` | `Promise`, `Oracle`, `Witness` | `verdict` | `validator` | A Witness of the Promise exists and the Promise has an Oracle in force. |
| `revoke` | `target`, `basis` | `revoked` | `authority` `orchestrator` `automation` | After the edit window, to withdraw a record with its reason. |
| `supersede` | `target`, `successor`, `basis` | `superseded` | `authority` `orchestrator` `automation` | After the edit window, to replace a record by a successor made first by its own verb. |

Every row also carries the envelope: actor, time, level, scope, session, and turn and tool call where known.

### Transitions

`—` in From means the act makes the record.

| Noun | From | To | By |
|---|---|---|---|
| Invariant | — | `in_force` | `stipulate` |
| Invariant | `in_force` | `superseded` | `supersede` |
| Invariant | `in_force` | `revoked` | `revoke` |
| Gap | — | `open` | `declare` |
| Gap | `open` | `addressing` | `formulate` `mint` |
| Gap | `open` `addressing` | `closed` | `decide` |
| Gap | `open` `addressing` | `tolerated` | `decide` |
| Gap | `open` `addressing` | `superseded` | `supersede` |
| Gap | `open` `addressing` | `revoked` | `revoke` |
| Candidate | — | `formulated` | `formulate` |
| Candidate | `formulated` `evaluated` | `evaluating` | `evaluate` |
| Candidate | `formulated` `evaluating` `evaluated` | `evaluated` | `evaluate` |
| Candidate | `formulated` `evaluating` `evaluated` | `accepted` | `decide` |
| Candidate | `formulated` `evaluating` `evaluated` | `declined` | `decide` |
| Candidate | `formulated` `evaluating` `evaluated` | `superseded` | `supersede` |
| Candidate | `formulated` `evaluating` `evaluated` | `revoked` | `revoke` |
| Decision | — | `in_force` | `decide` |
| Decision | `in_force` | `superseded` | `supersede` |
| Decision | `in_force` | `revoked` | `revoke` |
| Promise | — | `asserted` | `mint` |
| Promise | `asserted` | `assuring` | `define` `produce` |
| Promise | `assuring` | `assured` | `assure` |
| Promise | `asserted` `assuring` `assured` | `superseded` | `supersede` |
| Promise | `asserted` `assuring` `assured` | `revoked` | `revoke` |
| Oracle | — | `in_force` | `define` |
| Oracle | `in_force` | `superseded` | `supersede` |
| Oracle | `in_force` | `revoked` | `revoke` |
| Witness | — | `produced` | `produce` `refine` |
| Witness | `produced` | `judged` | `judge` |
| Witness | `produced` `judged` | `revoked` | `revoke` |
| Reference | — | `current` | `store` |
| Reference | `current` | `superseded` | `supersede` |
| Reference | `current` | `revoked` | `revoke` |

Notes:

- A Promise is **assuring** once it has both an Oracle in force and a live Witness: `produce` moves it when the
  Oracle already exists, `define` when the Witness already exists. `refine` never moves it, because refining needs
  a live Witness of the same Promise, which already made it assuring.
- **Decision outcomes.** For a Candidate: `accept` (to `accepted`), `decline` (to `declined`), `defer` and
  `investigate` (recorded, no state change). For a Gap: `close` (to `closed`), `tolerate` (to `tolerated`),
  `keep_open` (recorded, no state change). An accepted Candidate stays a Candidate after minting.
- **Superseding or revoking an assured Promise, an in-force Decision or an Invariant cites a Decision as basis**
  (guidance). An assured Promise is invariant behaviour: changing it is a superseding Promise, minted with its own
  Oracle and new Witnesses.
- **Automation agents** revoke or supersede only Candidates still undecided (guidance). Indexes hide superseded and
  revoked records; lineage keeps them.

### The edit window

- **For 10 minutes after the act that made a record, its author may `amend` it.** The window runs from that act's
  `recorded_at`; amendments do not extend it. The author is the same `actor.agent`.
- **The tool tells the author how long is left**, as `edit_window_closes_at` and seconds left, on the making act and
  on every amendment.
- **After the window, only `supersede` or `revoke`.** An amendment after the window, or by anyone else, is refused
  with the reason and the verbs that remain.
- **Every amendment is itself an act** with its own envelope; nothing is overwritten without a trace.
- **The same rule applies to an agent's board.** A lower layer may shorten the window, never lengthen it.

## 6. Judging and assurance

- **A Promise is asserted when minted** ("we want this to be true"), **assuring** when an Oracle in force and a
  live Witness exist, and **assured** when a judge finds that a Witness proves it.
- **Judge is the same at every level.** Input: the Promise as stated, its Oracle in force, one Witness of that
  Promise. Output: a verdict, with a reason.
  - `holds`: the Witness shows the Promise holds within its scope. If the Promise is assuring, this act's state
    change is `assure`.
  - `does_not_hold`: a demonstrated failure within scope, shown by a concrete probe and cited as
    `failure_evidence`. A hypothetical failure is never `does_not_hold`.
  - `inconclusive`: a verdict on the Witness, not on the Promise. It leads to `refine`.
- **Positive space only.** The judge decides the Promise as stated, within its scope. It does not widen the scope,
  add requirements, or try to prove a negative.
- **Gaps are declared, never gating.** Conditions under which the Promise might not hold are declared as Gaps by
  separate `declare` acts with `arose_in` set to the judge act. Such a Gap is binding as a finding: recorded,
  visible, and closed only by `decide`. It never blocks assurance, and it is not a Promise anyone asserted. Turning
  it into work takes `formulate`, `decide` and `mint`, which belong to other roles.
- **A judge holds `judge` and `declare` only.** It is free to be rigorous inside its scope, and it does not rule
  outside it.
- **Contradiction.** A later `does_not_hold` on an assured Promise under the Oracle in force leaves it `assured`
  and lists it in the `contradicted` query (section 10). See open question 5.

## 7. Roles and drift

### Roles and their verbs

| Role | Verbs | What the role is for |
|---|---|---|
| `authority` | `stipulate` `declare` `formulate` `decide` `mint` `define` `revoke` `supersede` | The accountable party: sets rules, decides, commits. |
| `orchestrator` | `declare` `formulate` `evaluate` `mint` `define` `revoke` `supersede` | Runs work through other agents and commits them to delegated Promises. |
| `scout` | `declare` `formulate` `evaluate` | Finds things out, with evidence. |
| `implementer` | `declare` `formulate` `produce` `refine` | Changes the subject and produces the Witnesses. |
| `validator` | `judge` `declare` | Judges, bounded by the Oracle and scope. |
| `advisor` | `declare` `formulate` `evaluate` | Gives a second opinion; the requester keeps ownership. |
| `automation` | `declare` `formulate` `refine` `revoke` `supersede` | Unattended agents: declare, formulate, add sightings; revoke or supersede only undecided Candidates. |

- **Guidance, not enforcement.** Roles and verbs are taught by prompts and skills. The tools record every act with
  its lineage and never refuse one for its role. An organisation maps its own roles and runtimes onto these.
- **At board level, a board's owner performs any verb on its own board's records.** The role table applies at
  repository level and above.
- **Structural acts** (`store`, `group`, `regroup`, `relate`, `amend`) are open to every role.
- **Drift signals**, measured from the act log and never a block:
  - a verb performed by a role that does not hold it (for example a validator deciding);
  - judging rounds per Promise;
  - Gaps declared per judgment;
  - Gaps never dispositioned by `decide`;
  - above board level, a judge act by the producer of the judged Witness;
  - amendments per act, and acts amended near the end of their window;
  - sessions with acts but no board, or a board that does not match the session's brief.

## 8. Levels, scope and layering

### Levels

| Level | Where it applies |
|---|---|
| `board` | One session's working outline. |
| `repository` | One repository. |
| `system` | A set of repositories or services that work together. |
| `organisation` | One organisation; each organisation has its own store and never shares it. |
| `bedrock` | The protocol reflecting on itself. |

- **Level is a property** of every act, and so of the records it makes, with a `scope` naming the instance (a
  session, a repository, a system). Adding a level or a whole domain adds a value; nothing else changes. An
  organisation may add values.
- **No forced hierarchy.** A board can stand alone. Belonging is an optional `relate ... belongs_to` link between
  scopes, added when it becomes true and never required up front. `binds` follows those links.

**Layering.** Rules come in layers: Bedrock, then the organisation, then the repository, then the agent at runtime.
Each layer adds and specialises; none redefines the layer below it. Redefining is a Bedrock change.

- **Bedrock only:** the nouns, the Plan group and the structural acts; the verbs and what each means; the states and
  transitions; the act envelope and lineage; the reference kinds; the judge rule.
- **An organisation adds:** level values, its roles mapped onto Bedrock's roles, visibility values, the procedures
  (skills) for each verb, a shorter edit window, tighter limits.
- **A repository adds:** scope names, judging additions in its own skills, its procedures.
- **The runtime adds:** board records and a session's own Plans.

Layers are where rules come from; levels are where records apply. They are separate properties.

## 9. References

### Reference kinds

| Kind | Location | Pinned by |
|---|---|---|
| `artifact` | `stored`: store, key, version, in the versioned object store | object version and sha256 digest |
| `repository_file` | `repository`, `commit`, `path` (any repository) | the commit |
| `website` | `url`, `retrieved_at`, and the `stored` markdown extraction | the stored extraction, its digest and retrieval time |

- **The tool does the storage.** An agent writes a document or points to a file; the tool stores it (S3-compatible,
  versioned) and returns a Reference. Agents never handle store keys.
- **First slice: markdown only.** A stored artifact or extraction is `text/markdown`. Other media come later through
  conversions; a kept original is its own Reference, named as the conversion's `source`.
- **Every conversion records what made it:** `tool`, `tool_version`, `converted_at`, `from_media_type`, and the
  `source` Reference where one is kept. A website Reference always carries one.
- **References are immutable.** A change is a new Reference that supersedes the old one.
- **References are depth, not law.** They never override a record that links them.
- **Visibility** is an organisation-defined value on each Reference, default `shared`; Bedrock only guarantees it is
  there.

## 10. Queries

Every noun is queryable by its states and its relations; the rest follow from the act log.

### The fixed queries

| Query | Answers |
|---|---|
| `by_state` | Records of one noun in the given states, optionally at a level or scope. |
| `relations` | A record's links in and out, each with the act that made it. |
| `binds` | Invariants in force for a scope and every scope it belongs to. |
| `open_work` | Gaps open or addressing, Candidates undecided, Promises asserted or assuring, Witnesses not yet judged. |
| `assured_by` | The judge act, Oracle and Witness that assured a Promise, and judge acts since. |
| `unjudged_witnesses` | Witnesses still `produced`, with their Promise. |
| `gaps_without_candidate` | Open Gaps with no Candidate responding and no Promise addressing. |
| `contradicted` | Assured Promises with a later `does_not_hold` under the Oracle in force. |
| `plan_view` | A Plan's members, their states and their `waits_on` links. |
| `how_did_we_get_here` | The path of acts backward from a record: Decisions, Candidates, Gaps, instructions, judgments. |
| `what_changed_since` | Acts recorded after a cursor within the reader's reach; each agent keeps its own last-seen cursor. |
| `transcript_behind` | An act's session, turn and tool-call pointers, for the transcript store to resolve. |
| `drift` | The drift signals of section 7, counted. |

## 11. Open questions

1. **Where Bedrock-level records live.** This draft assumes Bedrock's own small store, beside this repository; the
   repository keeps no `situation/` of its own today.
2. **Visibility of References attached at a private scope** (for example an operator's own workspace): an organisation value is
   provided; whether those References are shared or restricted is not decided.
3. **Identity.** Prefix plus a token unique per organisation store is assumed; how imported v1 records keep their
   original coordinates (and v1's reused ids) is for the import design.
4. **Two-phase acts.** Only `evaluate` has `begun` and `completed`. Whether `judge` needs the same, for long
   judgments, is open.
5. **Contradiction.** Should a later `does_not_hold` on an assured Promise move it back to `assuring`, or stay a
   query as drafted?
6. **Who may shorten the window and tighten limits.** Drafted as organisation-layer specialisations; the operator
   may prefer Bedrock-only.
7. **Derived links** (labels, similarity, links made by models used as functions) are not acts: they make nothing
   true and are stored apart with function, version and confidence. Their shape is not specified here.
8. **Plan completion.** A Plan has no completion statement; progress is read from members. Whether a Plan needs one
   is open.
9. **Roles.** The seven Bedrock roles and their verb sets are a first cut, to be tuned from the drift measures.
