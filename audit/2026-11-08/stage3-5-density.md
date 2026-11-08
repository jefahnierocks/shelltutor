---
title: Stages 3-5 and Finale Density (WP-18)
category: audit
component: stage3-5-density
status: active
version: 0.1.0
last_updated: 2026-11-08
tags: [audit, density, stage3, stage4, stage5, finale, wp-18, o-j]
priority: medium
---

# Stages 3-5 and Finale Density (WP-18)

Same row format as `stage2-density.md`. Heredoc lines are counted per screen
function with blanks; rendered rows come from the harness `screen-height`
table (Bash 5.3.20 and 3.2.57 give identical values). Budget: at most 18
heredoc lines and 22 rendered rows. Governing text: A5 and observation O-J.
Method: trim first, split second; no command removed.

| Screen | Heredoc before | Heredoc after | Rendered before | Rendered after | Concepts | Actions | Treatment and recommendation |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| 3.3 copy, move, delete | 21 | 18 | 25 | 22 | `cp`, `mv` (rename), `rm`, the safety habit | 4 | **trim** — the habit is one line; `mv`'s two sentences are one. Three verbs and one habit stay one family; keep with watch |
| 4.1 reading a command | 25 | 18 | 29 | 22 | command, options, arguments; quoting; `command -v` | 2 probes | **trim** — one example per idea; `command -v` keeps two probes (`vimtutor` is probed in 5.5); `ls -l /etc` is the option and argument example |
| 4.2 the pipe | 24 | 18 | 28 | 22 | pipe; stacking | 3 | **trim** — "things to notice" is one line; `wc` is introduced by its three uses |
| 4.3 redirection | 30 | 18 | 34 | 22 | `>`, `>>`, `<` | 4 | **split** from the old 4.3 — three operators of one idea; the pipe-plus-redirect example is one line |
| 4.4 globs (new) | (in 4.3) | 13 | (in 4.3) | 17 | `*` | 1 | **split** — one idea; carries the "predict before you act" sentence about `rm *`; the gate's `*.txt` history check is satisfied here |
| 5.1 print-and-exit vs full-screen | 23 | 17 | 27 | 21 | two kinds of command; exit keys | 1 | **trim** — the exit keys share one line |
| 5.2 entering and leaving Vim | 27 | 18 | 31 | 22 | enter safely; leave with `:q`, `:q!` | 3 | **trim** — reached 18 without splitting; keep with watch (the largest remaining Stage 5 lesson) |
| 5.3 buffer vs file | 35 | 17 | 39 | 21 | file, buffer, write; `:w :q :q! :wq` | 0 | **split** — the idea and the four commands, read only |
| 5.4 practice (new) | (in 5.3) | 18 | (in 5.3) | 22 | discard and save sequences on `practice.txt` | 2 sequences | **split** — practice only; the old 5.3 text unchanged |
| 5.5 calling vimtutor (was 5.4) | 22 | 15 | 26 | 19 | `vimtutor`; install hints | 1 | **trim** — install hints are two lines; the sentence about the gate points at 5.4 |
| finale | 31 | 21 | 31 | 21 | what was met; what is next | 0 | **trim** — commands wrap in three lines; keys, operators and ideas are one line each; install hints kept; the screen draws no chrome |

The Stage 4 intro says "Four lessons" and the Stage 5 intro "Five lessons".
Unchanged screens that sit at exactly 22: S3-I, S3-L1, S3-L2, S4-I, S5-GT1.

## Evidence

Bash 5.3.20 bundles are committed under `audit/2026-11-08/sim/wp18-*`
(`all`, `3`, `4`, `5`, `second-try-4`): all `ok`, no `error-signature`
events. Bash 3.2.57 runs of the same five are `ok` (scratch). The full
height table is in `wp18-all/current-rc/summary.md`: no screen above 22,
the finale 21.

## Watch items

Stage 4 now has four lessons before a gate whose task is a pipe and a glob;
4.3 and 4.4 should be timed in the next sittings. 5.2 is the densest Stage 5
lesson (three actions); observe whether `vim --version` and `vim` in one
screen is too much.
