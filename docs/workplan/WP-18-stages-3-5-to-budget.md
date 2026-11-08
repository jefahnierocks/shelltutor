---
title: WP-18 — Stages 3–5 and the finale to the screen budget
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-08
tags: [workplan, phase-b, stage3, stage4, stage5, finale, screen-budget, o-j]
priority: high
---

# WP-18 — Stages 3–5 and the finale to the screen budget

**Governing text**: `docs/direction-decisions-2026-11.md` amendment A5
(operator approval 2026-11-08), observation O-J, and
`audit/2026-11-08/phase-b-closure.md` (heights on current `main`).
**Tier**: core standard (sentinels, personas, density rows, bundles).
**Depends on**: nothing open. **Touches `shelltutor`**: yes, stages 3–5
lesson heredocs and the finale only; gates, verifiers and recaps unchanged.

## Goal

Every screen fits an 80×24 terminal with its header and prompt visible:
heredoc content ≤ 18 lines, rendered ≤ 22 rows. Nine lesson screens and
the finale do not, so their headings scroll off before the prompt appears.

## Read first

- `audit/2026-11-08/phase-b-closure.md` (heights table), O-J in
  `audit/2026-11-08/findings.md`, `audit/2026-11-08/stage2-density.md`
  (the row format to reuse), `docs/design-description.md` §4.1 (split rule),
  `docs/simulation-design-plan.md` §Pedagogy And UX (one idea per screen).
- `shelltutor` stage 3–5 lesson functions and `finale`; `scripts/sim/`
  sentinels and `stage_walk` for stages 3–5.

## Rules

1. **Trim first, split second.** A screen is trimmed if it can reach 18
   heredoc lines without losing an idea or a demonstrated command; it is
   split when it carries two ideas (the split rule) or cannot be trimmed.
2. **No command disappears** from the course and no gate changes. The
   commands table in `README.md` and the cleared-screen recaps stay true.
3. Every surviving or new screen ends in a `${G_PLAY}` line; one idea per
   screen; headings follow `N.k — title`.
4. Splits renumber later lessons in that stage; intros state the new
   count; sentinels and personas follow in the same commit as the copy.

## Starting heights and the expected treatment

| Screen | Rendered now | Treatment |
| --- | --- | --- |
| 3.3 copy, move, delete | 25 | trim (the "safety habit" block compresses to two lines) |
| 4.1 reading a command | 29 | trim (one example per idea; `command -v` keeps two probes) |
| 4.2 the pipe | 28 | trim ("Things to notice" to one line) |
| 4.3 redirection and globs | 34 | **split**: 4.3 redirection (`>`, `>>`, `<`), 4.4 globs (`*`) |
| 5.1 print-and-exit vs full-screen | 27 | trim (the two lists share one line each) |
| 5.2 entering and leaving Vim | 31 | trim; split into "entering" and "leaving" only if trimming cannot reach 18 |
| 5.3 buffer vs file | 39 | **split**: 5.3 the idea (read → edit → write, the four commands), 5.4 practice both sequences on `practice.txt` |
| 5.4 calling vimtutor (becomes 5.5) | 26 | trim (install hints to two lines) |
| finale | 31 | trim to ≤ 22 rows: keep the command list and "What's next", drop the duplicated keys/operators/ideas block or fold it to two lines; the finale is not a panel |

Stage 4 becomes four lessons, Stage 5 five. The Stage 4 and Stage 5 intro
counts change; the Stage 5 gate text that says "the file-vs-buffer exercise
from 5.3" is re-pointed to the new practice lesson.

## Harness

- `sentinels.py`: new `S4_L4`, `S5_L5`; retitle where headings change.
- `persona.py` `stage_walk`: the 4.3 commands split across 4.3/4.4 (the
  glob `ls *.txt` moves to 4.4); the 5.3 vim sequences move to 5.4; the
  `command -v vimtutor` probe to 5.5.
- Re-run `careful-beginner --stage all`, `--stage 3`, `4`, `5`, and
  `second-try 4` on Bash 3.2 and 5.x; commit the 5.x bundles; report the
  full height table: every screen ≤ 22, finale ≤ 22.

## Records

- New `audit/<date>/stage3-5-density.md`: one row per changed or new screen
  (concepts, actions, heredoc lines, rendered rows, recommendation).
- `ROADMAP.md` Phase 3 Amendments: one dated line (Stage 4 four lessons,
  Stage 5 five; what was split and why).
- `README.md` Stages table unchanged (commands only); `STATUS.md` one line;
  O-J marked resolved in `audit/2026-11-08/findings.md`.

## Acceptance

1. `make verify` green (FF-004, FF-008, FF-009 clean).
2. Height table: no screen above 22 rendered rows on Bash 5.x or 3.2;
   no heredoc above 18 lines.
3. Gates and verifiers byte-identical to `main` except the re-pointed
   Stage 5 gate sentence; all five gates still pass in the harness.
4. Every command in the README table still appears in a lesson.

## Commits

1. `feat(stage3): 3.3 trimmed to the screen budget`
2. `feat(stage4): 4.1 and 4.2 trimmed; 4.3 split into redirection and globs (four lessons)`
3. `feat(stage5): 5.1, 5.2 and 5.5 trimmed; 5.3 split into the idea and the practice (five lessons)`
4. `feat(finale): summary screen within the budget`
5. `chore(sim): stage 3–5 sentinels and walks; density rows; ROADMAP amendment; O-J resolved; evidence; STATUS`
