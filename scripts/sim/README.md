---
title: scripts/sim — contributor PTY harness
category: contributor-tooling
component: simulation
status: active
version: 0.2.0
last_updated: 2026-11-07
tags: [simulation, pty, evidence, ff-006c, contributor-tooling]
priority: medium
---

# scripts/sim — contributor PTY harness

Optional, contributor-side Python 3.9+ stdlib PTY harness that drives
a synthetic persona (`careful-beginner`, or `second-try` for the Stage 2 and
4 gates) through one stage, or all five stages, of `shelltutor` and
produces a v1 evidence bundle per run. Slice 1 and
FF-006c rung 1 of `docs/simulation-design-plan.md`.

This harness is **not** part of `make verify`. The runtime tutor is
bash-only; the harness is contributor tooling and exists so reviewers
can compare transcripts before and after each work package.

## Quick start

```sh
make sim                                    # --stage all, current-rc
make lesson-flow                            # Stage 1 only, current-rc
python3 scripts/sim/run.py --stage 3 --variant current-rc -v
python3 scripts/sim/run.py --stage all -v
python3 scripts/sim/compare.py <bundle-A> <bundle-B>   # before/after diff
```

Default output: `audit/<UTC-date>/sim/stage<N>/` or `.../sim/all/`, each
holding `current-rc/`. Needs a real pseudo-terminal; inside an
agent sandbox `pty.openpty` can fail (exit 6) — run it outside the sandbox.

## What it does

1. Allocates a fresh pseudo-terminal via `pty.openpty()`.
2. `fork()`s and `execvpe()`s the tutor under that PTY.
3. Drives the chosen persona through the requested stage(s)
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
   TAP `ok` requires `gate_passed` and `progress_ok` (and, for
   `second-try`, exactly one `Almost — you still need to`).

Controlled inputs (decision D-03), recorded in `summary.md`: `LC_ALL=C`,
`VIMINIT='set nocompatible'`, `PAGER=less`, `MANPAGER` and `LESS` unset,
`TERM` (default `xterm-256color`), `COLUMNS`/`LINES` from the PTY
geometry, and an empty per-run `HOME` so a pre-existing `~/.shelltutor`
cannot hide defects. Everything else is inherited and listed as a host
input. Recorded paths are repository-relative (D-15).

One variant exists, `current-rc` — the production script as learners run
it. The `no-system-rc-preview` variant and its `diff.md` were retired in
Slice 2: the practice shell no longer sources the system bashrc (contract
C-007), so there is nothing for it to isolate. `--variant no-system-rc-preview`
and `--variant both` exit 2 with a retirement message. Use `compare.py` for
before/after comparisons between two bundles.

## Personas

Two personas. `careful-beginner` covers all five stages; `second-try`
covers the Stage 2 and Stage 4 gates only.

- `careful-beginner` — types the print-and-exit commands each lesson
  lists and drives full-screen programs only where the lesson is about
  them (`man ls` in 5.1, `vim` in 5.2, 5.3 and the Stage 5 gate). It never
  improvises. If `man` is absent the 5.1 pager steps are skipped
  (`skip-man-missing`); if `vim` is absent a Stage 5/`all` run does not
  start (exit 8, `# SKIP` TAP line).

- `second-try` (`--persona second-try --stage 2|4`; any other stage exits
  2) — walks the stage as `careful-beginner` does, but fails the first
  `check` of the gate task on purpose to observe the first rung of the
  gate's escalating feedback (WP-05, decision D-14):
  - Stage 2 task: `mkdir practice`, `check` → wait for `ALMOST`
    (`Almost — you still need to`) → `cd practice`, `pwd`, `check` →
    `S2_CLEARED`.
  - Stage 4 task: `seq 1 100 | wc -l > count.txt`, `check` → `ALMOST` →
    `ls *.txt`, `check` → `S4_CLEARED`.
  - Recall answers are the same as `careful-beginner`'s. TAP `ok` requires
    the stage cleared and exactly one `Almost — you still need to` in the
    output; zero or two means the gate's feedback changed.

`confused-novice` and confusion events remain deferred (Slice 3) per the
design plan.

## Files

| File | Purpose |
| --- | --- |
| `run.py` | CLI entry; argparse, persona dispatch, run orchestration, summary writer. |
| `driver.py` | PTY driver loop (pty + selectors). |
| `selftest_modules.py` | Self-test for module persona tables (expansion and a fake-tutor drive). |
| `compare.py` | Unified diff of two bundles' normalized OUT projection. |
| `project.py` | Shared `terminal.jsonl` OUT projection (run.py, compare.py). |
| `persona.py` | careful-beginner walks for stages 1–5 and the finale; second-try for stages 2 and 4. |
| `sentinels.py` | Stable substring patterns per screen / question. |
| `recorder.py` | terminal.jsonl, events.jsonl, summary.md, result.tap writers. |
| `env.py` | Host snapshot + CRLF/ANSI normalization helpers. |
| `errors.py` | Typed exceptions per the dispatcher exit code table. |

## Modules

A stand-alone module is driven from a small table in
`persona.MODULE_TABLES` (`lessons` count plus a `gate` of `recall` answers
and `task` commands, and optionally `lesson_actions` — commands typed at
lesson k's prompt — and `prompt_after` — the prompt text expected after
lesson k's `next`), expanded by `persona.module_walk()`. The sentinels
come from the module heading convention, so none are registered per
module: intro `MODULE — <name>:`, lessons `<name> <k> — `, gate
`<name> — gate`, task `<name> — task`, cleared `✓ <name> cleared.`. The run execs
`shelltutor <name>`, expects `.progress` to stay absent (modules never save
progress), and writes under `audit/<date>/sim/module-<name>/`. No module
exists yet, so the table is empty.

`python3 scripts/sim/selftest_modules.py` (exit 0 or 1, stdlib, Python 3.9)
checks the expansion and drives a fake tutor that follows the heading
convention through `run.py --module`; the drive needs a pseudo-terminal and
is skipped with a message when none is available.

## Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | The run is green (`gate_passed` and `progress_ok`, plus one `ALMOST` for `second-try`). |
| 1 | Uncaught exception (traceback printed). |
| 2 | Unsupported persona / stage / flag. |
| 3 | retired (Slice 2; formerly `PatchTargetMissingError`). The number is kept so later codes do not move. |
| 4 | `SentinelNotFoundError` — sentinel missed within the per-sentinel timeout. |
| 5 | `PersonaRejectedError` — gate re-asked a question. |
| 6 | `NoTTYError` — `pty.openpty` failed. |
| 7 | `SandboxNotWritableError` — tempdir creation failed. |
| 8 | `PrerequisiteMissingError` — `vim` absent for `--stage 5`/`all`; TAP carries `# SKIP`. |

## CLI flags

| Flag | Default |
| --- | --- |
| `--variant current-rc` | `current-rc` (`no-system-rc-preview` and `both` were retired in Slice 2 and exit 2) |
| `--persona` | `careful-beginner` (or `second-try` with `--stage 2` or `4`) |
| `--stage {1,2,3,4,5,all}` | `1` when neither `--stage` nor `--module` is given |
| `--module <name>` | none; drives a stand-alone module from its table in `persona.MODULE_TABLES` (exclusive with `--stage`, exit 2 if both or if the module has no table) |
| `--out` | `audit/<UTC-date>/sim/stage<N>` or `.../sim/all` |
| `--timeout` | `30` (per-sentinel, seconds) |
| `--cols` / `--rows` | `80` / `24` |
| `--shelltutor` | `./shelltutor` |
| `--keep-sandbox` | off — fresh `SHELLTUTOR_HOME` and empty `HOME` tempdirs are removed after the run |
| `-v` / `--verbose` | off |

## Evidence

Each run writes `terminal.jsonl`, `events.jsonl`, `summary.md` and
`result.tap`. The harness cannot control `whoami`, so the host login name
would reach all of them; under decision D-19 the recorder treats it as a
host input, like temp paths, and replaces it with the fixed token `[user]`
before anything is written. The redaction covers terminal chunks (including
base64 rows and a name split across two reads), every string in
`events.jsonl` (the `answer-task-whoami` input included) and `summary.md`,
and it applies to the hosted runner's `runner` the same way. It affects only
what is written: the live stream the driver matches against is untouched.
`summary.md` records the choice under "Controlled inputs" as
`host_user: redacted as [user]`, or `host_user: not redacted (name too
short)` for names under three characters. Bundles committed before D-19 are
not rewritten.

The driver also records, per cleared screen, a `screen-height` event and a
"Screen heights" table in `summary.md`: the rendered lines between a clear
and the next practice prompt (blank line and practice footer included)
against a budget of 22 rendered lines, which equals the script's stated 20
content lines (heredoc 20 plus the blank line `show_screen` adds plus the
footer), so a 24-row terminal still shows the prompt. It is informational
only and never changes the TAP result or an exit code; gate recall screens
end without a prompt and are not measured.

## Hosted Linux evidence intake

The `sim-evidence` workflow (`.github/workflows/sim-evidence.yml`) runs
`run.py --stage all --variant current-rc` on `ubuntu-24.04` and uploads
the bundle as the artifact `sim-evidence-<sha>` (30-day retention). It
runs on `workflow_dispatch` and on push to `main`. It is evidence
capture, not a gate: the walk step has `continue-on-error`, so a green
workflow run does **not** mean a green bundle. The operator reviews each
artifact by hand and commits it deliberately:

1. Download the artifact for the run. The archive holds `current-rc/`
   (the `--out sim-out` directory contents).
2. Read `summary.md` and `events.jsonl`; confirm `gate_passed=true` and
   `progress_after=absent` and that `result.tap` is `ok`. List any
   `error-signature` events. A `skip-man-missing` intent or a `MAN_LS`
   timeout means `man` is absent on the runner: add
   `sudo apt-get update && sudo apt-get install --no-install-recommends -y man-db`
   before the walk and note that in the summary.
3. Check the bundle for operator-private content with the command below,
   run from the repository root. The harness records repo-relative paths
   and tempdirs only. The `grep -v` removes the one expected hit: lesson
   2.3 prints a fictional absolute path under a made-up user's home as a
   teaching example, so it appears in every bundle's terminal log.

```sh
grep -rn '/home/' <bundle> | grep -v '/home/alice/notes.txt'
```

4. Copy the bundle to `audit/<UTC-date>/sim/all-linux/current-rc/` and add
   a two-line "Provenance" section to that directory's `summary.md`: the
   run id and runner image, and the Bash version (`summary.md` records it
   as `bash_version`; the "Record host inputs" log shows it too).
5. Commit it as
   `chore(audit): Linux five-stage evidence from hosted run <run-id>`.
6. Compare against the same-revision macOS bundle with
   `python3 scripts/sim/compare.py audit/<date>/sim/all/current-rc audit/<date>/sim/all-linux/current-rc`;
   record any divergence signature in `audit/<date>/findings.md` as an
   observation.

Only synthetic harness bundles are committed; never a human transcript.

## Boundaries

- Python 3.9+ stdlib only. No third-party deps. No Pexpect.
- Not part of `make verify`. Runtime tutor stays bash-only.
- Synthetic evidence may be committed (`audit/<date>/sim/`); real
  human transcripts must not be committed (see
  `docs/simulation-design-plan.md` §Evidence Locations).
