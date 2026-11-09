---
title: WP-20 Stage 1 gate grounding — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-09
tags: [audit, wp-20, gate, recall, a7]
priority: medium
---

# WP-20 — evidence

Branch `wp/20-gate-grounding` from `9a50685`. Governing text: amendment A7;
sources: `audit/2026-11-09/walkthroughs.md` (F-017, F-018, O-P, O-Q, O-S, O-U,
O-V).

## Harness

Bash 5.3 bundles (committed): `audit/2026-11-09/sim/wp20-all/`,
`wp20-second-try-stage2/`, `wp20-second-try-stage4/`. Bash 3.2.57 runs
(`/bin/bash` first on `PATH`): same three commands, `ok`, not committed.
Stage 2 `second-try`: `Hint:` twice, the first navigation fact once, one
`not yet:` (the oracle enforces it; TAP `ok`).

Rendered heights (both Bash versions): S1-L1 22, S1-L2 18, S1-L3 19,
S1-GT 16, S1-C 19; no Stage 1 screen over budget.

## `normalize_answer` against the Stage 1 accepted lists

Run with the real function and the real lists read from `shelltutor`
(`scripts` scratch checker, not committed); identical output under Bash 3.2.57
and 5.3, and under `LC_ALL=C`.

| Q | typed | normalised | result |
| --- | --- | --- | --- |
| Q1 | `$` | `$` | accept |
| Q1 | `>` | `>` | REJECT (by design) |
| Q1 | `#` | `#` | REJECT |
| Q1 | `ls` | `ls` | REJECT |
| Q1 | `dollar sign` | `dollar sign` | accept |
| Q1 | `the dollar sign` | `the dollar sign` | accept |
| Q2 | `the folder` | `the folder` | accept |
| Q2 | `the folder I'm in` | `the folder im in` | accept |
| Q2 | `the folder you're in` | `the folder youre in` | accept |
| Q2 | `the folder you’re in` (U+2019) | `the folder youre in` | accept |
| Q2 | `the current directory` | `the current directory` | accept |
| Q2 | `the directory` | `the directory` | accept |
| Q2 | `where I am` | `where i am` | accept |
| Q2 | `a folder` | `a folder` | REJECT (not in A7 list) |
| Q2 | `print working directory` | `print working directory` | REJECT (not in A7 list) |
| Q3 | `to the screen` | `to the screen` | accept |
| Q3 | `on the screen` | `on the screen` | accept |
| Q3 | `standard out` | `standard out` | accept |
| Q3 | `the terminal window` | `the terminal window` | accept |
| Q3 | `the display` | `the display` | accept |

FF-009 (`scripts/check-hints.sh`) is clean with no hint rewording.
