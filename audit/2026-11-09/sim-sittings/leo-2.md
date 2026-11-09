# Synthetic walkthrough — Leo, sitting 2

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/leo.md` (Leo, 13, `gamer-brute-forcer`); learner role: child
- Simulation rules confirmed: zero forward knowledge, reading limit (commands, ▶ lines and command-colour text unless the screen is under eight lines), friction meter (quit at 8). No memory of sitting 1.
- Tutor revision: afce3fe (script 82792b6); invocation: `sitting.py start` with `--bash /bin/bash` (3.2.57), no `--arg` (begins at the welcome screen), persona `leo`
- `--info` lines shown: none

## Per screen

### welcome — SHELLTUTOR — a vimtutor prerequisite course
- **Read**: did not read (only the ▶ line).
- **Jargon**: none seen (not read).
- **Monologue**: Big wall of words. Only the arrow line matters.
- **Input** `[nav]` → `next` → accepted.
- **Interpretation**: Fine.
- **Ladder rung**: none.
- **Friction**: 0 (reading-only screen 1).

### orientation — Orientation
- **Read**: did not read (▶ line only; `shelltutor>` seen in command colour).
- **Jargon**: none read.
- **Monologue**: Skipped it. Arrow line says next again.
- **Input** `[nav]` → `next` → accepted.
- **Ladder rung**: none.
- **Friction**: 0 (reading-only screen 2).

### stage 1 intro — STAGE 1 — Where am I?
- **Read**: all (under eight lines of body).
- **Jargon**: none.
- **Monologue**: Short, read it. Third talky screen and no game yet.
- **Input** `[nav]` → `next` → accepted.
- **Ladder rung**: none.
- **Friction**: 1 (third reading-only screen in a row, +1).

### 1.1 — running commands
- **Read**: skimmed (read the three `echo` commands and the ▶ line; skipped the explanation).
- **Jargon**: none read.
- **Monologue**: A command at last. Typing them exactly.
- **Input** `[bash]` → `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` → each accepted, output echoed.
- **Interpretation**: It says things back. Easy.
- **Ladder rung**: none.
- **Friction**: 1.
- Then `[nav]` `next` → accepted.

### 1.2 — keyboard habits
- **Read**: skimmed (commands and key names; skipped the explanatory prose).
- **Jargon**: "shared part", "escape hatch".
- **Monologue**: Try each key. Tab filled in poem.txt like autocomplete in a game. Up brought the line back.
- **Input** `[bash]` → `echo p` + Tab (raw `echo p\t`) → `echo poem.txt` filled; Enter ran it. Up arrow then Enter ran it again. Ctrl+L (raw `\x0c`) cleared everything including the lesson. `[nav]` `show` brought it back. Ctrl+C (raw `\x03`) gave a fresh prompt. `[nav]` `next`.
- **Interpretation**: After Ctrl+L the screen went blank apart from the prompt; I only knew `show` because it was on a line I read.
- **Ladder rung**: none.
- **Friction**: 1.

### 1.3 — where am I, who am I, when is it
- **Read**: skimmed (the three commands and ▶ line).
- **Jargon**: "print working directory"; "prompt usually ends in $" (not read).
- **Monologue**: Commands in this game start with a slash.
- **Input** `[bash]` → `/whoami` → rejected: `bash: /whoami: No such file or directory`.
- **Interpretation**: It is not a file. No idea what that means. Try without the slash.
- **Ladder rung**: none (raw bash error; no tutor rung).
- **Friction**: 3 (+2 rejected input not understood).
- **Input** `[bash]` → `whoami` → output (login name, `[user]`); `pwd` → a long temp-folder path; `date` → date line. All accepted. `[nav]` `next`.
- **Friction**: 3.

### 1.4 — the shell, caught in the act
- **Read**: skimmed (commands `date`, `dtae`).
- **Jargon**: "terminal → shell → program" (skipped).
- **Input** `[bash]` → `date`, `dtae` → `command not found` as promised. `[nav]` `next`.
- **Friction**: 3.

### 1.5 — who else types here
- **Read**: did not read (12-line prose, ▶ line only).
- **Jargon**: none read.
- **Monologue**: Wall of text about AI. Skip.
- **Input** `[nav]` → `next` → accepted.
- **Friction**: 3 (reading-only screen 1 after a practice screen).

### gate — STAGE 1 — GATE (Q1)
- **Read**: skimmed (read the ┃ question block; skipped the intro text).
- **Jargon**: "normal bash window"; the question lists `$, ;, :, or #` without saying which is which.
- **Monologue**: A prompt again, so it must be the shell. I will type next.
- **Input** `[recall; believed bash/nav]` → `next` → rejected: "not quite. try again." plus "Hint: Lesson 1.3 compared this tutor's prompt with a normal one."
- **Interpretation**: Not quite? I do not remember 1.3 and cannot see what is wrong. Mash another.
- **Ladder rung shown**: hint (on the first miss); did not resolve the confusion (Leo had not read 1.3 and treated the question as another shell prompt).
- **Friction**: 6 (+1 mode confusion, +2 rejected not understood).
- **Input** `[recall]` → `ls` → rejected: same "not quite", same hint, plus "Passed stages are saved. Type quit to leave now; the next run starts this stage from its first lesson. Type show to see the question again."
- **Interpretation**: Same error, same hint. Homework. I am out.
- **Ladder rung shown**: hint again (no escalation); copied nothing, not resolved.
- **Friction**: 8 -> QUIT.

## Per gate

- Recall: Q1, 2 attempts, inputs rejected verbatim `next`, `ls`; rung reached: hint (repeated, same text). Q2, Q3 not reached.
- Task: not reached.
- Not cleared.

## End of sitting

- Final friction 8; quit at the Stage 1 gate, Q1 (screen "task", STAGE 1 — GATE). `stop` was run; the tutor was not exited by Leo.
- Stages cleared: none (lessons 1.1 to 1.5 completed; gate not passed).
- Equivalent human sitting time: estimate about 6 to 8 minutes, then a walk-away.
- **Candidate F-nnn**:
  - F-a (dead end): gate Q1, inputs `next` then `ls` returned the same hint text; the second miss did not escalate to facts (no worked answer). A child who skipped 1.3 prose has no route to the answer from the hint alone; the question lists four characters without a clue which fits. Needs maintainer reproduction (may be by design: facts from second miss per recent commit ahead of A7; here the second miss showed hint again, not facts).
- **Candidate O-nnn**:
  - O-a (mode confusion), gate Q1: the screen says "Type your answer in words; this is not the shell." Leo typed `next` to it. The gate intro block (not read) is the only place that distinguishes recall from the shell; the `[prompt] ┃ answer in words:` line looked like the shell prompt to him once the ┃ question appeared.
  - O-b (leading slash), 1.3: input `/whoami` gave "bash: /whoami: No such file or directory"; no sentence on screen explains that commands are typed without a slash or what "file or directory" means here.
  - O-c (pace), welcome, orientation, stage 1 intro: three consecutive screens with no practice prompt; Leo read only the ▶ lines and took +1 friction on the third.
  - O-d (Ctrl+L), 1.2: after Ctrl+L the lesson is blank with only the prompt; recovery depends on the "show brings the lesson back" phrase.
  - O-e (jargon), 1.3: "print working directory — the folder you're in"; 1.2: "shared part", "escape hatch".
  - O-f (reading load), 1.5: 12 lines of prose before the gate with no practice step.
- **Debrief** (out of character):
  - The gate intro "Type your answer in words; this is not the shell." sits above the question and was skipped; Leo's two inputs to Q1 were commands.
  - Q1 "which character usually ends the prompt? ($, ;, :, or #)" offers symbols but the hint "Lesson 1.3 compared this tutor's prompt with a normal one." names no symbol and the 1.3 sentence is in prose he did not read.
  - "bash: /whoami: No such file or directory" gave no route back to "whoami".
  - Three screens of "Type next" before 1.1 account for the first friction point.
  - Both rejected Q1 answers returned the identical hint line.
