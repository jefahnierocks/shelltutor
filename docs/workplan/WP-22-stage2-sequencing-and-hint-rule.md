---
title: WP-22 — Stage 2 sequencing, Stage 3–4 defect fixes, hint rule FF-010 (F-021..F-024)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, stage2, stage3, stage4, recall, fitness, a9]
priority: high
---

# WP-22 — Stage 2 sequencing, Stage 3–4 defect fixes, hint rule

**Governing text**: `docs/direction-decisions-2026-11.md` amendment A9
(operator approval 2026-11-09) and `audit/2026-11-09/walkthroughs.md`
round 3 (F-021, F-022, F-023, F-024, O-AH..O-AM). **Tier**: core
standard. **Touches `shelltutor`**: yes. A9 confirms: rejected correct
answers and false statements are defects and are fixed wherever they sit;
Stages 3–5 are otherwise not re-sequenced.

## Read first

The four findings with their line cites; `ask_question`; the Stage 2 gate
(`run_stage2` ~1470–1510, `gate_require_history`, `gate_escalate`); 2.4;
3.2 (~1618), 3.3; Stage 4 Q1 (~1913); `scripts/check-hints.sh`;
`CONTRIBUTING.md` §Fitness functions.

## Change 1 — Stage 2 teaches `mkdir`; the gate checks both items (F-022)

- 2.4 gains two lines before its `▶` line: `mkdir name  # make a folder`
  and the `▶` line becomes "Try `mkdir demo`, `ls -p`, then `next`."
  (2.4 ≤ 18 heredoc lines; drop a blank if needed.) If 2.4 cannot hold
  it, put it in 2.3 after `cd -`; report which.
- The first `check` at the Stage 2 gate prints the full `┃` checklist:
  `folder practice exists` and `cd into it (cd practice)`, each ✓ or ○
  with its `not yet:`; today it reports only the `cd` item. The `cd`
  item is satisfied only if the folder exists AND `cd` is in history
  (a failed `cd practice` no longer counts).
- The gate screen's `▶` line says "Type `check` when done." as today, and
  a new DIM line above it: "The task runs in this stage's own folder;
  `pwd` shows it." (O-AG). One more line at the top of the recall block,
  as at Stage 1: "First, three questions. Type your answer in words; this
  is not the shell." (O-AK).

## Change 2 — `~` accepts the lessons' gloss (F-021)

Stage 2 Q2 list gains `your home folder`, `your home directory`,
`your home`, `the home`, `home folder of the user`, `my home`. Hint
reworded per Change 5.

## Change 3 — Stage 4 Q1 (F-023)

List gains `the path /usr/bin/vim`, `the path to the vim program`,
`where the vim program is`, `where the program file is`, `the location of
vim`, `vim's location`, `its location`, `the full path`, `the full path to
vim`, `the folder and file name`. Hint becomes "Lesson 4.1: it answers
the question 'where does this program live?' with one line." (FF-009 must
pass; adjust the hint, not the list.) Any inputs from round 3 that still
fail go in the report.

## Change 4 — Ctrl+C truth and `q` (F-024, O-AI)

- 1.2's Ctrl+C lines: "the escape hatch at a prompt: if a command feels
  stuck, press it and you get a fresh prompt. Inside a full-screen program
  like `less` (Stage 3), `q` is the way out."
- 3.2's `▶` line: "Try both; `q` leaves `less`; then `next`."
- 3.3's `▶` line asks the learner to type the three commands: "Try `cp`,
  `mv` and `rm` on the practice files, then `next`." (Stage 3 lesson
  bodies are otherwise untouched.)

## Change 5 — FF-010: every recall hint points at its lesson

- New `scripts/check-hints.sh` rule (or `scripts/check-hint-anchors.sh`;
  the agent picks and documents): the second argument of every
  `ask_question` call must match `^Lesson [0-9]+(\.[0-9]+)?: ` after
  stripping colour variables. Add to `make check`, `CONTRIBUTING.md`
  §Fitness functions as FF-010, with the rule in words: a hint says where
  the fact was taught and names the concept; it never paraphrases the
  answer (a paraphrase invites the learner to type it back, and FF-009
  then forbids accepting it).
- Reword the hints that fail today (there are nine: Stage 1 Q1 missing
  colon; Stage 2 Q2; Stage 3 Q1, Q3; Stage 4 Q1, Q2, Q3; Stage 5 Q1, Q2).
  Each new hint: `Lesson N.k: <one clause naming the concept>`. FF-009 must
  still pass. Module questions already use `Lesson N:`; the regex admits
  them.

## Harness and records

- Personas: `careful-beginner` Stage 2 gate actions gain `mkdir practice`
  if not present; `second-try` Stage 2 first `check` oracle expects the
  two-item checklist (two `○` lines or one ✓ one ○; state which).
- Density rows for 1.2, 2.4, 3.2, 3.3, Stage 2 gate screen.
- `docs/contracts.md`: C-006 unchanged; note FF-010 under the hint rule.
- F-021..F-024 resolved with SHAs; O-AG, O-AI, O-AK addressed.
- `STATUS.md` one line.

## Acceptance

1. `make verify` green including FF-009 and FF-010; touched screens ≤ 18
   heredoc lines and ≤ 22 rendered rows.
2. careful-beginner `--stage all`, second-try 2 and 4 green on 3.2 and
   5.x.
3. Report: `normalize_answer` table for every round-3 rejected recall
   input now accepted; the first-`check` output at the Stage 2 gate quoted
   from a scratch sitting with no folder made; `q` exits `less` and 3.2's
   line says so.

## Commits

1. `feat(stage2): 2.4 teaches mkdir; gate check lists both items and requires the folder (F-022, O-AG, O-AK)`
2. `fix(gate): Stage 2 Q2 accepts the lessons' gloss for ~ (F-021)`
3. `fix(gate): Stage 4 Q1 accepts path forms; hint reworded (F-023)`
4. `fix(stage1,stage3): Ctrl+C truth, q leaves less, 3.3 asks to type cp mv rm (F-024, O-AI)`
5. `feat(check): FF-010 every recall hint is anchored to its lesson; nine hints reworded`
6. `chore(sim): personas and oracle; density rows; findings resolved; STATUS`
