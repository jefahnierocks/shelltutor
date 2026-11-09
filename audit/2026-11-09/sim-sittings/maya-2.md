# Synthetic walkthrough — one sitting (maya-2)

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/maya.md` (Maya, 19, graphic design student, `search-first-skimmer`); learner role: adult beginner. Second sitting; no memory of the first.
- Simulation rules confirmed: zero forward knowledge, reading limit (four prose lines, bold and ▶ lines read anyway), friction meter (quit at 8). Friction rule applied literally: +1 for any screen with more than four prose lines.
- Tutor revision: afce3fe (script 82792b6); invocation: server started by the maintainer, `/bin/bash` 3.2.57, no `--arg` (begins at the welcome screen).
- `--info` lines the persona was shown: none.

## Per screen

### welcome — SHELLTUTOR, a vimtutor prerequisite course
- **Read**: skimmed (read the first four lines; skipped the "Your work happens in ..." paragraph with the long temp path and "this is the real thing, not a simulation"; ▶ read).
- **Jargon**: "a vimtutor prerequisite course".
- **Monologue**: Five stages, fine. The rest is a wall of text, the arrow says type next.
- **Input** `[nav]` → `next` → accepted.
- **Interpretation**: ok.
- **Ladder rung**: none.
- **Friction**: 1 (+1 over reading limit, about nine prose lines).

### orientation — Orientation
- **Read**: skimmed (read to "keyboard-only"; skipped the four-words list tail and "A fifth word, check").
- **Jargon**: "practice prompt", "shelltutor>".
- **Monologue**: Wall of text again. Keyboard only, no clicking, ok. Skip to the arrow.
- **Input** `[nav]` → `next` → accepted.
- **Ladder rung**: none. **Friction**: 2 (+1 over limit).

### stage 1 intro — STAGE 1 — Where am I?
- **Read**: all. **Input** `[nav]` → `next` → accepted. **Friction**: 2.

### 1.1 — running commands
- **Read**: skimmed (skipped the final paragraph "echo just repeats its words back ... a name, then the words you hand it", and "If bash says command not found").
- **Jargon**: "command", "spaces separate words", "quotes group them".
- **Monologue**: Three things to try. Do them in order.
- **Input** `[bash]` → `echo hello` → `hello`; `echo I am at the shell` → `I am at the shell`; `echo "I am at the shell"` → `I am at the shell`; then `[nav]` `next`.
- **Interpretation**: Same output twice, so what was the point of the quotes? (not shown to matter here; she moves on).
- **Ladder rung**: none. **Friction**: 3 (+1 over limit).

### 1.2 — keyboard habits
- **Read**: skimmed (read the Tab entry; skipped the "(Other shells and setups differ.)" aside, and the Ctrl+C entry).
- **Jargon**: "bash finishes a word", "shared part", "escape hatch".
- **Monologue**: Tab is autocomplete, cool. Up arrow is history. Ctrl+C to get out, Ctrl+L clears.
- **Input** `[bash]` → `echo p<Tab>` → line became `echo poem.txt`; `\r` → `poem.txt`; `[bash]` Up arrow → `echo poem.txt` back on the line; Ctrl+C → fresh prompt; Ctrl+L → blank screen; `[nav]` `show` → lesson redisplayed; `next`.
- **Interpretation**: All four keys worked as described. Ctrl+L blanked the screen, `show` fixed it.
- **Ladder rung**: none. **Friction**: 4 (+1 over limit).

### 1.3 — where am I, who am I, when is it
- **Read**: skimmed (read the three commands; skipped the paragraph about the prompt ending in `>` versus `$`, and the "Stage 2 is all about folders" line).
- **Jargon**: "print working directory", "practice prompt starts".
- **Monologue**: A long weird path from pwd. It knows my name, creepy.
- **Input** `[bash]` → `whoami` → [user]; `pwd` → long temp folder path; `date` → date line; `[nav]` `next`.
- **Ladder rung**: none. **Friction**: 5 (+1 over limit).

### 1.4 — the shell, caught in the act
- **Read**: skimmed (read to "bash: is the shell"; skipped "terminal → shell → program" explanation).
- **Jargon**: "terminal → shell → program", "the shell is the program named bash".
- **Monologue**: Typo on purpose, so I know what happens.
- **Input** `[bash]` → `date` → date line; `dtae` → `bash: dtae: command not found`; `[nav]` `next`.
- **Ladder rung**: none. **Friction**: 6 (+1 over limit).

### 1.5 — who else types here
- **Read**: skimmed (read the first four lines; skipped the AI-assistant paragraph and the three habits list).
- **Jargon**: "goes through a shell", "An AI assistant that runs commands".
- **Monologue**: AI stuff, skip. Gate time.
- **Input** `[nav]` → `next` → accepted.
- **Ladder rung**: none. **Friction**: 7 (+1 over limit).

### task — STAGE 1 — GATE (recall)
- **Read**: all (short).
- **Jargon**: "Type your answer in words; this is not the shell."
- **Monologue** Q1: Options listed; vaguely remember a dollar sign. A guess I know is a guess (0). Q2: pwd printed my folder. Q3: it shows on the screen.
- **Input** `[recall]` → `$` → ✓; `the folder you are in` → ✓; `it shows up on the screen` → "not quite. try again." plus hint.
- **Interpretation**: I said the screen; the hint says "the window you type into". That is the screen. Why was mine wrong? I can't tell what they want.
- **Ladder rung shown**: hint ("Lesson 1.4: what a program prints comes back to you, in the window you type into."). Did not resolve the confusion: it restates what she answered.
- **Friction**: 9 (+2 rejected input not understood). Over 8: QUIT at the Stage 1 gate, Q3.

## Per gate

- Recall: Q1 one attempt (guess, accepted); Q2 one attempt, accepted; Q3 one attempt, rejected verbatim `it shows up on the screen`, rung reached: hint. Second attempt not made (quit).
- Task: not reached (no `check`, no checklist).
- Not cleared.

## End of sitting

- Final friction: 9. Quit at the Stage 1 gate recall, Q3 ("After whoami runs, where does its output go?"). Tutor had not exited; sitting ended by friction rule.
- Stages or module cleared: none (stage 1 lessons 1.1 to 1.5 completed; gate recall 2 of 3).
- Equivalent human sitting time: estimate about 10 minutes of reading and typing, plus a stall at Q3.
- **Candidate F-nnn**
  1. Screen `task` (Stage 1 gate Q3), input `it shows up on the screen`: a plain-language correct answer (the output appears on screen, in the window) was rejected with "not quite. try again."; the hint's own wording "in the window you type into" means the same thing.
- **Candidate O-nnn**
  1. Screens welcome, orientation, 1.1, 1.2, 1.3, 1.4, 1.5: every screen but the Stage 1 intro exceeds four prose lines; friction rose by one on each (7 of the 9 points). Example: "Your work happens in ... the tutor never writes outside that folder. Commands you run yourself have your full authority: this is the real thing, not a simulation."
  2. Screen `task` Q1, "In a normal bash window (not this tutor), which character usually ends the prompt?": the answer sits in the skipped last paragraph of 1.3 ("A normal bash window's prompt usually ends in $; same idea, different decoration."); an answer given by guess from the offered options.
  3. Screen `task` Q3 "where does its output go?": the expected wording is unclear; "screen", "terminal", "window" are not distinguished from the lesson's "comes back to you".
  4. Screen 1.1: `echo I am at the shell` and `echo "I am at the shell"` give identical output; the point of the comment "quotes group them into one" is not visible.
  5. Screen 1.2: after Ctrl+L, the screen is blank; she had to read "show brings the lesson back" at the end of a skipped line.
  6. Screen 1.3: `pwd` output is a long temp path with no relation to the "folders" she knows; "Here pwd shows the tutor's own folder" was skipped.
  7. Screen 1.4: "terminal  →  shell  →  program" was in the skipped part.
- **Debrief (out of character)**: The welcome and orientation paragraphs, and the 1.4 paragraph "Read who is speaking. bash: is the shell...", pushed the reading budget before any command was run. The Q3 prompt "After whoami runs, where does its output go?" has an accepted answer that "it shows up on the screen" did not meet, and the hint sentence "in the window you type into" reads as a restatement of that answer. The Q1 answer lives in the sentence "A normal bash window's prompt usually ends in $; same idea, different decoration." at the bottom of 1.3.
