---
title: shelltutor — 2026-11-07 Review Findings
category: audit
component: findings
status: active
version: 0.1.0
last_updated: 2026-11-07
tags: [audit, findings, portability, lessons, gates, locale, ff-008]
priority: high
---

# 2026-11-07 — Review Findings (cycle-planning static review)

Surfaced by a full read of `shelltutor` at revision `b2fdff7` while preparing
the 2026-11 work plan (`docs/workplan/README.md`). Each finding was reproduced
with a direct command on macOS (Darwin 27.0.0, Apple Silicon) against stock
`/bin/bash` 3.2.57 and Bash 5.3.20 unless marked **by inspection**. None has
yet been observed through the PTY harness: `WP-01` captures the five-stage
baseline that shows F-010 and F-011 as transcript evidence before `WP-02`
fixes them (observe-before-fix, per `docs/simulation-design-plan.md`).

Baseline at this review: `make check`, `make lint`, `make smoke` and
`make self-test` pass; the Stage 1 PTY harness (`current-rc` and
`no-system-rc-preview`) passes under Bash 3.2.57 and Bash 5.3.20; the hosted
`verify` workflow succeeded on the `main` push of `b2fdff7`. Running
`./shelltutor < /dev/null` exits 1 with the documented preflight diagnostic.

Severity uses the simulation evidence scale already applied to F-008 and
F-009 (4 = release-blocking, 3 = a learner on a supported surface is misled
or blocked, 2 = inconsistent across supported surfaces, 1 = cosmetic).

## F-010 — Lesson 5.3 promises a fixture that does not exist at lesson time

- **Severity**: 3. The lesson that teaches the stage's central idea (buffer
  versus file) contradicts itself on screen.
- **Where**: `stage5_lesson_3` says "A `practice.txt` fixture is in this
  stage's folder" and instructs `vim practice.txt`, `:q!`, then
  `cat practice.txt  # the file is unchanged`. The lesson runs through
  `lesson()` with no directory argument, so its practice prompt starts in
  `$SANDBOX`, not `$SANDBOX/stage5`. `stage5_seed_practice` is called only
  from `stage5_gate`.
- **Effect**: `vim practice.txt` opens a new empty buffer in `$SANDBOX`;
  after `:q!`, `cat practice.txt` prints `No such file or directory`. The
  second sequence (`:wq`) then creates the file in `$SANDBOX`, so the learner
  sees a different folder state than the gate later resets.
- **Root cause**: lessons for stages 3 to 5 run in `$SANDBOX` while their
  copy describes the stage folder. `stage3_intro` has the same mismatch
  ("We'll do everything inside `$SANDBOX/stage3`"), and Stage 3 lesson files
  (`hello.txt`, `notes/`) land in `$SANDBOX`.
- **Fix**: decision D-04 in `docs/workplan/README.md`; implemented by
  `WP-02` (stage 3 to 5 lessons run in their stage folder; stage fixtures are
  seeded on stage entry; contract C-003 updated).
- **Status**: open; fix scheduled in `WP-02`.

## F-011 — Lesson copy hardcodes `~/.shelltutor`

- **Severity**: 3. Violates the user-agnostic contract on the one override
  the project documents (`SHELLTUTOR_HOME`, contract C-004).
- **Where**: `stage2_lesson_2` ("If you wander, `cd ~/.shelltutor` brings
  you back"); `stage3_lesson_2` (`cat ~/.shelltutor/poem.txt`,
  `less ~/.shelltutor/poem.txt`). Every other screen renders the sandbox
  path from `${SANDBOX}`.
- **Effect**: with `SHELLTUTOR_HOME` set, which is exactly how the PTY
  harness and the Phase 2 checklist run the tutor, all three commands fail.
  Under the default location they teach a path the rest of the copy never
  shows.
- **Fix**: decision D-05; `WP-02` renders `${SANDBOX}` or a relative path and
  extends the FF-004 checker so the literal cannot return.
- **Status**: open; fix scheduled in `WP-02`.

## F-012 — `ask_question` whitespace collapse uses GNU sed `\+`

- **Severity**: 2. Same defect class as F-008 (GNU-only sed syntax).
- **Where**: `ask_question` normalises both the learner's answer and each
  accepted answer with `sed 's/[[:space:]]\+/ /g'`.
- **Demonstration** (macOS `/usr/bin/sed`):

  ```
  $ printf 'a   b' | sed 's/[[:space:]]\+/ /g'
  a   b        # BSD sed: \+ is not a repetition operator; nothing changes
  a b          # GNU sed
  ```

- **Effect**: an answer typed with a doubled internal space (for example
  "the  current working directory") is accepted on Linux and rejected on
  macOS. Trimming of leading and trailing space works on both.
- **Fix**: `tr -s '[:space:]' ' '` in a shared `normalize_answer()` helper
  (`WP-02`), plus the FF-008 checker proposed below so GNU-only text-tool
  syntax cannot re-enter the script.
- **Status**: open; fix scheduled in `WP-02`.

## F-013 — Stage 1 day-of-week verification assumes an English locale

- **Severity**: 3. The Stage 1 gate cannot be passed by a learner whose
  locale is not English, on either supported platform.
- **Where**: `stage1_gate` asks "What day of the week did `date` show?
  (Mon, Tue, Wed, Thu, Fri, Sat, Sun)", title-cases the first three
  characters of the answer, and `stage1_verify_task` compares that against
  `$(date +%a)`, which is localized.
- **Demonstration**:

  ```
  $ LC_ALL=C date +%a;  LC_ALL=de_DE.UTF-8 date +%a;  LC_ALL=fr_FR.UTF-8 date +%a;  LC_ALL=ja_JP.UTF-8 date +%a
  Sat   Sa.   sam.   土
  ```

  A German learner sees `Sa.` in the practice prompt. Typing `Sat` (as the
  question lists) normalises to `Sat` and never equals `Sa.`; typing `Sa`
  normalises to `Sa` and never equals `Sa.` either.
- **Fix**: decision D-06; `WP-02` accepts the C-locale and current-locale
  forms of `%a` and `%A`, compared case-insensitively with a trailing period
  ignored, and the question invites the learner to type the day "as `date`
  printed it".
- **Status**: open; fix scheduled in `WP-02`.

## Observations (recorded, not findings)

- **O-A — Gate spec/implementation drift.** `ROADMAP.md` Phase 3 specifies a
  history trace of `cd` operations for the Stage 2 gate and a `*.txt` glob in
  history for the Stage 4 gate. The implementation checks only
  `[ -d "$SANDBOX/stage2/practice" ]` and the content of `count.txt`. `WP-05`
  aligns implementation to the spec after the `WP-01` baseline exists; the
  Stage 2 requirement is reduced to "at least one `cd`" to match the task the
  screen actually assigns, recorded as a ROADMAP amendment.
- **O-B — Checklist path error.** `docs/phase2-walkthrough-checklist.md`
  names the Stage 2 gate folder as `$SANDBOX/practice/`; the code and
  contract C-003 say `$SANDBOX/stage2/practice/`. Corrected on 2026-11-07 in
  the plan-adoption commit.
- **O-C — `SHELLTUTOR_HOME` shape.** A trailing slash
  (`SHELLTUTOR_HOME=/tmp/x/`) makes the expected Stage 1 `pwd` value
  `/tmp/x//stage1` while the practice shell prints `/tmp/x/stage1`; a
  relative value makes the sandbox depend on the caller's working directory.
  Decision D-08; `WP-02` normalises the path at startup. **By inspection.**
- **O-D — Inherited history variables can break the Stage 1 commands-run
  check.** The practice shell inherits the learner's environment. An
  exported `HISTIGNORE` listing `pwd` or `date`, or `HISTCONTROL`, or `TMOUT`
  (which exits an idle interactive shell), changes what `history -a` records
  or whether the prompt survives. Folded into the Slice 2 scrub list
  (decision D-09, `WP-03`). Severity if observed in the field: 3.
  **By inspection.**
- **O-E — `/etc/bashrc` is a macOS name.** Debian-family Bash is built with
  a system rcfile (`/etc/bash.bashrc`) that an interactive shell reads before
  the `--rcfile` file, and only `--norc` suppresses it, which also suppresses
  `--rcfile`. Slice 2 therefore stops sourcing `/etc/bashrc` and neutralises
  the known Linux hooks (`command_not_found_handle`) instead of claiming a
  fully isolated shell. Decision D-09. **By inspection.**

## Proposed fitness function

### FF-008 — POSIX text-tool portability in script code

| Field | Value |
| --- | --- |
| Rule | Bash code in `shelltutor` (outside lesson heredocs) must not use GNU-only text-tool syntax: `sed` `\+`, `\?`, `\|`, `\L`, `\U`, `\l`, `\u`, `\s`, `\w`, `\d`, or `-i`; `grep -P`; `readlink -f`; `date -d`; `stat -c`. |
| Enforcement category | `static-analysis` |
| Scope | `shelltutor`, code lines outside heredocs, excluding comment lines and lines annotated `# nofitness:posix` |
| Failure condition | any match; exit 1 with `file:line: FF-008 …` |
| Implementation | `scripts/check-posix-tools.sh`, same shape as the sibling checkers (awk heredoc state machine, `--self-test`), wired into `make check` and `make self-test` (`WP-02`) |
| Related findings | F-008 (2026-05-23), F-012 |

The next audit cycle should admit FF-008 to the fitness-function catalogue
alongside FF-001 to FF-007.

## Cross-references

- `docs/workplan/README.md` — decision log D-04 to D-09 and the work
  packages that close these findings.
- `audit/2026-05-23/findings.md` F-008 — prior GNU-sed finding.
- `audit/2026-07-14/findings.md` F-009 — prior Bash-generation finding.
- `docs/contracts.md` C-003, C-004 — contracts that `WP-02` updates.
