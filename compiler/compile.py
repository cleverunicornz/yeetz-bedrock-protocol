"""Compile verified Bedrock, organisation and repository instruction inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

from check_sentences import duplicates

# migrations/2.0.0-to-2.0.1.md fixed the stable line in source;
# migrations/v2.0.1-to-v2.1.0.md adds the additive 2.1 line beside it.
STABLE_PACKAGE_VERSION = re.compile(r"2\.[01]\.(?:0|[1-9][0-9]*)", re.ASCII)


def entries(value):
    if isinstance(value, dict):
        if "path" in value:
            yield value
        else:
            for child in value.values():
                yield from entries(child)
    elif isinstance(value, list):
        for child in value:
            yield from entries(child)


def verify(root: Path) -> tuple[dict, dict[str, Path]]:
    root = root.resolve()
    manifest = json.loads((root / "manifest.json").read_text())
    version = manifest.get("version")
    if not isinstance(version, str) or STABLE_PACKAGE_VERSION.fullmatch(version) is None:
        raise ValueError(f"{root}: requires a stable 2.0.x or 2.1.x package version")
    packaged_version = (root / "VERSION").read_text().removesuffix("\n")
    if packaged_version != version:
        raise ValueError(f"{root}: manifest version does not match packaged VERSION")
    files = {}
    for entry in entries(manifest):
        name = entry["path"]
        if not isinstance(name, str) or Path(name).is_absolute() or ".." in Path(name).parts:
            raise ValueError("manifest path must stay inside its package")
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f"missing package file: {name}")
        if name in files:
            raise ValueError(f"duplicate manifest path: {name}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError(f"package digest mismatch: {name}")
        files[name] = path
    return manifest, files


def require(files, name):
    if name not in files:
        raise ValueError(f"file is not manifest-published: {name}")
    return files[name].read_text()


def repository_part(template: str, path: Path | None) -> str:
    """The repository block is one fixed text. Repository input, when given, is
    still validated so existing callers fail closed on record copies, but none
    of it is rendered: identity and ownership live in the graph."""
    if re.search(r"\{\{.*?\}\}", template):
        raise ValueError("the repository block template must be the fixed text")
    if path is None:
        return template
    data = json.loads(path.read_text())
    allowed = {"identity", "ownership", "scope", "bootstrap"}
    if not isinstance(data, dict):
        raise ValueError("repository input must be an object")
    if set(data) - allowed:
        raise ValueError(f"record copies or unsupported repository fields: {sorted(set(data) - allowed)}")
    if not {"identity", "ownership", "scope"} <= set(data):
        raise ValueError("repository identity, ownership and scope are required")
    data.setdefault("bootstrap", "Runtime supplies the tools and scope access.")
    if data["ownership"] not in ("OWNED", "UPSTREAM_FORK"):
        raise ValueError("ownership must be OWNED or UPSTREAM_FORK")
    for key, value in data.items():
        if not isinstance(value, str) or not value.strip() or len(value) > 256 or any(c in value for c in "\n\r<>{}"):
            raise ValueError(f"repository {key} must be one short plain line")
    return template


def compile_text(protocol_root: Path, org_root: Path, repository: Path | None, part: str) -> str:
    pm, protocol = verify(protocol_root)
    om, org = verify(org_root)
    root = require(protocol, pm["root_protocol"]["path"])
    organization = require(org, om["organization"]["path"])
    repo = repository_part(require(protocol, pm["repository_block"]["path"]), repository)
    if organization.count("<bedrock-organization>") != 1 or organization.count("</bedrock-organization>") != 1:
        raise ValueError("organisation input must have exactly one operating-layer block")
    if len(organization.splitlines()) > 12:
        raise ValueError("organisation input exceeds a few pointer lines")
    full = "\n".join(piece.strip() for piece in (root, organization, repo)) + "\n"
    if len(full.splitlines()) > 85:
        raise ValueError("compiled instruction file exceeds the short axiom layout")
    skill_paths = [p for p in [*protocol.values(), *org.values()] if p.name == "SKILL.md"]
    if not skill_paths:
        raise ValueError("paired manifests supply no skills")
    problems = duplicates(full, skill_paths)
    if problems:
        raise ValueError("\n".join(problems))
    if part == "user":
        return root.strip() + "\n\n" + organization.strip() + "\n"
    if part == "repository":
        return repo.strip() + "\n"
    return full


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol-root", type=Path, required=True)
    parser.add_argument("--org-root", type=Path, required=True)
    parser.add_argument("--repository", type=Path, help="optional; validated for compatibility, never rendered")
    parser.add_argument("--part", choices=("full", "user", "repository"), default="full")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = compile_text(args.protocol_root, args.org_root, args.repository, args.part)
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    if args.output:
        args.output.write_text(result)
    else:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
