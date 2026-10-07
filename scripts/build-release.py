#!/usr/bin/env python3
"""Build a protocol release's assets deterministically from a source tree.

Writes `bedrock-<VERSION>.tar.gz` (every manifest-published file plus VERSION
and manifest.json under `bedrock/`, sorted, ustar, owner 0, mode 0644, time 0,
gzip level 9 with time 0), a copy of `manifest.json`, and `SHA256SUMS` naming
both. Every published file is verified against its manifest digest first. The
same tree gives the same bytes; this releases nothing by itself.
"""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile


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


def build(source: Path, output: Path) -> Path:
    source = Path(source)
    manifest = json.loads((source / "manifest.json").read_text())
    version = (source / "VERSION").read_text().strip()
    if manifest.get("version") != version:
        raise ValueError(f"manifest version {manifest.get('version')} != VERSION {version}")
    names = {"VERSION", "manifest.json"}
    for entry in entries(manifest):
        data = (source / entry["path"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError(f"package digest mismatch: {entry['path']}")
        names.add(entry["path"])
    tar_bytes = io.BytesIO()
    with tarfile.open(fileobj=tar_bytes, mode="w", format=tarfile.USTAR_FORMAT) as tar:
        for name in sorted(names):
            data = (source / name).read_bytes()
            info = tarfile.TarInfo(f"bedrock/{name}")
            info.size, info.mode, info.mtime = len(data), 0o644, 0
            tar.addfile(info, io.BytesIO(data))
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    archive = f"bedrock-{version}.tar.gz"
    assets = {archive: gzip.compress(tar_bytes.getvalue(), compresslevel=9, mtime=0),
              "manifest.json": (source / "manifest.json").read_bytes()}
    for name, data in assets.items():
        (output / name).write_bytes(data)
    (output / "SHA256SUMS").write_text("".join(f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in assets.items()))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--source", type=Path, default=Path("."), help="protocol source tree (default: .)")
    parser.add_argument("--output", type=Path, required=True, help="directory for the release assets")
    args = parser.parse_args()
    try:
        out = build(args.source, args.output)
    except (OSError, ValueError, KeyError) as error:
        sys.exit(f"release build failed: {error}")
    sys.stdout.write((out / "SHA256SUMS").read_text())


if __name__ == "__main__":
    main()
