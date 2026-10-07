#!/usr/bin/env python3
"""Project a repository's situation records into SITUATION.md, deterministically.

Bedrock 2.1, contract section 8: records live in the situation domain and a
projection is never a source. Until the domain holds a repository's records, the
source is the repository's own `situation/` files, authored in the shape of
`templates/records/`. The format is fixed so that source can switch without the
output changing shape: a header naming the scope, the source, the commit read
and its date, then one section per record class in id order, repository level
only. Each record keeps every heading its template defines: one-line facts on
the record's line, the other headings as sections. References are pointers.
Witnesses, `context.md` and every path with a directory named `security` are
never read. A symbolic link anywhere in the source - the records directory, an
ancestor of it under the root, a class directory, a directory or a file - is
refused, never followed.

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
# (heading, directory, id prefix, facts, sections). Facts and sections are exactly the headings of
# templates/records/<class>.md, plus the legacy one-line facts that earlier records carry.
CLASSES = (
    ("Invariants", "invariants", "I", ("State", "Priority", "Applies to"), ("Invariant", "Basis")),
    ("Promises", "promises", "P", ("State", "Applies to"),
     ("Promise", "Scope", "Residual", "Basis", "From candidate", "Addresses")),
    ("Oracles", "oracles", "O", ("State", "Judges", "Arrangement"), ("Inputs", "Holds when", "Fails when", "Executable")),
    ("Decisions", "decisions", "D", ("State", "Status", "Date"),
     ("Decision", "Why", "Rejected", "Revisit when", "Considered", "Outcomes")),
    ("Gaps", "gaps", "G", ("State",), ("Gap", "Impact", "About", "Arose in")),
    ("Candidates", "candidates", "C", ("State",), ("Candidate", "Responds to")),
    ("Plans", "plans", "PLAN", ("State",), ("Members", "Waits on")),
)
LEGACY_FACTS = ("Status", "Date")
DEFAULTS = {"Applies to": "all environments"}
FENCE = re.compile(r"^\s*(```|~~~)")


def refuse_link(path):
    if path.is_symlink():
        raise ValueError(f"symbolic link refused: {path}")


def files(directory):
    """Every record file under directory, in a fixed order. A `security` directory is never entered and its
    contents never read; any other symbolic link is refused."""
    refuse_link(directory)
    if not directory.is_dir():
        return []
    found = []
    for entry in sorted(directory.iterdir()):
        if entry.name.casefold() == "security":
            continue
        refuse_link(entry)
        if entry.is_dir():
            found.extend(files(entry))
        elif entry.is_file() and entry.name != "AGENTS.md":
            found.append(entry)
    return found


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


def demote(text, levels=2):
    """Move a file's headings below the projection's record sections (####), outside code fences."""
    out, fenced = [], False
    for line in text.split("\n"):
        heading = None if fenced else re.match(r"(#{1,6}) ", line)
        if FENCE.match(line):
            fenced = not fenced
        elif heading:
            line = "#" * min(6, len(heading.group(1)) + levels) + line[len(heading.group(1)):]
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


def render_record(base, relative, record_id, path, facts, headings):
    title, preamble, sections = parse(path.read_bytes().decode("utf-8"))
    name = title.split(" — ", 1)[1].strip() if " — " in title else (title or record_id)
    line = []
    for heading in facts:
        value = first_line(sections.get(heading, "")) or DEFAULTS.get(heading, "")
        if heading == "State" and not value and record_id.startswith("PLAN-") and relative.count("/") == 2:
            value = Path(relative).parent.name  # plans/<state>/PLAN-...
        if value:
            line.append(f"{heading}: {value}")
    line.append(link(f"{base}/{relative}"))
    parts = [f"### {record_id} — {name}", " · ".join(line)]
    if preamble and record_id.startswith("PLAN-"):
        parts.append(demote(preamble))
    for heading in headings:
        if sections.get(heading):
            parts.extend([f"#### {heading}", demote(sections[heading])])
    return "\n\n".join(parts)


def natural(path):
    """Order paths by their numbers as numbers, so R-2 comes before R-10."""
    return [int(part) if index % 2 else part for index, part in enumerate(re.split(r"(\d+)", path))]


def project(situation, scope, commit, date, base="situation", root=None):
    situation = Path(situation)
    if root is not None:
        ancestor = Path(root)
        for part in situation.relative_to(root).parts:
            ancestor = ancestor / part
            refuse_link(ancestor)
    refuse_link(situation)
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
    for heading, directory, prefix, facts, sections in CLASSES:
        out.append(f"## {heading}")
        found = records(situation, directory, prefix)
        out.extend(render_record(base, rel, record_id, p, facts, sections) for _, rel, record_id, p in found)
        if not found:
            out.append("None.")
    out.append("## References")
    references = sorted((p.relative_to(situation).as_posix() for p in files(situation / "references")),
                        key=lambda r: (natural(r), r))
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
        text = project(args.root / args.situation, args.scope, commit, date, args.situation.strip("/"), root=args.root)
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
