# Compilation and distribution contract

The compiler independently admits stable protocol and organisation `2.0.x`
packages under `migrations/2.0.0-to-2.0.1.md`, and `2.1.x` beside them under
`migrations/v2.0.1-to-v2.1.0.md`. Each version is exactly
`2.(0|1).(0|[1-9][0-9]*)`, with no prerelease/build suffix or leading zeros,
and must equal that package's own `VERSION`. Different patches and the two
minor lines may pair. Other major/minor lines and malformed values fail closed. Consumers still
verify exact immutable source/archive/manifest pins; version compatibility
does not authenticate packages or bypass path/digest checks.
The organisation manifest keeps `version`, `description`,
`organization`, `skills`, `organization_situation`; its organisation entry
names `templates/organization.md`. That input is at most twelve lines,
wrapped by `<bedrock-organization>`, and contains scope/skill pointers only.
No image, fleet migration or full organisation rollout is needed to compile
this finite input. Qualified release pins are paired by the downstream image.

Every manifest entry is verified before compilation. The repository block is
one fixed text, `templates/repository-block.md`, rendered byte for byte;
nothing is filled in. Identity and ownership (with a fork's upstream
coordinate) live in the repository scope's context record in the graph.
`--repository` is optional and kept for existing callers: when given, its JSON
(`identity`, `ownership` `OWNED` or `UPSTREAM_FORK`, `scope`, optional
`bootstrap`, each one plain line of at most 256 characters) is still validated
and record copies or extra fields are refused, but none of it is rendered.

```sh
python3 compiler/compile.py --protocol-root . --org-root ../org-package --output AGENTS.md
python3 compiler/compile.py --protocol-root . --org-root ../org-package --part user --output user-AGENTS.md
python3 compiler/compile.py --protocol-root . --org-root ../org-package --part repository --output repository-AGENTS.md
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
are historical; no 2.x manifest publishes them.

## Repository checks

A repository under the protocol calls two reusable workflows, pinned to the
protocol version it adopts (`@v<version>` and `version: <version>`):
`.github/workflows/check-agents-md.yml` runs `scripts/check-agents-md.py`
against `templates/repository-block.md`, and
`.github/workflows/situation-projection.yml` runs
`scripts/situation-projection.py` and commits `SITUATION.md` to a public
repository's pull request head. Both fetch `bedrock-<version>.tar.gz`,
check it against the release's `SHA256SUMS` and every file against the
manifest before running anything from it. `scripts/build-release.py` builds
those three assets deterministically from a source tree.

Regenerate publication digests with `python3 compiler/generate_manifest.py`.
This does not release, install or activate anything. Scope migration and the
six canary gates remain downstream, followed by the operator's Stage2/3 hold.

## Repair an existing installation that omitted VERSION

The published protocol and organisation 2.0.0 archives include VERSION beside
their manifest. Older installers could validate the source VERSION and omit
it when copying the package. Before using this compiler, the consumer's
installer must verify its SAME original pinned archive/source and manifest,
then copy that package's exact VERSION bytes into its existing installed root.
Keep the existing package files, manifest and immutable pin unchanged; rerun
their path/digest checks and compile again. Organisation PR17 owns this
installer repair; protocol verification remains strict.

Never reconstruct VERSION from a manifest string or a guessed version, copy
it from another patch, relabel metadata or retag a release. If the original
verified source lacks VERSION, the installation remains unsupported until
its producer supplies a qualified package. Missing or mismatched VERSION
continues to fail closed.
