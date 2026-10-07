---
name: amend
verb: amend
description: Read before `amend` through the task graph structural interface.
---

# amend

Correct the making author’s record inside the original edit window.

The original making act defines the author and 600-second window. Amendments do not extend it. After expiry use supersede or revoke; never mutate history.

An amendment keeps an Invariant's or Promise's `applies_to` the making act's scope; naming another version scope is refused (`applies_to_mismatch`).

## Procedure

Read `contract/tool-interface.md` and its exact source pins in
`contract/tool-interface.json`. Resolve the earlier successful responses in
`contract/tool-examples/calls.json` before sending this single-tool argument.

```json
{
  "op": "act",
  "verb": "amend",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "target_act": "${declare.act_id}",
    "changes": {
      "gap": {
        "title": "Observed fixture coverage gap"
      }
    }
  },
  "request_id": "${run}:amend"
}
```

Keep the returned act identity, sequence and any made record identity.
Verify projection catch-up through watermark/head, then query the made or
changed record; scope links use binds/relations. Uncertain writes retain the
identical body and original request key. Role/principal are receiver stamps,
not arguments. The fixed schema defines semantic refusals; the client emits
a sanitized error rather than the native refusal body.
