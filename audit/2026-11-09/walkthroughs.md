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
  **Addressed for Stage 2 2026-11-09 by WP-22, `5d5757f`:** the Stage 2 task screen says the
  task runs in this stage's own folder and `pwd` shows it. The Stage 1 task
  screen is unchanged.

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

## Synthetic sittings, round 3

Sheets `sim-sittings/{leo,maya,arthur}-3.md` ran against `5d1d689` (WP-21);
`shelltutor` on `main` (`757d0a6`) is unchanged from that revision.

**Two things changed between round 2 and round 3, so comparisons are read
against both.** (1) The tutor: WP-21 (longer plain accepted forms; hint words
accepted; the second recall miss adds the shape line `Answer in a few words,
like the lesson did, not a full sentence.`, `shelltutor:668`, `709`; 1.1 names
the stray-slash and missing-space typos; 2.3 says `cd` goes home and `cd -`
comes back and ends in a try-it line; 2.2 lists `ls /`). (2) The persona
sheets: Leo and Maya ran on **v0.2** (Maya's density charge only on
consequence; Leo also reads each paragraph's first sentence), Arthur on
**v0.1**. Method as before; numbering continues at F-021 and O-AH.

**Result.** Leo quit at the Stage 2 gate task (friction 8), Maya at the Stage 4
gate recall Q1 after clearing Stages 1 to 3 (8), Arthur at Stage 2 gate Q2 (9).
Round 3 reached further than rounds 1 and 2: Maya cleared three gates.

### Friction by source

| Sheet (persona version) | Final | Reading charges | Rejections (+2) | Mode confusion | Gates cleared |
| --- | ---: | ---: | ---: | ---: | ---: |
| leo-3 (v0.2) | 8 | 1 | 8 (four) | 0 | -1 |
| maya-3 (v0.2) | 8 | 1 | 8 (four) | 2 | -3 (unfloored) |
| arthur-3 (v0.1) | 9 | 8 | 2 (one) | 0 | -1 |

Under v0.2 the reading charge falls from 7 (maya-2) to 1; the sittings now end
on rejections. Arthur still pays 8 reading points because his sheet is
unchanged. Leo's `notes` at Stage 2 Q3 is a correct rejection (a wrong answer
the hint then fixed); the other seven rejection points are F-021 to F-023.

### Round-2 items closed (with evidence)

- **F-019 closed.** Reproduced accepted: `it shows up on the screen`, `it
  comes back to me on the screen`, `it goes up one level, to the parent folder`
  and the comma-less form; `not to the screen` still rejected. Arthur's
  `it comes back to me on the screen` and Maya's `back to me on the screen`
  passed Stage 1 Q3 in round 3.
- **F-020 closed.** `back to me, in the window you type into` (the hint's words)
  is accepted at Stage 1 Q3. The same gap recurs at Stage 4 Q1 (F-023).
- **O-Z closed for the shape line.** Miss 2 now prints the shape line
  (reproduced at Stage 2 Q2 and seen by Maya at Stage 4 Q1). The hint text is
  still the same on every miss.
- **O-AB closed.** 2.3 says "`cd..` with no space is a different word"; no
  sheet typed `cd..` or `/echo`.
- **O-AC and O-AD closed.** 2.3's `cd` is "your home folder, outside this
  practice area" with a try-it line (`1373-1385`); 2.2 lists `ls /`. Arthur ran
  `cd ..`, `pwd`, `cd -` with no friction.
- **O-AF closed.** Arthur ran Ctrl+L with no charge.

### Findings (reproduced)

- **F-021 — Stage 2 Q2 rejects "your home folder", the lessons' own gloss.**
  Severity 2. 2.3 says "`cd`  # your home folder" (`1373`), 2.4 and the intro
  say "~ your home folder" (`1317`, `1395`); the list (`1446-1455`) holds `home`,
  `home folder`, `my home folder`, `the home folder` and directory forms, not
  `your`. Reproduced through `normalize_answer`:

  | Input | Exact | Accepted forms contained |
  | --- | --- | --- |
  | `your home folder` (leo, maya, arthur) | reject | `home`, `home folder` |
  | `a home folder` | reject | `home`, `home folder` |
  | `your home directory` | reject | `home`, `home directory` |
  | `your home` | reject | `home` |
  | `home`, `the home folder` | accept | |

  The hint "It is where `cd` with nothing after it takes you" (`1445`) names a
  different fact, so all three could not tell why `your home folder` failed
  (Leo found `home` by shortening). Three of three sheets. *Closes when*: the
  list takes `your home folder`/`directory`, or Q2 is worded as the gloss.
  Sheets: leo F-a, F-c; maya F-b; arthur F-a.
  **Resolved 2026-11-09 by WP-22 (A9), `37c3d07`:** the `your …` forms are accepted;
  the hint is anchored to Lesson 2.3 (`3913a98`).
- **F-022 — The Stage 2 gate task needs a command no earlier lesson shows, and
  the first `check` does not say so.** Severity 1 (dead end). The task asks to
  "make a folder called practice" (`1477`). Stage 2 lessons (intro to 2.4) never
  mention `mkdir`; its first appearance is the Stage 3 intro (`1569`) and 3.1
  (`1583`). The gate checks the history pattern `cd` first
  (`gate_require_history`, `1494-1496`), so the first `check` prints only
  `○ cd into it (cd practice) not yet: not in your history` (reproduced, scratch
  sitting). The hint with `mkdir` comes at attempt 2 (`gate_escalate`, `1500`;
  reproduced: second `check` printed `○ practice folder not yet: no practice
  folder in this stage's folder` and `Hint: mkdir makes the folder; cd moves into
  it; pwd shows where you are.`). Also reproduced: a failed `cd practice`
  (`bash: cd: practice: No such file or directory`) satisfied the `cd` check, so
  the learner advanced to the second message by typing it. Leo quit here
  (`make practice`, `new folder practice`, +4); Maya took three guesses and two
  `check` calls. *Closes when*: a Stage 2 screen names `mkdir`, or the task
  screen names it, or the first `check` names the missing folder.
  Sheets: leo F-b, maya F-c.
  **Resolved 2026-11-09 by WP-22 (A9), `5d5757f`:** 2.4 teaches `mkdir`; the first
  `check` lists both items and the `cd` item needs the folder.
- **F-023 — Stage 4 Q1 rejects the answer the learner just saw and the hint's
  own words.** Severity 2. List (`1916-1923`): `the path to vim`, `path to vim`,
  `a path`, `the path`, `where vim is`, `vim's path`, `vims path`,
  `/usr/bin/vim`. Reproduced:

  | Input | Exact | Accepted forms contained |
  | --- | --- | --- |
  | `the path /usr/bin/vim` (maya) | reject | `the path`, `/usr/bin/vim` |
  | `the folder and name of the program file` (maya; the hint, `1915`) | reject | none |
  | `a path like /usr/bin/vim` | reject | `a path`, `/usr/bin/vim` |
  | `it prints the path` | reject | `the path` |
  | `the full path` | reject | none |
  | `the path`, `/usr/bin/vim` | accept | |

  FF-009 (`scripts/check-hints.sh`) checks only that no accepted form appears
  inside the hint (the leak test); it does not check that the hint's own words
  would be accepted, which is why F-020's gap recurs. Maya lost 4 points here and
  quit. *Closes when*: the list takes the hint's words and path-plus-example
  forms; a check compares the hint's words with the list.
  Sheets: maya F-a.
  **Resolved 2026-11-09 by WP-22 (A9), `68e817e` (path forms; hint reworded) and
  `3913a98` (FF-010 anchors every hint).** Still rejected: `a path like
  /usr/bin/vim`, `it prints the path`.
- **F-024 — Lesson 1.2 says Ctrl+C gets you a fresh prompt, and inside `less`
  it does nothing.** Severity 3. 1.2: "Ctrl+C the escape hatch. If anything feels
  stuck, press it and you get a fresh prompt" (`937-938`). Reproduced in 3.2:
  after `less ../numbers.txt`, raw Ctrl+C left the pager (`:` prompt still
  showing); typing `next` reached `less` ("No next tag (press RETURN)"); only `q`
  returned to `shelltutor>`. 3.2 does give `q` (`1617-1619`, fifth prose line),
  but its `▶` line says "Try both, then next" (`1623`). Maya hit this (+2 mode
  confusion, +1 reading). *Closes when*: 1.2's sentence is limited to commands at
  the prompt, or 3.2's `▶` line names `q`. Sheets: maya O-c, O-d.
  **Resolved 2026-11-09 by WP-22 (A9), `8c11520`:** both ways: 1.2 limits Ctrl+C to the
  prompt and names `q`; 3.2's `▶` line names `q`.

### Observations (reproduced)

- **O-AH — `show` at a recall question echoes as an answer line but is not
  an attempt.** Reproduced at Stage 1 Q1: `show` printed `┃ answer in words: show`
  and redrew the question; the next real miss (`ls`) printed one message and the
  hint only, with no shape line or facts, so `show` did not count (`ask_question`
  `691`). Maya's candidate F-d is not a defect. *Closes when*: the echoed line is
  not shown as an answer (cosmetic). Sheets: maya F-d.
- **O-AI — 3.3's `▶` line does not ask to type `cp`, `mv` or `rm`.** `▶ Type next
  to take Stage 3's gate` (`1646`); Maya arrived at the gate task without having
  typed them and recovered by copying 3.1's shape. Sheets: maya O-e.
  **Addressed 2026-11-09 by WP-22, `8c11520`:** 3.3's `▶` line asks to type `cp`, `mv`, `rm`.
- **O-AJ — Host programs answer wrong guesses.** `make folder practice` gave
  `make: *** No rule to make target `folder'.  Stop.` and `help` printed 44 lines
  of builtin signatures with no `mkdir` (counted `help | wc -l`; `help | grep -c
  mkdir` is 0), both reproduced. Neither says what to type. Sheets: maya O-a, O-b;
  leo (`make practice`).
- **O-AK — The Stage 2 gate screen lacks "this is not the shell".** The Stage 1
  gate has it (`1012`); the Stage 2 gate opens with "Recall (three questions…)"
  only (`1416-1422`). Leo did not mistype this time. Sheets: leo O-b.
  **Addressed 2026-11-09 by WP-22, `5d5757f`:** the Stage 2 recall screen carries the line.
- **O-AL — Silence and the `cd ..` / `cd -` asymmetry.** `cd ..` prints nothing,
  `cd -` prints the path; 2.3's try-it line now asks for `pwd`. Sheets: leo O-c,
  arthur O-g.
- **O-AM — Terms used before they are taught (O-AE recurs) and drive letters.**
  `cat` and `~/projects` in 2.4 (`1389`), "root" undefined, `vimtutor` undefined
  (welcome), "bash" in 1.1. Arthur looked for a drive letter twice. Sheets:
  arthur O-a, O-c, O-d, O-e, O-h.

### Recurring

O-AG (`pwd` ends `…/stage1` at the Stage 1 task, `practice "$SANDBOX/stage1"
gate`, `1215`, and `…/stage2` at the Stage 2 task, `1490`, while 2.1 draws the
root) is now on three of three sheets (leo-3 1.3; maya O-g; arthur O-f). The
reading load (O-T) is Arthur's v0.1 cost (8 charges); under v0.2 it is 1. The
answer-format line of the shape hint has no example in the lessons (maya O-f).

### Candidate → disposition

| Sheet | Candidate | Disposition |
| --- | --- | --- |
| leo | F-a, F-c `your home folder` | F-021 |
| leo | F-b gate task dead end | F-022 |
| leo | O-a three reading-only screens | O-T (1 point under v0.2) |
| leo | O-b Stage 2 gate screen | O-AK |
| leo | O-c silent `cd ..` | O-AL |
| leo | O-d Q1 answer in unread 1.3 | F-017 closed; guess accepted |
| maya | F-a Stage 4 Q1 | F-023 |
| maya | F-b `your home folder` | F-021 |
| maya | F-c `mkdir` not taught | F-022 |
| maya | F-d `show` echo | O-AH (not a defect) |
| maya | O-a `make folder practice` | O-AJ |
| maya | O-b `help` | O-AJ |
| maya | O-c 3.2 exit key; O-d Ctrl+C | F-024 |
| maya | O-e 3.3 `▶` line | O-AI |
| maya | O-f shape example | recurring note |
| maya | O-g position shifts | O-AG |
| arthur | F-a `your home folder` | F-021 |
| arthur | O-a vimtutor; O-c, O-d, O-e, O-h | O-AM |
| arthur | O-b density (8 of 15) | O-T (v0.1 persona cost) |
| arthur | O-f stage1 pwd | O-AG |
| arthur | O-g silence | O-AL |

## Synthetic sittings, round 4

Sheets `sim-sittings/{leo,maya,arthur}-4.md` ran against `13847ef` (WP-22);
`shelltutor` on `main` (`fc46228`) is unchanged from that revision. **All three
personas ran on v0.2** (density and reading charges only on consequence; Leo
reads first sentences). The tutor changes since round 3 are WP-22: 2.4 teaches
`mkdir name` with a try-it line; the Stage 2 `check` lists both items; 1.2 limits
Ctrl+C to the prompt; 3.2's `▶` line names `q`; Stage 4 Q1 takes path forms; hints
are anchored `Lesson N:` (FF-010). Numbering continues at F-025 and O-AN.

**Result.** Maya and Arthur reached the finale (they are the first to clear all
five gates); Leo cleared Stages 1 to 3 and quit at Stage 4 Q3. Every
rejection in round 4 is on a recall question: Stage 1 Q3, Stage 2 Q3 and
Stage 4 Q2 and Q3.

### Friction by source (all v0.2)

| Sheet | Final | Reading | Rejections (+2) | Mode confusion | Gates cleared |
| --- | ---: | ---: | ---: | ---: | ---: |
| leo-4 | 8 (quit) | 1 | 10 (five) | 0 | -3 |
| maya-4 | 3 (finale) | 0 | 8 (four) | 0 | -5 |
| arthur-4 | 1 (finale) | 0 | 6 (three) | 0 | -5 |

Reading and mode-confusion charges are near zero under v0.2. Maya's gross
positive friction reached 8 but her meter is unfloored and gate refunds kept the
net at 3; her sheet records that she did not quit. All 24 rejection points came
from recall questions: F-025 (6), F-026 (12), F-027 (4) and O-AO (2).

### Round-3 items closed (with evidence)

- **F-021 closed.** `your home folder` accepted at Stage 2 Q2 for all three
  (also reproduced); the list now takes `your` forms.
- **F-022 closed.** 2.4 says `mkdir name` and "Try `mkdir demo`" (`1406`,
  `▶`); all three cleared the Stage 2 task first try. Reproduced the first
  `check`: `○ folder exists not yet: no practice folder…` and `○ cd into it not
  yet: make the folder first, then cd into it` (both items shown).
- **F-023 closed.** Stage 4 Q1 list (`1926-1944`) takes `the path /usr/bin/vim`,
  `the full path` and path forms; all three passed it (`/usr/bin/vim`, `the path
  to vim`, `the path`).
- **F-024 closed.** 1.2: "the escape hatch at a prompt … inside a full-screen
  program like `less` (Stage 3), `q` is the way out" (`937-939`); 3.2's `▶` says
  "`q` leaves `less`" (`1634`). Leo and Maya pressed `q`.
- **O-AI closed.** All three typed `cp`, `mv`, `rm` in 3.3.
- **O-AG recurs** (Maya O-B, Arthur O-e): the Stage 1 task `pwd` ends `/stage1`;
  the 1.3 and 2.1 `pwd` do not.

### Findings (reproduced)

- **F-025 — Stage 1 Q3's hint paraphrases the answer, and its own words are
  rejected (F-020's class, recurring after a rewording).** Severity 2. The hint
  is "Lesson 1.4: a program's output does not go into a file by itself; it
  comes straight back to you." (`1169`). Reproduced through `normalize_answer`
  (the list holds 20 forms):

  | Input (sheet) | Exact | Accepted forms contained |
  | --- | --- | --- |
  | `it comes straight back to you` (arthur; the hint) | reject | none |
  | `back to you` (arthur) | reject | none |
  | `it comes back to me on the screen in the terminal window` (arthur) | reject | 8, among them `the screen`, `the terminal window`, `on the screen` |
  | `the screen` (arthur, accepted last) | accept | |

  F-020 was closed by accepting the old hint's words; WP-22's new hint reintroduces
  the gap, and FF-010 (anchor check only, `check-hints.sh:74`) does not look at
  the hint's wording against the list. Arthur lost 6 points. *Closes when*: the hint
  names the concept without the answer's words, or the list takes the hint's tail;
  and a check compares the hint's words with the list. Sheets: arthur F-a, F-b.
  **Resolved 2026-11-09 by WP-23 (A10), `d7dd48e`:** the hint is reworded; FF-009 now
  also checks keyword phrases; the lists became keyword groups (`6257ce2`).
- **F-026 — Stage 4 Q2 rejects the lesson's two words joined by "and".**
  Severity 2. List (`1949-1955`): `> overwrites, >> appends`, `> overwrite, >>
  append`, `> writes over, >> adds to the end`, `>> appends`, `> overwrites`,
  `one overwrites one appends`, `> replaces >> appends`. `normalize_answer`
  (`661`) lowercases, strips only `'`, `.`, `,` and `!`, and collapses spaces:
  `>` and `>>` survive, so punctuation stripping does not affect them; it also
  turns the accepted `> overwrites, >> appends` into `> overwrites >> appends`,
  which is why the comma form passes. Reproduced:

  | Input (sheet) | Exact | Accepted forms contained |
  | --- | --- | --- |
  | `> overwrites and >> appends` (leo) | reject | `>> appends`, `> overwrites` |
  | `> overwrites the file and >> appends to the end` (maya) | reject | `>> appends`, `> overwrites` |
  | `overwrite append` (leo) | reject | none |
  | `overwrite vs append` (maya) | reject | none |
  | `one replaces what is in the file and the other adds to the end of it` (maya) | reject | none |
  | `one replaces the old file and two adds to the end` (leo) | reject | none |
  | `>> appends`, `> overwrites, >> appends` | accept | |

  Leo lost 6 points and Maya 6 here. The hint "Lesson 4.3: what each arrow does
  to a file that already exists" (`1948`) is the same on every miss and its words
  are not accepted (`what each arrow does…`, none contained). *Closes when*: the
  list takes "and"/"vs" forms and the plain-language forms, or Q2 states the
  shape ("name what each arrow does"). Sheets: leo F-a, F-b; maya F-A.
  **Resolved 2026-11-09 by WP-23, `6257ce2`:** two keyword groups (overwrite-words and
  append-words); `only appends` is refused by the negation guard.
- **F-027 — Stage 4 Q3 rejects `the space` and `the space splits it into two
  names`.** Severity 2. List (`1960-1968`): `because of the space`, `spaces split
  arguments`, `spaces split words`, `the space splits them`, `no quotes`,
  `missing quotes`, `because spaces`, `because of spaces`, `the shell splits on
  spaces`. Reproduced reject: `the space` (leo), `the space splits it into two
  names` (maya), `there is a space`; accept: `the space splits them`, `the shell
  splits on spaces`. The hint's words (`what separates the words after vim, and
  what quotes do`) are not accepted. The same fact as the accepted forms,
  one word different. Leo quit on it (+2); Maya +2. *Closes when*: the list
  takes `the space` and the `into two names` forms. Sheets: leo F-c, maya F-B.
  **Resolved 2026-11-09 by WP-23, `6257ce2`:** `space|spaces|split|...` group.
- **F-028 — The Stage 3 gate task step 1 needs redirection, taught in 4.3
  (same class as F-022, no dead end observed).** Severity 3. Step 1 is "create a
  file `notes.txt` containing the word `hello`" (`1711`). Stage 3 teaches
  `touch` (empty files) and gives redirection only as an aside, "To create a file
  with content, use redirection (Stage 4): `echo "first line" > greeting.txt`"
  (3.1, `1606`); the lesson `▶` line says "Make a few". The first `check`
  (reproduced) marks `○ done.txt has hello not yet: no done.txt in this folder`
  but not how; `echo hello > notes.txt` is spelled first in the attempt-2 hint
  (`1754`) and attempt-3 worked example (`1755`). All three round-4 sheets cleared
  it first try by copying the aside (Arthur: "Nothing printed, did I break it?").
  *Closes when*: 3.1's `▶` line asks to try the `echo … >` line, or step 1 names
  the form. Sheets: maya O-C, arthur O-a.
  **Resolved 2026-11-09 by WP-23 (Part B), `022f78b`:** 3.1 teaches `echo hello > notes.txt`.

### Observations (reproduced)

- **O-AN — The shape line does not predict the working answer.**
  "Answer in a few words, like the lesson did, not a full sentence."
  (`RECALL_SHAPE`, `668`) prints from miss 2 (`709`). Three quotes: Leo, "implies
  length was the problem, but `overwrite append` (two words) was also rejected";
  Maya, "the first sentence that told Maya how the matcher wanted to be answered,
  and it arrived after one rejection had already been scored"; Arthur, "the
  ladder never moved past the hint through four attempts". Reproduced: the line
  is the same on every later miss, and the two-word `overwrite append` is
  rejected (F-026 table). *Closes when*: the line names a shape the list accepts
  ("repeat the lesson's words") or the lists accept short and long forms.
  Sheets: leo O-c, maya O-G, arthur F-b.
  **Addressed 2026-11-09 by WP-23, `d7dd48e`:** the shape line is removed everywhere; short
  and long forms are accepted by keyword groups.
- **O-AO — Stage 2 Q3's answer is in a second sentence and the hint uses an
  unfamiliar word.** `the notes folder` rejected (Leo); 2.4 now says "In
  `~/projects`, the bare name `notes` means `~/projects/notes`" in one sentence
  after "Predict before you act"; the hint says "a relative name". Sheets: leo O-a.
- **O-AP — 4.4 ends `▶ Type next to take Stage 4's gate` with no command to try**
  (`1902`); Leo and Maya typed no glob before the gate (Arthur typed `ls *.txt`).
  Sheets: leo O-d.
- **O-AQ — Recurring, unchanged:** `#` asides on 1.1's command lines (arthur
  O-c; O-U); undefined terms (arthur O-d: `less`, `root`, `exits 0`, `grep ^a`,
  `discard form`, `PATH`, `vimtutor`; O-AM); silent commands (arthur O-g); Ctrl+L
  blanks the lesson and `show` recovers (arthur O-b). No density charge was
  applied; screens over the limit caused no wrong turn.

### Harness and protocol (not the tutor)

- **H-1 — Terminal residue after `man` and `vim`.** Reproduced in a scratch
  sitting (`man ls`, raw `q`; `vim practice.txt`): the returned screen text shows
  the pager `:` prompt, and Vim's redraw as `Pzz\`, run-together tilde rows and
  `"practice.txt" 1L, 7B�`. `sitting.py` strips colour codes and keeps the screen
  text since the last clear; Vim and `less` redraw without a clear. The only
  reliable cue is the `[prompt] shelltutor>` marker. Maya F-C. Not a tutor defect.
- **H-2 — `^[` after Esc.** Reproduced: after raw Esc the Vim line reads `--
  INSERT --^[`; the ESC byte is kept in the returned text. Arthur O-f. Not a tutor
  defect.
- **P-1 — Turn cap.** Arthur ran 154 persona inputs against a 120-turn cap, about
  45 of them raw single keystrokes in Vim, `less` and `man`. Round 1 recorded a
  90-turn cap; no cap value appears in `docs/sim-personas/README.md`, the
  sitting template or `sitting.py`. Protocol note: state the cap and whether a raw
  keystroke counts in the sheet template.

### Candidate → disposition

| Sheet | Candidate | Disposition |
| --- | --- | --- |
| leo | F-a, F-b (Q2) | F-026, O-AN |
| leo | F-c (Q3 `the space`) | F-027 |
| leo | O-a Stage 2 Q3 | O-AO |
| leo | O-b three reading-only screens | O-T (1 point) |
| leo | O-c shape line | O-AN |
| leo | O-d 4.4 | O-AP |
| leo | O-e 3.3 `mv hi.txt notes/` needs 3.1's folder | O-AQ (no sitting hit it) |
| maya | F-A (Q2) | F-026 |
| maya | F-B (Q3) | F-027 |
| maya | F-C raw residue | H-1 |
| maya | O-A, O-E, O-F | O-AQ (no consequence) |
| maya | O-B `/stage1` | O-AG |
| maya | O-C Stage 3 redirection | F-028 |
| maya | O-D 4.1 skipped sentence | F-027 context; no charge |
| maya | O-G shape line from miss 2 | O-AN |
| arthur | F-a, F-b (Stage 1 Q3) | F-025, O-AN |
| arthur | O-a Stage 3 redirection | F-028 |
| arthur | O-b, O-c, O-d, O-g | O-AQ |
| arthur | O-e `/stage1` | O-AG |
| arthur | O-f `^[` | H-2 |
| arthur | O-h pace | by-source table |
| arthur | 154 inputs vs 120 | P-1 |

## Synthetic sittings, round 5 (the exit test)

**Exit-test result: all three personas (v0.2) reached the finale without
quitting, with 150 or fewer turns each (final friction 0, -3 and -5); no
sitting hit a dead end and only three inputs were rejected, one of which is a
false rejection (F-030); one answer was a false accept (F-029).**
Sheets `sim-sittings/{leo,maya,arthur}-5.md` ran against `7e126cf` (WP-23);
`shelltutor` on `main` (`d88c564`) is unchanged from that revision. The tutor
changes since round 4 are WP-23: recall answers match by exact form or by keyword
groups with a negation guard (`recall_matches`, `shelltutor:683-720`; negation
list `RECALL_NEGATIONS`, `675`); the shape line is gone (`RECALL_SHAPE` appears
0 times); 3.1 teaches `echo hello > notes.txt` (`3.1`, "put words in a file");
Part C cleaned `sitting.py` replies. Personas unchanged from round 4 (all v0.2).
The sheets are untracked in the maintainer checkout at the time of writing; they
are cited by name. Numbering continues at F-029 and O-AR.

### Friction by source

| Sheet | Final | Reading | Rejections (+2) | Mode confusion | Gates cleared | Turns |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| leo-5 | 0 | 1 | 4 (two) | 0 | -5 | not stated |
| maya-5 | -3 | 0 | 2 (one) | 0 | -5 | not stated |
| arthur-5 | -5 | 0 | 0 | 0 | -5 | 150 of 160 |

Leo's two rejections are a correct rejection of `>` at Stage 1 Q1 (a wrong guess)
and the Stage 1 first `check` (O-AR). Maya's one is F-030. Arthur had none.

### Round-4 items closed (with evidence)

All reproduced through the tutor's own `recall_matches` (a probe that extracts
the real functions and `ask_question` calls from `shelltutor`):

- **F-025 closed.** Stage 1 Q3 (`1216`) now accepts `it comes straight back to
  you`, `back to you` and `it comes back to me on the screen in the terminal
  window`; the hint is "Lesson 1.4: whoami printed something; think about where
  you read it." (no paraphrase). Arthur passed with `it comes back to me on the
  screen`.
- **F-026 closed.** Stage 4 Q2 (`2010`) accepts `> overwrites and >> appends`,
  `overwrite append`, `overwrite vs append`, `> overwrites the file and >> appends
  to the end`, `one replaces what is in the file and the other adds to the end of
  it`, and `one replaces the old file and two adds to the end`. All three passed
  Stage 4 Q2 on the first try.
- **F-027 closed.** Stage 4 Q3 (`2024`) accepts `the space`, `the space splits it
  into two names`, `there is a space`.
- **F-028 closed.** 3.1 shows `echo hello > notes.txt  # put words in a file`; all
  three ran it and cleared the Stage 3 task first try.
- **O-AN closed.** The shape line is gone; no sheet mentions it.
- **F-023 stays closed**: `the path /usr/bin/vim`, `its path, /usr/bin/vim`
  accepted.

### Findings (reproduced)

- **F-029 — Keyword groups accept obviously wrong answers (false accept; the new
  class).** Severity 2. Stage 2 Q3 (`1518`) has the group
  `~/projects/notes|projects/notes|the notes folder|notes`; whole-word `notes`
  makes the bare name pass. Leo passed with `notes`, the answer he said was
  "obvious" without having read the sentence that teaches it. Reproduced
  accepted: `notes`, `i am in notes`, `my notes`, `cd notes`, `projects notes`,
  `notes folder in the home folder`; rejected: `projects`, `the projects folder`,
  `~/notes`, `/notes`, `~`. Probing every question's groups for a wrong answer
  that passes (negation words, such as `not`, correctly block "not notes"):

  | Question (line) | Wrong answer that passes |
  | --- | --- |
  | Stage 1 Q1 (`1184`) | `a dollar is wrong, it is a hash` |
  | Stage 1 Q2 (`1194`) | `the path to python`, `the user folder`, `a folder in the cloud` |
  | Stage 1 Q3 (`1216`) | `a window in my browser`, `to a file on the screen of my phone` |
  | Stage 2 Q1 (`1474`) | `it deletes the parent folder`, `it makes a parent folder` |
  | Stage 2 Q2 (`1496`) | `a home page`, `the home key` |
  | Stage 2 Q3 (`1518`) | `notes`, `i am in notes`, `projects notes` |
  | Stage 3 Q1 (`1733`) | `touch is wrong it is mkdir` |
  | Stage 3 Q2 (`1740`) | `gone to the trash` |
  | Stage 3 Q3 (`1749`) | `mv is wrong use cp`, `cp then mv` |
  | Stage 4 Q1 (`1986`) | `where`, `where is the manual` |
  | **Stage 4 Q2 (`2010`)** | **`> appends and >> overwrites` (the two words swapped)** |
  | Stage 4 Q3 (`2024`) | `because it splits the screen`, `a space is missing` |
  | Stage 5 Q1 (`2303`) | `type q then delete everything`, `q is for question` |
  | Stage 5 Q2 (`2313`) | `the w key in a game`, `write the file by deleting it` |
  | shells Q1/Q2/Q3 (`2706`, `2716`, `2726`) | `a folder program`; `command -v bash`; `login window` |
  | env Q1/Q2/Q3 (`3002`, `3009`, `3023`) | `export is wrong use set`; `a file name list`; `me> replaced shelltutor` |

  The Stage 4 Q2 swap is the most serious: the two groups are ANDed but not
  ordered, so a learner with the arrows reversed passes. The matcher corpus
  (`scripts/matching-corpus.tsv`, FF-011) holds `the notes folder` as an accept
  and no bare-`notes` or swapped-arrow reject. A one-word group
  (`touch`, `mv`, `q`, `home`, `where`, `w`) cannot tell a right answer from a
  wrong one that contains the word. *Closes when*: the corpus gains reject rows
  for these (bare `notes`, swapped `> appends and >> overwrites`, `touch is wrong
  it is mkdir`, `gone to the trash`), and the groups are tightened or the exact
  forms carry the weight for one-word answers. Sheets: leo F-A.
  **Resolved 2026-11-09 by WP-24 (A10), `8d8b21f` (13 reject rows; one-word groups
  tightened), `230e5e0` (ordered groups, `--reject`; 23 more rows).** Known limit:
  `>> overwrites and > appends` (words in order, arrows swapped) still passes.
- **F-030 — Stage 5 Q2 rejects `:wq (or :w) writes the buffer to the file`.**
  Severity 2. Group `:w|w|write` (`2313`). Whole-word matching pads the
  normalised answer with spaces; `normalize_answer` strips only `'`, `.`, `,` and
  `!` (`664`), so the parenthesis stays glued: the answer holds `:wq`, `(or` and
  `:w)`, none of which equals `:w`, `w` or `write`, and `writes` is not `write`.
  Reproduced: reject `:wq (or :w) writes the buffer to the file` and `:wq (or :w)`;
  accept `:wq`, `:w`, `:w writes the buffer to the file`, `write`, `w`. So `:wq`
  alone passes (Maya's hint was "Lesson 5.3: the colon command for putting the
  buffer into the file"; she retyped `:w`). Maya +2. *Closes when*: `normalize_answer`
  also drops `(` and `)` (and the corpus gains `:wq (or :w) writes the buffer to
  the file` as an accept), or `writes` joins the group. Sheets: maya F-A, F-B.
  **Resolved 2026-11-09 by WP-24, `9acbebd`:** `(`, `)` and `;` are dropped (not
  colons); `:wq`, `writes`, `write it`, `save`, `saves` join the group.

### Observations (reproduced)

- **O-AR — The Stage 1 gate task counts only commands run after it starts.**
  By design. `hist_mark=$(history_mark)` is taken when the task begins (`1245`),
  and `gate_require_history` reads only lines after it (`history_since`, `767-780`).
  Leo ran `whoami`, `pwd`, `date` in 1.3, so the first `check` printed `○ whoami
  not yet: not in your history` for all three (+2). The task screen says "run each
  of these once" (`1253`) and "Type check only after running all three" (`1262`);
  neither says earlier runs do not count. Sheets: leo F-B.
  **Addressed 2026-11-09 by WP-24, `e64869a`:** the task screen says only commands
  typed after it count.
- **O-AS — The finale lists commands the learner may not have run.** The list is
  static: `finale()` (`2471`) prints a fixed "you have met" heredoc (`commands`
  `echo, pwd, whoami, date, clear, exit, …, vimtutor`, `2478-2480`); nothing reads
  history or progress. Maya saw `exit` and `vimtutor` listed. Sheets: maya O-004.
  **Addressed 2026-11-09 by WP-24, `e64869a`:** the list is introduced with "This
  course covered:".
- **O-AT — The Stage 4 task verifies the file's content, not the pipeline.**
  `stage4_verify_task` (`1968-1972`) requires `count.txt` to exist and its content
  with whitespace removed to equal `100`; the history check requires only a `*.txt`
  glob (`2078`). Reproduced: `seq 1 100 | wc -l > count.txt` passes; `echo 100 >
  count.txt` passes; `seq 1 100 > count.txt` fails (its content collapses to
  `12345…100`), so Arthur's second reading is rejected, not accepted. "Save the
  count" admits the two readings the verifier tells apart. Sheets: maya O-005,
  arthur O-008.
  **Addressed 2026-11-09 by WP-24, `e64869a`:** the task says to count the lines of
  `seq 1 100` and save that number to `count.txt`.
- **O-AU — The Stage 3 gate deletes the file 3.1 made (Arthur's claim not
  reproduced).** Arthur wrote that `notes.txt` already existed at the task and was
  overwritten silently. Reproduced: after `echo hello > notes.txt` in 3.1, `ls`
  shows it; at the Stage 3 gate task `ls` shows nothing, because `stage3_gate`
  removes `notes.txt`, `backup.txt` and `done.txt` at entry (`1761`). The task text
  "create a file notes.txt" is therefore accurate; what is true is that the lesson's
  file disappears with no word on screen. Sheets: arthur O-006.
- **O-AV — Recurring, unchanged.** The prompt folder changes at the Stage 1 task
  (O-AG; three of three sheets: leo O-D, maya O-002, arthur O-001; the 1.3 sentence
  "Here pwd shows the tutor's own folder" is not retracted). Terms used before they
  are taught (O-AM/O-AQ): leo O-C; arthur O-002 (`bash`, `less`), O-007 (`exits 0`,
  `^`), O-009 (`:q!` in 5.2); `bare name`; no drive letter (arthur O-004); silent
  commands (arthur O-003, O-005); `vim --version` prints a screen of flags (maya
  O-001); the Stage 2 Q3 sentence sits in a skipped paragraph (leo, maya O-007);
  "(inside this stage's folder)" (maya O-003). The hint at Stage 1 Q1's first miss
  points at 1.3 (leo O-A) and the answer is the second sentence there.

### Harness (not the tutor)

- **H-3 — A full-screen program on screen is one long line.** While Vim is
  running, the reply is the drawing with cursor positioning ignored (tildes run
  together; after Esc "no visible change"). Part C removed the residue after the
  program exits; the live screen is unchanged. Sheets: leo O-F, maya O-006,
  arthur O-010.
  **Recorded 2026-11-09 as a known harness limit** in `scripts/sim/README.md`.

### Candidate → disposition

| Sheet | Candidate | Disposition |
| --- | --- | --- |
| leo | F-A `notes` accepted | F-029 |
| leo | F-B first `check` | O-AR |
| leo | O-A, O-B | O-AV, O-T |
| leo | O-C jargon | O-AV |
| leo | O-D `/stage1` | O-AV (O-AG) |
| leo | O-E no mode confusion | positive: "this is not the shell" held |
| leo | O-F capture | H-3 |
| maya | F-A, F-B `:wq (or :w)…` | F-030 |
| maya | O-001 `vim --version` | O-AV |
| maya | O-002 `/stage1` | O-AV |
| maya | O-003 "inside this stage's folder" | O-AV |
| maya | O-004 finale list | O-AS |
| maya | O-005 "save the count" | O-AT |
| maya | O-006 Esc invisible | H-3 |
| maya | O-007 Stage 2 Q3 sentence | O-AV |
| arthur | F none | -- |
| arthur | O-001 `/stage1` | O-AV (O-AG) |
| arthur | O-002, O-007, O-009 terms | O-AV |
| arthur | O-003 Ctrl+L/Ctrl+C silence | O-AV |
| arthur | O-004 drive letter | O-AV |
| arthur | O-005 silent `>` | O-AV |
| arthur | O-006 notes.txt exists | O-AU (not reproduced as stated) |
| arthur | O-008 "count" two readings | O-AT |
| arthur | O-010 insert mode invisible | H-3 |

## Operator review of the rendered welcome (2026-11-09, after WP-25)

Human review by the operator of the welcome screen at `dd297d2` (macOS, 80
columns). Full text: `docs/operator-review-welcome-2026-11-09.md`.

- **O-AW — The course-map row under the welcome box runs together.** Five
  stage names separated by double spaces read as one sentence, and the dots
  have no label (`shelltutor` welcome, the row after the box). The consultant
  response §5.3 proposed it; the proposal does not fit 80 columns with
  findable separators. *Closes when*: the map is vertical, inside the box,
  one stage per row with its own dot (WP-27).
  **Closed 2026-11-09 by WP-27, `5d50f46`** (rebased SHA on landing): the map
  is inside the box, one stage per row; passed stages show a green dot on a
  retake.
- **O-AX — The sandbox path row is jargon on the welcome and a missed
  lesson.** A `Sandbox:` row with a long path sits under the box; "sandbox"
  is undefined for a beginner and over-claims isolation. *Closes when*: the
  row leaves the welcome, on-screen copy says "practice folder" (WP-27), and
  the practice folder becomes a recurring teaching object in Stage 1 `pwd`,
  the Stage 2 tree and `cd`, Stage 3 and the `env` module (WP-26 and the
  `env` follow-up). Relates to O-AG/O-AV (the prompt folder changes at gate
  tasks without a word).
  **Closed for its rendering half 2026-11-09 by WP-27, `ca8ed86`:** the row is
  off the welcome and no screen, `-h`, `--info` label or error message prints
  "sandbox"; the teaching thread stays with WP-26 and the `env` follow-up.

Check requested by the review: the default practice folder is
`$HOME/.shelltutor` (`shelltutor:62`), so it sits under home and the `~`
lesson can use it; the `/var/folders/...` path in the screenshot came from
the coordinator's suggested `SHELLTUTOR_HOME=$(mktemp -d)` run command, not
from a learner default. Note the default is a dot-folder, hidden from plain
`ls`, which the Stage 2 `ls -a` lesson can use.
