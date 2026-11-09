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
  **Resolved 2026-11-09 by WP-20 (A7), `c11e605`:** 1.3 names both prompts; Q1
  asks about a normal bash window. `>` is still rejected by design.
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
  **Resolved 2026-11-09 by WP-20 (A7), `c803465`:** check table in
  `audit/2026-11-09/wp20-gate-grounding.md`. `a folder` and `print working
  directory` stay rejected (not in the approved lists).

### Observations (reproduced)

- **O-P — The recall prompt resembles the shell prompt.** The gate screen
  says "run a few commands and tell me what they printed" (`stage1_gate_screen`,
  `1000-1010`); Q1 then prints as a line of text followed by `  your answer:`
  (`675-676`), with no mode change on screen. Leo typed `ls` into it; the reply
  was the same `not quite. try again.` (`697`). One sitting, plus Leo's debrief.
  *Closes when*: the recall prompt names itself (for example "answer, not a
  command"). Sheets: leo O-b.
  **Addressed 2026-11-09 by WP-20, `08657e1`:** recall prints in the `┃` block
  with the cue "answer in words:"; the gate screen says this is not the shell.
- **O-Q — Ladder timing against friction.** The first rejection carries one
  message (`697`) whatever was typed (a shell command, a near miss, a wrong
  symbol); the hint arrives only on attempt 2 (`698-700`) and the navigation
  facts on attempt 3 (`701-703`). Every quitting sitting stopped at attempt 1
  of the question that ended it, so no hint was seen. Leo reached attempt 2 on
  Q1 and passed it by guessing. Mechanism is as designed (A1.1); the evidence
  is that friction peaks before the first hint. *Closes when*: the first miss
  says what shape of answer is wanted. Sheets: leo O-f, maya F-a, arthur F.
  **Addressed 2026-11-09 by WP-20, `ab450ff`:** the hint prints on miss 1;
  the navigation facts from miss 2 (C-006).
- **O-R — Leading slash.** `/echo hello` gives `bash: /echo: No such file or
  directory` (reproduced); 1.1 shows `echo hello` (`898`) and nothing connects the
  message to the slash. One sitting. Sheets: leo O-a.
- **O-S — Ctrl+L and Up leave the typed line, so `next` joins it.** Reproduced:
  after `echo p`+Tab, Enter, Up, Ctrl+L the prompt held `echo poem.txt `;
  `send next` printed `shelltutor> echo poem.txt next` then `poem.txt next`.
  Lesson 1.2 says "Ctrl+L clears the screen … show brings the lesson back"
  (`926`) and "Try each key, then type next" (`930`). Related to O-K. *Closes
  when*: 1.2 says Enter or Ctrl+C clears the line first. Sheets: maya O-a.
  **Addressed 2026-11-09 by WP-20, `f8e562f`:** the Up line says Enter runs it
  and Ctrl+C throws it away.
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
  **Partly addressed 2026-11-09 by WP-20, `f8e562f`:** 1.1 gains a
  `command not found` line; per A7 the asides stay and the identical-output
  point is left open.
- **O-V — Keys are not verified, and Enter is implicit.** Lessons advance on
  `next` alone (`1240`); Ctrl+L and Ctrl+C were never required (Leo). 1.2 does
  not say to press Enter after Tab (`921-925`; Arthur). By design for lessons;
  recorded as friction. Sheets: leo O-d, arthur O (Tab).
  **Addressed 2026-11-09 by WP-20, `f8e562f`:** the Tab line ends "then press
  Enter to run it." Keys are still not verified, by design.
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

## Synthetic sittings, round 2

Sheets `sim-sittings/{leo,maya,arthur}-2.md` ran against `82792b6` (WP-20).
`shelltutor` on `main` (`25ae8c3`) is unchanged from that revision. Method as
round 1: recall inputs through the tutor's own `normalize_answer`
(`shelltutor:656`) against the accepted lists; wording by line; the ladder and
Stage 2 commands driven with `sitting.py start --bash /bin/bash` (Bash 3.2.57).
Numbering continues: F-019 and O-Z (then O-AA, O-AB, ...).

**Result.** Leo quit at Stage 1 Q1 (friction 8), Maya at Stage 1 Q3 (9),
Arthur cleared Stage 1 and quit at Stage 2 Q1 (8). All three quit on a recall
rejection; Arthur is the first persona to clear a gate.

### Round-1 items round 2 closes (with evidence)

- **F-017 closed.** 1.3 now says "Your prompt here ends in `>`. A normal bash
  window's prompt usually ends in `$`" (`953-954`); Q1 asks about "a normal bash
  window" (`1133`). Maya and Arthur answered `$` and passed; reproduced `$`
  accepted, `>` and `#` rejected. Leo's two Q1 misses were `next` and `ls` (see
  O-AA), not the answer.
- **F-018 closed for the listed forms.** Q2's list now holds `the folder`,
  `the current directory`, `where i am`, `the folder youre in` (`1140-1158`);
  reproduced accepted: `the folder`, `the folder I'm in`, `the current
  directory`, `where I am`, `the folder you're in`. Maya and Arthur passed Q2 with
  `the folder you are in`. Q3's near misses `to the screen`, `standard out`,
  `the terminal window`, `the display` now accepted. Long answers are F-019.
- **O-Q closed as designed.** The hint now shows on the first miss in all three
  sittings; facts follow from miss 2 (see O-Z).
- **O-S and O-V (Enter after Tab) closed by text.** 1.2 says "then press Enter
  to run it" and "Enter runs it; Ctrl+C throws it away" (`928-929`). Maya and
  Arthur ran Up then Ctrl+C or Enter; no `next` was swallowed.
- **O-W closed for the 1.2 gap.** 1.1 now says "If bash says command not found,
  you mistyped" (`907`); Arthur typed `dir` at 2.2 and recorded no friction.

### Findings (reproduced)

- **F-019 — Long plain answers that contain an accepted phrase are rejected.**
  Severity 2. Reproduced through `normalize_answer`; "contained" means the
  normalised accepted form appears as whole words in the normalised input:

  | Input (sheet) | Exact | Accepted forms contained |
  | --- | --- | --- |
  | Stage 1 Q3: `it shows up on the screen` (maya) | reject | `the screen`, `screen`, `on the screen` |
  | Stage 1 Q3: `it comes back to me on the screen` (arthur) | reject | `the screen`, `screen`, `on the screen` |
  | Stage 2 Q1: `it goes up one level, to the parent folder` (arthur) | reject | `parent folder`, `up one`; also `goes up one level` once the comma is ignored |

  A containment rule is not safe alone: `not to the screen`, `nowhere, the
  screen stays blank`, `it does not go up one level` and `it goes down, not to
  the parent folder` all contain accepted forms and are wrong. Lists
  `1163-1173`, `1412-1420`. *Closes when*: the operator chooses between longer
  accepted forms, containment with a negation guard, or a hint that names the
  expected shape. Sheets: maya F-1, arthur F-001, F-002.
  **Resolved 2026-11-09 by WP-21 (A8), `6d9be96` (longer forms; punctuation
  dropped) and `24421d9` (answer-shape line from miss 2).** No containment
  rule; the four negation counterexamples stay rejected (table in
  `audit/2026-11-09/wp21-recall-shape.md`).
- **F-020 — The Q3 hint's own wording is not an accepted answer.** Severity 3.
  The hint says "in the window you type into" (`1162`); `back to me, in the
  window you type into` (arthur) is rejected and contains no accepted form
  (`window` alone is not in the list). *Closes when*: the list takes `window`
  forms or the hint uses an accepted word. Sheets: arthur F-001.
  **Resolved 2026-11-09 by WP-21, `6d9be96`:** the hint was reworded (it no
  longer uses the window wording) and the `window` forms are accepted.

### Observations (reproduced)

- **O-Z — The recall hint repeats and restates; the facts did appear.**
  Reproduced two misses at Stage 1 Q1: miss 1 printed `not quite. try again.`
  and `Hint: Lesson 1.3 compared this tutor's prompt with a normal one.`; miss 2
  printed the same hint and then `Passed stages are saved.`, `Type quit to
  leave now; the next run starts this stage from its first lesson.`, `Type show
  to see the question again.`; miss 3 printed all of it again (`ask_question`
  `700-704`). **Leo's F-a ("second miss showed the hint again, not facts") is not
  reproduced as a ladder defect**: the facts are present from miss 2, and the
  sheets' own transcripts record them (leo-2 second input; arthur-2 gate
  line). What is true: the hint text is identical on every miss, and for Q3 and
  Stage 2 Q1 it restates the learner's idea ("in the window you type into",
  "two dots name the folder that contains this one") without saying why the
  answer failed. *Closes when*: a later miss adds information the first did not
  (the accepted shape). Sheets: leo F-a, maya F, arthur F-003.
  **Addressed 2026-11-09 by WP-21, `24421d9`:** from miss 2 one fixed line
  says to answer in a few words, not a full sentence.
- **O-AA — Nav words and shell commands typed at the recall prompt (O-P
  recurs).** Reproduced: `next` at Q1 is a miss (output above), because the
  recall line takes only answers (`ask_question` `681-692`). The gate screen
  says "Type your answer in words; this is not the shell." (`1012`); Leo skimmed
  it. *Closes when*: a nav word at recall gets a one-line pointer. Sheets: leo O-a.
- **O-AB — `cd..` and a leading slash.** `cd..` gives `bash: cd..: command not
  found`; `/whoami` gives `bash: /whoami: No such file or directory`
  (reproduced); neither names the missing space or slash. O-R recurs (leo-2
  O-b). *Closes when*: 1.1 or 2.3 names the two typos. Sheets: arthur O-001, leo O-b.
  **Addressed 2026-11-09 by WP-21, `732492e`:** 1.1 names the stray `/` and the
  missing space; 2.3 names `cd..`.
- **O-AC — 2.3: "go home" is not the practice folder, and there is no try-it
  line.** Reproduced: after `cd`, `pwd` printed the home folder, not the
  sandbox; 2.3 says `cd` goes home (`1358`), then that prompts start in
  `$SANDBOX` (`1365`), uses `$HOME` unexplained (`1359`) and ends "Type next to
  continue". *Closes when*: one sentence ties `cd` to home and the way back.
  Sheets: arthur O-002, O-003.
  **Addressed 2026-11-09 by WP-21, `80fc754`:** 2.3 says `cd` goes home, outside
  the practice area, and `cd -` comes back; `$HOME` is gone; it ends in a
  try-it line.
- **O-AD — `ls /etc` is host output.** `ls /etc | wc -l` printed 81 here
  (`1343`); the lesson gives no reason to read it. Sheets: arthur O-004.
  **Addressed 2026-11-09 by WP-21, `95e2689`:** 2.2 lists `ls /` first.
- **O-AE — Terms used before they are taught.** `cat notes.txt` in 2.4
  (`1389`; `cat` is Stage 3), hidden names `.` and `..` in 2.2 (`1337`),
  `poem.txt` named in 1.2 without its source. Sheets: arthur O-005, O-010, O-011.
- **O-AF — Ctrl+L leaves a blank screen; recovery is `show`.** All three
  recovered with `show` (`930`). No friction. Sheets: leo O-d, maya O-5, arthur O-005.
- **O-AG — The prompt folder changes at the Stage 1 gate task.** `pwd` prints
  the sandbox in 1.3 and `.../stage1` in the task (`practice "$SANDBOX/stage1"
  gate`, `1200`; C-003). 1.3 says only "the tutor's own folder" (`950`).
  Sheets: arthur O-007.

### Recurring round-1 items

O-T (reading load) recurs: leo-2 O-c, O-f; maya-2 O-1, O-7. O-U (`#` asides and
identical echoes, `904-905`) recurs: maya-2 O-4, arthur O-006. O-X (jargon)
recurs: leo-2 O-e, maya-2 jargon lists, arthur O-009. O-Y (path and drive
letter) recurs: arthur O-008, maya O-6; Arthur's own note says 2.4's "Absolute
paths start from the root" answered it.

### Candidate → disposition

| Sheet | Candidate | Disposition |
| --- | --- | --- |
| leo | F-a (no facts at miss 2) | not reproduced as a defect; O-Z |
| leo | O-a mode confusion at Q1 | O-AA |
| leo | O-b `/whoami` | O-AB (O-R) |
| leo | O-c pace; O-f 1.5 load | O-T |
| leo | O-d Ctrl+L blank | O-AF |
| leo | O-e jargon | O-X |
| maya | F-1 `it shows up on the screen` | F-019 |
| maya | O-1 reading load; O-7 1.4 | O-T |
| maya | O-2 Q1 answer in skipped 1.3 paragraph | F-017 closed (`953-954`) |
| maya | O-3 Q3 wording unclear | F-019, F-020, O-Z |
| maya | O-4 identical echoes | O-U |
| maya | O-5 Ctrl+L blank | O-AF |
| maya | O-6 long path | O-Y |
| arthur | F-001, F-002 | F-019, F-020 |
| arthur | F-003 hint restates | O-Z |
| arthur | O-001 `cd..` | O-AB |
| arthur | O-002, O-003 | O-AC |
| arthur | O-004 `ls /etc` | O-AD |
| arthur | O-005 | O-AE, O-AF |
| arthur | O-006 identical echoes | O-U |
| arthur | O-007 `/stage1` | O-AG |
| arthur | O-008 drive letter | O-Y |
| arthur | O-009 jargon | O-X |
| arthur | O-010, O-011 | O-AE |

### About the simulation, not the tutor: friction by source

| Sheet | Final | Reading-limit charges | Rejections (+2 each) | Other |
| --- | ---: | ---: | ---: | --- |
| leo-2 | 8 | 1 | 6 (`/whoami`, `next`, `ls`) | 1 mode confusion |
| maya-2 | 9 | 7 | 2 (Q3) | 0 |
| arthur-2 | 8 | 1 (`ls /etc`) | 8 (Q3 twice, `cd..`, Stage 2 Q1) | -1 gate cleared |

Maya's sitting ended mostly on the reading meter (7 of 9) with a single
rejection; Leo's and Arthur's ended on rejections. The reading charge is a
persona parameter (her four-line limit makes almost every screen cost one), so
it measures relative density, not a tutor defect. Both kinds of point pushed
the three sittings past 8 in under 30 inputs.
