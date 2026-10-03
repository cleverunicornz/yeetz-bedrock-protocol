---
name: relate
verb: relate
description: Read before `relate` through the task graph structural interface.
---

# relate

Record optional scope belonging or record-about links.

Scope endpoints use scope:<level>/<scope>. belongs_to links are explicit; an absent link must not be invented from a URI prefix.

## Procedure

Read `contract/tool-interface.md` and its exact source pins in
`contract/tool-interface.json`. Resolve the earlier successful responses in
`contract/tool-examples/calls.json` before sending this single-tool argument.

```json
{
  "op": "act",
  "verb": "relate",
  "level": "repository",
  "scope": "${scope}",
  "payload": {
    "from": "scope:repository/${scope}",
    "to": "scope:organisation/fixture-org",
    "relation": "belongs_to"
  },
  "request_id": "${run}:relate"
}
```

Keep the returned act identity, sequence and any made record identity.
Verify projection catch-up through watermark/head, then query the made or
changed record; scope links use binds/relations. Uncertain writes retain the
identical body and original request key. Role/principal are receiver stamps,
not arguments. The fixed schema defines semantic refusals; the client emits
a sanitized error rather than the native refusal body.
