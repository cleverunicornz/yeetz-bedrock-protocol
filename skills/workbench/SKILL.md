---
name: workbench
description: Run heavy or interactive work on the repository's shared workbench - builds, clippy, filtered tests, lint, dev servers, docker compose stacks, Testcontainers, a Playwright browser, preview URLs, a desktop view. Covers when to use it, choosing each command's time (60 to 600 seconds), the workbench MCP tools for Claude Code and Codex, NOOA's tools and the HTTP fallback, sizes (normal and xl), and adding tools through the repository's devcontainer. Read it before compiling, testing, or starting servers.
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

- Reading, searching, editing, and git stay in the repo pod.
- **You choose every command's time: 60 to 600 seconds.** Pick what the
  command needs plus a margin: 60 for quick checks (`cargo clippy` on one
  crate, `pnpm tsc --noEmit`, a filtered `cargo nextest run <filter>`,
  `uv run pytest -k <expr>`, `ruff check`), more for builds and larger
  suites. At that time the command and everything it started are killed;
  other agents' commands, your services, and the workbench keep running.
- Work longer than 600 seconds (full suites, release builds, benchmarks) goes
  to CI as one job (`ci-runners`), not as many pieces.
- `cargo clippy -- -D warnings` is a compile sanity check: it must compile.
  Fix lints that are cheap and correct; leave code readable.

## How

Before every command and service start your worktree is synced: tracked and
untracked non-ignored files, changes only, deletions included. Ignored
directories (`target/`, `node_modules/`, `.venv/`) are never synced: install
dependencies on the workbench (`pnpm install`, `uv sync`). Git history is not
there.

**Claude Code and Codex: the `workbench` MCP tools** (already configured):

- `open(size?)`: opens the workbench (waits while it is queued or starting)
  and returns your workspace and ports. `size: "xl"` only for full stacks.
- `run(cmd, timeout_seconds)`: `timeout_seconds` is required, an integer from
  60 to 600. Returns `exit_code`, `timed_out`, `memory_exceeded`, parsed
  compiler and test diagnostics, and the last 200 lines of output with a note
  of what was cut; filter noisy commands with `| tail` or `| grep`.
- `service_start(name, command)`, `service_logs(name, tail?)`,
  `service_stop(name)`: long-lived processes (dev servers,
  `docker compose up`).
- `url(port)`: the local address for the browser and the preview URL for
  people.
- `desktop()`: a live desktop with a visible Chromium that people can watch.
- `status()`: idle time, running commands, limits, disk, services.
- `playwright_browser_*`: the workspace's Playwright browser tools (navigate,
  snapshot, click, ...); add `visible: true` to drive the desktop's Chromium.

**NOOA**: the same through `self.workbench`: `open(size=...)`, `run(cmd,
timeout=...)`, `service_start/stop/logs`, `url(port)`, `browser(visible=...)`,
`desktop()`, `status()`.

**Fallback for any harness without the MCP tools**: the workbench shim on
`127.0.0.1:8099`; `cwd` is your worktree path; `timeout_s` follows the same
60 to 600 rule:

```sh
W=127.0.0.1:8099; CWD=$(git rev-parse --show-toplevel)
curl -s -XPOST $W/v1/open -d "{\"cwd\":\"$CWD\"}"                 # add ,"size":"xl" for xl
curl -sN -XPOST $W/v1/run -d "{\"cwd\":\"$CWD\",\"cmd\":\"cargo nextest run parser\",\"timeout_s\":240}"
curl -s -XPOST $W/v1/service -d "{\"cwd\":\"$CWD\",\"name\":\"web\",\"command\":\"pnpm dev --port \$PORT --host 127.0.0.1\"}"
curl -s "$W/v1/service/logs?cwd=$CWD&name=web&tail=50"
curl -s -XDELETE $W/v1/service -d "{\"cwd\":\"$CWD\",\"name\":\"web\"}"
curl -s "$W/v1/url?cwd=$CWD&port=<port>"
curl -s -XPOST $W/v1/desktop -d "{\"cwd\":\"$CWD\"}"
curl -s "$W/v1/status?cwd=$CWD"
```

`run` streams NDJSON: `{"t":"o"|"e","d":...}` output, then `{"t":"exit",...}`
(`exit_code`, `timed_out`, `memory_exceeded`), then
`{"t":"summary","diagnostics":[...]}`.

- Ports: `$PORT` is the first port of your range; use anything in the range
  except the last three, which belong to the browser tools. Bind servers to
  `127.0.0.1` or `0.0.0.0`.
- Services are exempt from the command time and live until stopped or the
  workbench stops. Background processes started inside `run` end with it.
- The browser uses local addresses (`http://127.0.0.1:<port>`); the preview
  URL is for people.
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
