---
name: group
verb: group
description: Read before `group` through the task graph structural interface.
---

# group

Collect existing Candidates, Promises and Gaps in a Plan.

Only returned Candidate, Promise and Gap IDs are members. A Plan makes no assertion, assigns nothing and has no completion condition.
The work on a Gap member is formulate and refine; its outcome is decide, and it is complete when decided.

## Procedure

Read `contract/tool-interface.md` and its exact source pins in
`contract/tool-interface.json`. Resolve the earlier successful responses in
`contract/tool-examples/calls.json` before sending this single-tool argument.

```json
{
  "op": "act",
  "verb": "group",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "plan": {
      "title": "Fixture qualification",
      "members": [
        "${mint.made}"
      ],
      "waits_on": []
    }
  },
  "request_id": "${run}:group"
}
```

Keep the returned act identity, sequence and any made record identity.
Verify projection catch-up through watermark/head, then query the made or
changed record; scope links use binds/relations. Uncertain writes retain the
identical body and original request key. Role/principal are receiver stamps,
not arguments. The fixed schema defines semantic refusals; the client emits
a sanitized error rather than the native refusal body.
