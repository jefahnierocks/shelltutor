---
title: Stage 1 Density Follow-up (WP-04)
category: audit
component: stage1-density
status: active
version: 0.1.0
last_updated: 2026-11-08
tags: [audit, density, stage1, ux, wp-04]
priority: medium
---

# Stage 1 Density Follow-up (WP-04)

Follow-up to `audit/2026-05-23/stage1-density.md` after the work-plan
decision D-13: Stage 1 now has four lessons. The ordering rule in the
original audit is satisfied: the `current-rc` baseline (Slice 1) and the
five-stage baseline (WP-01) both pre-date this change.

## Original rows

| Original row | Action in WP-04 |
| --- | --- |
| S1-L1 `1.1 running commands` (SPLIT) | **Acted on.** Split into the new 1.1 (running commands) and 1.2 (keyboard habits). |
| S1-L2 `1.2 identity / location / time` (SPLIT or TRIM) | **Acted on (TRIM).** The `clear` block moved to the keyboard lesson and the Stage 2 forward reference became one plain sentence; no split needed. |
| S1-O `orientation()` (keep with watch) | Unchanged; still under watch. |
| S1-L3 `1.3 what just happened` (keep with watch) | Unchanged text, renumbered 1.4; still under watch. |
| S1-W, S1-I, S1-G | Unchanged except the intro now says "Four short lessons". |

## Re-tagged lesson screens

Content lines are the heredoc lines of each screen function, counting blank
lines (the vertical budget is 24 rows minus the practice prompt; none above
20).

| Screen | Content lines | Concepts introduced | Distinct actions | Recommendation |
| --- | ---: | --- | ---: | --- |
| S1-I `stage1_intro` | 7 | stage scope (five lessons + a small task; WP-12) | 1 | keep |
| S1-L1 `1.1 running commands` | 16 | `echo`; spaces separate words vs quotes group them; a command is a name plus words | 3 (the three `echo` forms) | **keep** — one concept family, three variations of one action |
| S1-L2 `1.2 keyboard habits` | 14 | Tab completion (shared part, second Tab lists); Up-arrow recall; Ctrl+L and `clear`; Ctrl+C | 4 (one keypress each) | **keep with watch** — four keys exceed the literal rule, but they are one family and each is a single keystroke; splitting again would fragment the card |
| S1-L3 `1.3 where / who / when` | 12 | `whoami`; `pwd`; `date`; why `pwd` shows the tutor folder | 3 | **keep** — trimmed |
| S1-L4 `1.4 the shell, caught in the act` | 18 | the shell speaks (`bash: dtae: command not found`); terminal → shell → program, anchored | 2 (`date`, `dtae`) | **keep** — WP-14 replaced the five-step list; the model now rests on something the learner sees. Footer `▶ Type next.` |
| S1-L5 `1.5 who else types here` | 16 | agent → shell → program; three habits (read the line, know the folder, read the output) | 0 (read) | **keep with watch** — WP-12; two read-only screens, 1.4 and 1.5, now precede the gate (A1.5) |

## Evidence

- **Before** (old three-lesson layout): `audit/2026-11-08/sim/stage1-slice2/`
  and `all-slice2/` (Bash 5.3.20), plus the `-bash32` bundles (3.2.57).
- **After** (four lessons): `audit/2026-11-08/sim/stage1-wp04/` (Bash 5.3.20)
  and `stage1-wp04-bash32/` (3.2.57): `ok`, `progress_after` = `1`, no error
  signatures. The walk exercises `echo` x3, Tab completion, Ctrl+L, Up-arrow
  recall, Ctrl+C and `whoami`/`pwd`/`date`. `--stage all` also passes under both
  Bash versions (scratch run, not committed).
- Ctrl+C is echoed as `^C` under Bash 5.3 and not under Bash 3.2; the fresh
  prompt appears in both.

## Watch items

The harness is deterministic and has no human pauses, so it cannot supply the
"long pause before `next`" signal the original audit asked for on S1-L4 (now
1.4) or the orientation card. Those two stay under watch until a human
Phase 2 walkthrough (`docs/phase2-walkthrough-checklist.md`) reports on them.

## WP-14 amendment (2026-11-08)

1.4 is replaced (O-L): the learner types `date`, then the mistyped `dtae`,
and reads `bash:` as the shell speaking. The harness records the error as
`expected-error` on S1-L4 only. Lesson 1.2's Ctrl+L and `show` sentences
are one line (O-K, A2.5; `clear` is kept in the same line). Heredoc lines
above are measured on the WP-14 revision; the S1-L5 row corrects the 19
recorded by WP-12 (the closing paragraph was cut for the chrome). Rendered
heights on Bash 5.3.20 and 3.2.57 (identical): S1-L1 20, S1-L2 18,
S1-L3 16, S1-L4 22, S1-L5 20. Stage 2 is in `stage2-density.md`.

## WP-20 amendment (2026-11-09)

Rows for the three lessons WP-20 touched (A7). Heredoc lines measured on
the WP-20 branch; rendered heights from `careful-beginner --stage all`,
identical on Bash 5.3 and 3.2.57. The 1.x names are the current numbering.

| Screen | Heredoc lines | Rendered | Change |
| --- | ---: | ---: | --- |
| S1-L1 `1.1 running commands` | 18 (was 16) | 22 (was 20) | One line after the three `echo` commands: `command not found` means a mistype, so type it again. The `#` asides stay. At the 22-row budget. |
| S1-L2 `1.2 keyboard habits` | 14 (was 14) | 18 (was 18) | Tab line ends "then press Enter to run it."; the Up line says Enter runs it and Ctrl+C throws it away. Same length. |
| S1-L3 `1.3 where / who / when` | 15 (was 12) | 19 (was 16) | Two lines (plus a blank) naming both prompts: this tutor's ends in `>`, a normal bash window's usually in `$` (F-017). |

## WP-21 amendment (2026-11-09)

Heredoc lines on the WP-21 branch; rendered heights identical on Bash 5.3 and
3.2.57 and unchanged from WP-20 (A8).

| Screen | Heredoc lines | Rendered | Change |
| --- | ---: | ---: | --- |
| S1-L1 `1.1 running commands` | 18 (was 18) | 22 (was 22) | The `command not found` line names `No such file`, a stray `/` and a missing space (O-AB); two lines, the blank above dropped. |
| S2-L2 `2.2 ls` | 16 (was 16) | 20 (was 20) | `ls /` replaces `ls /etc` as the first outside listing; `ls /usr/bin` stays (O-AD). |
| S2-L3 `2.3 cd` | 18 (was 18) | 22 (was 22) | `cd` goes home outside the practice area; `cd -` comes back; `cd..` named; `$HOME` removed; ends in a try-it line (O-AB, O-AC). The sandbox path line still wraps, so rendered rows stay at the budget. |

## WP-22 amendment (2026-11-09)

Heredoc lines on the WP-22 branch; rendered heights identical on Bash 5.3 and
3.2.57 (A9). Correction: the WP-21 row above gave 2.3 as 16 lines; it is 18
(unchanged by WP-21), measured per function.

| Screen | Heredoc lines | Rendered | Change |
| --- | ---: | ---: | --- |
| S1-L2 `1.2 keyboard habits` | 15 (was 14) | 19 (was 18) | Ctrl+C is the escape hatch at a prompt; inside a full-screen program such as `less`, `q` is the way out (F-024). |
| S2-L4 `2.4 names for places` | 18 (was 18) | 22 (was 22) | `mkdir name` line and the try-it line `Try mkdir demo, ls -p, then next`; the `cat notes.txt` paragraph became one bare-name line and the two absolute paths share a line (F-022). |
| S2-GT `Stage 2 gate task` | 14 (was 13) | 18 (was 17) | A DIM line: the task runs in this stage's own folder, `pwd` shows it (O-AG). The recall screen gains the "this is not the shell" line (6 lines). |
| S3-L2 `3.2 cat, less` | 18 (was 18) | 22 (was 22) | The try-it line names `q` (F-024). |
| S3-L3 `3.3 cp, mv, rm` | 18 (was 18) | 22 (was 22) | The try-it line asks to type `cp`, `mv` and `rm` (O-AI). |

## WP-23 amendment (2026-11-09)

| Screen | Heredoc lines | Rendered | Change |
| --- | ---: | ---: | --- |
| S3-L1 `3.1 creating` | 17 (was 18) | 21 | `echo hello > notes.txt` is a taught line (more on `>` in Stage 4); the try-it line is "Make a few, put a word in one, then next" (F-028). |

## WP-25 amendment (2026-11-09)

Chrome v2 (A11) changes the budget to a 19-row panel (20 rendered rows with the
blank under the rule): the footer moved above the rule, and the `▶` line has a
blank row on each side. Bodies are unchanged, so most screens grew by one or
two rows; an interim squeeze drops interior blank rows to hold a 21-row panel
hard cap. The full table (before WP-25, after, over 20) is in
`audit/2026-11-09/wp25-chrome-v2.md`; the screens over the new budget are the
input to WP-26.

## WP-27 amendment (2026-11-09)

| Screen | Rendered | Change |
| --- | ---: | --- |
| S1-W `welcome` | 21 (was 19) | The course map moves inside the box, one stage per row with a dot each (O-AW); the dots-and-names row and the `Sandbox:` row under the box go (O-AX). 17 box rows, all exactly 80 columns in both glyph forms; the review allows 22. |
