# Additive 2.1.0 observation

Observed 2026-10-07 at source head
`5c8ee3f361b626d20c5cb1ca4d544810103f4535` of
https://github.com/cleverunicornz/yeetz-bedrock-protocol/pull/43, judged by
`contract/release-2.1.md`.

## Before the implementation

The new worked examples `18-plan-holds-a-gap`, `19-gap-member-still-waited-upon`
and `20-applies-to-a-version` were added first; `contract/check.py` refused them
(15 disagreements: protocol `2.1.0` not admitted, Gap members and `applies_to`
unknown). The projector, AGENTS.md check and release build tests failed on the
missing scripts; the retraction tests failed on the missing function.

## At the head

- Protocol qualification, https://github.com/cleverunicornz/yeetz-bedrock-protocol/actions/runs/37655742377:
  success. Untouched 2.0 baseline semantics, source semantics (`OK: prose,
  contract, schema, examples, verb skills and role table agree`), 57 unit tests
  OK, actionlint 1.7.12 with shellcheck 0.11.0 clean, this repository's
  `situation/` projected twice with identical bytes (commit read
  `cc1597ba0e1f8d3988b3fbbb38d0c21dba594dab`), manifest regeneration byte-equal,
  compiled example byte-equal; published pair: the v2.0.0 compiler's refusal
  reproduced and the 2.1.0 candidate compiled in all three modes.
- Native protocol replay, https://github.com/cleverunicornz/yeetz-bedrock-protocol/actions/runs/37655742224:
  success. The pinned receiver's vendored contract equals this contract with
  exactly the 2.1 additions retracted.
- `tests/test_build_release.py` rebuilt the published v2.0.1 `SHA256SUMS`
  (archive `e5b2a061…befea91`, manifest `6b921f05…f1b26`) byte for byte.
- A deliberate unquoted expansion in a scratch workflow was reported as SC2086
  by the same actionlint and shellcheck pair, so the lint step runs shellcheck.

## Not observed

No receiver implementing the 2.1 additions, no caller's run of either reusable
workflow against a published v2.1.0 release, and no migrated scope.
