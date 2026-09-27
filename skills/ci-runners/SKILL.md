---
name: ci-runners
description: The organization's GitHub Actions runners for application repositories - the exact runs-on lines, sizes, which runner fits which job, what to do when a job is OOM-killed or runs out of disk, and the Rust and Docker build caches. Read it when writing or changing a workflow, or when a CI job is killed, slow, queued, or lacks a tool.
---

# ci-runners

Every CI job runs on an organization runner: one ephemeral container per job
on the organization's cluster. Which label fits which job is an organization
rule; this skill gives the sizes, the exact `runs-on` line, and the details.

## Sizes

| Label | Memory / disk | Parallelism `N` | Examples |
|---|---|---|---|
| `automation-test-s` | 5 GiB / 30 GiB | 2 | unit tests, lint |
| `automation-test-l` | 10 GiB / 60 GiB | 4 | clippy on large workspaces |
| `automation-test-xl` | 6 GiB job + 24 GiB Docker / 100 GiB | 8 | Testcontainers, compose stacks, federation suites |
| `build-native` | 15 GiB / 40 GiB | 6 | Rust and Go release builds |
| `build-docker` | 6 GiB job + 24 GiB Docker / 40 GiB | 8 | image builds, jobs with `services:` |

```yaml
runs-on: {group: ci, labels: automation-test-s}
```

- `automation-infra-v2` belongs to the infrastructure repository alone; other
  repositories target the five labels above, in runner group `ci`.
- Any other label, including retired `cvu-*` labels, matches no runner: the
  job waits until GitHub cancels it after 24 hours.
- Test runners and `build-*` jobs wait for capacity when the pool is full;
  they never evict a running job.

## Inside a job

- Images are Ubuntu 24.04 with passwordless `sudo`: `sudo apt-get install -y
  <pkg>` works in a step. The test image has the Docker CLI but no daemon; jobs
  that need a daemon use `automation-test-xl` or `build-docker`.
- `nproc` shows the node's CPUs, not the slot. Each runner sets
  `CARGO_BUILD_JOBS`, `NEXTEST_TEST_THREADS`, `RUST_TEST_THREADS`,
  `GOMAXPROCS`, and `MAKEFLAGS=-jN` to its `N`; scripts that call
  `make -j$(nproc)` pass `N` instead.
- Per-core speed is about a third of a current desktop CPU. Timeouts
  calibrated on GitHub-hosted runners need about 3x headroom.
- Docker networks on these runners use MTU 1370. A compose file that pins a
  higher MTU in `driver_opts` stalls TLS to the internet; leave MTU unset.
- A tool many repositories need goes into the runner image by pull request to
  the `runner-images` repository; a missing capability of the runners
  themselves is an issue in the infrastructure repository.

## Killed jobs: move up a size

Exit code 137, `Killed`, `OOMKilled`, or an eviction for ephemeral storage
means the job outgrew its slot. Move it one size up:

- `automation-test-s` -> `automation-test-l`;
- a compile-bound job -> `build-native`;
- a Docker-hosted test suite -> `automation-test-xl`;
- on the Docker runners, a single container exiting 137 with
  `OOMKilled=true` while the job continues outgrew the Docker cap (23 GiB):
  split the stack or move heavy compilation out of the containers.

Slot sizes change only from measured utilisation, by the operator; ask in an
issue to the infrastructure repository with the run URL.

## Caching

### Rust: sccache, automatic

Every runner compiles Rust through sccache with a per-repository cache prefix.
A workflow adds nothing; `sccache --show-stats` in a step shows hits so far and
the job log ends with the totals.

- Opt out with `env: {RUSTC_WRAPPER: ""}` at job or step level; a job that
  sets its own `RUSTC_WRAPPER` or `CARGO_INCREMENTAL` overrides the runner.
- Jobs inside `container:` do not inherit the runner environment and compile
  uncached.
- Cached: rustc compilations with stable paths. Not cached: linking, build
  script execution, tests, and `cargo install` into a random directory (set a
  fixed `CARGO_TARGET_DIR`).
- The first run of a repository pays the uploads; later runs are faster.

### Go

`actions/setup-go` with its built-in cache.

### Docker image layers: registry cache in GHCR

On `build-docker`, read and write a BuildKit cache in the image's own GHCR
package under the tag `buildcache`, after logging in to GHCR with the job's
`GITHUB_TOKEN` (`packages: write`):

```bash
cache=(--cache-from "type=registry,ref=ghcr.io/<owner>/<package>:buildcache"
       --cache-to "type=registry,ref=ghcr.io/<owner>/<package>:buildcache,mode=max,ignore-error=true")
docker build "${cache[@]}" --tag "$IMAGE:$TAG" .
```

With `docker/build-push-action`, use the same values in `cache-from` and
`cache-to`. No `setup-buildx-action` is needed. Consumers pin digests;
`:buildcache` is never deployed. Put `ARG`s whose value changes per commit
(revision labels) after the expensive steps.

### Rust inside Docker builds

Pass the runner's sccache settings as BuildKit secrets and consume them only in
the cargo `RUN`, so they never land in a layer or the image history:

```bash
sccache=()
if [ "${RUSTC_WRAPPER:-}" = sccache ] && [ -n "${SCCACHE_BUCKET:-}" ]; then
  for v in AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY SCCACHE_BUCKET SCCACHE_ENDPOINT SCCACHE_REGION SCCACHE_S3_KEY_PREFIX; do
    if [ -n "${!v:-}" ]; then sccache+=(--secret "id=$v,env=$v"); fi
  done
fi
docker build "${cache[@]}" "${sccache[@]}" --tag "$IMAGE:$TAG" .
```

```dockerfile
RUN --mount=type=secret,id=AWS_ACCESS_KEY_ID,env=AWS_ACCESS_KEY_ID \
    --mount=type=secret,id=AWS_SECRET_ACCESS_KEY,env=AWS_SECRET_ACCESS_KEY \
    --mount=type=secret,id=SCCACHE_BUCKET,env=SCCACHE_BUCKET \
    --mount=type=secret,id=SCCACHE_ENDPOINT,env=SCCACHE_ENDPOINT \
    --mount=type=secret,id=SCCACHE_REGION,env=SCCACHE_REGION \
    --mount=type=secret,id=SCCACHE_S3_KEY_PREFIX,env=SCCACHE_S3_KEY_PREFIX \
    if [ -n "${SCCACHE_BUCKET:-}" ]; then \
      export RUSTC_WRAPPER=sccache SCCACHE_S3_USE_SSL=true SCCACHE_IGNORE_SERVER_IO_ERROR=1 CARGO_INCREMENTAL=0; \
    fi \
 && cargo build --locked --release \
 && if [ -n "${RUSTC_WRAPPER:-}" ]; then sccache --stop-server || true; fi
```

Install sccache in the build stage pinned by checksum. `--stop-server` at the
end of the `RUN` flushes pending cache writes. Keep `set -x` away from lines
that expand the credentials; a missing secret leaves the variables unset and
local builds compile uncached.

## Fork pull requests

Private repositories never run fork pull requests. In public repositories an
external contributor's run waits for a maintainer's approval; approve only
after reading the workflow changes.
