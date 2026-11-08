---
title: shelltutor — 2026-11-08 Landing Findings
category: audit
component: findings
status: active
version: 0.1.0
last_updated: 2026-11-08
tags: [audit, findings, portability, practice-shell, bash-floor, resolved]
priority: high
---

# 2026-11-08 — Landing Findings

Surfaced by the operator while landing the 2026-11 cycle (push, hosted
evidence intake, first macOS Phase 2 walk). Recorded here before any fix,
per the findings flow in `docs/simulation-design-plan.md`.

## F-014 — The practice shell is whichever `bash` is first on `PATH`

- **Severity**: 3. The project's Bash 3.2 validation claims rest on the
  practice shell, and the practice shell was not necessarily 3.2.
- **Where**: `practice()` launches `INPUTRC=/dev/null bash --rcfile
  /dev/fd/3 -i …`. The bare `bash` resolves through `PATH`, not to the
  interpreter running the script. On a workstation with Homebrew Bash
  first on `PATH`, `/bin/bash ./shelltutor` renders lessons under 3.2.57
  but every practice prompt (and every gate task) runs under Bash 5.x.
- **Effect**: the 2026-11-08 macOS walkthrough "under Bash 3.2" exercised
  a 3.2 outer script and a 5.x practice shell. The harness avoided this
  only because it puts the chosen Bash first on `PATH`. F-009's fd-3
  rcfile fix was validated the same way, so it is not in doubt; the
  Readline/`bind` behaviour in C-007 is proven on both generations by the
  2026-11-07 pty probe.
- **Fix**: launch the practice shell with `"$BASH"` (the absolute path of
  the running interpreter, set by Bash itself), so the outer script and
  the practice shell are always the same binary. Document in C-007; the
  Phase 2 checklist asks the walker to run `echo $BASH_VERSION` at the
  first practice prompt and record it.
- **Status**: resolved in `8d2c7bf` (`WP-09`): `practice()` launches `"$BASH"`. With
  `/bin/bash` as the outer script and Homebrew Bash first on `PATH`, a practice
  prompt reported `BASH_VERSION` 5.3.20 before the fix and 3.2.57 after. C-007 and
  the Phase 2 checklist (step 0) say so.

## Observations

- **O-F** The hosted-evidence intake grep for home-directory prefixes hits
  lesson 2.3's absolute-path example (a notes file under a fictional
  user's home) on every intake. The intake text should exclude that known
  string. (`WP-09`) **Done** (`b4457c9`): the intake grep pipes through `grep -v`
  for that path.
- **O-G** `summary.md` does not record the Bash version that ran the
  tutor; the workflow log does. The harness should capture
  `bash --version` (first line) of the `bash` it will resolve, in run
  metadata. (`WP-09`) **Done** (`b4457c9`): `bash_path` and `bash_version` are in
  run metadata and `summary.md`.
- **O-H** No macOS `--stage all` bundle exists after WP-04/WP-05; the
  `all-slice2` baseline predates the Stage 1 split, so Linux intakes
  compare against stale Stage 1 content. A fresh macOS bundle is needed
  as the like-for-like baseline. (`WP-09`) **Done**: `sim/all-current/current-rc`
  (macOS, Bash 5.3.20); its Stage 1 text matches `all-linux/current-rc` apart from
  the user name, date and day-of-week answer.
- **O-J** Ten screens exceed the 20-line vertical budget the script
  states for itself (`shelltutor:576-580`: 24 rows minus the practice
  prelude). Measured on 2026-11-08 at `469046b` by counting here-document
  content lines per screen function (blank lines included):
  `stage2_lesson_3` 23, `stage3_lesson_3` 21, `stage4_lesson_1` 25,
  `stage4_lesson_2` 24, `stage4_lesson_3` 30, `stage5_lesson_1` 23,
  `stage5_lesson_2` 27, `stage5_lesson_3` 35, `stage5_lesson_4` 22,
  `finale` 31; `stage4_intro` is exactly 20. All Stage 1 screens and all
  other intros fit. On an 80×24 terminal the heading and first lines of an
  over-budget screen scroll off before the prompt appears; the `▶` line
  stays visible. The density audits covered Stage 1 only, which is why
  this went unmeasured; `docs/design-description.md` §3.3 and §4.1
  described the budget as a course-wide property and are corrected to
  cite this observation. Not a Phase B package by itself; recorded for
  the operator's decision (the WP-12 sentences are added net-zero so
  neither 3.3 nor 4.3 grows).
- **O-I** `sim-evidence` runs on every push to `main` (about 13 s each)
  and produces an artifact per commit; only reviewed bundles are intaken.
  Acceptable as designed (D-17); the operator may narrow the trigger to
  `workflow_dispatch` later if the noise bothers.
