# Bedrock protocol source

This public repository owns the fixed Bedrock contract, executable protocol
procedures, short instruction templates and their deterministic compiler.
It is exempt from consuming itself: situation/ and organization/ contain
historical distribution bytes, not this repository's knowledge records.
The release's protocol Decision is recorded in its migration note.

Read contract/stage0.md, migrations/2.0.0-draft-to-2.0.0.md and
migrations/v2.0.1-to-v2.1.0.md before changing this deliverable. Contract nouns, verbs, states, outcomes and role guidance
remain fixed in contract/bedrock-v2.yaml and bedrock-v2.schema.json.
Protocol templates are neutral; organisation operating policy comes from
the separate paired organisation package. Never copy records or skill
sentences into compiled instructions; there are no noun skills.

Executable procedure mechanics live in contract/skills/ and
contract/structural-skills/, pinned by contract/tool-interface.json.
Keep semantic checks while validating the actual tool envelope. Caller IDs,
role and principal are not receiver stamps. assure is a transition queried
through assured_by, never a submitted act. Source replay uses isolated test
identity and cannot prove production trust or runtime board integration.

Preserve collected source work and author history under
handoff/stage0-unvalidated/. Correct by forward commits; never rewrite it.
Published edits require VERSION, manifest digests and a migration note.
For authoring, read contract/communication/ste100-writing.md; assigned
communication-convention reviews use contract/communication/ste100-review/SKILL.md.
Regenerate manifest.json with compiler/generate_manifest.py.
Run qualification through .github/workflows/qualify.yml or the workbench;
never treat a not-run check as qualification. A complete draft, independent
Codex validation, physical probes, green exact-head CI and adjudicated Base
review precede READY/merge. Merge authority comes from the active assignment.

Stage0 source qualification precedes downstream canary qualification.
A source release never activates runtime defaults. Stage0/1 can proceed
when qualified; after all six canary gates STOP/report before Stage2/3.
Private references use declared owner/repo@commit#path coordinates.
This repository carries no credentials, transcripts or security-vault detail.
