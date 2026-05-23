---
title: scripts/sim — contributor PTY harness
category: contributor-tooling
component: simulation
status: active
version: 0.1.0
last_updated: 2026-05-23
tags: [simulation, pty, evidence, slice1, contributor-tooling]
priority: medium
---

# scripts/sim — contributor PTY harness

Optional, contributor-side Python 3.9+ stdlib PTY harness that drives
the `careful-beginner` persona through Stage 1 of `shelltutor` and
produces a v1 evidence bundle. Slice 1 of
`docs/simulation-design-plan.md`.

This harness is **not** part of `make verify`. The runtime tutor is
bash-only; the harness is contributor tooling and exists so reviewers
can compare Stage 1 transcripts before and after each hardening
slice.

## Quick start

```sh
make lesson-flow                            # both variants, default out
python3 scripts/sim/run.py --variant current-rc -v
python3 scripts/sim/run.py --variant no-system-rc-preview -v
```

Default output: `audit/<UTC-date>/sim/stage1/{current-rc,no-system-rc-preview}/`
plus a top-level `diff.md` when `--variant both` is used.

## What it does

1. Allocates a fresh pseudo-terminal via `pty.openpty()`.
2. `fork()`s and `execvpe()`s the tutor under that PTY.
3. Drives the careful-beginner persona through Stage 1 by waiting for
   stable substring sentinels and writing the next input on each
   match.
4. Records every PTY chunk to `terminal.jsonl`, every sentinel match
   and persona input to `events.jsonl`, and a summary to `summary.md`
   plus a one-line TAP result to `result.tap`.

Two back-to-back baselines are produced by default:

- `current-rc` — the production script as learners run it.
- `no-system-rc-preview` — a harness-generated patched copy in a
  tempdir with the `/etc/bashrc` source line replaced by a
  provenance comment. **Diagnostic only**; not a production code
  path.

`diff.md` carries the unified diff of the OUT-direction UTF-8 chunks
between the two variants — input to the Slice 2 hardening decision.

## Persona scope

Slice 1 ships **one** persona × **one** stage:

- `careful-beginner`
- Stage 1

Other personas (`confused-novice`, etc.) and other stages are
deferred to Slice 3+ per the design plan's "First Three Slices"
sequencing.

## Files

| File | Purpose |
| --- | --- |
| `run.py` | CLI entry; argparse, variant orchestration, summary/diff writers. |
| `driver.py` | PTY driver loop (pty + selectors). |
| `persona.py` | careful-beginner Stage 1 action list. |
| `sentinels.py` | Stable substring patterns per screen / question. |
| `recorder.py` | terminal.jsonl, events.jsonl, summary.md, result.tap writers. |
| `patcher.py` | no-system-rc-preview substitution. |
| `env.py` | Host snapshot + CRLF/ANSI normalization helpers. |
| `errors.py` | Typed exceptions per the dispatcher exit code table. |

## Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | Both variants green (`gate_passed=true`). |
| 1 | Uncaught exception (traceback printed). |
| 2 | Unsupported persona / stage / flag. |
| 3 | `PatchTargetMissingError` — `/etc/bashrc` source line absent or non-unique. |
| 4 | `SentinelNotFoundError` — sentinel missed within the per-sentinel timeout. |
| 5 | `PersonaRejectedError` — gate re-asked a question. |
| 6 | `NoTTYError` — `pty.openpty` failed. |
| 7 | `SandboxNotWritableError` — tempdir creation failed. |

## CLI flags

| Flag | Default |
| --- | --- |
| `--variant {current-rc,no-system-rc-preview,both}` | `both` |
| `--persona` | `careful-beginner` (only one supported in Slice 1) |
| `--stage` | `1` (only one supported in Slice 1) |
| `--out` | `audit/<UTC-date>/sim/stage1` |
| `--timeout` | `30` (per-sentinel, seconds) |
| `--cols` / `--rows` | `80` / `24` |
| `--shelltutor` | `./shelltutor` |
| `--keep-sandbox` | off — fresh `SHELLTUTOR_HOME` tempdir is removed after each variant |
| `--keep-patched-script` | off — preview tempdir is removed after the preview run |
| `-v` / `--verbose` | off |

## Boundaries

- Python 3.9+ stdlib only. No third-party deps. No Pexpect.
- Not part of `make verify`. Runtime tutor stays bash-only.
- Synthetic evidence may be committed (`audit/<date>/sim/`); real
  human transcripts must not be committed (see
  `docs/simulation-design-plan.md` §Evidence Locations).
