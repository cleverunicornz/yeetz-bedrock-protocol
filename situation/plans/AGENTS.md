# Plans

A plan is a thin container that groups promises into one delivery effort.
It does not restate what the promises say and does not carry design detail.

## File naming

```
plans/<lifecycle>/PLAN-<six digits>-<kebab-case-name>.md
```

Lifecycle directories: `draft/`, `active/`, `done/`, `abandoned/`. The
directory is the lifecycle state; the file does not repeat it.

## Required headings

- `Promises` — links to every promise in this effort
- `Dependencies` — ordering between promises, when any exists
- `Completion` — the target states that constitute plan completion

## Rules

- A plan contains promises, dependencies, and a completion condition.
  Nothing else.
- Completion is defined by promise states, never by prose judgment.
- Moving a plan between lifecycle directories is an explicit commit that
  explains the transition in its message.
- A done plan's promises must have reached the states its Completion
  section requires.

## Reference discipline

Files inside this repository are referenced by repository-root-relative
path. Files in external public repositories are referenced only by full
public URL. Files in external private repositories are referenced by
declared coordinate — `Private: owner/repo@<ref>#<path>` — never by an
unauthenticated URL, never undeclared. Never reference a local clone, a
private checkout, or a machine-local path.

A declared-private reference that cannot be fetched is expected, not an
error: never stop for one, never remove it, never invent its contents.
Content from a private reference never crosses into a public document.
