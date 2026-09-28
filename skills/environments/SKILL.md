---
name: environments
description: How applications are tested beyond unit tests and how they get staging, per-PR test and production environments on the organization's Kubernetes platform - Testcontainers for integration tests, one set of Kubernetes manifests per application, deploying through pull requests, and resource budgets that a human sets and the repository's AGENTS.md records. Read it before writing integration tests, deployment manifests, or anything that needs a running environment.
---

# environments

## Testing layers

1. **Unit tests** run in the repository's normal test runner.
2. **Integration tests** start the real dependencies they need (Postgres, S3,
   the Matrix homeserver, the identity provider) with **Testcontainers** from
   the test code and throw them away afterwards. They run on the workbench
   (`workbench`) or in CI on a runner with Docker (`ci-runners`). Docker
   Compose is not used for tests or deployments.
3. **Full-system tests** run against a deployed environment (below), driven by
   end-to-end tests such as Playwright.

Use the organization's own services as dependencies (for Matrix, poda-chat),
not third-party stand-ins, when the repository says so.

## Environments

- **Staging:** one long-lived environment per product, running the latest
  merged version of its applications together; reachable only on the tailnet.
- **Per-PR test environment:** short-lived, one per pull request, removed
  when the pull request closes.
- **Production:** you observe it read-only (logs, metrics, status). You never
  change it directly.

Every application keeps **one** set of Kubernetes manifests in its own
repository: `deploy/k8s/base/` plus one overlay per environment
(`deploy/k8s/staging/`, `deploy/k8s/pr/`, `deploy/k8s/production/`). The same
manifests deploy every environment. You deploy by changing manifests in a pull
request; the platform applies merged changes. You do not apply manifests to
shared environments yourself.

## Budgets: a human decides, AGENTS.md records

Every environment has a memory budget in **units** (1 unit = 5 GiB; memory
request = limit; CPU is shared). You never choose a budget yourself.

1. Read the repository block of the root `AGENTS.md` for the environment
   settings: units per environment, dependencies, and the environment's
   address.
2. If a value you need is missing, **stop and ask the human**. Recommend a
   value with its reasoning, and wait for confirmation.
3. Record the confirmed values in the repository block through a pull
   request. From then on every agent uses them.
4. If a deployment fails for lack of room (out of memory, quota exhausted),
   do not raise the budget. Report the failure to the human with a proposed
   new value; after confirmation, update the repository block the same way.

## When the platform cannot do it yet

If the environment you need does not exist on the platform, open an issue in
`cleverunicornz/infra-v2` describing the application, the environment and the
budget the human confirmed, and link it from your work.
