---
title: Phase B Closure Check
category: audit
component: phase-b-closure
status: active
version: 0.1.0
last_updated: 2026-11-08
tags: [audit, closure, baseline, risks, tensions, screen-height]
priority: medium
---

# Phase B Closure Check

A findings-style check of `main` at `6473241` against the baseline's risks
(`docs/design-description.md` §3.4) and tensions (§6). One line per item:
**closed**, **partly**, or **open**, with the evidence. Line numbers are
`shelltutor` at this revision. No change to the script; no new analysis.

## Drop-off risks (§3.4)

| # | Risk | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | Recall answer not in the list; no way out | **partly** | Mechanism closed: `ask_question` (`668-705`) takes a hint, answers `show` and `quit` (`farewell_exit`, `529`), and from the third miss prints the navigation facts (`recall_navigation`, `662`); WP-10, C-006. Answer lists are not yet widened: that waits for the rejected-answer record (`audit/2026-11-08/walkthroughs.md`, sitting 1 of 3). |
| 2 | Stage 5 without Vim | **open** | The gate still needs `vim` (`2232-2300`); `--info` warns (`301`). Intrinsic to a `vimtutor` preparer (decisions §3). |
| 3 | Stage 1 follow-up prompts | **closed** | `stage1_followup` (`1088-1100`) accepts `show` and `quit`; the pwd answer matches the logical or physical path (`1014-1030`); WP-10. |
| 4 | First full-screen program | **open** | Lessons 3.2 and 5.1 unchanged; text only. |
| 5 | No pause after "Stage N cleared" | **closed** | `stage_cleared` (`2458`) stops after stages 1-4; stage 5 flows into the finale (`2357`); WP-11. |
| 6 | Quitting mid-gate | **partly** | Behaviour unchanged (the stage restarts from its first lesson, by design, D8); the third recall miss now says so and that `quit` is safe (`662`). |

## Tensions (§6)

| # | Tension | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | Recall has no ladder | **closed** | Three rungs for all fifteen questions (`668-705`); FF-009 `check-hints` guards the hints; `second-try` observes the rungs. |
| 2 | "No skip" versus the CLI jump | **open** | Intended; wording unchanged (`17`, `163`; C-001). |
| 3 | Handoff: pointer or launch | **closed** | `--info` says the finale "names" `vimtutor` (`305`); the finale prints the command; WP-11 `6d80022`. |
| 4 | `--info` promises skips that do not exist | **closed** | Lines `291` and `296` now say the example "will not work until it is installed"; WP-11 `6d80022`. |
| 5 | Prompt character taught versus shown | **open** | Stage 1 Q1 still accepts `$` (`1124-1126`); the practice prompt is `shelltutor> ` (`585`, C-007). |
| 6 | Objective breadth versus gate breadth | **open** | No new verifiers; `ls`, `cat`, `less`, quoting remain unverified. Stage 2 now teaches `ls -p` (WP-14) but its gate is unchanged. |
| 7 | Fading runs backwards at the gate | **partly** | Pre-task hints removed at stages 2-4 (WP-10 `e511b98`; the task screens say what the gate checks). Stage 5 still spells out the keystrokes (`2236-2244`, `2285-2290`). |
| 8 | Safety sentence location | **closed** | The welcome carries the authority sentence (`840`); operator question O-3 resolved by A2/A3. |
| 9 | Two load rules | **open** | Both in force; reconciled per screen in `stage1-density-followup.md` and `stage2-density.md`. |
| 10 | Mid-stage state not persisted | **open** | Intended (ROADMAP progress model); revisit only if observed to matter (D8). |
| 11 | Practice-shell interpreter | **closed** | `"$BASH"` since WP-09; the harness records the Bash path and version in every bundle. |
| 12 | Coupling of observation to copy | **open** | Still a two-file change for core screens; modules derive sentinels from the heading convention, so a module copy edit touches one file. |
| 13 | Human pacing unobserved | **partly** | Phase A sitting 1 is recorded; sittings 2 and 3 are pending; the tutor records no timing (D8). |
| 14 | A learner must install Vim | **open** | Same as risk 2. |
| 15 | Screen budget is a Stage 1 fact | **partly** | Measured for every screen (below); Stages 1-2, the chrome and the module are within 22 rendered rows; Stages 3-5 and the finale are not. |

Count: risks 2 closed, 2 partly, 2 open; tensions 5 closed, 3 partly, 7 open.

## Screen heights on current `main`

Scratch run, `careful-beginner --stage all`, Bash 5.3.20, harness
`screen-height` table (rendered rows from the clear to the prompt; budget 22
= 18 heredoc lines + chrome + footer). Result: `ok`, no error signatures.

**Over 22 rendered rows (nine screens):**

| Screen | Rendered | Baseline O-J heredoc lines | Note |
| --- | ---: | ---: | --- |
| S3-L3 `stage3_lesson_3` | 25 | 21 | unchanged apart from chrome; WP-12's sentence was net zero |
| S4-L1 | 29 | 25 | unchanged |
| S4-L2 | 28 | 24 | unchanged |
| S4-L3 | 34 | 30 | unchanged; WP-12's sentence net zero |
| S5-L1 | 27 | 23 | unchanged |
| S5-L2 | 31 | 27 | unchanged |
| S5-L3 | 39 | 35 | unchanged; the longest screen |
| S5-L4 | 26 | 22 | unchanged |
| FIN `finale` | 31 | 31 | the finale draws no chrome, so rendered equals heredoc |

**Against the O-J set:** the ten screens of O-J are all still present except
`stage2_lesson_3` (23 heredoc lines), which WP-14 trimmed: it is now S2-L3
(22) and S2-L4 (22), both at the budget. Every other O-J screen is over by
the same four rows the chrome adds to its heredoc count (two rules, a blank,
the footer). The set is therefore unchanged except for WP-14's Stage 2
trim.

**At exactly 22 (within budget):** S1-L4, S2-L3, S2-L4, S3-I, S3-L1, S3-L2,
S4-I, S5-GT1. **Within budget otherwise:** all of Stage 1 (the largest is 22),
Stage 2's other screens (at most 21), every cleared screen (19), and the
`shells` module (at most 21, `audit/2026-11-08/sim/module-shells/`).

## Notes for the operator

- Stages 3-5 are the one place the course still breaks its own screen
  budget; no package owns them. The decisions' module standard prevents new
  curriculum from joining them, but trimming S4-L1 to S4-L3, S5-L1 to S5-L4
  and the finale is a core-standard change that would need a density review.
- `STATUS.md` still lists WP-14 and WP-16 as "branch" rows although both
  have landed; the coordinator's status pass can correct them.
