<bedrock-repository>
## <repository name>

- Identity: one sentence stating what this repository is and produces.
- Ownership: `OWNED`, or `UPSTREAM_FORK` with the public upstream coordinate.
- Phase and implementation map: `situation/context.md`.
- Critical invariants: each `critical` invariant verbatim, one per line, each
  linking its record under `situation/invariants/`.
- Verification: exactly one of two recorded cases. Assured: the exact
  workflow or command to dispatch, the witness it produces, and the rule that
  gate claims cite the resulting run URL — written only when the linked
  Promise, Oracle, and Witness records support the gate claims it backs.
  Unassured: a bounded statement that no assured witness route is presently
  recorded, linking the Gap that retains the absence and any proposed
  Candidate without promoting it. A workflow merely present in the repository
  is evidence, never an assurance by itself.
- Tool priority: repository-specific tool preferences beyond the organization
  defaults, or `organization defaults`.
- Donor boundary: the commit at which legacy material became historical, when
  a BACKPORT occurred; otherwise `none`.
</bedrock-repository>
