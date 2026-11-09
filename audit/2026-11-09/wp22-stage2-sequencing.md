---
title: WP-22 Stage 2 sequencing and hint rule — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-09
tags: [audit, wp-22, stage2, recall, ff-010, a9]
priority: medium
---

# WP-22 — evidence

Branch `wp/22-stage2-sequencing` from `966a962`. Governing text: amendment A9;
sources: `audit/2026-11-09/walkthroughs.md` round 3 (F-021..F-024, O-AG, O-AI,
O-AK).

## Harness

Bash 5.3 bundles (committed): `audit/2026-11-09/sim/wp22-all/`,
`wp22-second-try-stage2/`, `wp22-second-try-stage4/`. Bash 3.2.57 runs (`/bin/bash`
first on `PATH`): same commands, `ok`, not committed. `q` leaves `less` in the
`careful-beginner` walk (`leave-less-pager`, 3.2). `second-try 2` first check:
one done item (the folder, made by `mkdir practice`) and one `○` item (`cd into
it`, `not yet: not in your history`); the oracle asserts the cd reason once and
the folder reason never. `make check` runs FF-009 and FF-010; both clean.

Rendered heights (both Bash versions; none over budget): 1.2 19 (was 18), 2.4 22
(22), Stage 2 gate task 18 (17), 3.2 22 (22), 3.3 22 (22).

## First `check` at the Stage 2 gate, no folder made (scratch sitting)

Quoted from `sitting.py start --arg 2` after the three Stage 2 recall answers:

```
shelltutor> check

┃ ○ folder exists  not yet: no practice folder in this stage's folder
┃ ○ cd into it     not yet: make the folder first, then cd into it
┃ Run the ones marked ○, then type check again.
```

The second `check` adds `┃ Hint: mkdir makes the folder; cd moves into it; pwd
shows where you are.` (attempt 2, as before).

## `normalize_answer` against the real lists (round-3 inputs)

Real function and lists read from `shelltutor`.

| Q | typed | normalised | result |
| --- | --- | --- | --- |
| S2 Q2 | `your home folder` | `your home folder` | accept |
| S2 Q2 | `your home directory` | `your home directory` | accept |
| S2 Q2 | `your home` | `your home` | accept |
| S2 Q2 | `a home folder` | `a home folder` | REJECT |
| S2 Q2 | `home` | `home` | accept |
| S2 Q2 | `the home folder` | `the home folder` | accept |
| S4 Q1 | `the path /usr/bin/vim` | `the path /usr/bin/vim` | accept |
| S4 Q1 | `the folder and name of the program file` | `the folder and name of the program file` | REJECT |
| S4 Q1 | `a path like /usr/bin/vim` | `a path like /usr/bin/vim` | REJECT |
| S4 Q1 | `it prints the path` | `it prints the path` | REJECT |
| S4 Q1 | `the full path` | `the full path` | accept |
| S4 Q1 | `the path` | `the path` | accept |
| S4 Q1 | `/usr/bin/vim` | `/usr/bin/vim` | accept |
| S4 Q1 | `the folder and file name` | `the folder and file name` | accept |

Still rejected, from the same round (not in the A9 lists): `a home folder`
(F-021), `the folder and name of the program file` (the old S4 Q1 hint; the
hint is replaced), `a path like /usr/bin/vim` and `it prints the path` (F-023).
