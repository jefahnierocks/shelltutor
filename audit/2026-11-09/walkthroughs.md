---
title: Phase A Walkthroughs — 2026-11-09 (synthetic sittings)
category: audit
component: walkthroughs
status: active
version: 0.1.0
last_updated: 2026-11-09
tags: [phase-a, walkthrough, synthetic-sittings, findings, a6]
priority: high
---

# Phase A Walkthroughs — 2026-11-09

Continues `audit/2026-11-08/walkthroughs.md`. This file records **synthetic
sittings** (amendment A6): candidate evidence from `sim-sittings/{leo,maya,arthur}-1.md`,
recorded here only after reproduction on the real tutor. It does not satisfy
Phase A's exit, which still waits for human sittings (one on Bash 3.2). F and
O numbers continue from F-016 and O-O.

## Synthetic sittings

**Result.** All three personas quit at the Stage 1 gate recall, after 23 to 28
inputs, at friction 8 or 9 (Leo Q2 attempt 1, Maya Q2 attempt 1, Arthur Q1
attempt 1). None reached the gate task, Stage 2 or the hint rung of the ladder
on the question that ended the sitting.

**Method.** The sheets ran at `a25caf7`; `shelltutor` is byte-identical at
`4a5b25e` (`git diff a25caf7 4a5b25e -- shelltutor` is empty). Recall rejections
were reproduced by passing the exact input through the tutor's own
`normalize_answer` (`shelltutor:656`) against the accepted lists read from the
Stage 1 `ask_question` calls (`1124-1149`). The 1.2 residue and the two raw
bash errors were driven with `sitting.py start --bash /bin/bash` (Bash 3.2.57):
`raw "echo p<Tab>"`, Enter, `raw "\x1b[A"`, `raw "\x0c"`, `send next`. Screen
wording is cited by line. Line counts are heredoc lines (blanks included).

### Findings (reproduced)

- **F-017 — Stage 1 Q1 asks for `$`, which no Stage 1 screen teaches, while the
  prompt on screen ends in `>`.** Severity 2. Q1 accepts only `$`
  (`1125-1127`); the orientation shows `shelltutor>` (`855`) and no screen in
  1.1 to 1.5 shows or names a `$` prompt (no match for a prompt-ending sentence
  in `827-1000`). Reproduced through `normalize_answer`: `>` (Arthur), `#`
  (Maya, her first guess) and `ls` (Leo) are rejected; `$` accepted. Two of
  three sittings answered with what they saw or guessed. *Closes when*: a 1.x
  screen shows and names the `$` convention, or the question is reworded to what
  the learner sees. Sheets: arthur F, maya F-b, leo O-b (Q1 stage).
- **F-018 — Plain-language answers to a recall question are rejected, including
  one the lesson itself uses.** Severity 2. Q2's accepted list (`1132-1139`) has
  eight forms. Rejected, verified: `the folder` (Leo), `the folder I'm in`
  (Maya; normalises to `the folder i'm in`, the list holds `the folder im in`
  without the apostrophe), `the current directory`, `the directory`, `a folder`,
  `where I am`, `print working directory`, and `the folder you're in`, which is
  the 1.3 gloss word for word (`943`). Same pattern on Q3 (`1144-1149`),
  found while reproducing, not in the sheets: `to the screen`, `standard out`,
  `the terminal window`, `the display` rejected. *Closes when*: the lists are
  widened from these inputs and apostrophes are normalised in
  `normalize_answer`. Sheets: leo F-a, maya F-a.

### Observations (reproduced)

- **O-P — The recall prompt resembles the shell prompt.** The gate screen
  says "run a few commands and tell me what they printed" (`stage1_gate_screen`,
  `1000-1010`); Q1 then prints as a line of text followed by `  your answer:`
  (`675-676`), with no mode change on screen. Leo typed `ls` into it; the reply
  was the same `not quite. try again.` (`697`). One sitting, plus Leo's debrief.
  *Closes when*: the recall prompt names itself (for example "answer, not a
  command"). Sheets: leo O-b.
- **O-Q — Ladder timing against friction.** The first rejection carries one
  message (`697`) whatever was typed (a shell command, a near miss, a wrong
  symbol); the hint arrives only on attempt 2 (`698-700`) and the navigation
  facts on attempt 3 (`701-703`). Every quitting sitting stopped at attempt 1
  of the question that ended it, so no hint was seen. Leo reached attempt 2 on
  Q1 and passed it by guessing. Mechanism is as designed (A1.1); the evidence
  is that friction peaks before the first hint. *Closes when*: the first miss
  says what shape of answer is wanted. Sheets: leo O-f, maya F-a, arthur F.
- **O-R — Leading slash.** `/echo hello` gives `bash: /echo: No such file or
  directory` (reproduced); 1.1 shows `echo hello` (`898`) and nothing connects the
  message to the slash. One sitting. Sheets: leo O-a.
- **O-S — Ctrl+L and Up leave the typed line, so `next` joins it.** Reproduced:
  after `echo p`+Tab, Enter, Up, Ctrl+L the prompt held `echo poem.txt `;
  `send next` printed `shelltutor> echo poem.txt next` then `poem.txt next`.
  Lesson 1.2 says "Ctrl+L clears the screen … show brings the lesson back"
  (`926`) and "Try each key, then type next" (`930`). Related to O-K. *Closes
  when*: 1.2 says Enter or Ctrl+C clears the line first. Sheets: maya O-a.
- **O-T — Stage 1 reading load.** Heredoc lines: welcome 14, orientation 17,
  intro 7, 1.1 16, 1.2 14, 1.4 18, 1.5 16. Welcome, orientation and the intro
  are three reading-only screens before the first prompt (`827-890`); 1.4 and
  1.5 follow two more. Leo read only `▶` lines on the first two; Maya skimmed
  five of seven; Arthur reported five screens over his limit. The Ctrl+C
  sentence Maya skipped is the last line of the 1.2 block (`927-928`). *Closes
  when*: the first-run prose is cut or split; no new fact. Sheets: leo O-c,
  maya O-b, O-d, arthur O (density).
- **O-U — Asides on copyable lines; the two echoes print alike.** `1.1` puts
  `# spaces separate words` and `# quotes group them into one` on the lines to
  type (`902-903`). Reproduced: both lines, comments included, print
  `I am at the shell`; the claimed difference is invisible. Maya and Arthur typed
  the `#` text. *Closes when*: the asides move off the command line and the
  example shows a difference. Sheets: maya O-c, arthur O (identical output).
- **O-V — Keys are not verified, and Enter is implicit.** Lessons advance on
  `next` alone (`1240`); Ctrl+L and Ctrl+C were never required (Leo). 1.2 does
  not say to press Enter after Tab (`921-925`; Arthur). By design for lessons;
  recorded as friction. Sheets: leo O-d, arthur O (Tab).
- **O-W — `cls`.** Reproduced: `bash: cls: command not found`. 1.2 says
  "(clear too)" (`926`) without saying `clear` is typed; 1.4 explains the error
  two screens later (`954-976`). Persona-specific (DOS reader). Sheets: arthur O.
- **O-X — Unexplained terms and one gloss order.** "vimtutor prerequisite
  course" (`830`), `bash:` and "the program named bash" in one screen
  (`963`, `970`), and 1.3 glosses `pwd` as "print working directory" before the
  plain wording (`943`). Sheets: maya O-e, arthur O, leo O-e.
- **O-Y — Orientation and 1.3 wording for a DOS reader.** "A fifth word, check,
  appears … when relevant" is read as possibly required (`865`); `pwd` prints a
  path with no drive letter and 1.3 defers to Stage 2 (`947`). Persona-specific.
  Sheets: arthur O (two lines).

### Not reproduced

- **maya O-f** (a wrong guess at an untaught gate question is not scored as
  "rejected and not understood"). This concerns the simulation's scoring rule 6,
  not the tutor; routed to the sitting template, not to `shelltutor`.

### Candidate → disposition

| Sheet | Candidate | Screen id, input | Disposition |
| --- | --- | --- | --- |
| leo | F-a | S1-G Q2, `the folder` | F-018 |
| leo | O-a | S1-L1, `/echo hello` | O-R |
| leo | O-b | S1-G Q1, `ls` | O-P (and F-017 for the answer) |
| leo | O-c | welcome, orientation, intro | O-T |
| leo | O-d | S1-L2, Ctrl+L and Ctrl+C untried | O-V |
| leo | O-e | S1-L3, `pwd` gloss | O-X |
| leo | O-f | S1-G, `ls` and `the folder` | O-Q |
| maya | F-a | S1-G Q2, `the folder I'm in` | F-018 |
| maya | F-b | S1-G Q1, `$` untaught | F-017 |
| maya | O-a | S1-L2, Ctrl+L then `next` | O-S |
| maya | O-b | S1-L2, Ctrl+C line skipped | O-T |
| maya | O-c | S1-L1, `# …` on the line | O-U |
| maya | O-d | welcome, 1.4, 1.5 prose | O-T |
| maya | O-e | welcome, 1.4 jargon | O-X |
| maya | O-f | rule 6 scoring | not reproduced |
| arthur | F (possible) | S1-G Q1, `>` | F-017 |
| arthur | O density | orientation, 1.1, 1.2, 1.4, 1.5 | O-T |
| arthur | O cls | S1-L2, `cls` | O-W |
| arthur | O Tab/Enter | S1-L2 | O-V |
| arthur | O identical echoes | S1-L1 | O-U |
| arthur | O bash twice | S1-L4 | O-X |
| arthur | O Q1 untaught | S1-G Q1 | F-017 |
| arthur | O pwd path | S1-L3 | O-Y |
| arthur | O fifth word | orientation | O-Y |

### Convergence

All three sittings ended at the Stage 1 gate recall, which is the course's
first mastery gate: F-017 and F-018 are two answer-list defects, O-P and O-Q
the prompt and ladder context around them. Fixing the lists alone would not
have kept Leo, who never read the gate screen; fixing the ladder alone would
not have kept Arthur, whose `>` is the visible prompt.
