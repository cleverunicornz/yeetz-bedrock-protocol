"""SITUATION.md is a deterministic projection of a repository's situation records (contract section 8)."""
import importlib.util
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/situation-projection.py"
spec = importlib.util.spec_from_file_location("situation_projection", SCRIPT)
projection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(projection)

COMMIT = "0123456789abcdef0123456789abcdef01234567"
RECORDS = {
    "AGENTS.md": "# Situation\n\nNamespace rules.\n",
    "context.md": "# Context\n\nNot projected.\n",
    "invariants/AGENTS.md": "# Invariants\n",
    "invariants/I-000010-later.md": "# I-000010 — Later rule\n\n## Priority\n\nstandard\n\n## Invariant\n\nThe later rule.\n",
    "invariants/I-000002-earlier.md": (
        "# I-000002 — Earlier rule\n\n## Priority\n\ncritical\n\n## Applies to\n\n`agent-runtime/2`\n\n"
        "## Invariant\n\nThe earlier rule,\nwrapped.\n\n## Basis\n\n- a decision\n"
    ),
    "promises/P-000001-thing.md": (
        "# P-000001 — A thing works\n\n## State\n\nimplemented\n\n## Promise\n\nThe thing works.\n\n"
        "## Oracle\n\n`situation/oracles/O-000001-thing.md`\n"
    ),
    "oracles/O-000001-thing.md": (
        "# O-000001 — Judge the thing\n\n## State\n\ndesigned\n\n## Judges\n\n"
        "`situation/promises/P-000001-thing.md`\n\n## Pass\n\n- it works\n"
    ),
    "decisions/D-000003-choose.md": (
        "# D-000003 — Choose\n\n## Status\n\naccepted\n\n## Date\n\n2026-10-07\n\n## Decision\n\n"
        "### Part one\n\n1. Do it.\n\n```text\n## not a section\n```\n\n## Why\n\nBecause.\n"
    ),
    "gaps/G-000004-missing.md": "# G-000004 — Something is missing\n\n## State\n\nopen\n\n## Gap\n\nIt is missing.\n",
    "gaps/security/G-000005-hidden.md": "# G-000005 — Hidden finding\n\n## State\n\nopen\n\n## Gap\n\nSECRET-GAP\n",
    "candidates/C-000006-maybe.md": "# C-000006 — Maybe this\n\n## State\n\nproposed\n\n## Candidate\n\nPerhaps.\n",
    "decisions/D-000011-templated.md": (
        "# D-000011 — Templated decision\n\n## State\n\ndecided\n\n## Decision\n\nUse the 2.1 template.\n\n"
        "## Why\n\nIt is the format.\n"
    ),
    "plans/PLAN-000012-gaps.md": (
        "# PLAN-000012 — Gap plan\n\n## State\n\ngrouped\n\n## Members\n\n- G-000004\n- C-000006\n"
    ),
    "plans/draft/PLAN-000007-later.md": "# PLAN-000007 — The plan\n\nGroups the work.\n\n## Promises\n\n- P-000001\n",
    "references/D-000003/notes.md": "# Notes\n\nREFERENCE-BODY\n",
    "references/security/leak.md": "SECRET-REFERENCE\n",
    "security/I-000099-hidden.md": "# I-000099 — SECRET-ROOT\n",
    "witnesses/P-000001/W-000008-run.md": "# W-000008 — A run\n\nWITNESS-BODY\n",
}


def write_tree(root, records, order=None):
    for name in order or records:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(records[name].encode())


def git(root, *args, env=None):
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True, env=env).stdout


class Projection(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.tmp = Path(directory.name)
        self.situation = self.tmp / "repo/situation"
        write_tree(self.situation, RECORDS)

    def render(self, situation=None):
        return projection.project(situation or self.situation, "example-owner/example", COMMIT, "2026-10-07")

    def test_header_names_scope_source_commit_date_and_disclaimer(self):
        lines = self.render().splitlines()
        self.assertEqual(lines[0], "# SITUATION — example-owner/example")
        header = "\n".join(lines[:12])
        self.assertIn("projection; not a source of truth", header)
        self.assertIn("- Scope: `example-owner/example`", header)
        self.assertIn("- Source: `situation/` files", header)
        self.assertIn(f"- Commit read: `{COMMIT}`", header)
        self.assertIn("- Date: 2026-10-07", header)

    def test_sections_are_the_fixed_classes_in_order(self):
        sections, fenced = [], False
        for line in self.render().splitlines():
            fenced ^= line.startswith("```")
            if not fenced and line.startswith("## "):
                sections.append(line)
        self.assertEqual(sections, ["## Invariants", "## Promises", "## Oracles", "## Decisions", "## Gaps",
                                    "## Candidates", "## Plans", "## References"])

    def test_records_are_in_numeric_id_order_with_state_and_scope(self):
        text = self.render()
        self.assertLess(text.index("### I-000002 — Earlier rule"), text.index("### I-000010 — Later rule"))
        self.assertIn("Priority: critical · Applies to: `agent-runtime/2` · [situation/invariants/I-000002-earlier.md]"
                      "(situation/invariants/I-000002-earlier.md)", text)
        self.assertIn("Priority: standard · Applies to: all environments", text)
        self.assertIn("The earlier rule,\nwrapped.", text)
        self.assertIn("State: implemented · Applies to: all environments", text)
        self.assertIn("State: designed · Judges: `situation/promises/P-000001-thing.md`", text)
        self.assertIn("Status: accepted · Date: 2026-10-07", text)
        self.assertIn("State: open · ", text)
        self.assertIn("State: proposed · ", text)
        self.assertIn("### PLAN-000007 — The plan\n\nState: draft · ", text)
        self.assertIn("Groups the work.", text)

    def test_record_templates_shape_projects(self):
        text = self.render()
        self.assertIn("### D-000011 — Templated decision\n\nState: decided · ", text)
        self.assertIn("#### Decision\n\nUse the 2.1 template.", text)
        self.assertIn("#### Why\n\nIt is the format.", text)
        self.assertIn("### PLAN-000012 — Gap plan\n\nState: grouped · ", text)
        self.assertIn("#### Members\n\n- G-000004\n- C-000006", text)

    def test_projected_headings_are_exactly_the_published_template_headings(self):
        templates = ROOT / "templates/records"
        for heading, directory, prefix, facts, sections in projection.CLASSES:
            with self.subTest(records=heading):
                text = (templates / f"{directory[:-1]}.md").read_text()
                self.assertTrue(text.startswith(f"# {prefix}-<number> — <title>\n"))
                published = re.findall(r"(?m)^## (.+)$", text)
                legacy = [h for h in facts if h in projection.LEGACY_FACTS]
                self.assertEqual(sorted(h for h in facts + sections if h not in legacy), sorted(published))
                self.assertEqual(list(sections), [h for h in published if h in sections], "sections keep template order")

    def test_every_template_heading_of_a_templated_record_is_rendered(self):
        """A record written from its template keeps every field in the projection."""
        situation = self.tmp / "templated/situation"
        for heading, directory, prefix, facts, sections in projection.CLASSES:
            template = (ROOT / "templates/records" / f"{directory[:-1]}.md").read_text()
            body = template.replace("<number>", "000077").replace("<title>", f"Templated {heading}")
            path = situation / directory / f"{prefix}-000077-templated.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)
        text = projection.project(situation, "o/r", COMMIT, "2026-10-07")
        for heading, directory, prefix, facts, sections in projection.CLASSES:
            template = (ROOT / "templates/records" / f"{directory[:-1]}.md").read_text()
            for name, value in re.findall(r"(?m)^## (.+)\n\n(.+)$", template):
                with self.subTest(records=heading, heading=name):
                    if name in sections:
                        self.assertIn(f"#### {name}\n\n{value}", text)
                    else:
                        self.assertIn(f"{name}: {value}", text)

    def test_plan_members_and_oracle_conditions_are_projected(self):
        situation = self.tmp / "fields/situation"
        write_tree(situation, {
            "plans/PLAN-000001-p.md": "# PLAN-000001 — P\n\n## State\n\ngrouped\n\n## Members\n\n- G-000001\n\n"
                                      "## Waits on\n\n- G-000001 upon C-000002\n",
            "oracles/O-000001-o.md": "# O-000001 — O\n\n## State\n\ndefined\n\n## Judges\n\nP-000001\n\n"
                                     "## Inputs\n\nThe run log.\n\n## Holds when\n\nEvery row.\n\n"
                                     "## Fails when\n\nA row is missing.\n\n## Arrangement\n\ndeterministic\n",
        })
        text = projection.project(situation, "o/r", COMMIT, "2026-10-07")
        for present in ("#### Members\n\n- G-000001", "#### Waits on\n\n- G-000001 upon C-000002",
                        "#### Inputs\n\nThe run log.", "#### Holds when\n\nEvery row.",
                        "#### Fails when\n\nA row is missing.", "Arrangement: deterministic"):
            self.assertIn(present, text)

    def test_section_headings_are_demoted_and_fences_respected(self):
        text = self.render()
        self.assertIn("#### Decision\n\n##### Part one", text)
        self.assertIn("```text\n## not a section\n```", text)
        self.assertIn("#### Why\n\nBecause.", text)

    def test_references_are_pointers_only(self):
        text = self.render()
        self.assertIn("- [situation/references/D-000003/notes.md](situation/references/D-000003/notes.md)", text)
        self.assertNotIn("REFERENCE-BODY", text)

    def test_security_witnesses_and_context_are_never_projected(self):
        text = self.render()
        for absent in ("SECRET", "G-000005", "leak.md", "I-000099", "WITNESS-BODY", "W-000008", "Not projected",
                       "Namespace rules"):
            self.assertNotIn(absent, text)

    def assert_refused(self, situation=None, root=None):
        with self.assertRaisesRegex(ValueError, "symbolic link"):
            projection.project(situation or self.situation, "o/r", COMMIT, "2026-10-07", root=root)

    def test_a_linked_file_is_refused(self):
        (self.tmp / "outside.md").write_text("# P-000002 — OUTSIDE\n")
        (self.situation / "promises/P-000002-outside.md").symlink_to(self.tmp / "outside.md")
        self.assert_refused()

    def test_a_linked_directory_inside_a_class_is_refused(self):
        (self.situation / "candidates/linked").symlink_to(self.situation / "gaps/security", target_is_directory=True)
        self.assert_refused()

    def test_a_linked_class_directory_is_refused(self):
        real = self.tmp / "elsewhere"
        write_tree(real, {"I-000050-linked.md": "# I-000050 — LINKED RULE\n\n## Priority\n\nstandard\n"})
        shutil.rmtree(self.situation / "invariants")
        (self.situation / "invariants").symlink_to(real, target_is_directory=True)
        self.assert_refused()

    def test_a_linked_source_directory_or_ancestor_is_refused(self):
        linked = self.tmp / "repo/linked-situation"
        linked.symlink_to(self.situation, target_is_directory=True)
        self.assert_refused(linked, root=self.tmp / "repo")
        (self.tmp / "repo/docs").symlink_to(self.tmp / "repo", target_is_directory=True)
        self.assert_refused(self.tmp / "repo/docs/situation", root=self.tmp / "repo")

    def test_links_inside_security_directories_are_never_read(self):
        (self.situation / "gaps/security/G-000013-linked.md").symlink_to(self.tmp / "missing.md")
        self.assertNotIn("G-000013", self.render())

    def test_cli_refuses_a_linked_class_directory(self):
        shutil.rmtree(self.situation / "oracles")
        (self.situation / "oracles").symlink_to(self.situation / "promises", target_is_directory=True)
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.tmp / "repo"), "--scope", "o/r",
                                 "--commit", COMMIT, "--date", "2026-10-07"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_references_are_in_numeric_id_order(self):
        write_tree(self.situation, {"references/R-10.md": "ten\n", "references/R-2.md": "two\n",
                                    "references/D-000003/R-000011-later.md": "x\n",
                                    "references/D-000003/R-000009-earlier.md": "x\n"})
        text = self.render()
        self.assertLess(text.index("references/R-2.md"), text.index("references/R-10.md"))
        self.assertLess(text.index("R-000009-earlier.md"), text.index("R-000011-later.md"))

    def test_same_input_same_bytes_whatever_the_file_order_or_line_endings(self):
        other = self.tmp / "other/situation"
        crlf = {name: body.replace("\n", "\r\n") for name, body in RECORDS.items()}
        write_tree(other, crlf, order=sorted(RECORDS, reverse=True))
        self.assertEqual(self.render().encode(), self.render().encode())
        self.assertEqual(self.render(other).encode(), self.render().encode())
        self.assertTrue(self.render().endswith("\n") and not self.render().endswith("\n\n"))

    def test_empty_class_says_none(self):
        empty = self.tmp / "empty/situation"
        (empty / "invariants").mkdir(parents=True)
        text = projection.project(empty, "o/r", COMMIT, "2026-10-07")
        self.assertIn("## Gaps\n\nNone.\n", text)


class GitSource(unittest.TestCase):
    """The commit read is the last commit that changed situation/, so committing the projection is stable."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.repo = Path(directory.name) / "repo"
        write_tree(self.repo / "situation", RECORDS)
        self.env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e", "GIT_COMMITTER_NAME": "t",
                    "GIT_COMMITTER_EMAIL": "t@e", "GIT_COMMITTER_DATE": "2026-10-05T23:30:00-02:00",
                    "GIT_AUTHOR_DATE": "2026-10-05T23:30:00-02:00"}
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "records", env=self.env)
        self.records_commit = git(self.repo, "rev-parse", "HEAD").strip()

    def run_cli(self, *extra):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.repo), "--scope", "o/r", *extra],
                              capture_output=True, text=True)

    def test_commit_read_and_utc_date_come_from_git(self):
        commit, date = projection.source(self.repo, "situation")
        self.assertEqual((commit, date), (self.records_commit, "2026-10-06"))

    def test_header_is_the_last_records_commit_never_the_head_or_today(self):
        """Project, commit the result, project again: same bytes, and the header still names the records commit."""
        self.assertEqual(self.run_cli("--output", "SITUATION.md").returncode, 0)
        first = (self.repo / "SITUATION.md").read_bytes()
        git(self.repo, "add", "SITUATION.md")
        git(self.repo, "commit", "-q", "-m", "projection", env={**self.env, "GIT_COMMITTER_DATE": "2027-01-01T00:00:00Z"})
        head = git(self.repo, "rev-parse", "HEAD").strip()
        self.assertNotEqual(head, self.records_commit)
        self.assertEqual(self.run_cli("--output", "SITUATION.md").returncode, 0)
        second = (self.repo / "SITUATION.md").read_bytes()
        self.assertEqual(second, first)
        header = second.decode().split("## Invariants")[0]
        self.assertIn(f"- Commit read: `{self.records_commit}`", header)
        self.assertIn("- Date: 2026-10-06", header)
        self.assertNotIn(head, header)
        self.assertNotIn("2027-01-01", header)
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")

    def test_committing_the_projection_does_not_change_it(self):
        self.assertEqual(self.run_cli("--output", "SITUATION.md").returncode, 0)
        first = (self.repo / "SITUATION.md").read_bytes()
        git(self.repo, "add", "SITUATION.md")
        git(self.repo, "commit", "-q", "-m", "projection", env={**self.env, "GIT_COMMITTER_DATE": "2027-01-01T00:00:00Z"})
        self.assertEqual(self.run_cli("--check").returncode, 0)
        self.assertEqual(self.run_cli("--output", "SITUATION.md").returncode, 0)
        self.assertEqual((self.repo / "SITUATION.md").read_bytes(), first)

    def test_security_only_commits_do_not_move_the_commit_read(self):
        (self.repo / "situation/gaps/security/G-000005-hidden.md").write_text("changed\n")
        git(self.repo, "commit", "-qam", "security", env=self.env)
        self.assertEqual(projection.source(self.repo, "situation")[0], self.records_commit)

    def test_check_fails_when_records_change(self):
        self.assertEqual(self.run_cli("--output", "SITUATION.md").returncode, 0)
        (self.repo / "situation/gaps/G-000004-missing.md").write_text("# G-000004 — Renamed\n\n## State\n\nclosed\n")
        git(self.repo, "commit", "-qam", "gap", env=self.env)
        result = self.run_cli("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SITUATION.md", result.stderr)

    def test_missing_situation_directory_is_refused(self):
        shutil.rmtree(self.repo / "situation")
        self.assertNotEqual(self.run_cli("--commit", COMMIT, "--date", "2026-10-07").returncode, 0)


if __name__ == "__main__":
    unittest.main()
