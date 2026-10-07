---
name: regroup
verb: regroup
description: Read before `regroup` through the task graph structural interface.
---

# regroup

Change a Plan membership or its optional waits-on links; members are Candidates, Promises and Gaps.

The Plan must already exist. Removing a member still named by a waits-on link is refused; order is optional.

## Procedure

Read `contract/tool-interface.md` and its exact source pins in
`contract/tool-interface.json`. Resolve the earlier successful responses in
`contract/tool-examples/calls.json` before sending this single-tool argument.

```json
{
  "op": "act",
  "verb": "regroup",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "plan": "${group.made}",
    "add_members": [
      "${formulate.made}"
    ]
  },
  "request_id": "${run}:regroup"
}
```

Keep the returned act identity, sequence and any made record identity.
Verify projection catch-up through watermark/head, then query the made or
changed record; scope links use binds/relations. Uncertain writes retain the
identical body and original request key. Role/principal are receiver stamps,
not arguments. The fixed schema defines semantic refusals; the client emits
a sanitized error rather than the native refusal body.
