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
| **Invariant** | `I` | `stipulated` `superseded` `revoked` | `stipulate` | A binding rule in a scope. |
| **Gap** | `G` | `declared` `decided` `superseded` `revoked` | `declare` | An absence, concern or uncertainty, at its actual certainty. |
| **Candidate** | `C` | `formulated` `evaluated` `decided` `superseded` `revoked` | `formulate` | A brief hypothesis: a possible response, derived from evidence, not a commitment. |
| **Decision** | `D` | `decided` `superseded` `revoked` | `decide` | A collapsed choice with its grounds. |
| **Promise** | `P` | `asserted` `assured` `superseded` `revoked` | `mint` | A falsifiable commitment: "we want this to be true". |
| **Oracle** | `O` | `defined` `superseded` `revoked` | `define` | How one Promise is judged: inputs, holds-when, fails-when, arrangement. |
| **Witness** | `W` | `produced` `judged` `revoked` | `produce` | One observation from one real run, retained before and independent of any verdict. |
| **Reference** | `R` | `stored` `superseded` `revoked` | `store` | Pinned supporting depth: a stored artifact, a repository file at a commit, or a website extraction. |

Fields (limits in "Field limits" below; `?` marks optional):

- **Invariant:** `title`, `rule`, `priority` (`critical` or `standard`). Optional basis links.
- **Gap:** `title`, `statement`, `impact?`. Optional `about` links and `arose_in` (the act during which it arose,
  for example a judgment).
- **Candidate:** `title`, `hypothesis`. At least one `responds_to` link (a Gap, Witness, Decision, Reference or
  Candidate). Depth goes in References.
- **Decision:** `title`, `statement`, `why`, `rejected?` (alternative and why), `revisit_when?`. Optional
  `considered` links and per-subject `outcomes`.
- **Promise:** `title`, `statement`, `scope`, `residual?`. A `basis`: a Decision (the grounds), or a Reference
  holding the accepted instruction or specification; optional `from_candidate` and `addresses` (Gaps).
- **Oracle:** `title`, `judges` (one Promise), `inputs`, `holds_when`, `fails_when`, `arrangement` (`human`,
  `agent`, `deterministic`, `mixed`), `executable?`. A wholly human Oracle is complete as it stands.
- **Witness:** `title`, `observes` (one Promise), `observed_at`, `coordinate` (what was run: a commit, a release, a
  draft, any version coordinate), `result` (what was observed, never a verdict), `evidence` (at least one
  Reference).
- **Reference:** see section 9.

### Plan: a group, not a noun

A **Plan** (`PLAN` prefix) groups Candidates and Promises, nothing more: `title`, `members`, and optional, loose
`waits_on` links between members (`member` waits upon `upon`). Order is never required up front. Each member is
named once; a `regroup` that adds another noun, removes what the Plan does not hold, or removes a member a `waits_on`
link still names is refused (`bad_member`). A Plan asserts
nothing and has no completion condition; its progress is read from its members' states. It is made by the
structural act `group`, changed by `regroup`, and withdrawn by `revoke`. A Plan's states are `grouped`,
`regrouped` and `revoked`.

### States: one rule

- **A record's state is the past tense of the last verb applied to it.** No other state words exist.
  - Invariant: `stipulated`.
  - Gap: `declared`, then `decided`.
  - Candidate: `formulated`, then `evaluated`, then `decided`.
  - Decision: `decided`.
  - Oracle: `defined`.
  - Witness: `produced`, then `judged`.
  - Reference: `stored`.
- **The one exception is the Promise:** `asserted` (by `mint`), then `assured` (a judgment held).
- **Every noun may also be `superseded` or `revoked`**, except that a Witness is never superseded (section 6,
  rule e).
- **A record's first state is the past tense of the verb that makes its noun.** A Witness made by `refine` is
  therefore `produced`. `refine` on a Gap or Candidate adds a sighting and gives no state; `relate` and `amend`
  give none either.
- **A state changes only when an act is done.** No act has phases. Work in progress shows on the agent's board,
  not in a record's state.
- **The latest standing act wins** (section 5): a state comes from the last act that still stands.

### Outcomes

What a judgment, a decision or an evaluation concluded is the act's **outcome**, recorded on the act. An outcome is
never a state word.

| Act | Subject | Outcomes |
|---|---|---|
| `evaluate` | Candidate | `favourable` `unfavourable` `mixed` `inconclusive` |
| `decide` | Candidate | `accept` `decline` |
| `decide` | Gap | `close` `keep` |
| `judge` | Promise | `holds` `does_not_hold` `inconclusive` |

A `decide` act with either outcome leaves its subject `decided`. A `judge` act leaves its Witness `judged`; its
outcome (the `verdict`) decides whether the Promise is `assured`.

### Field limits

| Kind | Limit | Fields | Also |
|---|---|---|---|
| `title` | 256 characters | `title` | A Witness coordinate and a rejected alternative. Aim for one line. |
| `text` | 1024 characters | `statement` `rule` `hypothesis` `why` `scope` `inputs` `reason` `note` | Holds-when, fails-when, impact, residual and revisit-when. |
| `result` | 512 characters | `result` | A Witness's observed result. |

Limits are counted in characters. For a title, aim for one line. An oversized write is refused with the field, its
size and the limit; nothing is cut silently. Point, never copy: write the detail into a Reference and link it. A
lower layer may tighten a limit, never loosen it.

## 4. Verbs

### The thirteen verbs

| # | Verb | Kind | Makes or changes | Meaning |
|---|---|---|---|---|
| 1 | `stipulate` | act | `Invariant` | State a binding rule in a scope. A Decision is optional basis; an axiom needs none. |
| 2 | `declare` | act | `Gap` | Record an absence, concern or uncertainty. Assigns nothing. |
| 3 | `formulate` | act | `Candidate` | Derive a possible response from evidence. |
| 4 | `evaluate` | act | `Candidate` | Investigate a Candidate; findings are References; the outcome feeds `decide`. |
| 5 | `decide` | act | `Decision` `Candidate` `Gap` | Collapse a choice: record each subject's outcome and the grounds. Never mints. |
| 6 | `mint` | act | `Promise` | Make a commitment, directly (on a Decision or an accepted instruction) or from an accepted Candidate (via its Decision). |
| 7 | `define` | act | `Oracle` | Make the judgment rule for one Promise. |
| 8 | `produce` | act | `Witness` | Retain an observation of a real run, with no verdict. |
| 9 | `refine` | act | `Witness` `Gap` `Candidate` | Add without changing a claim: a better Witness after an inconclusive verdict, or a sighting on a Gap or Candidate. |
| 10 | `judge` | act | `Witness` `Promise` | Apply the Promise's Oracle to one Witness, once per (Witness, Oracle) pair: `holds`, `does_not_hold` or `inconclusive`. |
| 11 | `assure` | transition | `Promise` | The Promise becomes `assured`. Not performed by anyone: the state change when a `holds` judgment becomes the latest standing one. |
| 12 | `revoke` | act | `Invariant` `Gap` `Candidate` `Decision` `Promise` `Oracle` `Witness` `Reference` `Plan` | Withdraw a record or a Plan, with a reason. History stays. |
| 13 | `supersede` | act | `Invariant` `Gap` `Candidate` `Decision` `Promise` `Oracle` `Reference` | Replace a record by a successor of the same noun. History stays. |

### Where the draft list and the rulings pulled apart, and how this draft resolves it

1. **`assure` is one of the thirteen, but it is a state transition, not an act.** It keeps its name and its place
   in the list, with kind `transition`. No one performs it and it has no act node of its own; it is recorded as the
   state change of the `judge` act whose verdict is `holds` (section 6), or of the `revoke` after which a `holds`
   judgment is again the latest standing one (section 5). The twelve other verbs are performed acts.
2. **`refine` is wider than "a better Witness".** Automation must add evidence to an existing Candidate instead of
   writing a duplicate, and a Gap collects further observations. Both are refinement: they add, and change no claim.
   On a Witness, `refine` makes a new Witness linked to the earlier one (a Witness is immutable); on a Gap or
   Candidate it adds a sighting (a note and optional References). Independent sightings feed scoring.
3. **Nothing in the thirteen makes a Reference or a Plan.** Both are made by **structural acts** (below): recorded
   with the same envelope and lineage as a verb, open to every role, but they make nothing true. A Reference is
   depth and asserts nothing; a Plan only groups. "Only a verb makes something true" holds.
4. **Witnesses are never superseded.** An observation happened; replacing it would rewrite history. An inadequate
   Witness is refined; a misattributed one is revoked with its reason.
5. **A Gap is decided only by `decide`** (outcome `close` or `keep`). A judge's declared Gap is binding as a finding and the implementer cannot
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
| `regroup` | Plan | Add or remove members or `waits_on` links. |
| `relate` | an optional link | Add or remove `belongs_to` (scope to scope) or `about` (record to record). Never required up front. |
| `amend` | the author's own record | Correct one's own record within the edit window: the projected record takes the corrected fields. |

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
| `evaluate` | `Candidate` | `findings`, `outcome` | `orchestrator` `scout` `advisor` | A Candidate needs investigation before deciding. Recorded once the investigation is done, with its outcome. |
| `decide` | `considered` | `Decision`, `outcomes` | `authority` | A choice collapses: a Candidate accepted or declined, a Gap closed or kept, any recorded choice. |
| `mint` | `basis`, `from_candidate`, `addresses` | `Promise` | `authority` `orchestrator` | A commitment is accepted. Direct: basis is a Decision (the grounds) or a Reference holding the accepted instruction. Via a Candidate: basis is the Decision that accepted it; citing any other Decision is refused (`wrong_basis`). |
| `define` | `Promise` | `Oracle` | `authority` `orchestrator` | Best before `produce`. A retrospective Oracle is ordinary and honest about its time. |
| `produce` | `Promise`, `evidence` | `Witness` | `implementer` | A real run observed the Promise's subject. |
| `refine` | `target`, `evidence` | `Witness`, `sighting` | `implementer` `automation` | After an inconclusive verdict; or a further independent sighting of a Gap or Candidate. |
| `judge` | `Promise`, `Oracle`, `Witness` | `verdict` | `validator` | A Witness of the Promise exists, the Promise has an Oracle neither superseded nor revoked, and that (Witness, Oracle) pair is not yet judged. |
| `revoke` | `target`, `basis` | `revoked` | `authority` `orchestrator` `automation` | After the edit window, to withdraw a record with its reason. |
| `supersede` | `target`, `successor`, `basis` | `superseded` | `authority` `orchestrator` `automation` | After the edit window, to replace a record by a successor made first by its own verb. |

Every row also carries the envelope: actor, time, level, scope, session, and turn and tool call where known.

### Transitions

`—` in From means the act makes the record. A `recomputed` row is the state that remains when the act a state rested
on is revoked or superseded (below).

| Noun | From | To | By | Note |
|---|---|---|---|---|
| Invariant | — | `stipulated` | `stipulate` | |
| Invariant | `stipulated` | `superseded` | `supersede` | |
| Invariant | `stipulated` | `revoked` | `revoke` | |
| Gap | — | `declared` | `declare` | |
| Gap | `declared` | `decided` | `decide` | |
| Gap | `decided` | `declared` | `revoke` `supersede` | recomputed |
| Gap | `declared` `decided` | `superseded` | `supersede` | |
| Gap | `declared` `decided` | `revoked` | `revoke` | |
| Candidate | — | `formulated` | `formulate` | |
| Candidate | `formulated` | `evaluated` | `evaluate` | |
| Candidate | `formulated` `evaluated` | `decided` | `decide` | |
| Candidate | `decided` | `evaluated` | `revoke` `supersede` | recomputed |
| Candidate | `decided` | `formulated` | `revoke` `supersede` | recomputed |
| Candidate | `formulated` `evaluated` `decided` | `superseded` | `supersede` | |
| Candidate | `formulated` `evaluated` `decided` | `revoked` | `revoke` | |
| Decision | — | `decided` | `decide` | |
| Decision | `decided` | `superseded` | `supersede` | |
| Decision | `decided` | `revoked` | `revoke` | |
| Promise | — | `asserted` | `mint` | |
| Promise | `asserted` | `assured` | `assure` | |
| Promise | `assured` | `asserted` | `judge` | |
| Promise | `assured` | `asserted` | `revoke` | recomputed |
| Promise | `asserted` | `assured` | `revoke` | recomputed |
| Promise | `asserted` `assured` | `superseded` | `supersede` | |
| Promise | `asserted` `assured` | `revoked` | `revoke` | |
| Oracle | — | `defined` | `define` | |
| Oracle | `defined` | `superseded` | `supersede` | |
| Oracle | `defined` | `revoked` | `revoke` | |
| Witness | — | `produced` | `produce` `refine` | |
| Witness | `produced` | `judged` | `judge` | |
| Witness | `produced` `judged` | `revoked` | `revoke` | |
| Reference | — | `stored` | `store` | |
| Reference | `stored` | `superseded` | `supersede` | |
| Reference | `stored` | `revoked` | `revoke` | |
| Plan | — | `grouped` | `group` | |
| Plan | `grouped` | `regrouped` | `regroup` | |
| Plan | `grouped` `regrouped` | `revoked` | `revoke` | |

Notes:

- **A Promise is `assured` while its latest standing judgment is `holds`**, and `asserted` otherwise; `inconclusive`
  judgments do not count, being verdicts on the Witness. `define` and `produce` never move a Promise. `holds`
  moves it by the `assure` transition; a later `does_not_hold` moves it back by `judge`.
- **An act a table does not allow is refused**, with the reason. Evaluating a `decided` Candidate, for example, is
  refused; a later Decision may decide it again.
- **A Candidate decided `accept` stays a Candidate after minting.** Minting from a Candidate needs its latest
  standing outcome to be `accept`.
- **Superseding or revoking an assured Promise, a Decision or an Invariant cites a Decision as basis**
  (guidance). An assured Promise is invariant behaviour: changing it is a superseding Promise, minted with its own
  Oracle and new Witnesses.
- **Automation agents** revoke or supersede only Candidates not yet `decided` (guidance). Indexes hide superseded
  and revoked records; lineage keeps them.

### The latest standing act wins

- **A state comes from the last act that still stands.** An act stands unless the record it rests on is superseded
  or revoked. A judgment rests on its Witness; a `decide` outcome on a subject rests on its Decision. Every other
  act rests on nothing. `revoke` and `supersede` acts always stand: revoking a successor does not restore what it
  superseded. So an assured Promise goes back to `asserted` when a later judgment says `does_not_hold`: that
  judgment is now the latest.
- **When an act stops standing, the states that rested on it are recomputed from what remains** (the `recomputed`
  rows above). An assured Promise goes back to `asserted` when the Witness behind its assurance is revoked, unless
  an earlier `holds` judgment still stands and is again the latest. A Candidate or Gap whose Decision is revoked, or
  superseded by one that does not decide it, is again `evaluated`, `formulated` or `declared`.
- **Recomputation goes one step and creates no work** (section 6, rules a and d).
- Worked example: `contract/examples/11-latest-standing-act.yaml`.

### The edit window

- **For 10 minutes after the act that made a record, its author may `amend` it.** The window runs from that act's
  `recorded_at`; amendments do not extend it. The author is the same `actor.agent`.
- **An amendment of an amendment corrects the same record.** The tool follows the amended act back to the act that
  made the record and measures the window, and the author, from that act. Only an act that made a record is
  amended: amending an act that made none (`evaluate`, `judge`, `revoke`, `supersede`, `regroup`, `relate`, a
  sighting) is refused (`not_amendable`). Worked examples: `contract/examples/14-amend-of-amend-window.yaml`,
  `contract/examples/15-amend-needs-made-record.yaml`.
- **An amendment changes only the record the act made.** Its `changes` name that record and its corrected fields;
  the projected record takes them (`contract/examples/05-edit-window.yaml`). Another key, or a changed `id`, is
  refused (`not_amendable`).
- **Following the targets back never loops.** An amendment that targets itself, or a chain that meets an act twice,
  is refused (`amend_cycle`; `contract/examples/16-amend-self-reference.yaml`). Act ids are unique in the log: a
  second act with a recorded id is refused (`duplicate_act_id`; `contract/examples/17-duplicate-act-id.yaml`).
- **The tool tells the author how long is left**, as `edit_window_closes_at` and seconds left, on the making act and
  on every amendment.
- **After the window, only `supersede` or `revoke`.** An amendment after the window (`edit_window_closed`), or by
  anyone else (`not_author`), is refused with the reason and the verbs that remain.
- **Every amendment is itself an act** with its own envelope; nothing is overwritten without a trace.
- **The same rule applies to an agent's board.** A lower layer may shorten the window, never lengthen it.

## 6. Judging and assurance

- **A Promise is asserted when minted** ("we want this to be true") and **assured** while its latest standing
  judgment finds that a Witness proves it.
- **Judge is the same at every level.** Input: the Promise as stated, its Oracle (neither superseded nor revoked),
  one Witness of that Promise, and a (Witness, Oracle) pair not yet judged. Output: an outcome, the `verdict`, with
  a reason.
  - `holds`: the Witness shows the Promise holds within its scope. The Promise is `assured` (the `assure`
    transition).
  - `does_not_hold`: a demonstrated failure within scope, shown by a concrete probe and cited as
    `failure_evidence`. A hypothetical failure is never `does_not_hold`. An assured Promise goes back to
    `asserted`.
  - `inconclusive`: a verdict on the Witness, not on the Promise; the Promise's state is unchanged. `refine` may
    follow.
- **Positive space only.** The judge decides the Promise as stated, within its scope. It does not widen the scope,
  add requirements, or try to prove a negative.
- **Gaps are declared, never gating.** Conditions under which the Promise might not hold are declared as Gaps by
  separate `declare` acts with `arose_in` set to the judge act. Such a Gap is binding as a finding: recorded,
  visible, and decided only by `decide`. It never blocks assurance, and it is not a Promise anyone asserted. Turning
  it into work takes `formulate`, `decide` and `mint`, which belong to other roles.
- **A judge holds `judge` and `declare` only.** It is free to be rigorous inside its scope, and it does not rule
  outside it.

### No recursive invalidation

Agents have been seen trapped in a loop: rejudge, then a new Witness, then rejudge. These rules keep it from
starting.

a. **Recomputing a state never creates work.** No act is ever required or generated automatically by a state
   change; agents decide what to do next.

b. **One judgment per (Witness, Oracle) pair.** A rejudge happens only when the Witness or the Oracle is new.
   Judging the same pair again is not an act: the tool refuses it (`already_judged`).

c. **Only a `does_not_hold` verdict, or revoking the Witness behind the assurance, removes assurance.** Superseding
   the Oracle or a Reference does not: the Promise stays assured until a newer judgment says otherwise. The query
   `assured_under_earlier_oracle` lists such Promises.

d. **Changes go one step and never cascade.** Revoking a Witness changes that Witness and its Promise's state,
   nothing else. No revocation or supersession causes another.

e. **Witnesses are never superseded.** A better observation is a new Witness made by `refine`, and that new Witness
   is judged like any other.

Worked example, `contract/examples/10-no-recursive-invalidation.yaml`:

1. Promise P-1 is minted and Oracle O-1 defined. Witness W-1, a run at the first commit, is judged against O-1:
   `holds`. P-1 is `assured`.
2. O-2, a stricter Oracle, is defined and supersedes O-1. P-1 stays `assured` and nobody has to rejudge (c, a).
3. W-2, a later run, is judged against O-2: `does_not_hold`, with its failure evidence. P-1 is `asserted`. W-1 and
   its judgment stay as they were; no other record changes and no act is generated (a, d).
4. The fix is domain work, not an act. W-3, a run after the fix, is judged against O-2: `inconclusive`, a verdict
   on W-3 that leaves P-1 `asserted`. W-4, made by `refine` of W-3, is judged against O-2 like any other Witness:
   `holds`. P-1 is `assured` again (e).
5. An agent then tries to judge W-2 against O-2 again "because the fix landed". The tool refuses it:
   `already_judged` (b). The pair was judged once; the fix is shown by W-4. The loop never starts.

`contract/check.py` replays the example and checks that P-1 passes `asserted`, `assured`, `asserted`, `assured`,
that every act changes only the records in its one-step reach, and that no act is ever generated.

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
  - Gaps never decided;
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
- **Every conversion records what made it:** `tool`, `tool_version`, `converted_at` and `from_media_type`, and a
  `source` Reference only where an original is kept. A website Reference always carries its conversion record; its
  source is its `url`.
- **References are immutable.** A change is a new Reference that supersedes the old one. Superseding a Reference
  never removes assurance (section 6, rule c).
- **References are depth, not law.** They never override a record that links them.
- **Visibility** is an organisation-defined value on each Reference, default `shared`. It is always present on a
  stored Reference: when a `store` act gives none, the tool fills the default. References attached at a private scope, such as an operator's console, are visible only there; organisation
  policy sets this.

## 10. Queries

Every noun is queryable by its states and its relations; the rest follow from the act log.

### The fixed queries

| Query | Answers |
|---|---|
| `by_state` | Records of one noun in the given states, optionally at a level or scope. |
| `relations` | A record's links in and out, each with the act that made it. |
| `binds` | Invariants `stipulated` (neither superseded nor revoked) for a scope and every scope it belongs to. |
| `open_work` | Gaps `declared` or last decided `keep`, Candidates `formulated` or `evaluated`, Promises `asserted`, Witnesses `produced`. |
| `assured_by` | The standing judge act, Oracle and Witness behind an assured Promise, and judge acts since. |
| `unjudged_witnesses` | Witnesses in state `produced`, with their Promise. |
| `gaps_without_candidate` | Gaps `declared` or last decided `keep`, with no Candidate responding and no Promise addressing (a relation query). |
| `assured_under_earlier_oracle` | Assured Promises whose standing `holds` judgment applied an Oracle since superseded. |
| `plan_view` | A Plan's members, their states and their `waits_on` links. |
| `how_did_we_get_here` | The path of acts backward from a record: Decisions, Candidates, Gaps, instructions, judgments. |
| `what_changed_since` | Acts recorded after a cursor within the reader's reach; each agent keeps its own last-seen cursor. |
| `transcript_behind` | An act's session, turn and tool-call pointers, for the transcript store to resolve. |
| `drift` | The drift signals of section 7, counted. |

## 11. Questions closed in review 1

1. **Where Bedrock-level records live.** Bedrock has its own database.
2. **Visibility of References attached at a private scope.** References attached at an operator's console are
   visible only at the console; organisation policy sets this (section 9).
3. **Identity.** Yes, as drafted: a prefix plus a token unique per organisation store. How imported v1 records keep
   their original coordinates (and v1's reused ids) is settled in the import design.
4. **Two-phase acts.** No. No act has phases, `evaluate` included; a state changes only when an act is done, and
   work in progress shows on the agent's board.
5. **Contradiction.** Answered by the latest-standing-act rule (section 5): a later `does_not_hold` moves an
   assured Promise back to `asserted`.
6. **Who may shorten the window and tighten limits.** Yes, the organisation layer (section 8).
7. **Derived links** (labels, similarity, links made by models used as functions). Yes: they are not acts, make
   nothing true, and are stored apart with function, version and confidence. Their shape comes with the scoring
   work.
8. **Plan completion.** No. A Plan has no completion condition; progress is read from its members.
9. **Roles.** Yes: the seven Bedrock roles and their verb sets are a first cut, tuned from the drift measures.
10. **Backward moves.** Answered by the latest-standing-act rule (section 5): states are recomputed from the acts
    that still stand. An assured Promise goes back to `asserted` when the Witness behind its assurance is revoked;
    recomputation goes one step and never cascades (section 6, rule d).
