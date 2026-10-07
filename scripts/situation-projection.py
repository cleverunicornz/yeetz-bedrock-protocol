#!/usr/bin/env python3
"""Project a repository's situation records into SITUATION.md, deterministically.

Bedrock 2.1, contract section 8: records live in the situation domain and a
projection is never a source. Until the domain holds a repository's records, the
source is the repository's own `situation/` files, authored in the shape of
`templates/records/`. The format is fixed so that source can switch without the
output changing shape: a header naming the scope, the source, the commit read
and its date, then one section per record class in id order, repository level
only. Witnesses, `context.md` and every path with a directory named `security`
are never read, and no symbolic link is followed.

The commit read is the last commit that changed `situation/` (outside
`security` directories), and the date is that commit's UTC date, so committing
the projection does not change it: same records, same bytes.
"""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

DISCLAIMER = "projection; not a source of truth"
# (heading, directory, id prefix, metadata headings, statement heading); None is the plan's preamble.
CLASSES = (
    ("Invariants", "invariants", "I", ("Priority", "Applies to"), "Invariant"),
    ("Promises", "promises", "P", ("State", "Applies to"), "Promise"),
    ("Oracles", "oracles", "O", ("State", "Judges"), None),
    ("Decisions", "decisions", "D", ("State", "Status", "Date"), "Decision"),
    ("Gaps", "gaps", "G", ("State",), "Gap"),
    ("Candidates", "candidates", "C", ("State",), "Candidate"),
    ("Plans", "plans", "PLAN", ("State",), ""),
)
DEFAULTS = {"Applies to": "all environments"}
FENCE = re.compile(r"^\s*(```|~~~)")


def excluded(path, base):
    """Symlinks, nested AGENTS.md and anything that is or resolves under a `security` directory or outside base."""
    real, real_base = path.resolve(), base.resolve()
    if path.is_symlink() or path.name == "AGENTS.md" or not real.is_relative_to(real_base):
        return True
    parts = (*path.relative_to(base).parts, *real.relative_to(real_base).parts)
    return any(part.casefold() == "security" for part in parts)


def files(directory):
    if not directory.is_dir():
        return []
    return [p for p in directory.rglob("*") if p.is_file() and not excluded(p, directory)]


def parse(text):
    """Return (title, preamble, {section: body}) with sections split outside code fences."""
    title, preamble, sections, current, fenced = "", [], {}, None, False
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced and not title and line.startswith("# "):
            title = line[2:].strip()
            continue
        elif not fenced and line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
            continue
        (sections[current] if current is not None else preamble).append(line)
    return title, block(preamble), {name: block(lines) for name, lines in sections.items()}


def block(lines):
    text = "\n".join(lines).strip("\n")
    return "\n".join(line.rstrip() for line in text.split("\n")).strip()


def demote(text):
    out, fenced = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced and re.match(r"#{1,5} ", line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def first_line(text):
    return next((line.strip() for line in text.split("\n") if line.strip()), "")


def link(path):
    return f"[{path}]({path})"


def records(situation, directory, prefix):
    pattern = re.compile(rf"{prefix}-(\d+)(?:-.*)?\.md")
    found = []
    for path in files(situation / directory):
        match = pattern.fullmatch(path.name)
        if match:
            relative = path.relative_to(situation).as_posix()
            found.append((int(match.group(1)), relative, f"{prefix}-{match.group(1)}", path))
    return sorted(found)


def render_record(base, relative, record_id, path, metadata, statement):
    title, preamble, sections = parse(path.read_bytes().decode("utf-8"))
    name = title.split(" — ", 1)[1].strip() if " — " in title else (title or record_id)
    facts = []
    for heading in metadata:
        value = first_line(sections.get(heading, "")) or DEFAULTS.get(heading, "")
        if heading == "State" and not value and record_id.startswith("PLAN-") and relative.count("/") == 2:
            value = Path(relative).parent.name  # plans/<state>/PLAN-...
        if value:
            facts.append(f"{heading}: {value}")
    facts.append(link(f"{base}/{relative}"))
    body = preamble if statement == "" else sections.get(statement, "") if statement else ""
    parts = [f"### {record_id} — {name}", " · ".join(facts)]
    if body:
        parts.append(demote(body))
    return "\n\n".join(parts)


def project(situation, scope, commit, date, base="situation"):
    situation = Path(situation)
    if not situation.is_dir():
        raise ValueError(f"no situation directory: {situation}")
    out = [
        f"# SITUATION — {scope}",
        DISCLAIMER,
        "\n".join([f"- Scope: `{scope}`", f"- Source: `{base}/` files", f"- Commit read: `{commit}`",
                   f"- Date: {date}"]),
        "Repository-level records by class, in id order; each links its file. Generated on every pull request; "
        "edit the records, never this file.",
    ]
    for heading, directory, prefix, metadata, statement in CLASSES:
        out.append(f"## {heading}")
        found = records(situation, directory, prefix)
        out.extend(render_record(base, rel, record_id, p, metadata, statement) for _, rel, record_id, p in found)
        if not found:
            out.append("None.")
    out.append("## References")
    references = sorted(p.relative_to(situation).as_posix() for p in files(situation / "references"))
    out.append("\n".join("- " + link(f"{base}/{r}") for r in references) if references else "None.")
    return "\n\n".join(out) + "\n"


def source(root, situation):
    """The last commit that changed the situation records outside security directories, and its UTC date."""
    env = {**os.environ, "TZ": "UTC"}
    result = subprocess.run(
        ["git", "-C", str(root), "log", "-1", "--format=%H %cd", "--date=format-local:%Y-%m-%d", "--",
         situation, f":(exclude,glob){situation}/**/security/**"],
        check=True, capture_output=True, text=True, env=env).stdout.split()
    if len(result) != 2:
        raise ValueError(f"no commit has changed {situation}/")
    return result[0], result[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", type=Path, default=Path("."), help="repository root (default: .)")
    parser.add_argument("--scope", required=True, help="the repository scope, owner/name")
    parser.add_argument("--situation", default="situation", help="records directory under the root")
    parser.add_argument("--commit", help="commit read (default: last commit that changed the records)")
    parser.add_argument("--date", help="date of the commit read, YYYY-MM-DD (default: its UTC committer date)")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--output", help="write the projection to this path under the root")
    action.add_argument("--check", action="store_true", help="fail unless SITUATION.md under the root is current")
    args = parser.parse_args()
    try:
        commit, date = (args.commit, args.date) if args.commit and args.date else source(args.root, args.situation)
        text = project(args.root / args.situation, args.scope, commit, date, args.situation.strip("/"))
    except (OSError, ValueError, UnicodeDecodeError, subprocess.CalledProcessError) as error:
        sys.exit(f"situation projection failed: {error}")
    if args.check:
        target = args.root / "SITUATION.md"
        if not target.is_file() or target.read_bytes() != text.encode():
            sys.exit("SITUATION.md is not the current projection of the situation records")
        print("SITUATION.md is current")
    elif args.output:
        (args.root / args.output).write_bytes(text.encode())
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
