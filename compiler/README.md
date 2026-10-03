# Compilation and distribution contract

The compiler independently admits stable protocol and organisation `2.0.x`
packages under `migrations/2.0.0-to-2.0.1.md`. Each version is exactly
`2.0.(0|[1-9][0-9]*)`, with no prerelease/build suffix or leading zeros,
and must equal that package's own `VERSION`. Different patches may pair.
Other major/minor lines and malformed values fail closed. Consumers still
verify exact immutable source/archive/manifest pins; version compatibility
does not authenticate packages or bypass path/digest checks.
The organisation manifest keeps `version`, `description`,
`organization`, `skills`, `organization_situation`; its organisation entry
names `templates/organization.md`. That input is at most twelve lines,
wrapped by `<bedrock-organization>`, and contains scope/skill pointers only.
No image, fleet migration or full organisation rollout is needed to compile
this finite input. Qualified release pins are paired by the downstream image.

Every manifest entry is verified before compilation. Repository input is JSON
with `identity`, `ownership` (`OWNED` or `UPSTREAM_FORK`), `scope`, optional
`bootstrap`; each is one plain line of at most 256 characters. Records and
extra fields are refused. Bootstrap names only information needed to reach
the graph; it is not a place for policy, budget or knowledge record copies.

```sh
python3 compiler/compile.py --protocol-root . --org-root ../org-package --repository repository.json --output AGENTS.md
python3 compiler/compile.py --protocol-root . --org-root ../org-package --repository repository.json --part user --output user-AGENTS.md
python3 compiler/compile.py --protocol-root . --org-root ../org-package --repository repository.json --part repository --output repository-AGENTS.md
python3 compiler/check_sentences.py --agents AGENTS.md --skills contract/skills contract/structural-skills ../org-package/skills .agents/skills
```

The full rendering is for review and questioning. Runtime user instructions
install the `user` rendering; the repository root installs `repository`.
Do not install the full rendering at both levels. The compiler checks all
manifest-listed protocol and organisation skills even for split output.
Repository skills are supplied to the standalone duplication check in CI.
Missing paths fail; omit the repository skill argument when none exist.

The package root installs as `bedrock/`. Copy the exact `VERSION` and
`manifest.json` beside the installed files for both `bedrock/` and `org/`.
Preserve `contract/`, `compiler/`
and template paths there, including every `tool_examples` and `migrations`
entry. These hold the procedures' response-binding fixture and the authority
Decision; they are digest-verified publication dependencies. Copy manifest `verb_skills` from
`contract/skills/<verb>/SKILL.md` and `structural_skills` from
`contract/structural-skills/<operation>/SKILL.md` to
`bedrock/skills/<name>/SKILL.md`. There are thirteen verb procedures and five
structural procedures; no noun skill. Organisation skills install separately
under `org/skills/`. Namespace and old organisation bytes remaining in source
are historical; the 2.0.0 manifest does not publish them.

Regenerate publication digests with `python3 compiler/generate_manifest.py`.
This does not release, install or activate anything. Scope migration and the
six canary gates remain downstream, followed by the operator's Stage2/3 hold.
