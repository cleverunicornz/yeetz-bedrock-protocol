"""Reject prose sentences copied from skills into compiled agent instructions."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def sentences(text: str) -> set[str]:
    # Syntax is discarded, prose is retained, including front-matter triggers.
    front = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    descriptions = []
    if front:
        lines = front.group(1).splitlines()
        for index, line in enumerate(lines):
            if line.startswith("description:"):
                value = line.split(":", 1)[1].strip()
                if value in ("|", "|-", "|+", ">", ">-", ">+"):
                    value = " ".join(child.strip() for child in lines[index + 1:] if child.startswith((" ", "\t")))
                elif len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                descriptions.append(value)
        text = text[front.end():]
    text = re.sub(r"^```.*?^```[^\n]*", "", text, flags=re.M | re.S)
    text = re.sub(r"^~~~.*?^~~~[^\n]*", "", text, flags=re.M | re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_`]+", "", text)
    # A list item, heading or blank line starts a fresh prose block; soft
    # line wrapping inside one block does not change its sentence identity.
    blocks = descriptions
    pending = []
    for line in text.splitlines():
        boundary = not line.strip() or bool(re.match(r"\s*(?:#{1,6}\s|[-+]\s|\d+[.)]\s|\|)", line))
        if boundary and pending:
            blocks.append(" ".join(pending))
            pending = []
        if re.match(r"\s*#{1,6}\s", line):
            continue
        if line.strip().startswith("|"):
            for cell in re.split(r"(?<!\\)\|", line.strip().strip("|")):
                cell = cell.strip()
                if cell and not re.fullmatch(r":?-+:?", cell):
                    blocks.append(cell)
            continue
        line = re.sub(r"^\s*(?:#{1,6}\s+|[-+]\s+|\d+[.)]\s+|>\s*)", "", line).strip()
        if line and not line.startswith("|") and line != "---":
            pending.append(line)
    if pending:
        blocks.append(" ".join(pending))
    out = set()
    for block in blocks:
        for part in re.split(r"(?<=[.!?])\s+", block):
            normal = re.sub(r"\s+", " ", part).strip().casefold().rstrip(".!?")
            if normal:
                out.add(normal)
    return out


def duplicates(agents: str, skills: list[Path]) -> list[str]:
    source = sentences(agents)
    problems = []
    for path in sorted(set(skills)):
        for sentence in sorted(source & sentences(path.read_text())):
            problems.append(f"duplicated sentence in AGENTS and {path}: {sentence}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=Path, required=True)
    parser.add_argument("--skills", type=Path, nargs="+", required=True)
    args = parser.parse_args()
    files = []
    for path in args.skills:
        if not path.exists():
            parser.error(f"missing skill input: {path}")
        files.extend(path.rglob("SKILL.md") if path.is_dir() else [path])
    if not files:
        parser.error("no skills supplied")
    problems = duplicates(args.agents.read_text(), files)
    for problem in problems:
        print(problem, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
