"""Materialize private source specimens from existing pinned images in heavy CI.

No Git credential or private implementation enters the protocol repository.
Image revision labels and file-byte agreement are separate provenance facts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def command(*args):
    return subprocess.check_output(args, text=True).strip()


def copy_image(spec, output, name):
    image = spec["specimen_image"]
    if "@sha256:" not in image:
        raise ValueError("specimen image must be immutable")
    subprocess.run(["docker", "pull", image], check=True)
    cid = command("docker", "create", "--entrypoint", "/bin/true", image)
    try:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            subprocess.run(["docker", "cp", f"{cid}:{spec['specimen_path']}", str(package)], check=True)
            output.mkdir(parents=True, exist_ok=True)
            if name == "graph":
                destination = output / "src/taskgraph"
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(package, destination)
                shutil.copytree(package / "_bedrock", output / "vendor/bedrock")
                shutil.copytree(package / "sql", output / "sql")
            else:
                destination = output / "images/repo-pod/runtime"
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(package, destination)
        verified = []
        for entry in spec["files"]:
            # Dependency configuration comes from separately pinned metadata;
            # production images do not carry their CI configuration directory.
            if entry["path"].startswith("ci/"):
                continue
            path = output / entry["path"]
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != entry["sha256"]:
                raise ValueError(f"{name} image/source byte mismatch: {entry['path']}: {actual} != {entry['sha256']}")
            verified.append(entry["path"])
        revision = command("docker", "inspect", "--format", '{{index .Config.Labels "org.opencontainers.image.revision"}}', cid)
        receipt = {"mode": "image-byte-specimen", "image": image,
                   "image_revision_label": revision, "expected_source_commit": spec["commit"],
                   "verified_files": verified}
        (output / ".source-image.json").write_text(json.dumps(receipt, sort_keys=True) + "\n")
        print(json.dumps({"source": name, **receipt}, sort_keys=True))
    finally:
        subprocess.run(["docker", "rm", cid], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    opts = parser.parse_args()
    interface = json.loads((ROOT / "tool-interface.json").read_text())
    for name in ("graph", "client"):
        copy_image(interface[name], opts.output / name, name)


if __name__ == "__main__":
    main()
