---
title: Synthetic sitting - leo-1
category: audit
component: sim-sitting
status: candidate-evidence
version: 0.1.0
last_updated: 2026-11-09
tags: [audit, simulation, synthetic-sitting, leo]
priority: medium
---

# Synthetic walkthrough - Leo, sitting 1

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/leo.md` (Leo, 13, `gamer-brute-forcer`); learner role: child
- Simulation rules confirmed: zero forward knowledge, reading limit (commands, `▶` lines and command-coloured text only, unless a screen is under eight lines), friction meter (+2 / +1 / +1 / -1, quit at 8). Friction +1 for prose-over-limit was applied only to reading-only screens after the second in a row, as the persona sheet states; screens that had a practice prompt were not charged for skipped prose.
- Tutor revision: `a25caf7`; invocation: `sitting.py start --bash /bin/bash --persona leo` (no `--arg`, entry at the welcome screen); Bash used: `/bin/bash` 3.2.57
- `--info` lines shown: none

## Per screen

### welcome - SHELLTUTOR, a vimtutor prerequisite course
- **Read**: skimmed; read only the `▶` line. Did not read the prose (12 lines).
- **Jargon**: "prerequisite", "the tutor never writes outside that folder"
- **Monologue**: Lots of words. The arrow line says type next. ok.
- **Input** `[nav]` -> `next` -> accepted.
- **Interpretation**: Next one.
- **Ladder rung**: none. **Friction**: 0 (first reading-only screen).

### orientation - Orientation
- **Read**: skimmed; read the `▶` line only. Did not read "Four words steer the tutor", the "shelltutor>" explanation, or the resize note.
- **Jargon**: "keyboard-only", "practice prompt"
- **Monologue**: Again the arrow line says next. Skipped the middle.
- **Input** `[nav]` -> `next` -> accepted.
- **Ladder rung**: none. **Friction**: 0 (second reading-only screen in a row).

### Stage 1 intro - STAGE 1 - Where am I?
- **Read**: all (under eight lines).
- **Jargon**: "the prompt"
- **Monologue**: Short one. Lessons, a task. Fine, next.
- **Input** `[nav]` -> `next` -> accepted.
- **Ladder rung**: none. **Friction**: 1 (+1, third reading-only screen in a row).

### 1.1 - running commands
- **Read**: skimmed; read the command lines (`echo hello`, the other two echo lines) and the `▶` line. Did not read "a name, then the words you hand it".
- **Jargon**: "the words you hand it", "the shape of every command"
- **Monologue**: echo hello is the magic word. Commands start with slash, right? `/echo hello`.
- **Input** `[bash]` -> `/echo hello` -> `bash: /echo: No such file or directory` (rejected).
- **Interpretation**: It says echo is wrong. The screen has no slash though. Try it exactly.
- **Ladder rung**: none (raw bash error only). Did not resolve the confusion by itself; he fixed it by copying the screen.
- **Friction**: 3 (+2 rejected, not understood).
- Further inputs `[bash]`: `echo hello` -> `hello`; `echo I am at the shell` -> `I am at the shell`; `echo "I am at the shell"` -> `I am at the shell`; `next` `[nav]` -> accepted. Friction stays 3.

### 1.2 - keyboard habits
- **Read**: skimmed; read the four key names and the `▶` line. Did not read the Tab explanation beyond `echo p`, the "Other shells and setups differ" line, or the Ctrl+C paragraph.
- **Jargon**: "bash finishes a word", "shared part", "escape hatch"
- **Monologue**: Try each key. Typing `echo p`, then Tab. Up arrow brings back the old command. Skipping the Ctrl ones, they look boring.
- **Input** `[bash]` -> `echo p` + Tab (`raw`) -> line became `echo poem.txt`; Enter -> `poem.txt`; Up arrow (`raw`) -> `echo poem.txt` recalled; Enter -> `poem.txt`; then `next` `[nav]` -> accepted. Ctrl+L and Ctrl+C never tried.
- **Interpretation**: It typed a word for me. Cool.
- **Ladder rung**: none. **Friction**: 3.

### 1.3 - where am I, who am I, when is it
- **Read**: skimmed; read the three command names and the `▶` line. Did not read "Here pwd shows the tutor's own folder".
- **Jargon**: "print working directory" (in the comment on the `pwd` line)
- **Monologue**: Three words, whoami pwd date.
- **Input** `[bash]` -> `whoami` -> `[user]`; `pwd` -> a long temp path; `date` -> the date; then `next` `[nav]`.
- **Interpretation**: pwd printed a long path with slashes.
- **Ladder rung**: none. **Friction**: 3.

### 1.4 - the shell, caught in the act
- **Read**: skimmed; read `date`, `dtae` and the `▶` line. Did not read "Read who is speaking" or the terminal / shell / program paragraph.
- **Jargon**: "terminal -> shell -> program", "The shell is the program named bash"
- **Monologue**: Type date, type dtae. Command not found, so spelling is picky.
- **Input** `[bash]` -> `dtae` -> `bash: dtae: command not found`; `next` `[nav]`.
- **Ladder rung**: none. **Friction**: 3.

### 1.5 - who else types here
- **Read**: did not read (reading-only; 14 lines); read the `▶` line.
- **Jargon**: "goes terminal -> shell -> program", "habits count twice"
- **Monologue**: Wall of words about AI. Arrow says next for the gate.
- **Input** `[nav]` -> `next` -> accepted.
- **Ladder rung**: none. **Friction**: 3 (only one reading-only screen in a row; no charge).

### gate - STAGE 1 - GATE (Q1: Which character usually ends a shell prompt? ($, ;, :, or #))
- **Read**: skimmed the intro; read the question line.
- **Jargon**: "Recall", "shell prompt"
- **Monologue**: Another prompt. Guess it is the same kind. Try ls.
- **Input** `[bash]` (believed) -> `ls` -> `not quite. try again.` (rejected).
- **Interpretation**: It's a question, not the shell. Pick one of the four.
- **Ladder rung**: message ("not quite. try again."); the question was redrawn directly under it. The redrawn question resolved the confusion.
- **Friction**: 6 (+2 rejected, not understood; +1 mode confusion).

### gate Q1 retry
- **Monologue**: Dollar looks like the shell thing from videos.
- **Input** `[recall]` -> `$` -> accepted (`✓`). Friction 6 (no -1; the gate is not cleared).

### gate Q2 - What does pwd print?
- **Read**: all.
- **Jargon**: none on the question itself. The answer expected is unclear to him; the lesson wording "print working directory" and "the folder you're in" were on the skipped lines.
- **Monologue**: pwd printed a long path with slashes. I'd say the folder.
- **Input** `[recall]` -> `the folder` -> `not quite. try again.` (rejected).
- **Interpretation**: Not quite again? What does it want, one word? I don't know what it wants. This is stupid, I'm out.
- **Ladder rung**: message only ("not quite. try again."); no hint rung reached. Nothing told him what shape of answer is wanted.
- **Friction**: 8 (+2 rejected, not understood). **Quit.**

## Per gate

- Recall: Q1 two attempts (rejected verbatim: `ls`), rung: message only. Q2 one attempt (rejected verbatim: `the folder`), rung: message only. Q3 never shown.
- Task: not reached.
- Cleared / not cleared: not cleared.

## End of sitting

- Final friction: 8; quit at the gate, Q2 ("What does pwd print?"), after 23 persona inputs. The hard cap of 90 turns was not reached.
- Stages or module cleared: none (lessons 1.1 to 1.5 walked; the Stage 1 gate was not cleared).
- Equivalent human sitting time: estimate about 8 to 10 minutes for 23 inputs and a few stalls.
- **Candidate F-nnn**:
  - F-a (gate Q2, input `the folder`): a plain-language description of what `pwd` printed is rejected with only "not quite. try again." and no indication of the expected form; for a learner who skipped the 1.3 prose, no way to find the accepted answer. May be a dead end for a brute-forcer if the accepted set is narrow. Needs a maintainer to check what answers the gate accepts.
- **Candidate O-nnn**:
  - O-a (1.1, input `/echo hello`): bash's raw `bash: /echo: No such file or directory` is the only response to a leading slash; the screen offers no connection between that message and the slash.
  - O-b (gate Q1, input `ls`): the gate looks identical to the practice prompt; he typed a shell command into a recall question (mode confusion). Only "not quite. try again." and the redrawn question told him.
  - O-c (welcome, orientation, Stage 1 intro): three reading-only screens in a row before the first practice prompt; he read only `▶` lines on the first two.
  - O-d (1.2): Ctrl+L and Ctrl+C were never practised and nothing checked them; "Try each key, then type next." accepted `next` regardless.
  - O-e (1.3): "pwd  # print working directory - the folder you're in" gives "working directory" as the first gloss, before the plain wording.
  - O-f (gate Q2): "not quite. try again." is the same reply for a wrong shell command (`ls`) and for a near-miss plain-English answer (`the folder`).
- **Debrief** (out of character):
  - The sentence "Then a practical task: run a few commands and tell me what they printed." and the Q1 line "Which character usually ends a shell prompt?" look like the practice prompt, so he typed a command at it.
  - The Q2 question "What does pwd print?" has no stated answer form; the lesson's answer sat in "pwd  # print working directory - the folder you're in" and "Here pwd shows the tutor's own folder", both outside what he read.
  - The reply "not quite. try again." was identical for both rejections and gave no clue why; this reply drove both +2 steps toward quitting.
  - The first two screens' prose ("Four words steer the tutor") was skipped, so the rule that the `shelltutor>` prompt takes commands but the gate prompt takes answers was never read.
