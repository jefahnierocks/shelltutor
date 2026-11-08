---
title: WP-04 — Stage 1 density split (lessons 1.1–1.4)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-07
tags: [workplan, stage1, density, lessons, ux]
priority: medium
---

# WP-04 — Stage 1 density split (lessons 1.1–1.4)

**Depends on**: WP-03 (its Tab wording is embedded below; the hardened
Readline contract is what the new keyboard lesson teaches). **Blocks**:
nothing. **Touches `shelltutor`**: yes (Stage 1 screens only).
**Operator gate**: none.

## Goal

Act on the two `SPLIT` / `SPLIT or TRIM` rows of
`audit/2026-05-23/stage1-density.md`: split lesson 1.1 into a running-
commands screen and a keyboard-habits screen, trim the identity lesson,
renumber Stage 1 to four lessons, keep the harness in step, and record the
follow-up density audit. The ordering rule in the density audit is
satisfied: the `current-rc` baseline (Slice 1) and the five-stage baseline
(WP-01) both exist.

## Read first

- `docs/workplan/README.md` decision D-13.
- `audit/2026-05-23/stage1-density.md` (S1-L1, S1-L2 rows and the
  "Slice 1 baseline ordering rule").
- `docs/simulation-design-plan.md` §Pedagogy And UX (tone rules; the
  split rule).
- `shelltutor`: `stage1_intro`, `stage1_lesson_1`, `stage1_lesson_2`,
  `stage1_lesson_3`, `run_stage1`, and the vertical-budget comment above
  `welcome()`.
- `scripts/sim/sentinels.py`, `scripts/sim/persona.py` (Stage 1 walk),
  `scripts/sim/recorder.py` (`known_rough_edges`).
- `ROADMAP.md` Phase 3 "Per-stage detail — Stage 1".

## Exact screens

Replace `stage1_lesson_1`, `stage1_lesson_2`, `stage1_lesson_3` with four
functions. Function names: `stage1_lesson_1` … `stage1_lesson_4`;
`run_stage1`'s `lessons` array lists all four between `stage1_intro` and
the gate.

`stage1_intro`: change "Three short lessons (about 10 minutes)" to
"Four short lessons (about 10 minutes)" and "start lesson 1.1" stays.

**1.1 — running commands** (budget ~15 content lines):

```
${H1}1.1 — running commands${RST}

At the prompt below, type this and press Enter:

  ${CMD}echo hello${RST}

You'll see ${DIM}hello${RST} printed, then the prompt comes back. Now try:

  ${CMD}echo I am at the shell${RST}      ${DIM}# spaces separate words${RST}
  ${CMD}echo "I am at the shell"${RST}    ${DIM}# quotes group them into one${RST}

${CMD}echo${RST} just repeats its words back. It is the simplest command
there is, and its shape is the shape of every command you'll meet:
a name, then the words you hand it.

${INSTR}▶ Try all three, then type ${CMD}next${INSTR}.${RST}
```

**1.2 — keyboard habits** (budget ~17 content lines):

```
${H1}1.2 — keyboard habits${RST}

Four keys make the shell comfortable. Try each one now.

  ${KEY}Tab${RST}       bash finishes a word. Type ${CMD}echo p${RST}, press ${KEY}Tab${RST}:
            it becomes ${CMD}echo poem.txt${RST}. Several matches? The first
            ${KEY}Tab${RST} fills in the shared part; ${KEY}Tab${RST} again lists them.
            (Other shells and setups differ.)
  ${KEY}↑${RST}         brings back the last command. Enter runs it again.
  ${KEY}Ctrl+L${RST}    clears the screen; the command ${CMD}clear${RST} does the same.
            Type ${CMD}show${RST} to bring this lesson back afterwards.
  ${KEY}Ctrl+C${RST}    the escape hatch. If anything feels stuck, press it
            and you get a fresh prompt.

${INSTR}▶ Try each key, then type ${CMD}next${INSTR}.${RST}
```

**1.3 — where am I, who am I, when is it** (budget ~13 content lines):

```
${H1}1.3 — where am I, who am I, when is it${RST}

Three commands that ask the system about itself.

  ${CMD}whoami${RST}     ${DIM}# the user name you're logged in as${RST}
  ${CMD}pwd${RST}        ${DIM}# print working directory — the folder you're in${RST}
  ${CMD}date${RST}       ${DIM}# the current date and time${RST}

Here ${CMD}pwd${RST} shows the tutor's own folder, because that is where
this practice prompt starts. Stage 2 is all about folders.

${INSTR}▶ Run all three, then type ${CMD}next${INSTR}.${RST}
```

**1.4 — what just happened**: the current 1.3 screen unchanged except the
title line becomes `${H1}1.4 — what just happened${RST}`.

Tone check against the design plan: concise, concrete, no praise copy, no
anthropomorphism. Keep it that way if you adjust wording to fit a line.

## Harness follow-through

- `sentinels.py`: `LESSON_1_2` → `1.2 — keyboard habits`;
  `LESSON_1_3` → `1.3 — where am I, who am I, when is it`; new
  `LESSON_1_4` → `1.4 — what just happened`.
- `persona.py` Stage 1 walk:
  - 1.1: `echo hello`, `echo I am at the shell`, `echo "I am at the shell"`.
  - 1.2: raw `echo p\t` → wait `echo poem.txt` → raw `\n` → `PROMPT`;
    raw `\x0c` (Ctrl+L) → `PROMPT`; raw `\x1b[A` then raw `\n` (Up, Enter;
    reruns `echo poem.txt`) → `PROMPT`; raw `\x03` (Ctrl+C) → `PROMPT`;
    then `next`.
  - 1.3: `whoami`, `pwd`, `date`, `next`.
  - 1.4: `next`.
  - Screen ids `S1-L1` … `S1-L4`.
- `recorder.known_rough_edges(1)`: S1-L1 and S1-L2 rows become
  "resolved in WP-04 (see `audit/<date>/stage1-density-followup.md`)";
  S1-O and S1-L3 (now S1-L4) stay "keep with watch".

## Records

- `audit/<date>/stage1-density-followup.md`: re-tag the four lesson
  screens with concepts / actions / recommendation using the original
  audit's table shape; state which original rows were acted on and which
  remain under watch; cite the pre- and post-change harness bundles.
- `ROADMAP.md` Phase 3: add a subsection `### Amendments` (if WP-05 has
  not already created it) with a dated entry: "2026-11 (WP-04): Stage 1
  carries four lessons (1.1 running commands, 1.2 keyboard habits, 1.3
  where/who/when, 1.4 what just happened). The stage's commands and gate
  are unchanged." Do not rewrite the original per-stage detail.
- `README.md`: no change (the Stages table lists commands, not lesson
  counts; `clear` is still taught in 1.2).
- `STATUS.md`: one-liner.

## Acceptance criteria

1. Every Stage 1 screen renders within the vertical budget (count content
   lines; none above 20).
2. `make check lint smoke` and `make self-test` pass; FF-004 and FF-008
   clean.
3. Harness `--stage 1` and `--stage all` pass under Bash 3.2 and 5.x,
   including the Tab, Ctrl+L, Up and Ctrl+C actions.
4. `./shelltutor -h` still lists five stages; nothing outside Stage 1
   changed in `shelltutor`.

## Commits (in order)

1. `feat(stage1): split lesson 1.1 into running commands and keyboard habits; trim identity lesson`
   — script only, four lessons, intro text. Body cites S1-L1, S1-L2,
   FF-006b.
2. `chore(sim): Stage 1 sentinels and persona for the four-lesson layout`
3. `docs(audit): Stage 1 density follow-up; ROADMAP Phase 3 amendment`
   — includes the new harness bundle for `--stage 1` and STATUS.

## Report

Template in `docs/workplan/README.md`; include the content-line count per
Stage 1 screen.
