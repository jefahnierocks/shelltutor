---
title: scripts/sim — contributor PTY harness
category: contributor-tooling
component: simulation
status: active
version: 0.1.0
last_updated: 2026-11-07
tags: [simulation, pty, evidence, ff-006c, contributor-tooling]
priority: medium
---

# scripts/sim — contributor PTY harness

Optional, contributor-side Python 3.9+ stdlib PTY harness that drives
the `careful-beginner` persona through one stage, or all five stages,
of `shelltutor` and produces a v1 evidence bundle per run. Slice 1 and
FF-006c rung 1 of `docs/simulation-design-plan.md`.

This harness is **not** part of `make verify`. The runtime tutor is
bash-only; the harness is contributor tooling and exists so reviewers
can compare transcripts before and after each work package.

## Quick start

```sh
make sim                                    # --stage all, both variants
make lesson-flow                            # Stage 1 only, both variants
python3 scripts/sim/run.py --stage 3 --variant current-rc -v
python3 scripts/sim/run.py --stage all --variant no-system-rc-preview -v
python3 scripts/sim/compare.py <bundle-A> <bundle-B>   # before/after diff
```

Default output: `audit/<UTC-date>/sim/stage<N>/` or `.../sim/all/`, each
holding `{current-rc,no-system-rc-preview}/` plus a top-level `diff.md`
when `--variant both` is used. Needs a real pseudo-terminal; inside an
agent sandbox `pty.openpty` can fail (exit 6) — run it outside the sandbox.

## What it does

1. Allocates a fresh pseudo-terminal via `pty.openpty()`.
2. `fork()`s and `execvpe()`s the tutor under that PTY.
3. Drives the careful-beginner persona through the requested stage(s)
   by waiting for stable substring sentinels and writing the next input
   on each match. `--stage N` (N ≥ 2) execs `shelltutor N` (C-001);
   `1` and `all` run with no argument.
4. Records every PTY chunk to `terminal.jsonl`, every sentinel match
   and persona input to `events.jsonl`, and a summary to `summary.md`
   plus a one-line TAP result to `result.tap`.
5. Scans practice-shell output after persona input on lesson screens for
   `No such file or directory`, `command not found`, `: not found`,
   `Permission denied`, `syntax error` and `Is a directory`; each hit is
   a non-fatal `error-signature` event listed in `summary.md`.
6. Reads `.progress` before sandbox cleanup: stages 1–4 expect the stage
   number, stage 5 and `all` expect it absent (the finale removes it).
   TAP `ok` requires `gate_passed` and `progress_ok`.

Controlled inputs (decision D-03), recorded in `summary.md`: `LC_ALL=C`,
`VIMINIT='set nocompatible'`, `PAGER=less`, `MANPAGER` and `LESS` unset,
`TERM` (default `xterm-256color`), `COLUMNS`/`LINES` from the PTY
geometry, and an empty per-run `HOME` so a pre-existing `~/.shelltutor`
cannot hide defects. Everything else is inherited and listed as a host
input. Recorded paths are repository-relative (D-15).

Two back-to-back baselines are produced by default:

- `current-rc` — the production script as learners run it.
- `no-system-rc-preview` — a harness-generated patched copy in a
  tempdir with the `/etc/bashrc` source line replaced by a
  provenance comment. **Diagnostic only**; not a production code
  path.

`diff.md` carries the unified diff of the OUT-direction UTF-8 chunks
between the two variants — input to the Slice 2 hardening decision.

## Persona scope

One persona, five stages:

- `careful-beginner` — types the print-and-exit commands each lesson
  lists and drives full-screen programs only where the lesson is about
  them (`man ls` in 5.1, `vim` in 5.2, 5.3 and the Stage 5 gate). It never
  improvises. If `man` is absent the 5.1 pager steps are skipped
  (`skip-man-missing`); if `vim` is absent a Stage 5/`all` run does not
  start (exit 8, `# SKIP` TAP line).

Other personas (`confused-novice`, `second-try`) are deferred per the
design plan.

## Files

| File | Purpose |
| --- | --- |
| `run.py` | CLI entry; argparse, variant orchestration, summary/diff writers. |
| `driver.py` | PTY driver loop (pty + selectors). |
| `compare.py` | Unified diff of two bundles' normalized OUT projection. |
| `project.py` | Shared `terminal.jsonl` OUT projection (run.py, compare.py). |
| `persona.py` | careful-beginner walks for stages 1–5 and the finale. |
| `sentinels.py` | Stable substring patterns per screen / question. |
| `recorder.py` | terminal.jsonl, events.jsonl, summary.md, result.tap writers. |
| `patcher.py` | no-system-rc-preview substitution. |
| `env.py` | Host snapshot + CRLF/ANSI normalization helpers. |
| `errors.py` | Typed exceptions per the dispatcher exit code table. |

## Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | Every requested variant green (`gate_passed` and `progress_ok`). |
| 1 | Uncaught exception (traceback printed). |
| 2 | Unsupported persona / stage / flag. |
| 3 | `PatchTargetMissingError` — `/etc/bashrc` source line absent or non-unique. |
| 4 | `SentinelNotFoundError` — sentinel missed within the per-sentinel timeout. |
| 5 | `PersonaRejectedError` — gate re-asked a question. |
| 6 | `NoTTYError` — `pty.openpty` failed. |
| 7 | `SandboxNotWritableError` — tempdir creation failed. |
| 8 | `PrerequisiteMissingError` — `vim` absent for `--stage 5`/`all`; TAP carries `# SKIP`. |

## CLI flags

| Flag | Default |
| --- | --- |
| `--variant {current-rc,no-system-rc-preview,both}` | `both` |
| `--persona` | `careful-beginner` (only one supported) |
| `--stage {1,2,3,4,5,all}` | `1` |
| `--out` | `audit/<UTC-date>/sim/stage<N>` or `.../sim/all` |
| `--timeout` | `30` (per-sentinel, seconds) |
| `--cols` / `--rows` | `80` / `24` |
| `--shelltutor` | `./shelltutor` |
| `--keep-sandbox` | off — fresh `SHELLTUTOR_HOME` and empty `HOME` tempdirs are removed after each variant |
| `--keep-patched-script` | off — preview tempdir is removed after the preview run |
| `-v` / `--verbose` | off |

## Boundaries

- Python 3.9+ stdlib only. No third-party deps. No Pexpect.
- Not part of `make verify`. Runtime tutor stays bash-only.
- Synthetic evidence may be committed (`audit/<date>/sim/`); real
  human transcripts must not be committed (see
  `docs/simulation-design-plan.md` §Evidence Locations).
