---
name: workbench
description: Run heavy or interactive work on the repository's shared workbench - builds, clippy, filtered tests, lint, dev servers, docker compose stacks, Testcontainers, a Playwright browser, preview URLs, a desktop view. Covers when to use it, commands that run until they end with calls that wait at most 600 seconds, reading the whole output, the workbench MCP tools for Claude Code and Codex, NOOA's tools and the HTTP fallback, sizes (normal and xl), and adding tools through the repository's devcontainer. Read it before compiling, testing, or starting servers.
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
- **A command runs until it ends.** No command has a time limit unless you
  set `deadline_seconds`; leave it out unless you want the command stopped at
  that time. Only `cancel(run_id)` or your `deadline_seconds` stops a command.
- **A call waits at most `wait_seconds`**: 120 by default, at most 600. When
  the wait ends first, the answer says `running`, with the `run_id` and the
  output so far, and the command goes on. Call `wait(run_id)` again as often
  as the work needs. For long work (full suites, release builds, benchmarks)
  `start` it and `wait` for it. CI stays the receipt for a pull request
  (`ci-runners`).
- A running command's `status` shows its last output and CPU use. After 10
  minutes with neither it is flagged `stalled`: look at it and decide whether
  to cancel; it is never stopped for that.
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
- `run(cmd, wait_seconds?, deadline_seconds?)`: runs the command and waits
  up to `wait_seconds` (default 120, at most 600). Finished: `exit_code`,
  `memory_exceeded`, whether your deadline or a cancel stopped it, parsed
  compiler and test diagnostics, and its output. Still going: `running` and
  its `run_id`.
- `start(cmd, deadline_seconds?)`: starts a command and answers with its
  `run_id` at once. `wait(run_id, wait_seconds?)` waits again and returns the
  output since the previous wait. `status(run_id)`, `cancel(run_id)`, and
  `runs()` list your workspace's runs.
- **Output is never lost.** Every byte of a run's output is kept. An answer
  carries at most 30,000 characters. A longer output comes as its start and
  its end, with the cut positions stated. `output(run_id, start, length)`
  reads any part by byte position.
- `service_start(name, command)`, `service_stop(name)`: long-lived processes
  (dev servers, `docker compose up`). `service_logs(name, tail?)` gives the
  last lines. `service_logs(name, from)` gives the whole log from a byte
  position, at most 30,000 characters a call, with the position to read next.
- `url(port)`: the local address for the browser and the preview URL for
  people.
- `desktop()`: a live desktop with a visible Chromium that people can watch.
- `status()`: idle time, running commands, limits, disk, services.
- `playwright_browser_*`: the workspace's Playwright browser tools (navigate,
  snapshot, click, ...); add `visible: true` to drive the desktop's Chromium.

**NOOA**: the same through `self.workbench`: `open(size=...)`,
`run(cmd, wait_seconds=..., deadline_seconds=...)`, `start`, `wait`,
`status(run_id)`, `cancel`, `output`, `runs`, `service_start/stop`,
`service_logs(name, tail=..., from_=...)`, `url(port)`,
`browser(visible=...)`, `desktop()`, `status()`. A result's `output` holds
the whole output of the run so far.

**Fallback for any harness without the MCP tools**: the workbench shim on
`127.0.0.1:8099`; `cwd` is your worktree path; the same waits and deadlines:

```sh
W=127.0.0.1:8099; CWD=$(git rev-parse --show-toplevel)
curl -s -XPOST $W/v1/open -d "{\"cwd\":\"$CWD\"}"                 # add ,"size":"xl" for xl
curl -s -XPOST $W/v1/runs -d "{\"cwd\":\"$CWD\",\"cmd\":\"cargo nextest run parser\",\"wait_seconds\":120}"
curl -s "$W/v1/runs/<run_id>/wait?cwd=$CWD&wait_seconds=600&from=<byte>"    # again while "running"
curl -s "$W/v1/runs/<run_id>/output?cwd=$CWD&start=<byte>&length=<bytes>"
curl -s -XDELETE $W/v1/runs/<run_id> -d "{\"cwd\":\"$CWD\"}"          # cancel
curl -s -XPOST $W/v1/service -d "{\"cwd\":\"$CWD\",\"name\":\"web\",\"command\":\"pnpm dev --port \$PORT --host 127.0.0.1\"}"
curl -s "$W/v1/service/logs?cwd=$CWD&name=web&tail=50"            # or &from=<byte>: the log from there
curl -s -XDELETE $W/v1/service -d "{\"cwd\":\"$CWD\",\"name\":\"web\"}"
curl -s "$W/v1/url?cwd=$CWD&port=<port>"
curl -s -XPOST $W/v1/desktop -d "{\"cwd\":\"$CWD\"}"
curl -s "$W/v1/status?cwd=$CWD"
```

`POST /v1/runs` without `wait_seconds` answers with the `run_id` at once.
With it, and on `/wait`, the answer is JSON: `state` (`running`, `done`, or
`lost` when the workbench stopped under it), `run_id`, `output` (`text`,
`from`, `to`, `cut`, `path`), and when done `exit` and `diagnostics`.

- Ports: `$PORT` is the first port of your range; use anything in the range
  except the last three, which belong to the browser tools. Bind servers to
  `127.0.0.1` or `0.0.0.0`.
- Services live until stopped or the workbench stops. Background processes
  started inside a command end with that command.
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
