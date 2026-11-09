---
title: WP-20 — Stage 1 gate grounding (F-017, F-018, O-P, O-Q, O-S, O-V)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, stage1, gate, recall, ladder, a7]
priority: high
---

# WP-20 — Stage 1 gate grounding

**Governing text**: `docs/direction-decisions-2026-11.md` amendment A7
(operator approval of all five items, 2026-11-09) and
`audit/2026-11-09/walkthroughs.md` (F-017, F-018, O-P, O-Q, O-S, O-U,
O-V, O-W). **Tier**: core standard. **Touches `shelltutor`**: yes, Stage
1 screens, `ask_question`, `normalize_answer`, the Stage 1 recall lists.

## Goal

Make the Stage 1 gate passable by a learner who read the lessons: teach
what Q1 asks, accept the plain answers the lessons themselves use, show the
hint on the first recall miss, make recall visibly the tutor speaking, and
remove two mechanical traps in 1.1 and 1.2.

## Read first

- A7; the two findings and the observations above, with their line cites.
- `shelltutor`: `normalize_answer`, `ask_question`, `fb_*` helpers,
  `stage1_lesson_1`..`stage1_lesson_3`, the Stage 1 `ask_question` calls.
- `scripts/check-hints.sh` (FF-009), `scripts/sim/persona.py`
  (`second_try` recall misses), `run.py` (recall oracle counts).

## Change 1 — Q1 taught and reworded (F-017; item 1)

- Lesson 1.3 gains two lines after the `pwd` sentence: "Your prompt here
  ends in `>`. A normal bash window's prompt usually ends in `$`; same idea,
  different decoration." (1.3 is 12 lines; stays ≤ 18.)
- Q1 becomes: "Q1: In a normal bash window (not this tutor), which
  character usually ends the prompt? (`$`, `;`, `:`, or `#`)". Accepted:
  `$`, `dollar`, `dollar sign`, `the dollar sign`. Hint: "Lesson 1.3
  compared this tutor's prompt with a normal one." (FF-009 must pass; the
  hint must not contain `$` or "dollar".)

## Change 2 — Plain answers accepted; apostrophes normalised (F-018; item 2)

- `normalize_answer` also deletes apostrophes (`'` and `’`) so "I'm" and
  "you're" match `im`/`youre` forms.
- Q2 accepted list gains: `the folder`, `this folder`, `the directory`,
  `the current directory`, `current directory`, `where i am`,
  `the folder youre in`, `the folder you are in`, `the folder im in`.
- Q3 accepted list gains: `to the screen`, `on the screen`, `standard out`,
  `the terminal window`, `the display`.
- Re-run FF-009; if the Q3 hint now leaks (it mentions "the window"),
  reword the hint, not the list.
- Amendment A7 extends A4: reproduced synthetic findings are a valid source
  for widening; cite `audit/2026-11-09/walkthroughs.md` in the commit body.

## Change 3 — Recall ladder: hint on the first miss (O-Q; item 3)

For recall questions only: miss 1 → message plus `Hint:`; miss 2 and later
→ hint plus the three navigation facts. Tasks keep their three rungs. C-006
updated accordingly. Harness: `second-try` Stage 2 misses Q1 twice (not
three times); the oracle expects `Hint:` exactly twice and the first
navigation fact exactly once.

## Change 4 — Recall is visibly the tutor (O-P; item 4)

Recall questions and the Stage 1 follow-ups render inside the `┃` block:
`┃ Q1: …` in Q, then `┃ answer in words: ` as the input cue (replacing
"your answer:"). The gate screen's "run a few commands and tell me what
they printed" stays, but a line is added: "First, three questions. Type
your answer in words; this is not the shell." Sentinels for the question
texts are unchanged (`Q1:` … prefixes still match after the bar).

## Change 5 — Two mechanical traps (O-S, O-V, O-U; item 5)

- 1.2: Tab line ends "then press Enter to run it."; Up line becomes
  "brings back the last line. Enter runs it; Ctrl+C throws it away."
  Keep ≤ 18 lines.
- 1.1: one line after the three echo commands: "If bash says
  `command not found`, you mistyped: type it again." (1.1 is 16; becomes
  17.) The `#` asides stay; add nothing else.

## Harness and records

- Personas: `second-try` Stage 2 recall misses reduced to two; Stage 1
  walk unchanged (the extra lines are read-only).
- Density follow-up rows for 1.1, 1.2, 1.3 (append to
  `audit/2026-11-08/stage1-density-followup.md`).
- `docs/contracts.md` C-006 (recall rung order).
- F-017, F-018 resolved with SHAs; O-P, O-Q, O-S, O-U, O-V marked
  addressed in `audit/2026-11-09/walkthroughs.md`.
- `STATUS.md` one line.

## Acceptance

1. `make verify` green (FF-009 included); every Stage 1 screen ≤ 18 heredoc
   lines and ≤ 22 rendered rows.
2. `careful-beginner --stage all` and `second-try 2`, `4` green on Bash 3.2
   and 5.x; Stage 2 `second-try`: `Hint:` ×2, first fact ×1.
3. The reproduced rejections from F-017/F-018 (`>` is still rejected by
   design; `the folder`, `the folder I'm in`, `the folder you're in`,
   `to the screen`, `standard out`) now pass through `normalize_answer`
   against the new lists, shown in the report.
4. Then the three personas are re-run (sittings `*-2`) by the coordinator.

## Commits

1. `fix(gate): Stage 1 Q1 taught in 1.3 and asked about a normal bash window (F-017)`
2. `fix(gate): plain answers accepted at Stage 1 Q2/Q3; apostrophes normalised (F-018)`
3. `feat(gate): recall shows the hint on the first miss; facts from the second (A7)`
4. `feat(gate): recall rendered as the tutor speaking — ┃ block and "answer in words" (O-P)`
5. `fix(stage1): Enter after Tab, Up then Enter or Ctrl+C, command-not-found line (O-S, O-V)`
6. `chore(sim): second-try recall misses; density rows; C-006; findings resolved; evidence; STATUS`
