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
        "description": "Bedrock 2.0 fixed contract, executable procedures and short instruction compiler; organisation is a separate paired package.",
        "root_protocol": entry("templates/root-protocol.md"),
        "repository_block": entry("templates/repository-block.md"),
        "contract": [entry(p) for p in ("contract/bedrock-v2.md", "contract/bedrock-v2.yaml", "contract/bedrock-v2.schema.json", "contract/tool-interface.md", "contract/tool-interface.json", "contract/stage0.md", "contract/stage0-witness.md", "contract/patch-compatibility.md", "contract/gaps/SO-000117-skill-verb-declaration.md")],
        "verb_skills": many("contract/skills/*/SKILL.md"),
        "structural_skills": many("contract/structural-skills/*/SKILL.md"),
        "tool_examples": many("contract/tool-examples/*.json") + many("contract/tool-examples/*.py"),
        "migrations": [entry("migrations/2.0.0-draft-to-2.0.0.md"), entry("migrations/2.0.0-to-2.0.1.md")],
        "roles": entry("contract/roles.md"),
        "compiler": many("compiler/*.py") + many("compiler/*.md"),
        "distribution": {"protocol_root": "bedrock", "verb_skill_source": "contract/skills", "structural_skill_source": "contract/structural-skills", "installed_skill_root": "bedrock/skills", "organisation_root": "org"},
    }
    (ROOT / "manifest.json").write_text(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    main()
