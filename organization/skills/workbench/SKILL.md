---
name: workbench
description: Run heavy or interactive work on the repository's shared workbench - builds, clippy, filtered tests, lint, dev servers, docker compose stacks, Testcontainers, a Playwright browser, preview URLs, a desktop view. Covers when to use it, the 3-minute command cap, sizes (normal and xl), the HTTP interface every harness can call, and adding tools through the repository's devcontainer. Read it before compiling, testing, or starting servers.
---

# workbench

Your repo pod is small: it holds Paseo, your harness, and your worktree. Every
repository also has one shared **workbench** on a large pool node with Rust
(clippy, rustfmt, cargo-nextest, sccache), Node LTS with pnpm, Python 3 with
uv, a Docker daemon, Chromium with Playwright MCP, and common build
dependencies. Your worktree gets its own workspace there: its own source
directory, cargo target directory, and port range. Other agents of the
repository work in their own workspaces on the same workbench.

## When

- Compiling, testing, dev servers, Docker, and browsers run on the workbench.
  Reading, searching, editing, and git stay in the repo pod.
- **Every command has a hard 3-minute cap (180 s).** Keep commands short:
  `cargo clippy --all-targets -- -D warnings`, a filtered
  `cargo nextest run <filter>`, `pnpm tsc --noEmit`, `uv run pytest -k <expr>`,
  `ruff check`.
- Longer work (full suites, release builds, benchmarks) runs on the GitHub
  test runners: push the branch and let CI run it (`ci-runners`). A long job
  stays one CI job rather than many 3-minute pieces.
- `cargo clippy -- -D warnings` is a compile sanity check: it must compile.
  Fix lints that are cheap and correct; leave code readable.

## How

Before every command and service start your worktree is synced: tracked and
untracked non-ignored files, changes only, deletions included. Ignored
directories (`target/`, `node_modules/`, `.venv/`) are never synced: install
dependencies on the workbench (`pnpm install`, `uv sync`). Git history is not
there.

**Any harness** — the workbench shim listens on `127.0.0.1:8099` in the repo
pod; `cwd` is your worktree path:

```sh
W=127.0.0.1:8099; CWD=$(git rev-parse --show-toplevel)
curl -s -XPOST $W/v1/open -d "{\"cwd\":\"$CWD\"}"                 # open (add ,"size":"xl"); returns workspace, ports, mcp_url
curl -sN -XPOST $W/v1/run -d "{\"cwd\":\"$CWD\",\"cmd\":\"cargo nextest run parser\",\"timeout_s\":170}"
curl -s -XPOST $W/v1/service -d "{\"cwd\":\"$CWD\",\"name\":\"web\",\"command\":\"pnpm dev --port \$PORT --host 127.0.0.1\"}"
curl -s "$W/v1/service/logs?cwd=$CWD&name=web&tail=50"
curl -s -XDELETE $W/v1/service -d "{\"cwd\":\"$CWD\",\"name\":\"web\"}"
curl -s "$W/v1/url?cwd=$CWD&port=<port>"                           # preview URL for people + local URL
curl -s -XPOST $W/v1/desktop -d "{\"cwd\":\"$CWD\"}"               # live desktop with a visible Chromium
curl -s "$W/v1/status?cwd=$CWD"                                    # idle time, running commands, disk, caps
```

`run` streams NDJSON: `{"t":"o"|"e","d":...}` output, then
`{"t":"exit",...}` with `exit_code`, `timed_out`, `memory_exceeded`, and a
final `{"t":"summary","diagnostics":[...]}` of parsed compiler and test
diagnostics. `open` returns `mcp_url` (headless browser) and `mcp_visible_url`
(the desktop's browser): Playwright MCP endpoints for your workspace.

**NOOA** — the same through `self.workbench`: `open(size=...)`, `run(cmd,
timeout=...)`, `service_start/stop/logs`, `url(port)`, `browser(visible=...)`,
`desktop()`, `status()`.

- Ports: `$PORT` is the first port of your range; use anything in
  `$WORKBENCH_PORT_BASE..$WORKBENCH_PORT_END` except the last three, which
  belong to the browser tools. Bind servers to `127.0.0.1` or `0.0.0.0`.
- Services are exempt from the cap and live until stopped or the workbench
  stops; `docker compose up` works as a service. Background processes started
  inside `run` end with it.
- The browser uses local addresses (`http://127.0.0.1:<port>`); the preview
  URL from `url` is for people.
- After about 30 minutes without activity the workbench stops; workspaces and
  caches stay, and the next `open` restarts it. `open` answering `waiting`
  means capacity is in use; it waits for a slot.

## Size: normal or xl

- **Normal**: 10 GiB (6 GiB tools, 4 GiB Docker), 5 GiB per command. Builds,
  filtered tests, a dev server, a small compose stack.
- **xl**: 20 GiB (8 GiB tools, 12 GiB Docker), 7 GiB per command. Full-stack
  end-to-end testing, for example a web client, a homeserver, and Postgres in
  compose with a Chromium driving them. Open with `"size":"xl"`; a running
  normal workbench is replaced (workspaces and caches stay, services restart),
  so decide before starting services. xl takes twice the capacity: use it when
  the stack needs it.
- A repository that always needs xl sets `"size": "xl"` in its devcontainer
  (below). When the kernel OOM-kills a normal workbench, the next `open`
  brings it back as xl by itself.

## Missing tools: devcontainer by pull request

A one-off `apt-get install -y ...` (commands run as root) or `pnpm add -g`
inside `run` unblocks you now. The permanent fix is the repository's
`.devcontainer/devcontainer.json`, changed by pull request: standard Dev
Container `features` or a Dockerfile on the base workbench image, and
workbench settings under `customizations.cvu`:

```jsonc
{
  "image": "ghcr.io/cleverunicornz/runner-images/interactive-workbench",
  "features": { "ghcr.io/devcontainers/features/go:1": {} },
  "customizations": { "cvu": {
    "services": [ { "name": "db", "command": "docker compose up db" } ],
    "caches": [ "~/.gradle" ],
    "size": "xl",
    "resources": { "memory": "12Gi" }
  } }
}
```

`services` start automatically per workspace, `caches` persist between
workbench restarts, `resources.memory` (up to 16 GiB) raises the tools
container.
