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
| S1-L2 `1.2 keyboard habits` | 15 | Tab completion (shared part, second Tab lists); Up-arrow recall; Ctrl+L and `clear`; Ctrl+C | 4 (one keypress each) | **keep with watch** — four keys exceed the literal rule, but they are one family and each is a single keystroke; splitting again would fragment the card |
| S1-L3 `1.3 where / who / when` | 12 | `whoami`; `pwd`; `date`; why `pwd` shows the tutor folder | 3 | **keep** — trimmed |
| S1-L4 `1.4 what just happened` | 18 | terminal → shell → program; five-step pipeline | 0 (read) | **keep with watch** — footer now `▶ Type next.` |
| S1-L5 `1.5 who else types here` | 19 | agent → shell → program; three habits (read the line, know the folder, read the output) | 0 (read) | **keep with watch** — WP-12; two read-only screens, 1.4 and 1.5, now precede the gate (A1.5) |

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
