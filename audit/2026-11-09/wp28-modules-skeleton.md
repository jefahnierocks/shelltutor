---
title: WP-28 modules to the skeleton — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-10
tags: [audit, wp-28, modules, skeleton, a12, a13, a15]
priority: medium
---

# WP-28 — evidence

Branch `wp/28-modules-skeleton` from `f068cb3`. Governing text: A12, A13 and A15
(`docs/workplan/WP-28-modules-skeleton.md`, copy as written there).

## Rendered height of every module screen (budget 20)

| Screen | shells | env |
| --- | ---: | ---: |
| intro | 15 | 15 |
| lesson 1 | 18 | 19 |
| lesson 2 | 18 | 19 |
| lesson 3 | 18 | 18 |
| lesson 4 | | 18 |
| lesson 5 | | 18 |
| lesson 6 | | 19 |
| task | 17 | 17 |
| cleared | 15 | 17 |

Before (WP-26 bundles, squeeze gone): shells intro 20, lessons 20, 23, 22, task
22, cleared 15; env intro 22, lessons 21, 22, 20, 17, 23, task 20, cleared 16. The harness now fails a module run when a screen
passes the budget (`HEIGHT_ALLOWED` has no module entry). No module copy needed
a blank row dropped.

## Harness

Bash 5.3 bundles (committed): `audit/2026-11-09/sim/wp28-module-shells/`,
`wp28-module-env/` (UTF-8), `wp28-module-shells-ascii/`, `wp28-module-env-ascii/`,
`wp28-module-env-ascii-bash32/`. All module runs are `ok` on 3.2.57 and 5.3, in
UTF-8 and ASCII; `compare_heights.py` shows identical row counts between the
forms and between the Bash versions. The core walk and `second-try 2` and `4`
are `ok` on 5.3 and the core walk on 3.2 (the harness environment changed, below).
`selftest_modules`, `selftest_sitting`, `selftest_home` and `selftest_redaction`
pass.

## The review points that were code

1. env 2 prints `pet=` and `pet=owl`.
2. The env 4 persona types both `PS1=` lines; `module_walk` has a new
   `lesson_prompts` table, and the walk waits for `\nme> ` and then `\n$ `, in
   order (a `selftest_modules` case asserts it).
3. `SHELLTUTOR_HOME`: the script never reassigned, exported or unset it, so the
   practice shell already received the learner's value; the rule is now written
   down (C-004 row, C-007 "Not controlled" row, a script comment) and checked by
   `scripts/sim/selftest_home.py` (unset stays unset, relative stays relative,
   a trailing slash stays).
4. The env task needs `TOPIC=shell`, `export TOPIC` and a child `bash -c` in the
   history, plus `shell` in `seen.txt`. Checked in a scratch sitting: a
   double-quoted `bash -c "echo $TOPIC" > seen.txt` with no export fails with
   `[ ] export TOPIC`; with the export it passes. **Single and double quotes
   cannot be told apart once the variable is exported**, so the old
   single-quote pattern in the history check is gone, and the gate says it
   checks what it can.
5. Task screens say "the module's own folder"; no path placeholder.
6. shells 1 uses `ps -o pid,comm` (heredoc text; FF-008 is clean).
9. The header is `── Module ───…── shells  1/3 ──` (`gate` and `task` in place of
   `k/n`); titles carry no position prefix; the intro title is `<name>: <title>`.
   Sentinels, `module_walk` and `selftest_modules` follow; CONTRIBUTING's heading
   table is updated.
11. The module standard is three to six lesson screens in the decisions doc.
Also: the shells task is verified by file content and its history check accepts
`which zsh`, so `which zsh > zsh.txt` passes (checked in a scratch sitting); a
script comment at env 2 says `bash -c` resolves through `PATH` and need not be
the practice shell's binary (not F-014).

## D-19 redaction result

The login name does not appear anywhere in the committed module bundles
(`grep -rl` for it finds nothing), and `terminal.jsonl` shows
`LESSHISTFILE=/Users/[user]/...` where the host path had the name. The
`Redactor` replaces the name as a substring in terminal chunks (including a name
split across chunks), events and the summary, so `USER=` and `LOGNAME=` lines are
covered. Because the name did not survive, no fix was needed, but I added
`scripts/sim/selftest_redaction.py` anyway (one chunk, a split name, a
non-UTF-8 chunk, an event payload and a later text file; 7 redactions).

**A second finding.** `env | head` in the env module printed the *operator's whole
environment* into the bundle: the harness child inherited every variable
(`ITERM_PROFILE`, `CLAUDE_CODE_CHILD_SESSION`, tool and shell variables, whatever
the first ten lines held). Redaction only covers the login name, so a secret in
that environment could have been committed. `run.py` now passes the child a short
allowlist (`PATH`, `USER`, `LOGNAME`, `SHELL`, `TMPDIR`, `TERM`) plus the variables
it sets itself; every run above used it.
