---
title: shelltutor Phase 2 Walkthrough Checklist
category: planning
component: phase2-checklist
status: active
version: 0.2.0
last_updated: 2026-11-07
tags: [phase2, portability, walkthrough, manual-validation]
priority: medium
---

# Phase 2 Walkthrough Checklist

Operator-facing checklist for the ROADMAP Phase 2 portability
validation. The PTY harness automates a deterministic walkthrough
(`careful-beginner` through all five stages with `make sim`, FF-006c rung 1,
plus a `second-try` persona for the Stage 2 and 4 gates); Phase 2 closure
still needs a **human** walking the full five-stage course on real
terminals, because the harness exercises a synthetic persona, not a human
reader who can react to UX rough edges.

## Closure matrix

Per `docs/simulation-design-plan.md` §Phase 2 Relationship, Phase 2
closes when all rows below are recorded. Each row gets a single
line in `STATUS.md` under "What Is True Now" with the date, host
identification (OS/version/arch), and the observed outcome.

| Surface | Required | Notes |
| --- | --- | --- |
| macOS stock `/bin/bash` 3.2.57, all five stages | yes | The project's tagline-supported platform. Apple Silicon and Intel both count; record which. |
| Debian/Ubuntu-family Bash 5.x, all five stages | yes | Any current Debian/Ubuntu release suffices. Record release name. |
| Fedora-family Bash 5.x, all five stages | optional | Useful but not required for Phase 2 closure. |
| No-TTY negative test | yes | Single command; see below. |

## How to run a stage walkthrough

For each platform, in a fresh terminal:

0. Invoke the tutor with the Bash under test explicitly: for Bash 3.2 on
   macOS run `/bin/bash ./shelltutor`. A bare `./shelltutor` resolves its
   `#!/usr/bin/env bash` shebang through `PATH`, so it runs whichever
   `bash` is first there. The practice shell is always the same binary as
   the outer script (`$BASH`, C-007), so at the first practice prompt run
   `echo $BASH_VERSION` and record the value in the STATUS line.
1. Run `./shelltutor --info` first and note any `not ok` line (bash
   version, writable sandbox, `/dev/tty`, `vim`/`vimtutor`). It prints the
   environment check before any lesson screen renders.
2. Start the course with a clean sandbox so the walkthrough doesn't inherit
   prior progress:

```bash
SHELLTUTOR_HOME=/tmp/shelltutor-phase2-$(date +%s) ./shelltutor
```

Walk each stage through to its gate-task verification. Record per
stage:

1. **Renders cleanly** — no truncated lines, no missing color
   sequences, no obvious vertical-budget overrun.
2. **Practice prompt works** — `next`, `prev`, `show`, `quit`, and
   `check` (at gates) behave per `docs/contracts.md` C-002.
3. **Gate task passes** — recall Q&A and filesystem-checked task
   both clear without unexpected failure modes.
4. **Stage cleared** message appears.

If a stage fails on a platform, capture: bash version, OS/distro,
stage number, observed failure, and stop the walkthrough for that
platform. Open a finding in `audit/<date>/findings.md` (see F-008
template).

## The five stages

Stage 1 has four lessons (1.1 running commands, 1.2 keyboard habits,
1.3 where/who/when, 1.4 what just happened); the others have three or
four as their intro screens say.

| # | Stage | Gate-task surface |
| --- | --- | --- |
| 1 | Where am I? | run `whoami`, `pwd`, `date`; answer three follow-ups. The day may be typed as `date` printed it in your locale (`Sat`, `Sa.` and `Saturday` all count). |
| 2 | Paths and the filesystem | create `$SANDBOX/stage2/practice/`, `cd` into it (the gate looks for a `cd` in your practice history), confirm with `pwd`. |
| 3 | Files and operations | inside `$SANDBOX/stage3/`, create `notes.txt` containing "hello", copy → `backup.txt`, rename `notes.txt` → `done.txt`, remove `backup.txt`. |
| 4 | Commands, streams, composition | inside `$SANDBOX/stage4/`, `seq 1 100 \| wc -l > count.txt`; list the `*.txt` glob (the gate looks for the glob in your practice history). |
| 5 | Ready for vimtutor | inside `$SANDBOX/stage5/`, edit `practice.txt`: first phase quits without saving (`:q!`); second phase saves (`:wq`). |

Where the practice prompt starts: stages 1 and 2 start in `$SANDBOX`
(the Stage 1 gate task starts in `$SANDBOX/stage1`); stages 3 to 5 start in
their stage folder for lessons and gates (`docs/contracts.md` C-003).

Gate feedback while walking: a first failed `check` shows what the gate saw;
a second adds a hint; a third adds a worked example the learner still types
themselves. A gate never passes on repeated failure alone. Record a stage as
failed only if the gate rejects a correct attempt, not if you exercised the
hints on purpose.

## No-TTY negative test

A core constraint: the tutor must refuse to run when stdin/stdout
isn't a real terminal, and it must do so with a clear diagnostic
(not a crash, not a hang).

Run, from any platform:

```bash
./shelltutor < /dev/null > /tmp/shelltutor-no-tty.log 2>&1
echo "exit=$?"
cat /tmp/shelltutor-no-tty.log
```

Expected: exit code 1 and a stderr message naming the missing TTY
(per the script's `preflight()` function). The log file must NOT
contain lesson copy — the tutor must bail in preflight, not begin
rendering lessons against a pipe.

A second variant, simulating a CI environment:

```bash
bash -c './shelltutor' < /dev/null 2>/tmp/shelltutor-cron.log
echo "exit=$?"
cat /tmp/shelltutor-cron.log
```

Same expected outcome.

## How to record results

For each platform, append a single line to `STATUS.md` under
"What Is True Now":

```markdown
- **Phase 2 walkthrough**: <platform identifier>, bash <version>,
  all five stages cleared cleanly on <YYYY-MM-DD>. No-TTY negative
  test exits 1 with the documented preflight diagnostic.
```

Example:

```markdown
- **Phase 2 walkthrough**: macOS 15.5 Apple Silicon, bash 3.2.57,
  all five stages cleared cleanly on 2026-05-24. No-TTY negative
  test exits 1 with the documented preflight diagnostic.
```

If anything failed, write a finding in
`audit/<date>/findings.md` first, then add a single-line STATUS
entry pointing at the new `<finding-id>` and its dated findings path.

## Cross-references

- `ROADMAP.md` Phase 2 — exit criteria.
- `docs/simulation-design-plan.md` §Phase 2 Relationship — closure
  matrix.
- `docs/contracts.md` C-002, C-003 — what to verify at each gate.
- `audit/2026-05-23/findings.md` F-008 — example of how to record
  a surfaced finding (the BSD-sed bug found by the Slice 1
  harness).
- `STATUS.md` "Decision-Disagreement Rule" — STATUS is the
  current-truth landing for Phase 2 closure entries.

## What is **not** in this checklist

- License decision (Phase 4) — see `docs/license-decision.md`.
- Slice 2 hardening — see Slice 1's evidence and
  `docs/sim-slice-2-sketch.md`.
- Full re-run of the PTY harness on Linux — that is a separate
  contributor track (the non-gating `sim-evidence` workflow, FF-006c) and is
  not a Phase 2 closure gate. The human Linux walkthrough is.
