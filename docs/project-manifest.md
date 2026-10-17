---
title: Project declaration and contributor verification
category: reference
component: project-interface
status: active
version: 0.1.0
last_updated: 2026-10-17
tags: [manifest, contributors, verification]
priority: medium
---

# Project declaration and contributor verification

`project.yaml` follows Specification 1 from
[project-manifest Release 1](https://github.com/jefahnierocks/project-manifest/releases/tag/release-1).
It is the one project declaration for inventory and workstation consumers.
`STATUS.md` remains the detailed status of record. Declaration values neither
execute commands nor prove a deployment, producer admission or runtime acceptance.

The repo owns the offline binding in `scripts/check-project-manifest.py`:

| Binding | Exact value |
| --- | --- |
| Release source | `56e3920089726e585eaa0fd7f4dc94e6938a1e0c` |
| Domain-separated release-table digest | `f7ff9dd0972af5d3a6a3348c3e092de1a6acd97fa3975e13e522cf80ce5e7df2` |
| Separate bootstrap SHA-256 | `2ccf58e0da97bbbd9dae173d1cca047d465c4a2d950ee6e56052309a9689cf4f` |

The twenty-file payload plus descriptor live in `vendor/project-manifest/release-1/`.
The separately pinned bootstrap is `vendor/project-manifest/release_verifier.py`.
These are unmodified public MIT artifacts, with the license retained. That license
does not decide shelltutor's still-deferred product license. Git attributes protect
their literal bytes and the root manifest's LF representation. Re-vendoring is a
reviewed project change, not an automatic dependency update.

## Contributor entrypoint

Prepare Python 3.11+ and Git 2.56+ outside the gate, then run `make verify` or
`scripts/verify-project.sh`. The latter takes no arguments and delegates to Make.
The gate uses no network and installs nothing. A selected interpreter can be passed
as `PYTHON=/absolute/path/to/python3`; put prepared Git first on a command-scoped
`PATH`. Never change global runtimes to satisfy this repo.

`make verify` checks the independently bound release, the declaration and consumer
regressions, then preserves the existing static, optional ShellCheck and smoke
checks. `make self-test` still exercises the four native checkers. Python/Git are
contributor tools only: a learner still runs `./shelltutor` with Bash/POSIX tools.
The optional PTY harness retains its separate Python 3.9+ floor and its existing
non-gating status. The five-stage human portability walks remain separate.

The declaration maps only `check` to the executable wrapper. Setup/build/dev/test/
format roles are null rather than inventing commands; native checker self-tests
remain available through Make. Activation is `none`, with no secrets, stacks or
host requirements. Empty platforms makes no architecture qualification claim.

## Observation selection

No arguments selects tracked working bytes. A newly added target must be in the
index before Git can include it in this observation. Direct staged checking uses:

```bash
python3 -I -S -B scripts/check-project-manifest.py --staged
```

For a linked worktree, explicitly provide its reviewed Git common directory with
`--git-common-dir /absolute/common/directory`, or set `SHELLTUTOR_GIT_COMMON_DIR`
for `make verify`. No other checkout is inferred or searched. Inherited Git
overrides are refused; the gate never silently removes them.

`--rev FULL_COMMIT_OID`, or `SHELLTUTOR_MANIFEST_REV` for Make/CI, checks the
declaration and references in that commit's tree. Native checks still execute the
current checkout; a revision selector does not certify a historical native gate.
Each observation uses one captured UTC date. Exit 0 means the released declaration
checks and this repo's expected command/activation shape passed; exit 1 means an
invalid declaration, binding mismatch or shape disagreement; exit 2 means a check
could not run. The JSON keeps declaration, native-shape and runtime claims separate.

## Hosted preparation

The new `verify` workflow is a source proposal until its first actual hosted run
passes. It uses Ubuntu 24.04, explicitly selected Python 3.13.16 from setup-python,
and the Git-only `scripts/prepare-ci-git.py`. Preparation downloads Git 2.56.0 from
the fixed kernel.org URL, checks its pinned official HTTPS SHA-256, and builds into
one fresh runner-owned temporary prefix with no Rust or install hardlinks. It does
not install a Python floor, Gitleaks or project dependencies. Compiler/zlib build
prerequisites are prepared explicitly in the ephemeral runner. This is not a tar
signature verification claim.

Only the verification step prepends that Git to PATH. `make verify` receives the
explicit prepared Python and full GitHub commit OID. Both push and pull_request
run without branch/path filters; the job is named `verify`. Workflow existence does
not prove effective required checks. Actual hosted qualification and protection
readback are recorded separately before landing/enforcement claims.
See [the current qualification status](../STATUS.md) for completed and pending
checks.
