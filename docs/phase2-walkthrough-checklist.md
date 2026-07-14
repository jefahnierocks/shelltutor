---
title: shelltutor Phase 2 Walkthrough Checklist
category: planning
component: phase2-checklist
status: active
version: 0.1.0
last_updated: 2026-07-14
tags: [phase2, portability, walkthrough, manual-validation]
priority: medium
---

# Phase 2 Walkthrough Checklist

Operator-facing checklist for the ROADMAP Phase 2 portability
validation. The Slice 1 PTY harness (FF-006b) automates a
`careful-beginner` Stage 1 walkthrough; Phase 2 closure still needs
a **human** walking the full five-stage course on real terminals,
because the harness exercises a deterministic synthetic persona, not
a human reader who can react to UX rough edges.

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

```bash
# Use a clean sandbox so the walkthrough doesn't inherit prior progress.
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

The script's `--info` flag prints the environment check before any
lesson screen renders; consider running it before each platform's
walkthrough.

| # | Stage | Gate-task surface |
| --- | --- | --- |
| 1 | Where am I? | run `whoami`, `pwd`, `date`; answer three follow-ups (verified via filesystem + `$(date +%a)`). |
| 2 | Paths and the filesystem | create `$SANDBOX/practice/`, navigate between it and `$HOME`. |
| 3 | Files and operations | inside `$SANDBOX/stage3/`, create `notes.txt` containing "hello", copy → `backup.txt`, rename `notes.txt` → `done.txt`, remove `backup.txt`. |
| 4 | Commands, streams, composition | inside `$SANDBOX/stage4/`, `seq 1 100 \| wc -l > count.txt`; list `*.txt` glob. |
| 5 | Ready for vimtutor | inside `$SANDBOX/stage5/`, edit `practice.txt`: first phase quits without saving (`:q!`); second phase saves (`:wq`). |

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
  contributor track (FF-006b on Linux) and is not a Phase 2
  closure gate. The human Linux walkthrough is.
