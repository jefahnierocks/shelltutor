---
title: WP-26 lesson skeleton — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-09
tags: [audit, wp-26, lessons, density, content, a13]
priority: medium
---

# WP-26 — evidence

Branch `wp/26-lesson-skeleton` from `fd25474`. Governing text: A13 and
`docs/workplan/WP-26-lesson-skeleton.md`. Copy is §3 as written; the lesson
functions were generated from that file, so the words are the file's.

## Rendered height of every screen

"Before" is `wp25-all` (21 lessons); budget 20 rendered rows (19 panel rows).
`New` is a screen that did not exist before. The harness now fails a core run
when a screen passes the budget; the welcome is allowed 21 (A12), and the
finale is not a panel. The gate recall screens end at the `? ` prompt, not the
shell prompt, so the tracker has no row for them.

| Screen | Before | After | Over 20 |
| --- | ---: | ---: | --- |
| S1-W | 19 | 21 | yes |
| S1-O | 22 | 17 | no |
| S1-I | 13 | 12 | no |
| S1-L1 | 22 | 18 | no |
| S1-L2 | 21 | 19 | no |
| S1-L3 | 21 | 19 | no |
| S1-L4 | 22 | 20 | no |
| S1-L5 | 22 | 18 | no |
| S1-GT | 19 | 20 | no |
| S1-C | 20 | 20 | no |
| S2-I | 22 | 12 | no |
| S2-L1 | 22 | 20 | no |
| S2-L2 | 22 | 19 | no |
| S2-L3 | 22 | 18 | no |
| S2-L4 | 22 | 17 | no |
| S2-L5 | new | 20 | no |
| S2-L6 | new | 18 | no |
| S2-GT | 20 | 20 | no |
| S2-C | 18 | 18 | no |
| S3-I | 23 | 12 | no |
| S3-L1 | 22 | 20 | no |
| S3-L2 | 22 | 15 | no |
| S3-L3 | 22 | 17 | no |
| S3-L4 | new | 16 | no |
| S3-L5 | new | 17 | no |
| S3-GT | 22 | 19 | no |
| S3-C | 19 | 19 | no |
| S4-I | 24 | 12 | no |
| S4-L1 | 22 | 18 | no |
| S4-L2 | 22 | 19 | no |
| S4-L3 | 22 | 18 | no |
| S4-L4 | 19 | 17 | no |
| S4-L5 | new | 17 | no |
| S4-L6 | new | 17 | no |
| S4-GT | 22 | 19 | no |
| S4-C | 20 | 20 | no |
| S5-I | 17 | 13 | no |
| S5-L1 | 22 | 16 | no |
| S5-L2 | 22 | 17 | no |
| S5-L3 | 22 | 19 | no |
| S5-L4 | 22 | 18 | no |
| S5-L5 | 21 | 18 | no |
| S5-L6 | new | 16 | no |
| S5-GT1 | 22 | 20 | no |
| S5-GT2 | 20 | 20 | no |
| FIN | 24 | 24 | yes |

Modules (not in this package; the squeeze that held them to 22 is gone, so two
grew): shells M-I 20, M-L1 20, M-L2 23, M-L3 22, M-GT 22, M-C 15; env M-I 22, M-L1 21, M-L2 22, M-L3 20, M-L4 17, M-L5 23, M-GT 20, M-C 16. WP-28 applies the skeleton to them.

## Hint renumbering (FF-010 anchors)

| Question | Old anchor | New anchor | Because |
| --- | --- | --- | --- |
| 1 Q1 `$` | Lesson 1.3 | Lesson 1.3 | unchanged: 1.3's notice |
| 1 Q2 `pwd` | Lesson 1.3 | Lesson 1.3 | unchanged |
| 1 Q3 where output goes | Lesson 1.1 (WP-23 text said 1.4) | Lesson 1.1 | §5: the output appears in 1.1's block |
| 2 Q1 `cd ..` | Lesson 2.3 | Lesson 2.3 | unchanged |
| 2 Q2 `~` | Lesson 2.3 | Lesson 2.4 | 2.4 Home and back |
| 2 Q3 `cd notes` | Lesson 2.4 | Lesson 2.5 | 2.5 Names for places |
| 3 Q1 touch | Lesson 3.1 | Lesson 3.1 | unchanged |
| 3 Q2 after rm | Lesson 3.3 | Lesson 3.5 | 3.5 Removing |
| 3 Q3 rename | Lesson 3.3 | Lesson 3.4 | 3.4 Copy and move |
| 4 Q1 `command -v` | Lesson 4.1 | Lesson 4.1 | unchanged |
| 4 Q2 `>` vs `>>` | Lesson 4.3 | Lesson 4.4 | 4.4 Into a file |
| 4 Q3 two files | Lesson 4.1 | Lesson 4.2 | 4.2 Spaces and quotes |
| 5 Q1 exit man | Lesson 5.1 | Lesson 5.1 | unchanged |
| 5 Q2 write | Lesson 5.3 | Lesson 5.3 | unchanged; "buffer" in the hint is now "copy" |
| 5 Q3 `:q!` | Lesson 5.3 | Lesson 5.4 | 5.4 Throw it away; "buffer" is now "working copy" |

Module hints (`Lesson N:`) are unchanged. FF-009 (exact forms and keyword
phrases), FF-010 and FF-011 (235 cases) are clean.

## Whitespace trims and words changed

- 2.1 and 2.5 had 14 body rows: two interior blank rows each were dropped
  (the one after the paragraph that ends in a colon, then the one above the
  notice). No word changed.
- Gate task screens: the new grey line `This task runs in <stage folder>;
  pwd shows it.` is on all six task screens. On Stage 3 and Stage 4 it
  replaces the `You will work inside <folder>.` and `Work inside <folder>.`
  lines (same fact; two words of wording differ). Stage 3, 4 and 5 task
  screens lost blank rows; Stage 5 phase 1 folds its three Vim sub-steps
  into two lines (`i, type a few letters, Esc` on one line), as phase 2
  already does.
- 1.3 and 1.4: no change needed.

## Open points for the coordinator

- §5 says to add "the screen" to 1.1's aside for the output question, while §3
  prints that aside as `# prints hello, then the prompt returns`. I kept §3
  verbatim; 1.4's notice still says "the window", which the Stage 1 Q3 group
  accepts, and `terminal`/`window`/`back to you` are in the group.
- The welcome (S1-W) is 21 rendered rows (20 panel rows) as WP-27 specified.
- Modules (`shells`, `env`) still print `shells 2 — ...`-style titles and are
  23 rows on two screens; WP-28.

## Harness

Bash 5.3 bundles (committed): `audit/2026-11-09/sim/wp26-all/` (UTF-8),
`wp26-ascii-all/`, `wp26-ascii-all-bash32/` (3.2.57), `wp26-second-try-stage2/`,
`wp26-second-try-stage4/`, `wp26-module-shells/`, `wp26-module-env/`. Sixteen
runs on 3.2.57 and 5.3, UTF-8 and ASCII: all `ok`. `compare_heights.py`: 46
screens identical between the forms and between the Bash versions.
