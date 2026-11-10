---
title: WP-29 round-6 copy fixes — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-09
tags: [audit, wp-29, copy, recall, round6, a14]
priority: low
---

# WP-29 — evidence (commits 1–4; commit 5, Leo v0.3, is a6's)

Branch `wp/29-copy-fixes` from `2efa8bb`. Governing text: A14 and
`audit/2026-11-09/walkthroughs.md` round 6 (F-031, O-AY..O-BG).

## Harness

Bash 5.3 bundles (committed): `audit/2026-11-09/sim/wp29-all/` (UTF-8),
`wp29-ascii-all/`, `wp29-ascii-all-bash32/`, `wp29-second-try-stage2/`,
`wp29-second-try-stage4/`, `wp29-module-shells/`, `wp29-module-env/`. Twelve
runs on 3.2.57 and 5.3, UTF-8 and ASCII: all `ok`. `compare_heights.py`: 46
screens identical between the forms and the Bash versions. The harness
enforces the 20-rendered-row budget on every core screen (it passed); only the
welcome (21, A12) and the finale (24, not a panel) are above 20.

## Heights that moved (rendered rows; budget 20)

| Screen | WP-26 | Now | Why |
| --- | ---: | ---: | --- |
| S1-C | 20 | 19 | `clear` row dropped from the cleared list |
| S2-L4 | 17 | 18 | the notice is two lines |
| S3-I, S4-I | 12 | 14 | the stage-folder line (two lines) |
| S5-I | 13 | 15 | the stage-folder line (two lines) |
| S4-L3 | 18 | 19 | the stream sentence takes a second model line |
| S4-L6 | 17 | 18 | the glob sentence |

Every other screen is unchanged; 2.5 stays at 20.

## Words changed beyond the package, and layout choices

- 2.5: the new four-line block needed two more rows than 2.5 had. The three
  short names (`.`, `..`, `~`) now share one line (layout only). No word of the
  package's wording changed; the earlier-dropped blank before the block stays
  dropped.
- 4.6: "A name with * in it is called a glob." joins the notice, ahead of
  "Predict before you act: rm * would remove everything in the folder." The
  notice is two lines.
- The stage-folder line is a separate two-line paragraph in each intro,
  wrapped by hand; `pwd` in it is typeable green.

## Corpus (FF-011)

235 to 246 cases (accepted 118 to 126, rejected 117 to 120). Against the
previous script the new file fails five accept rows (`no the changes were
thrown away`, `no it is unchanged`, `no it did not change`, `the file did not
change`, `no nothing changed`); with the change all 246 pass. FF-009 and FF-010
are clean.
