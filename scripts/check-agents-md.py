#!/usr/bin/env python3
"""Check that a root AGENTS.md repository block is the published fixed text, byte for byte.

Bedrock 2.1, contract section 8: the repository block is one fixed text,
`templates/repository-block.md`. Only that block is compared; the user-level
protocol block is delivered by the runtime and is not checked here.
"""
import argparse
import difflib
from pathlib import Path
import re
import sys

BLOCK = re.compile(rb"^<bedrock-repository>\r?\n.*?^</bedrock-repository>(?:\r?\n|\Z)", re.M | re.S)


def check(agents: bytes, template: bytes) -> str | None:
    """None when the block matches; otherwise the reason."""
    blocks = BLOCK.findall(agents)
    if len(blocks) != 1:
        return f"AGENTS.md must hold exactly one repository block; found {len(blocks)}"
    if blocks[0] != template:
        diff = difflib.unified_diff(template.decode("utf-8", "replace").splitlines(keepends=True),
                                    blocks[0].decode("utf-8", "replace").splitlines(keepends=True),
                                    "fixed text", "AGENTS.md")
        return "".join(diff) + "\nthe AGENTS.md repository block must equal the fixed text byte for byte"
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--agents", type=Path, required=True, help="the repository's root AGENTS.md")
    parser.add_argument("--template", type=Path, required=True, help="the release's templates/repository-block.md")
    args = parser.parse_args()
    try:
        problem = check(args.agents.read_bytes(), args.template.read_bytes())
    except OSError as error:
        sys.exit(f"AGENTS.md check failed: {error}")
    if problem:
        sys.exit(problem)
    print("the AGENTS.md repository block is the fixed text")


if __name__ == "__main__":
    main()
