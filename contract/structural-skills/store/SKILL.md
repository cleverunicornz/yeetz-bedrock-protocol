---
name: store
verb: store
description: Read before `store` through the task graph structural interface.
---

# store

Retain supporting depth with its source coordinate.

The Reference is returned by the service; repository-file pointers pin a commit, while stored artifacts carry a version and digest. Agents do not choose object-store keys.

## Procedure

Read `contract/tool-interface.md` and its exact source pins in
`contract/tool-interface.json`. Resolve the earlier successful responses in
`contract/tool-examples/calls.json` before sending this single-tool argument.

```json
{
  "op": "reference.put",
  "level": "repository",
  "scope": "${scope}",
  "reference": {
    "title": "Accepted fixture specification",
    "kind": "repository_file",
    "repository": "cleverunicornz/yeetz-bedrock-protocol",
    "commit": "${fixture_commit}",
    "path": "contract/tool-examples/probe.py"
  },
  "request_id": "${run}:instruction"
}
```

Keep the returned act identity, sequence and any made record identity.
Verify projection catch-up through watermark/head, then query the made or
changed record; scope links use binds/relations. Uncertain writes retain the
identical body and original request key. Role/principal are receiver stamps,
not arguments. The fixed schema defines semantic refusals; the client emits
a sanitized error rather than the native refusal body.
