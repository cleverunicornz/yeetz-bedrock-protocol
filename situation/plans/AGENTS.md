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
path. Files outside this repository are referenced only by full public URL.
Never reference a local clone, a private checkout, or a machine-local path.
Every reference must resolve for a reader on any machine.
