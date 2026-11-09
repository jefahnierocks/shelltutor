---
title: WP-21 — Recall answer shape and small Stage 1–2 grounding (F-019, F-020, O-Z, O-AB, O-AC, O-AD)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, stage1, stage2, recall, a8]
priority: high
---

# WP-21 — Recall answer shape and small Stage 1–2 grounding

**Governing text**: `docs/direction-decisions-2026-11.md` amendment A8
(operator approval 2026-11-09) and `audit/2026-11-09/walkthroughs.md`
round 2 (F-019, F-020, O-Z, O-AB, O-AC, O-AD). **Tier**: core standard.
**Touches `shelltutor`**: yes: `ask_question`, three accepted lists, one
hint, lessons 1.1, 2.2, 2.3. **Not** a containment rule (A8: the
negation counterexamples in F-019 are real; shaping the answer is cheaper
than guarding it).

## Read first

F-019's table and counterexamples; F-020; O-Z; O-AB, O-AC, O-AD.
`shelltutor`: `ask_question` (~673), Stage 1 Q3 (~1160), Stage 2 Q1
(~1409), lesson 1.1 (~900), 2.2 (~1335), 2.3 (~1355). `scripts/check-hints.sh`.

## Change 1 — Longer accepted forms and the hint's own words (F-019, F-020)

- Stage 1 Q3 list gains: `it shows up on the screen`, `shows up on the
  screen`, `it comes back to me on the screen`, `comes back on the screen`,
  `back to me on the screen`, `the window`, `the window you type into`,
  `in the window you type into`, `back to me in the window you type into`,
  `the terminal window`-style forms already present stay.
- Stage 2 Q1 list gains: `it goes up one level to the parent folder`,
  `goes up one level to the parent folder`, `up one level to the parent
  folder`, `goes to the parent folder`, `it goes to the parent folder`,
  `up to the parent folder`, `goes up one`, `up a level`.
- `normalize_answer` also drops commas, periods and exclamation marks
  (the sheet input had a comma). Verify on 3.2 and 5.x and under
  `LC_ALL=C`.
- FF-009: the Q3 hint now contains accepted words ("in the window you type
  into"). Reword the hint, not the list: "Lesson 1.4: a program's output
  does not go into a file by itself; it comes straight back to you." Run
  `make check`; if a leak remains, adjust the hint again.

## Change 2 — The second miss names the expected shape (O-Z)

In `ask_question`, from miss 2 onward, one extra line before the three
facts: `Answer in a few words, like the lesson did, not a full sentence.`
Same line for every question (A1.1: no per-question variation). Rendered
inside the `┃` block in DIM. `second-try` oracle: the line appears exactly
once in the Stage 2 recall run (miss 2 only, since that persona misses
twice); add a sentinel. C-006 gains the line as non-contractual wording.

## Change 3 — Typos named (O-AB)

- 1.1's existing line becomes: "If bash says `command not found` or
  `No such file`, you mistyped: a stray `/` in front, or a missing space.
  Type it again." (one line; 1.1 stays ≤ 18 heredoc lines; wrap to two if
  80 columns need it and drop the blank line above instead).
- 2.3 gains, after the `cd ..` line: `cd..` with no space is a different
  word; bash cannot find it. (one line)

## Change 4 — 2.3 home versus practice folder; try-it line (O-AC)

- 2.3's `cd` line reads: `cd` alone goes to your home folder, outside this
  practice area; `cd "$SANDBOX"`-style literal is NOT shown. Instead the
  line after says: "Type `cd -` to come back where you were." (confirm
  `cd -` works in the practice shell on 3.2; it does, OLDPWD is set.)
- Replace 2.3's "Type next to continue" ending with the course's form:
  `▶ Try cd .., pwd, then cd -, then next.`
- Remove the unexplained `$HOME` if it appears on the screen; keep `~`.

## Change 5 — Smaller first listing (O-AD)

2.2: replace `ls /etc` with `ls /` (a dozen entries on macOS and Linux; the
gloss "the top of everything"). Keep `ls /usr/bin` as the second example
and add the gloss "long: many commands live here". Harness: no error
signature change.

## Harness and records

- Density rows for 1.1, 2.2, 2.3 appended to the density follow-up.
- `docs/contracts.md` C-006 wording line.
- F-019, F-020 resolved with SHAs; O-Z, O-AB, O-AC, O-AD addressed in
  `audit/2026-11-09/walkthroughs.md`.
- `STATUS.md` one line.

## Acceptance

1. `make verify` green; FF-009 clean; every touched screen ≤ 18 heredoc
   lines and ≤ 22 rendered rows.
2. careful-beginner `--stage all`, second-try 2 and 4 green on 3.2 and
   5.x; the shape line appears once in second-try 2.
3. Report shows a `normalize_answer` table for all round-2 rejected inputs
   (F-019, F-020) now accepted, and the four negation counterexamples
   still rejected.

## Commits

1. `fix(gate): longer plain forms at Stage 1 Q3 and Stage 2 Q1; punctuation normalised; Q3 hint reworded (F-019, F-020)`
2. `feat(gate): second recall miss names the expected answer shape (O-Z)`
3. `fix(stage1,stage2): typo lines for stray slash and cd.. (O-AB)`
4. `fix(stage2): 2.3 says cd goes home and cd - comes back; try-it line (O-AC)`
5. `fix(stage2): ls / as the first outside listing (O-AD)`
6. `chore(sim): shape sentinel; density rows; C-006; findings resolved; STATUS`
