---
title: WP-15 screen chrome — screen heights and Bash 3.2 finding
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-08
tags: [audit, wp-15, chrome, screen-height, bash-3-2]
priority: medium
---

# WP-15 — screen heights before and after, and the Bash 3.2 offset

Rendered rows between a screen's clear and the practice prompt, from
`careful-beginner --stage all` (same harness counter, budget 22). "Before" is
`main` at `d21ca58`; "after" is `wp/15-screen-chrome`. Bundles:
`audit/2026-11-08/sim/wp15-all/` and `wp15-second-try-stage{2,4}/` (Bash
5.3.20). The 3.2.57 runs (`/bin/bash`) were made with the same commands and
are not committed.

| Screen | Before (5.x) | After (5.x) | After (3.2.57) | Over after (5.x) |
| --- | ---: | ---: | ---: | --- |
| S1-W | 15 | 18 | 22 | no |
| S1-O | 19 | 21 | 25 | no |
| S1-I | 9 | 11 | 15 | no |
| S1-L1 | 18 | 20 | 24 | no |
| S1-L2 | 17 | 19 | 23 | no |
| S1-L3 | 14 | 16 | 20 | no |
| S1-L4 | 20 | 22 | 26 | no |
| S1-GT | 14 | 16 | 20 | no |
| S2-I | 19 | 21 | 25 | no |
| S2-L1 | 17 | 19 | 23 | no |
| S2-L2 | 20 | 22 | 26 | no |
| S2-L3 | 25 | 27 | 31 | yes |
| S2-GT | 15 | 17 | 21 | no |
| S3-I | 20 | 22 | 26 | no |
| S3-L1 | 20 | 22 | 26 | no |
| S3-L2 | 20 | 22 | 26 | no |
| S3-L3 | 23 | 25 | 29 | yes |
| S3-GT | 20 | 22 | 26 | no |
| S4-I | 22 | 22 | 26 | no |
| S4-L1 | 27 | 29 | 33 | yes |
| S4-L2 | 26 | 28 | 32 | yes |
| S4-L3 | 32 | 34 | 38 | yes |
| S4-GT | 19 | 21 | 25 | no |
| S5-I | 13 | 15 | 19 | no |
| S5-L1 | 25 | 27 | 31 | yes |
| S5-L2 | 29 | 31 | 35 | yes |
| S5-L3 | 37 | 39 | 43 | yes |
| S5-L4 | 24 | 26 | 30 | yes |
| S5-GT1 | 21 | 22 | 26 | no |
| S5-GT2 | 16 | 18 | 22 | no |
| FIN | 31 | 31 | 31 | yes |

- The chrome adds exactly two rows (header, lower rule; the blank moved).
  S1-W also gains one row for the authority sentence (15 to 18).
- Two screens fit at 21 and 22 rows before and would have exceeded the budget:
  S4-I and S5-GT1. Each lost one or two blank lines (no wording change) and
  now render at 22. No screen that fit before exceeds 22 after.
- The ten screens over budget in the WP-13 table (S2-L3, S3-L3, S4-L1, S4-L2,
  S4-L3, S5-L1, S5-L2, S5-L3, S5-L4, FIN) are unchanged in kind and remain
  for WP-14 or a later package; each is two rows taller except FIN, which has
  no panel.

## Why Bash 3.2 reads four rows taller

Not a counting artefact; the rows are on screen. In the raw stream, between
the footer bar and the first prompt, `/bin/bash` 3.2.57 on macOS prints:

```
ESC[?1034h
(blank)
The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
```

`ESC[?1034h` (meta key) is zero-width; the blank line and the three-line
Apple banner are four real rows, once per practice-shell start. Bash 5.x prints
only `ESC[?2004h`. The counter is correct and is left alone. Finding for
the coordinator: every practice screen under macOS `/bin/bash` is four rows
taller than the budget assumes, so at 24 rows the header of a 20-row screen
scrolls off. Apple's banner is silenced by `BASH_SILENCE_DEPRECATION_WARNING=1`
in the environment of the practice shell, a one-token addition to the launch
line in `practice()`; it is not part of WP-15 and was not applied here.
