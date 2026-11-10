---
title: WP-25 chrome v2 — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-09
tags: [audit, wp-25, chrome, screens, rendering, a11]
priority: medium
---

# WP-25 — evidence

Branch `wp/25-chrome-v2` from `1f7fcad`. Governing text: A11 and
`docs/design-consultant-response-2026-11.md`. Rendering only: no lesson-body
sentence changed; the one added sentence is "First, three questions. Type your
answer in words; this is not the shell." on the Stage 3–5 and module gate
intros (Stages 1 and 2 already had it), because the recall prompt no longer
says "answer in words".

## Harness

Bash 5.3 bundles (committed): `audit/2026-11-09/sim/wp25-all/` (UTF-8),
`wp25-ascii-all/` (ASCII), `wp25-ascii-all-bash32/` (ASCII on 3.2.57),
`wp25-second-try-stage2/`, `wp25-second-try-stage4/`, `wp25-module-shells/`,
`wp25-module-env/`. Eighteen runs, UTF-8 and ASCII on 3.2.57 and 5.3 (stage
walk, second-try 2 and 4, both modules): all `ok`. `scripts/sim/compare_heights.py`:
UTF-8 against ASCII, 5.x against 3.2, and the module runs have identical row
counts on every screen (39 screens in the stage walk). All 43 header rows are
exactly 80 columns in both glyph sets.

## Screens over the 19-row panel budget (more than 20 rendered rows)

Input for WP-26. "Before" is `wp24-all` (budget then 22 rendered rows); every
screen gained one or two rows (a blank after the `▶` line, a blank under the
rule).

| Screen | Before | After | Over 20 |
| --- | ---: | ---: | --- |
| S1-W | 18 | 19 | no |
| S1-O | 21 | 22 | yes |
| S1-I | 11 | 13 | no |
| S1-L1 | 22 | 22 | yes |
| S1-L2 | 19 | 21 | yes |
| S1-L3 | 19 | 21 | yes |
| S1-L4 | 22 | 22 | yes |
| S1-L5 | 20 | 22 | yes |
| S1-GT | 17 | 19 | no |
| S1-C | 19 | 20 | no |
| S2-I | 21 | 22 | yes |
| S2-L1 | 20 | 22 | yes |
| S2-L2 | 20 | 22 | yes |
| S2-L3 | 22 | 22 | yes |
| S2-L4 | 22 | 22 | yes |
| S2-GT | 18 | 20 | no |
| S2-C | 19 | 18 | no |
| S3-I | 22 | 23 | yes |
| S3-L1 | 21 | 22 | yes |
| S3-L2 | 22 | 22 | yes |
| S3-L3 | 22 | 22 | yes |
| S3-GT | 21 | 22 | yes |
| S3-C | 19 | 19 | no |
| S4-I | 22 | 24 | yes |
| S4-L1 | 22 | 22 | yes |
| S4-L2 | 22 | 22 | yes |
| S4-L3 | 22 | 22 | yes |
| S4-L4 | 17 | 19 | no |
| S4-GT | 21 | 22 | yes |
| S4-C | 19 | 20 | no |
| S5-I | 15 | 17 | no |
| S5-L1 | 21 | 22 | yes |
| S5-L2 | 22 | 22 | yes |
| S5-L3 | 21 | 22 | yes |
| S5-L4 | 22 | 22 | yes |
| S5-L5 | 19 | 21 | yes |
| S5-GT1 | 22 | 22 | yes |
| S5-GT2 | 18 | 20 | no |
| FIN | 21 | 24 | yes |

Modules (rendered): shells M-L2 22, M-L3 22, M-GT 22; env M-I 22, M-L1 21,
M-L2 22, M-L5 22. The interim squeeze holds every screen to the 21-panel-row
hard cap (22 rendered) except three with no interior blank left to drop:
S3-I 23, S4-I 24 and the finale 24 (not a panel; no prompt follows). The gate
screens with the added sentence all fit.

## `seen:` strings rewritten (`not yet:` is gone)

| Where | Was | Now |
| --- | --- | --- |
| history check (Stages 1, 4, modules) | not in your history | none typed since the task began |
| Stage 1 answers | that is not what whoami / pwd printed; not the day date printed | your answer differs from the whoami / pwd / date line |
| Stage 2 folder | no practice folder in this stage's folder | no practice folder in the stage folder |
| Stage 2 cd | not in your history; make the folder first, then cd into it | no cd in your history; no folder to be inside yet |

The other reasons were already observations (`no done.txt in this folder`,
`it holds: ...`, `notes.txt is still here`, `it still reads exactly before`).

## Remaining `SUB` / `KEY` / `DIR` uses

`KEY`: removed (0). `${SUB}`: 12 in the two modules; `"$SUB"`: 19 in `--info`.
`${DIR}`: 7 in the two modules. Core screens use none.

## Notes

- The consultant mock-up (§5.4) shows a first miss without a hint. Not adopted:
  A7 rests on sitting evidence (every round-1 persona quit before any hint
  appeared). Every miss prints `not quite. hint: ...`; from the second miss the
  three navigation facts follow. `second-try 2` asserts `hint:` twice and the
  first fact once; the Stage 2 and 4 oracle also asserts one checklist closing
  line (`Finish the step marked [ ]`).
- The header uses the short stage titles (Paths, Files, Commands and streams);
  the stage intro bodies still print the long ones (`STAGE 2 — Paths and the
  filesystem`), a WP-26 item. README's stage table matches the header.
