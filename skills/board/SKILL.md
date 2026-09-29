---
name: board
description: Keep your session board - the outline of what this session set out to do, in the Bedrock kinds (plan, promise, oracle, witness, gap, candidate, decision, invariant, reference). Covers when to write what, the one-line view you see every turn, field limits and how to point instead of copy, sub-agents (pre-fill, delegation label, attach, propose, accept or decline), replacement sessions (adopt), reading other boards of your repository, and cross-repository work (contract first). Read it at the start of every session and before you create a sub-agent.
---

# board

Every session has a board: a short outline of what you set out to do and how
it will be judged, kept in the Bedrock kinds. It survives compaction, context
resets and replacement sessions; its active items are shown to you every turn
as one line each. It is an outline, not a book: it holds titles, short
statements and pointers; the detail lives in files, commits, pull requests and
records it points to.

The board is your working memory for the session and your only task list.
Harness auto-memory and the harnesses' own to-do lists (Claude Code's task
list, Codex's plan tool, NOOA's `self.todo`) are off: plan and track every
step on the board, with states and notes. What the next session or another
agent must know goes on the board (for this work) or into the repository's
records (for good).

## Tools

- **Claude Code and Codex:** the MCP tool `board` (one tool, `op` plus
  fields) and the resource `board://current`.
- **NOOA:** `self.board` (`plan`, `add`, `update`, `state`, `note`, `link`,
  `unlink`, `focus`, `prefill`, `propose`, `accept`, `decline`, `join` (the
  `attach` op), `adopt`, `view`, `history`, `boards`, `board`); its view is
  in your context every turn.
- **Shell:** `cvu-board view`, `cvu-board add kind=gap title="..."`.

Ids: `P-3` is yours; `a2/P-3` belongs to agent `a2` of your tree (the view
shows handles); `<session>/P-3` names any item of your repository's boards.

## When to write what

- **At the start:** `plan` (one line: what this session sets out to do), then
  a `promise` for each result you will deliver, each with an `oracle` (how it
  will be judged) before you start the work.
- **While working:** set states as they change (`open`, `active`, `blocked`,
  `done`); `focus` the item you are on; break a promise into smaller items
  (gaps, candidates, sub-promises) when you need a step list; add a `gap`
  for what is missing or
  unclear, a `decision` when you choose between options (with `why`), a
  `candidate` for an idea not yet committed to, an `invariant` for a rule the
  work must keep, a `reference` for something found and cited.
- **When you have evidence:** a `witness` under the oracle, with
  `witness_result` (what was observed, pass or fail) and a ref to the run,
  pull request or commit (`rel: evidenced_by`).
- **When plans change:** never delete. Mark the old item `superseded` with its
  `successor`, or `revoked` with a `reason`.
- **At the end:** every promise is `done` with its witness, or left open with
  a note that says what remains.

## Limits: point, never copy

- title about 120 characters; statement, why, reason and each note about 200
  tokens; witness result about 100 tokens.
- refs: as many as you need, each a **pointer** (a URN, a repository path, a
  commit, `#123` or `owner/repo#123`, a URL) plus a label of about 20 words.
  `rel` says what it is: `about` (default), `depends_on`, `implements`,
  `evidenced_by`. Add `pinned` with the commit a path was read at.
- A write over a limit is refused with a message naming the field, its size
  and the limit. Shorten it, or write the detail into a file and link it.
  Nothing is cut silently.
- Never paste file contents, logs or transcripts into the board. A lower
  circle points to a higher one and never copies it: cite repository records
  and organization rules by their id or path.

## What you see

Every turn: your active items (`open`, `active`, `blocked`) one line each
with ids and the cues `oracle needed` / `witness needed`, the item you were
delegated from, proposals waiting for your answer, and one line per other
agent of your tree. `view <id>` shows one item in full; `view` with
`tree: true` its sub-tree; `view` with `state: done` the finished items;
`history <id>` its changes.

## Sub-agents

The first agent of a session is the board's root; every agent it creates
joins its tree.

1. **Pre-fill before you create.** `prefill` with `parent` = your item the
   sub-agent works on and `items` = its starting items: the delegated promise
   with its oracle, known gaps, references (`parent: "#1"` names an earlier
   item of the same list). It returns a delegation `<item>#<n>`.
2. **Create the agent with the label** `cvu.board.delegation=<item>#<n>`
   (Paseo `create_agent` `labels`), and also put the line
   `board: <item>#<n>` in the brief. The child starts from its pre-filled
   items, never from an empty board.
3. **A child** that does not see its items runs `attach` (NOOA: `join`) with
   the delegation from its brief. It owns its pre-filled items and changes
   them directly.
4. **Items you do not own:** `propose` a change (title, statement, state,
   successor, note, refs) with a `reason`; the owner sees it and runs
   `accept` or `decline` (with a reason). Answer proposals to your items
   promptly: they are shown to you every turn.

## Replacement sessions

A session stopped by a usage limit is never resumed. The new session runs
`adopt` with the previous session's id (`previous`): it takes that session's
place in the tree and its unfinished items.

## Other boards and other repositories

- `boards` lists every board of your repository, past and present; `board`
  with `target_session` reads one. Use them to see what else is happening in
  the repository before you start overlapping work.
- Boards of other repositories are never read live. Work across repositories
  is contract first: the upstream repository states the behaviour as a
  Promise in its records; you add a ref with `rel: depends_on` to that
  Promise's URN and build against it; delivery shows when its Witness lands
  on the upstream default branch.
