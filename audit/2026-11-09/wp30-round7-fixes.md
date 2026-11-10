---
title: WP-30 round-7 fixes — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-10
tags: [audit, wp-30, copy, recall, shells, round7, a16]
priority: low
---

# WP-30 — evidence (commits 1–4; commit 5, Leo v0.3.1, is a6's)

Branch `wp/30-round7-fixes` from `db7dc63`. Governing text: A16 and
`audit/2026-11-09/walkthroughs.md` round 7 (F-032, F-033, O-BH..O-BL).

## Harness

Bash 5.3 bundles (committed): `audit/2026-11-09/sim/wp30-all/` (UTF-8),
`wp30-ascii-all/`, `wp30-ascii-all-bash32/`, `wp30-second-try-stage2/`,
`wp30-second-try-stage4/`, `wp30-module-shells/`, `wp30-module-env/` and their
ASCII twins. Fourteen runs on 3.2.57 and 5.3, UTF-8 and ASCII: all `ok`;
`compare_heights.py` shows identical row counts between the forms and the Bash
versions (46 stage-walk screens, 6 shells, 9 env). The login name does not
appear in any committed bundle. Every core and module screen is within the
20-row budget; only the welcome (21) and the finale (24, not a panel) are above.

## Heights that moved (rendered rows; budget 20)

| Screen | Before | Now | Why |
| --- | ---: | ---: | --- |
| S1-L1 | 18 | 20 | the slash sentence (two lines) joins the notice |
| S1-L4 | 20 | 19 | the slash sentence leaves 1.4 |
| S2-L3 | 18 | 19 | the backslash line |
| S5-L2 | 17 | 19 | the `<Enter>` sentence, wrapped at 80 columns |
| S5-L6 | 16 | 17 | the learner-first install line plus one grey line |
| env M-L5 | 18 | 19 | the aside sits on its own line |

shells 1 stays at 18 rows.

## Layout choices and widths

- env 5: the new aside is 56 characters, too long beside `echo "[$SHELLTUTOR_HOME]"`
  at 80 columns, so it sits on the next line under the command (layout only; no
  word changed).
- 5.2: the `<Enter>` sentence is 86 characters and wraps after "not".
- shells 1: the notice says "The second line prints one row: a number and a
  name." Real `ps -o pid,comm` also prints a `PID COMM` header; the copy is the
  package's. Under the harness the name is `/opt/homebrew/bin/bash`, which ends in
  bash.
- A scan of all bundle screens found no other line over 80 columns apart from
  the host paths and Vim's own screen.

## Corpus (FF-011)

246 to 266 cases (accepted 126 to 138, rejected 120 to 128): twelve accept rows
for the new exact forms and eight reject rows (the four residual false accepts
`the folder of the manual`, `a file in a folder`, `the date and the folder`,
`the directory listing`, plus `where the program is`, `where is the manual`,
`the path of the program`, `directory of files`). Against the previous script
fifteen of the new rows fail; with the change all 266 pass. FF-009 and FF-010
are clean (the new hint contains no accepted form or phrase).
