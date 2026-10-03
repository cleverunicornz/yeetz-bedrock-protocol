"""Show the pinned published compiler's failure and the candidate package's fix."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile

import test_patch_compatibility as checks

ARCHIVE_SHA256 = "5be7e35e8390d1332bb660ace4b6233eef4c12b892f87cd504241d4baef2b9c2"
MANIFEST_SHA256 = "914d4cb5fc2dd4cb024cf8c2cd10ac053d73127d2f5f8ea4dfb32078734be160"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    if hashlib.sha256(args.archive.read_bytes()).hexdigest() != ARCHIVE_SHA256:
        raise ValueError("published baseline archive digest mismatch")
    case = checks.PatchCompatibilityTests()
    case.setUp()
    try:
        unpacked = Path(case.tmp.name) / "published"
        unpacked.mkdir()
        with tarfile.open(args.archive) as archive:
            archive.extractall(unpacked, filter="data")
        baseline = unpacked / "bedrock"
        if hashlib.sha256((baseline / "manifest.json").read_bytes()).hexdigest() != MANIFEST_SHA256:
            raise ValueError("published baseline manifest digest mismatch")
        case.version(case.org, "2.0.1")
        old = case.compile(baseline)
        if old.returncode != 1 or old.stdout or "requires the paired 2.0.0 package" not in old.stderr:
            raise ValueError("published compiler did not reproduce the expected version refusal")
        print(json.dumps({"baseline": "published v2.0.0", "archive_sha256": ARCHIVE_SHA256,
                          "manifest_sha256": MANIFEST_SHA256, "organization": "synthetic 2.0.1",
                          "exit_code": old.returncode, "result": "EXPECTED_FAILURE"}))
        candidate = case.package()
        for part in ("full", "user", "repository"):
            new = case.compile(candidate, part)
            if new.returncode != 0:
                raise ValueError(new.stderr)
            print(json.dumps({"candidate_version": (candidate / "VERSION").read_text().strip(),
                              "organization": "synthetic 2.0.1", "part": part,
                              "output_sha256": hashlib.sha256(new.stdout.encode()).hexdigest(),
                              "result": "PASS", "boundary": "finite manifest-only producer package"}))
    finally:
        case.doCleanups()


if __name__ == "__main__":
    main()
