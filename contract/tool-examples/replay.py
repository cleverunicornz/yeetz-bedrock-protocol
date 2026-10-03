"""Replay public arguments through the pinned client and real native HTTP/store/projector.

Run only on the workbench or source CI. Testcontainers starts an isolated pinned
PostgreSQL/AGE dependency. No platform token, service selector or deployed
identity is read. The configured Stamp seam is deliberately unqualified.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib
import json
import re
import secrets
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from check_calls import project, substitute, validate_arguments
from probe import observe

ROOT = Path(__file__).resolve().parents[1]
INTERFACE = json.loads((ROOT / "tool-interface.json").read_text())
FIXTURE = json.loads((ROOT / "tool-examples/calls.json").read_text())


def check_reference_response(args, out, checks):
    if out.get("state") != checks["state"]:
        raise AssertionError("Reference state differs")
    if "sha256_of" in checks:
        expected = checks["sha256_of"]
        if out.get("markdown") != expected or out.get("sha256") != hashlib.sha256(expected.encode()).hexdigest():
            raise AssertionError("stored Reference markdown or SHA differs")
        if not out.get("version") or out["version"] == "null":
            raise AssertionError("stored Reference has no immutable object version")
    elif out.get("reference") != args["id"]:
        raise AssertionError("Reference pointer identity differs")


def fixture_arguments(key, values):
    step = next(step for step in FIXTURE["steps"] if step["key"] == key)
    return substitute(step["arguments"], values)


def pinned_source(root, spec):
    specimen = root / ".source-image.json"
    receipt = None
    if specimen.is_file():
        receipt = json.loads(specimen.read_text())
        if receipt.get("image") != spec["specimen_image"] or receipt.get("expected_source_commit") != spec["commit"]:
            raise AssertionError("image specimen provenance differs from pinned interface")
    else:
        actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        if actual != spec["commit"]:
            raise AssertionError(f"source pin {actual} != {spec['commit']}")
    for entry in spec["files"]:
        if receipt and entry["path"].startswith("ci/"):
            continue
        digest = hashlib.sha256((root / entry["path"]).read_bytes()).hexdigest()
        if digest != entry["sha256"]:
            raise AssertionError(f"source digest differs: {entry['path']}")


def compare_semantics(graph_source):
    import yaml
    base = yaml.safe_load((graph_source / "vendor/bedrock/contract/bedrock-v2.yaml").read_text())
    local = yaml.safe_load((ROOT / "bedrock-v2.yaml").read_text())
    # The parent's release coordinate changes only publication identity.
    # Actual source keeps its own pinned vendored contract; never patch it.
    base.pop("bedrock")
    local.pop("bedrock")
    if base != local:
        raise AssertionError("fixed semantics differ from native source contract")
    base_schema = json.loads((graph_source / "vendor/bedrock/contract/bedrock-v2.schema.json").read_text())
    local_schema = json.loads((ROOT / "bedrock-v2.schema.json").read_text())
    for schema in (base_schema, local_schema):
        schema["properties"]["protocol"].pop("const")
        schema.pop("title", None)
    if base_schema != local_schema:
        raise AssertionError("fixed act schema differs beyond release coordinate/title")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph-source", type=Path, required=True)
    parser.add_argument("--client-source", type=Path, required=True)
    parser.add_argument("--fixture-commit", required=True)
    opts = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", opts.fixture_commit):
        parser.error("fixture commit must be the full commit containing this fixture")
    pinned_source(opts.graph_source, INTERFACE["graph"])
    pinned_source(opts.client_source, INTERFACE["client"])
    compare_semantics(opts.graph_source)
    sys.path.insert(0, str(opts.graph_source / "src"))
    sys.path.insert(0, str(opts.client_source / "images/repo-pod/runtime"))
    import psycopg
    from psycopg import sql
    from psycopg_pool import ConnectionPool
    from testcontainers.core.container import DockerContainer
    from taskgraph import admin, api, queries
    from taskgraph.identity import Stamp
    from taskgraph.projector import Projector
    from taskgraph.references import Bucket, References
    from taskgraph.store import Store
    import cvu_task_graph as client
    import cvu_task_graph_mcp as mcp_source
    if mcp_source.SCHEMA != INTERFACE["client_tool"]["schema"]:
        raise AssertionError("pinned actual client schema differs from adapter")
    if {k: sorted(v) for k, v in client.FIELDS.items()} != {k: sorted(v) for k, v in INTERFACE["client_fields"].items()}:
        raise AssertionError("actual client per-operation fields differ from adapter")
    if sorted(api.ACT_FIELDS) != sorted(INTERFACE["operations"]["act"]["allowed"]):
        raise AssertionError("actual native act fields differ from adapter")
    if set(queries.QUERIES) != set(INTERFACE["queries"]):
        raise AssertionError("actual fixed query names differ from adapter")
    if (opts.graph_source / ".source-image.json").is_file():
        config = {"IMAGE": INTERFACE["dependencies"]["postgres"]["image"],
                  "PRELOAD": INTERFACE["dependencies"]["postgres"]["preload"]}
    else:
        config = dict(line.split("=", 1) for line in (opts.graph_source / "ci/platform-postgres.env").read_text().splitlines()
                      if line and not line.startswith("#"))
    image = config["IMAGE"]
    preload = config["PRELOAD"]
    if "@sha256:" not in image or not re.fullmatch("[a-z_]+", preload):
        raise AssertionError("unqualified database dependency pin")
    command = ("initdb -D /tmp/pgdata -U postgres --auth=trust --locale=C.UTF-8 >/dev/null && "
               "echo 'host all all all trust' >> /tmp/pgdata/pg_hba.conf && "
               "exec postgres -D /tmp/pgdata -c listen_addresses='*' -c unix_socket_directories=/tmp "
               f"-c shared_preload_libraries='{preload}' -c max_connections=40")
    container = DockerContainer(image).with_exposed_ports(5432).with_kwargs(
        user="26:26", entrypoint="bash").with_command(["-c", command])
    # Disposable fixture authentication is generated in memory and consumed
    # directly by MinIO/boto3; it never appears in logs or source artifacts.
    s3_access, s3_secret = "fixture" + secrets.token_hex(8), secrets.token_hex(32)
    minio_image = INTERFACE["dependencies"]["minio"]["image"]
    minio = (DockerContainer(minio_image).with_exposed_ports(9000)
             .with_env("MINIO_ROOT_USER", s3_access).with_env("MINIO_ROOT_PASSWORD", s3_secret)
             .with_kwargs(entrypoint="/opt/bitnami/minio/bin/minio")
             .with_command(["server", "/tmp/protocol-reference-data"]))
    print("dependency_image=" + image)
    print("object_dependency_image=" + minio_image)
    with container, minio, tempfile.TemporaryDirectory(prefix="bedrock-call-replay-") as scratch:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", endpoint_url=f"http://{minio.get_container_host_ip()}:{minio.get_exposed_port(9000)}",
                          aws_access_key_id=s3_access, aws_secret_access_key=s3_secret, region_name="us-east-1",
                          config=Config(signature_version="s3v4", s3={"addressing_style": "path"}))
        deadline = time.monotonic() + 90
        while True:
            try:
                s3.list_buckets()
                break
            except Exception:
                if time.monotonic() >= deadline:
                    raise AssertionError("isolated MinIO did not become ready") from None
                time.sleep(.25)
        bucket_name = "protocol-references"
        s3.create_bucket(Bucket=bucket_name)
        s3.put_bucket_versioning(Bucket=bucket_name, VersioningConfiguration={"Status": "Enabled"})
        host, port = container.get_container_host_ip(), container.get_exposed_port(5432)
        base_dsn = f"host={host} port={port} dbname=postgres user=postgres"
        ready = False
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            try:
                with psycopg.connect(base_dsn, connect_timeout=2):
                    ready = True
                    break
            except psycopg.OperationalError:
                time.sleep(.25)
        if not ready:
            raise AssertionError("scratch database did not become ready")
        roles = {k: "bedrock_fixture_" + k for k in ("owner", "api", "importer", "projector", "reader")}
        name = "bedrock_fixture"
        with psycopg.connect(base_dsn, autocommit=True) as conn:
            for role in ("api", "importer", "projector"):
                conn.execute(sql.SQL("create role {} login").format(sql.Identifier(roles[role])))
            conn.execute(sql.SQL("create database {}").format(sql.Identifier(name)))
        def dsn(role="postgres"):
            user = "postgres" if role == "postgres" else roles[role]
            return f"host={host} port={port} dbname={name} user={user}"
        with psycopg.connect(dsn()) as conn:
            conn.execute(admin.store_sql(name, **roles))
            conn.commit()
        class FixtureIdentity:
            role = "scout"
            def stamp(self, headers):
                return Stamp(kind="agent", principal="isolated-fixture", role=self.role,
                             repository="example/protocol")
        identity = FixtureIdentity()
        store = Store(dsn("api"))
        with ConnectionPool(dsn("api"), min_size=1, max_size=2) as pool:
            app = api.App(store, pool, identity, References(store, {"references": Bucket(s3, bucket_name)}))
            server = api.serve(app, "127.0.0.1", 0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            projector = Projector(dsn("projector"), reader=roles["reader"])
            projector.open()
            parsed = urlsplit(f"http://127.0.0.1:{server.server_address[1]}")
            # The value below is a public fixture marker, never a platform secret.
            marker = Path(scratch) / "fixture-marker"
            marker.write_text("isolated-fixture-public-marker")
            state = Path(scratch) / "client-state"
            state.mkdir(mode=0o700)
            values = {"scope": "fixture-scope", "run": "fixture-run", "session": "fixture:session",
                      "fixture_commit": opts.fixture_commit,
                      "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                      "probe_result": observe()}
            real_configuration, real_lineage, real_exchange = client.configuration, client.lineage, client.exchange
            client.configuration = lambda: (parsed.geturl(), parsed, str(marker), state, 10)
            client.lineage = lambda: {"session": values["session"], "repository": "example/protocol"}
            exchanges = []
            def capture(parsed, path, body, token, timeout):
                exchanges.append((path, json.loads(body) if body is not None else None))
                return real_exchange(parsed, path, body, token, timeout)
            client.exchange = capture
            def count():
                with psycopg.connect(dsn()) as conn:
                    return conn.execute("select count(*) from tg.acts").fetchone()[0]
            def call(args):
                validate_arguments(args, INTERFACE)
                client.validate(args)
                before = len(exchanges)
                result = client.call(args)
                expected = project(args, client.lineage())
                if len(exchanges) != before + 1 or exchanges[-1] != expected:
                    raise AssertionError("actual client HTTP projection differs from documented full envelope")
                return result
            def query(name, **params):
                projector.catch_up()
                result = call({"op": "query", "name": name, "params": params})
                if result["watermark"] != result["head"]:
                    raise AssertionError("actual projector did not catch up")
                return result
            try:
                for step in FIXTURE["steps"]:
                    identity.role = step["role"]
                    args = substitute(step["arguments"], values)
                    if args["op"] == "query":
                        projector.catch_up()
                    before = count()
                    out = call(args)
                    values[step["key"]] = out
                    checks = substitute(step.get("check", {}), values)
                    if args["op"] in ("act", "reference.put"):
                        if count() != before + 1:
                            raise AssertionError("successful write did not append exactly one act")
                        replayed = call(args)
                        if not replayed["replayed"] or (replayed["act_id"], replayed["made"]) != (out["act_id"], out["made"]):
                            raise AssertionError("original-key replay did not preserve actual allocated IDs")
                        if count() != before + 1:
                            raise AssertionError("original-key replay appended another act")
                        with psycopg.connect(dsn()) as conn:
                            row = conn.execute("select actor_role, actor_principal from tg.acts where act_id=%s",
                                               (out["act_id"],)).fetchone()
                        if row != (step["role"], "isolated-fixture"):
                            raise AssertionError("receiver stamp differed from fixture configuration")
                        subject = checks.get("subject", out["made"])
                        if subject:
                            record = query("record", id=subject)
                            if record["watermark"] < out["seq"] or record["record"]["state"] != checks["state"]:
                                raise AssertionError("affected-record readback disagreed with expected state")
                        out_read = query("transcript_behind", act=out["act_id"])
                        if out_read["pointers"]["session"] != values["session"]:
                            raise AssertionError("actual act provenance did not preserve session")
                    elif args["op"] == "query" and args["name"] == "assured_by":
                        if out["state"] != checks["state"]:
                            raise AssertionError("assurance query state differs")
                        standing = out["standing"]["act_id"] if out["standing"] else None
                        if standing != checks["standing_act"]:
                            raise AssertionError("standing judgment differs")
                    elif args["op"] == "reference.get":
                        check_reference_response(args, out, checks)
                        if "sha256_of" in checks:
                            # The isolated bucket gets a newer version behind
                            # the same key. The API must keep reading the
                            # Reference's original version, never the latest.
                            versions = s3.list_object_versions(Bucket=bucket_name).get("Versions", [])
                            stored = [version for version in versions if version["VersionId"] == out["version"]]
                            if len(stored) != 1:
                                raise AssertionError("stored Reference version is absent or ambiguous in MinIO")
                            replacement = s3.put_object(Bucket=bucket_name, Key=stored[0]["Key"],
                                                        Body=b"A later isolated object version.\n", ContentType="text/markdown")
                            if replacement.get("VersionId") in (None, "null", out["version"]):
                                raise AssertionError("MinIO did not create a distinct later object version")
                            again = call(args)
                            if (again["version"], again["sha256"], again["markdown"]) != (out["version"], out["sha256"], out["markdown"]):
                                raise AssertionError("stored Reference readback changed its pinned version")
                    print("PASS call=" + step["key"])
                for step in FIXTURE["negative_steps"]:
                    identity.role = step["role"]
                    args = substitute(step["arguments"], values)
                    before = count()
                    try:
                        call(args)
                    except client.ClientError as error:
                        if f": {step['refusal']}; request refused" not in str(error):
                            raise AssertionError(f"{step['key']}: wrong actual refusal {error}") from error
                    else:
                        raise AssertionError(f"{step['key']}: native API unexpectedly admitted request")
                    if count() != before:
                        raise AssertionError(f"{step['key']}: refusal appended a row")
                    print("PASS refusal=" + step["key"])
                # Native envelope exclusion is tested independently of the client schema.
                first = fixture_arguments("stipulate", values)
                path, body = project(first, client.lineage())
                body["request_id"] = "fixture-forged-actor"
                body["actor"] = {"role": "authority"}
                before = count()
                status, answer = real_exchange(parsed, path, json.dumps(body).encode(), marker.read_text(), 10)
                if status != 409 or answer != {"refusal": "invalid_act"} or count() != before:
                    raise AssertionError("native caller actor exclusion failed")
                # Reuse with changed intent must fail without a second append.
                changed = dict(first)
                changed["payload"] = {"invariant": {"title": "Changed fixture", "rule": "Changed.", "priority": "standard"}}
                try:
                    call(changed)
                except client.ClientError as error:
                    if "already belongs to different arguments" not in str(error):
                        raise
                else:
                    raise AssertionError("changed client intent reused a key")
                if count() != before:
                    raise AssertionError("conflicting key changed native authority")
                final = query("open_work", level="repository", scope=values["scope"])
                print(json.dumps({"result": "PASS", "qualification": "isolated source replay only",
                    "graph_commit": INTERFACE["graph"]["commit"], "client_commit": INTERFACE["client"]["commit"],
                    "fixture_commit": opts.fixture_commit, "calls": len(FIXTURE["steps"]),
                    "refusals": len(FIXTURE["negative_steps"]), "head": final["head"], "watermark": final["watermark"]}, sort_keys=True))
            finally:
                client.configuration, client.lineage, client.exchange = real_configuration, real_lineage, real_exchange
                projector.close()
                server.shutdown()
                server.server_close()
                thread.join(timeout=10)
                store.close()


if __name__ == "__main__":
    main()
