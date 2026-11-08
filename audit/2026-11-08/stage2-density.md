---
title: Stage 2 Density (WP-14)
category: audit
component: stage2-density
status: active
version: 0.1.0
last_updated: 2026-11-08
tags: [audit, density, stage2, ux, wp-14]
priority: medium
---

# Stage 2 Density (WP-14)

Same method and table shape as `audit/2026-05-23/stage1-density.md` and
`stage1-density-followup.md`: content lines are the heredoc lines of each
screen function, counting blanks; rendered rows come from the harness
`screen-height` table (Bash 5.3.20 and 3.2.57 give identical values). The
budget is at most 18 heredoc lines and at most 22 rendered rows.

Why Stage 2 changed: observations O-M and O-N in
`audit/2026-11-08/walkthroughs.md` (path and `.` / `..` / `~` named before
the learner has a position; `ls -l` output unexplained), and A2.3.

| Screen | Content lines | Rendered rows | Concepts introduced | Distinct actions | Recommendation |
| --- | ---: | ---: | --- | ---: | --- |
| S2-I `stage2_intro` | 17 | 21 | stage scope (four lessons); `pwd`, `ls`, `cd`; `.` `..` `~` named | 1 | **keep** — a reference list; the symbols are explained in 2.4 |
| S2-L1 `2.1 where you are` | 16 | 20 | current directory (drawn as a tree with the learner in it); `pwd` | 1 (`pwd`, after predicting) | **keep** — new in WP-14; the position is shown before the command |
| S2-L2 `2.2 ls: what is here` | 16 | 20 | `ls`; `ls -p` marks folders; `ls -a` shows hidden names | 3 (one flag each) | **keep with watch** — three flags of one command; `ls -l` removed (O-N; belongs with permissions, D7) |
| S2-L3 `2.3 cd: moving` | 18 | 22 | `cd` with a path, with no argument, `~`, `-`, `..` | 6 (one line each) | **keep with watch** — unchanged content from the old 2.2; action count was already high; at the rendered budget |
| S2-L4 `2.4 names for places` | 18 | 22 | `.` `..` `~` as names for places; relative and absolute paths | 0 (read) | **keep with watch** — trimmed from 23 to 18 lines (one example per list dropped, `./notes.txt` removed); read-only, follows the six-action 2.3 |
| S2-G / S2-GT | unchanged | 17 (task) | gate recall and task unchanged | | keep |

## Evidence

`audit/2026-11-08/sim/all-wp14/` (Bash 5.3.20): `careful-beginner --stage
all` ok, zero `error-signature` events, one `expected-error` (S1-L4,
`bash: dtae: command not found`). Scratch runs, not committed: Bash 3.2.57
`--stage all`, `--stage 1`, `--stage 2` and `second-try --stage 2`, all ok;
5.3 `--stage 1`, `--stage 2` and `second-try --stage 2` ok.

## Watch items

The harness has no human pauses. The next two sittings should record, at
Stage 2: the time on 2.1 and whether `pwd` is predicted aloud; whether
`ls -p` is understood without help; and whether 2.3 followed by 2.4 is
too long before the gate.
