# Bedrock roles and their verbs

Bedrock has seven roles. Each holds a set of the thirteen verbs; what each
verb means, its inputs, outputs and refusals are in its skill,
`contract/skills/<verb>/SKILL.md`. This table is derived from
`contract/bedrock-v2.yaml` (`roles` and `verbs`) and stated in prose in
`contract/bedrock-v2.md` section 7.

## Roles and their verbs

| Role | Verbs | What the role is for |
|---|---|---|
| `authority` | `stipulate` `declare` `formulate` `decide` `mint` `define` `revoke` `supersede` | The accountable party: sets rules, decides, commits. |
| `orchestrator` | `declare` `formulate` `evaluate` `mint` `define` `revoke` `supersede` | Runs work through other agents and commits them to delegated Promises. |
| `scout` | `declare` `formulate` `evaluate` | Finds things out, with evidence. |
| `implementer` | `declare` `formulate` `produce` `refine` | Changes the subject and produces the Witnesses. |
| `validator` | `judge` `declare` | Judges, bounded by the Oracle and scope. |
| `advisor` | `declare` `formulate` `evaluate` | Gives a second opinion; the requester keeps ownership. |
| `automation` | `declare` `formulate` `refine` `revoke` `supersede` | Unattended agents: declare, formulate, add sightings; revoke or supersede only undecided Candidates. |

## Verbs and their roles

| Verb | Held by | Skill |
|---|---|---|
| `stipulate` | `authority` | `contract/skills/stipulate/SKILL.md` |
| `declare` | `authority` `orchestrator` `scout` `implementer` `validator` `advisor` `automation` | `contract/skills/declare/SKILL.md` |
| `formulate` | `authority` `orchestrator` `scout` `implementer` `advisor` `automation` | `contract/skills/formulate/SKILL.md` |
| `evaluate` | `orchestrator` `scout` `advisor` | `contract/skills/evaluate/SKILL.md` |
| `decide` | `authority` | `contract/skills/decide/SKILL.md` |
| `mint` | `authority` `orchestrator` | `contract/skills/mint/SKILL.md` |
| `define` | `authority` `orchestrator` | `contract/skills/define/SKILL.md` |
| `produce` | `implementer` | `contract/skills/produce/SKILL.md` |
| `refine` | `implementer` `automation` | `contract/skills/refine/SKILL.md` |
| `judge` | `validator` | `contract/skills/judge/SKILL.md` |
| `assure` | none: a transition, not performed | `contract/skills/assure/SKILL.md` |
| `revoke` | `authority` `orchestrator` `automation` | `contract/skills/revoke/SKILL.md` |
| `supersede` | `authority` `orchestrator` `automation` | `contract/skills/supersede/SKILL.md` |

## How the table applies

- **Guidance, not enforcement.** Roles and their verbs are taught by prompts
  and skills. Tools record every act with its lineage and never refuse one for
  its role. The runtime stamps an act's role from what executes the agent; an
  agent never sets its own role.
- **At board level**, a board's owner performs any verb on its own board's
  records. The table applies at repository level and above.
- **Structural acts** (`store`, `group`, `regroup`, `relate`, `amend`) are
  open to every role; they make nothing true.
- **Every act** is refused when its id is already recorded
  (`duplicate_act_id`), and an act the transition table does not allow is
  refused with its reason.
- **Some separations follow from the table:** the judge does not decide, fix
  or mint; the evaluator informs a decision and does not make it; the
  producer of a Witness does not judge it above board level; only the
  authority decides.
- **Drift** is measured from the act log and never blocks: a verb performed
  by a role that does not hold it; judging rounds per Promise; Gaps declared
  per judgment; Gaps never decided; above board level, a judge act by the
  producer of the judged Witness; amendments per act and acts amended near the
  end of their window; sessions with acts but no board, or a board that does
  not match the session's brief.
- **An organisation maps its own roles and runtimes onto these.** The
  procedures by which its agents perform each verb are organisation policy,
  layered on these skills; they add and specialise, and never redefine a
  verb.
