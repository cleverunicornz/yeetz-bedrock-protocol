# I-000001 — GitHub work goes through the github MCP tools

## Priority

critical

## Invariant

Pull requests, reviews, issues, projects and CI results are read and changed
through the `github` MCP tools. `git` carries commits and pushes; `gh` waits
on a run and covers only what the tools do not.

## Basis

- [D-000001](org/situation/decisions/D-000001-knowledge-in-records-skills-as-verbs.md)
