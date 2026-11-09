---
title: WP-24 matcher tightening — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-09
tags: [audit, wp-24, recall, matching, ff-011, a10]
priority: medium
---

# WP-24 — evidence

Branch `wp/24-matcher-tightening` from `23f9aef`. Sources:
`audit/2026-11-09/walkthroughs.md` round 5 (F-029, F-030, O-AR, O-AS, O-AT).

## Corpus counts (FF-011)

| Point | Cases | Accepted | Rejected |
| --- | ---: | ---: | ---: |
| `main` before WP-24 (WP-23) | 184 | 102 | 82 |
| 36 probe reject rows added against the old groups | 220 | 102 | 118 |
| After commit 1 (13 probe rows + 8 protecting accept rows) | 205 | 110 | 95 |
| After commit 2 (23 probe rows + 3 ordered accept rows) | 230 | 113 | 117 |
| After commit 3 (4 accept rows for F-030) | 235 | 118 | 117 |

With all 36 probe rows against the unchanged groups, FF-011 fails on all 36
(`36 of 220 cases failed`): every probed wrong answer passed before. Commit 1
fails on its 13 rows before the group change and passes after; commit 3 fails
on three of its four accept rows before the normalisation change and passes
after. Final: accepted 102 to 118 (+16), rejected 82 to 117 (+35). One probe
row I added beyond the sheet, `>> overwrites and > appends`, is not rejectable
by ordered groups (the words are in the lesson's order); I dropped it and
recorded the limit in C-006.

## Group changes

One-word members replaced by lesson phrases: S1 Q2 (`folder`, `directory`,
`path`, `location`), S1 Q3 (`window`), S2 Q3 (`notes`), S4 Q1 (`where`,
`path`, `folder`, `location`), S4 Q2 (`end`), shells Q2 (the bare `command -v`),
env Q2 (`list`). `--reject` phrase lists on fifteen questions; `--ordered` on
S4 Q2. Nothing accepted by the WP-23 corpus stopped being accepted.

## Harness

Bash 5.3 bundles (committed): `audit/2026-11-09/sim/wp24-all/`,
`wp24-second-try-stage2/`, `wp24-second-try-stage4/`, `wp24-module-shells/`,
`wp24-module-env/`. Bash 3.2.57 runs: same commands, all `ok`, not committed.
No screen over budget; S1 gate task 17 rows, S4 gate task 21.
