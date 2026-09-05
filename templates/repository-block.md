<bedrock-repository>
## <repository name>

- Identity: one sentence stating what this repository is and produces.
- Ownership: `OWNED`, or `UPSTREAM_FORK` with the public upstream coordinate.
- Phase and implementation map: `situation/context.md`.
- Critical invariants: each `critical` invariant verbatim, one per line, each
  linking its record under `situation/invariants/`.
- Verification: how a witness is produced for this repository, naming the
  exact workflow or command to dispatch, and the rule that gate claims cite
  the resulting run URL.
- Tool priority: repository-specific tool preferences beyond the organization
  defaults, or `organization defaults`.
- Donor boundary: the commit at which legacy material became historical, when
  a BACKPORT occurred; otherwise `none`.
</bedrock-repository>
