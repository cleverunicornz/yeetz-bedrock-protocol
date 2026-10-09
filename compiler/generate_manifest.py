"""Generate the protocol publication manifest deterministically."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def entry(path):
    path = Path(path)
    return {"path": path.as_posix(), "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}


def many(pattern):
    return [entry(p.relative_to(ROOT)) for p in sorted(ROOT.glob(pattern)) if p.is_file()]


def main():
    data = {
        "version": (ROOT / "VERSION").read_text().strip(),
        "description": "Bedrock 2.1 fixed contract, STE100 communication, executable procedures, record templates, short instruction compiler and repository checks; organisation is a separate paired package.",
        "root_protocol": entry("templates/root-protocol.md"),
        "repository_block": entry("templates/repository-block.md"),
        "record_templates": many("templates/records/*.md"),
        "contract": [entry(p) for p in ("contract/bedrock-v2.md", "contract/bedrock-v2.yaml", "contract/bedrock-v2.schema.json", "contract/tool-interface.md", "contract/tool-interface.json", "contract/stage0.md", "contract/stage0-witness.md", "contract/patch-compatibility.md", "contract/patch-compatibility-witness.md", "contract/release-2.1.md", "contract/release-2.1-witness.md", "contract/gaps/SO-000117-skill-verb-declaration.md")],
        "verb_skills": many("contract/skills/*/SKILL.md"),
        "structural_skills": many("contract/structural-skills/*/SKILL.md"),
        "tool_examples": many("contract/tool-examples/*.json") + many("contract/tool-examples/*.py"),
        "migrations": [entry("migrations/2.0.0-draft-to-2.0.0.md"), entry("migrations/2.0.0-to-2.0.1.md"), entry("migrations/v2.0.1-to-v2.1.0.md")],
        "roles": entry("contract/roles.md"),
        "compiler": many("compiler/*.py") + many("compiler/*.md"),
        "repository_checks": [entry(p) for p in (".github/workflows/check-agents-md.yml", ".github/workflows/situation-projection.yml", "scripts/check-agents-md.py", "scripts/situation-projection.py")],
        "distribution": {"protocol_root": "bedrock", "verb_skill_source": "contract/skills", "structural_skill_source": "contract/structural-skills", "installed_skill_root": "bedrock/skills", "organisation_root": "org"},
    }
    data["contract"] += many("contract/communication/*.md") + many("contract/communication/*/SKILL.md")
    data["migrations"].append(entry("migrations/v2.1.0-to-v2.1.1.md"))
    (ROOT / "manifest.json").write_text(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    main()
