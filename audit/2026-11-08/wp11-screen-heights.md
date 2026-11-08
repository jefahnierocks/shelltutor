---
title: WP-11 — Bash 3.2 screen heights after silencing the Apple banner (F-016)
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-08
tags: [audit, wp-11, f-016, screen-height, bash-3-2]
priority: medium
---

# WP-11 commit 0 — F-016 proof

Rendered rows between a screen's clear and the practice prompt,
`careful-beginner --stage all` under Bash 3.2.57 (`/bin/bash` first on
`PATH`), same counter, budget 22. "Before" is `main` at `7f3a28b`
(WP-15 chrome, banner still printed); "after" adds
`BASH_SILENCE_DEPRECATION_WARNING=1` on the practice launch line.

| Screen | Before (3.2) | After (3.2) | Delta |
| --- | ---: | ---: | ---: |
| S1-W | 22 | 18 | 4 |
| S1-O | 25 | 21 | 4 |
| S1-I | 15 | 11 | 4 |
| S1-L1 | 24 | 20 | 4 |
| S1-L2 | 23 | 19 | 4 |
| S1-L3 | 20 | 16 | 4 |
| S1-L4 | 26 | 22 | 4 |
| S1-GT | 20 | 16 | 4 |
| S2-I | 25 | 21 | 4 |
| S2-L1 | 23 | 19 | 4 |
| S2-L2 | 26 | 22 | 4 |
| S2-L3 | 31 | 27 | 4 |
| S2-GT | 21 | 17 | 4 |
| S3-I | 26 | 22 | 4 |
| S3-L1 | 26 | 22 | 4 |
| S3-L2 | 26 | 22 | 4 |
| S3-L3 | 29 | 25 | 4 |
| S3-GT | 26 | 22 | 4 |
| S4-I | 26 | 22 | 4 |
| S4-L1 | 33 | 29 | 4 |
| S4-L2 | 32 | 28 | 4 |
| S4-L3 | 38 | 34 | 4 |
| S4-GT | 25 | 21 | 4 |
| S5-I | 19 | 15 | 4 |
| S5-L1 | 31 | 27 | 4 |
| S5-L2 | 35 | 31 | 4 |
| S5-L3 | 43 | 39 | 4 |
| S5-L4 | 30 | 26 | 4 |
| S5-GT1 | 26 | 22 | 4 |
| S5-GT2 | 22 | 18 | 4 |
| FIN | 31 | 31 | 0 |

Every screen that ends at a practice prompt drops by four rows; FIN has no
practice prompt and is unchanged. The after column equals the Bash 5.x
column in `wp15-screen-heights.md` row for row.

One implementation note: Apple's bash checks the variable after it has run
the rcfile (the banner prints after the footer the rcfile emits), so an
`unset` in the rcfile defeats it. The first attempt did exactly that and the
table did not move; the variable therefore stays set in the practice shell.

## Full table with the cleared screens (commit 3)

`careful-beginner --stage all`, budget 22. 3.2.57 and 5.3.20 now agree on
every row. The new cleared screens (S1-C to S4-C) render at 19 rows with
15 lines of content; the Stage 1-4 gate screens are unchanged.

| Screen | WP-15 (5.x) | WP-11 (5.x) | WP-11 (3.2) | Over (5.x) |
| --- | ---: | ---: | ---: | --- |
| S1-W | 18 | 18 | 18 | no |
| S1-O | 21 | 21 | 21 | no |
| S1-I | 11 | 11 | 11 | no |
| S1-L1 | 20 | 20 | 20 | no |
| S1-L2 | 19 | 19 | 19 | no |
| S1-L3 | 16 | 16 | 16 | no |
| S1-L4 | 22 | 22 | 22 | no |
| S1-GT | 16 | 16 | 16 | no |
| S1-C | — | 19 | 19 | no |
| S2-I | 21 | 21 | 21 | no |
| S2-L1 | 19 | 19 | 19 | no |
| S2-L2 | 22 | 22 | 22 | no |
| S2-L3 | 27 | 27 | 27 | yes |
| S2-GT | 17 | 17 | 17 | no |
| S2-C | — | 19 | 19 | no |
| S3-I | 22 | 22 | 22 | no |
| S3-L1 | 22 | 22 | 22 | no |
| S3-L2 | 22 | 22 | 22 | no |
| S3-L3 | 25 | 25 | 25 | yes |
| S3-GT | 22 | 22 | 22 | no |
| S3-C | — | 19 | 19 | no |
| S4-I | 22 | 22 | 22 | no |
| S4-L1 | 29 | 29 | 29 | yes |
| S4-L2 | 28 | 28 | 28 | yes |
| S4-L3 | 34 | 34 | 34 | yes |
| S4-GT | 21 | 21 | 21 | no |
| S4-C | — | 19 | 19 | no |
| S5-I | 15 | 15 | 15 | no |
| S5-L1 | 27 | 27 | 27 | yes |
| S5-L2 | 31 | 31 | 31 | yes |
| S5-L3 | 39 | 39 | 39 | yes |
| S5-L4 | 26 | 26 | 26 | yes |
| S5-GT1 | 22 | 22 | 22 | no |
| S5-GT2 | 18 | 18 | 18 | no |
| FIN | 31 | 31 | 31 | yes |
