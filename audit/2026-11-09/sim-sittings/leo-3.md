# Synthetic walkthrough — Leo, sitting 3

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/leo.md`, Leo, 13, `gamer-brute-forcer`; learner role: child
- Persona sheet version: 0.2.0
- Simulation rules confirmed: zero forward knowledge, reading limit (commands, `▶` lines, command-colour text, first sentence of each paragraph; whole screen if under eight lines; the rest recorded as "did not read"), friction meter (quit at 8).
- Tutor revision: 7204741 (script 5d1d689). Invocation: `sitting.py start` with `--bash /bin/bash` (3.2.57), no `--arg` (begins at the welcome screen), persona `leo`; Leo's third sitting, no memory of earlier ones.
- `--info` lines shown: none.

Friction accounting note: while sitting I briefly over-counted a charge on 1.1 (a screen with commands to type is not reading-only). Corrected below; the totals here are the corrected ones. Decisions were not affected.

## Per screen

### welcome — SHELLTUTOR, a vimtutor prerequisite course
- **Read**: skimmed. Read the `▶` line and the first sentence of each paragraph. Did not read: "Each stage is a few short lessons...", the folder paragraph after its first sentence.
- **Jargon**: none read.
- **Monologue**: It says type next. Fine.
- **Input** `[nav]` → `next` → accepted.
- **Ladder**: none. **Friction**: 0 (reading-only #1).

### orientation — Orientation
- **Read**: skimmed (first sentences, `shelltutor>` line, `▶` line). Did not read: the four steer words list, the "fifth word, check" paragraph.
- **Jargon**: none read.
- **Monologue**: shelltutor> is where I type. next to begin.
- **Input** `[nav]` → `next` → accepted. **Friction**: 0 (reading-only #2).

### Stage 1 intro — STAGE 1 — Where am I?
- **Read**: all (under eight lines). **Jargon**: none.
- **Monologue**: More next. When do I get to type stuff.
- **Input** `[nav]` → `next` → accepted.
- **Friction**: 1 (+1, third reading-only screen in a row).

### 1.1 — running commands
- **Read**: commands, `▶` line, first sentences. Did not read: "If bash says command not found...", "echo just repeats its words back..." beyond first sentence.
- **Jargon**: "a name, then the words you hand it" (not read in full).
- **Monologue**: Finally something to type.
- **Input** `[bash]` → `echo hello` → hello; `echo I am at the shell` → printed; `echo "I am at the shell"` → printed; then `[nav]` `next`.
- **Ladder**: none. **Friction**: 1.

### 1.2 — keyboard habits
- **Read**: Tab/up/Ctrl+C lines, `▶`. Did not read: parenthetical about other shells.
- **Jargon**: "escape hatch" (skipped).
- **Monologue**: Tab filled in poem.txt, that is like autocomplete in chat. Up brought the line back. Ctrl+C threw it away.
- **Input** `[bash]` → raw `echo p<Tab>` → `echo poem.txt`; Enter → poem.txt; raw up arrow → line returned; raw Ctrl+C → fresh prompt; `[nav]` `next`.
- **Ladder**: none. **Friction**: 1.

### 1.3 — where am I, who am I, when is it
- **Read**: three commands, `▶`, first sentences. Did not read: "Your prompt here ends in >... usually ends in $".
- **Jargon**: "print working directory" in a comment line.
- **Monologue**: It knows my name. pwd is a long path, the same one from the very start.
- **Input** `[bash]` → `whoami`, `pwd`, `date` → each printed; `[nav]` `next`. **Friction**: 1.

### 1.4 — the shell, caught in the act
- **Read**: commands, `▶`, first sentences. Did not read: "Read who is speaking...", "The terminal is the window...".
- **Jargon**: "terminal → shell → program" (read as a diagram only).
- **Monologue**: I type the broken one first, dtae.
- **Input** `[bash]` → `dtae` → `bash: dtae: command not found` (as the screen said); `date` → printed; `[nav]` `next`. **Friction**: 1 (expected error, not a rejection Leo failed to understand).

### 1.5 — who else types here
- **Read**: skimmed. Did not read: second sentence of paragraph 1, the AI-assistant paragraph beyond its first sentence, the three habit lines.
- **Jargon**: "goes through a shell the same way" (not read).
- **Monologue**: Something about AI helpers. Whatever. Gate next.
- **Input** `[nav]` → `next`. **Friction**: 1 (reading-only #1).

### Stage 1 gate (recall) — STAGE 1 — GATE
- **Read**: all (under eight lines), including "this is not the shell".
- **Monologue**: A quiz, type answers. Four choices, I guess the dollar sign.
- **Input** `[recall]` → `$` → accepted; `the folder you're in` → accepted; `the screen` → accepted.
- **Ladder**: none. **Friction**: 1.

### Stage 1 gate task — STAGE 1 — GATE TASK
- **Read**: all.
- **Input** `[bash]` → `whoami`, `pwd`, `date` → printed (pwd now ends in /stage1); `[nav]` `check`; `[follow-up]` the user name (written `[user]`), the full pwd path, `Mon` → all accepted.
- **Friction**: 0 (-1 gate cleared).

### Stage 1 cleared — ✓ Stage 1 cleared
- **Read**: skimmed. **Input** `[nav]` `next`. **Friction**: 0 (reading-only #1).

### Stage 2 intro
- **Read**: first sentence of the paragraph, the `pwd ls cd` lines, `▶`. Did not read the path-symbols paragraph in full.
- **Monologue**: Dots and a squiggle.
- **Input** `[nav]` `next`. **Friction**: 0 (reading-only #2).

### 2.1 — where you are
- **Read**: tree drawing, `▶`. **Monologue**: matches the you-are-here line.
- **Input** `[bash]` `pwd` → long path; `[nav]` `next`. **Friction**: 0.

### 2.2 — ls: what is here
- **Read**: command lines, `▶`.
- **Input** `[bash]` `ls -p` → `numbers.txt poem.txt stage1/ stage2/`; `ls /` → top-level folders; `[nav]` `next`. **Friction**: 0.

### 2.3 — cd: moving
- **Read**: `▶` line and command lines. Did not read: "cd.. with no space is a different word", the stage-start paragraph.
- **Jargon**: "current folder", "parent folder" (comment).
- **Monologue**: cd .. then pwd, the path got shorter, like leaving a room.
- **Input** `[bash]` `cd ..` → nothing printed; `pwd` → parent path; `cd -` → printed the practice folder; `[nav]` `next`. **Friction**: 0.

### 2.4 — names for places
- **Read**: skimmed. Did not read: "Predict before you act. In ~/projects, cat notes.txt reads ~/projects/notes.txt..." and the relative/absolute paragraph beyond first lines.
- **Jargon**: "Relative paths start where you are", "Absolute paths start from the root".
- **Input** `[nav]` `next`. **Friction**: 0 (reading-only #1).

### Stage 2 gate (recall) — STAGE 2 — GATE
- **Read**: all.
- **Monologue**: Same quiz style. Answer in words.
- **Input** `[recall]`:
  - Q1 `goes up one folder` → accepted.
  - Q2 `your home folder` → rejected ("not quite. try again."), hint: "It is where cd with nothing after it takes you." Friction +2 = 2. Leo: that is what the list said; typed `home` → accepted.
  - Q3 `notes` → rejected, hint: "Lesson 2.4: a relative name starts from the folder you are already in." Friction +2 = 4. Leo followed the hint: `~/projects/notes` → accepted.
- **Ladder**: hint twice; the Q2 hint was a pointer to a different fact and resolved nothing by itself (answer found by guessing `home`); the Q3 hint worked as a pointer and was followed.
- **Friction**: 4.

### Stage 2 gate task — STAGE 2 — GATE TASK
- **Read**: the numbered list. Never saw how to make a folder taught anywhere.
- **Jargon**: "inside this stage's folder".
- **Monologue**: Make a folder called practice. Nobody taught the word.
- **Input** `[bash]` `make practice` → `make: *** No rule to make target `practice'.  Stop.` (rejected, not understood, +2 = 6). `new folder practice` → `bash: new: command not found` (+2 = 8). Quit.
- **Ladder**: none shown at the shell prompt.
- **Friction**: 8, quit here.

## Per gate

- **Stage 1**: recall Q1-Q3 each correct first try; task correct first try (`whoami`, `pwd`, `date`, `check`, three follow-ups). Cleared.
- **Stage 2**: recall Q1 first try; Q2 two attempts (`your home folder` rejected, `home` accepted), hint rung; Q3 two attempts (`notes` rejected, `~/projects/notes` accepted), hint rung. Task: 2 attempts, both rejected (`make practice`, `new folder practice`), `check` never run, nothing marked. Not cleared.

## End of sitting

- **Final friction**: 8. Quit at Stage 2 gate task. By source: reading-only charges +1 (Stage 1 intro); rejections +8 (four, at +2: Q2 `your home folder`, Q3 `notes`, `make practice`, `new folder practice`); mode confusion 0; gate cleared -1 (Stage 1). Net 1 + 8 - 1 = 8.
- **Stages cleared**: Stage 1 only (Stage 2 recall passed, task not cleared). Server did not exit.
- **Equivalent human sitting time**: about 20 to 25 minutes (estimate): Stage 1 about 10, Stage 2 lessons about 5, gate stall about 5 to 10.
- **Candidate F-nnn**
  - F-a: Stage 2 gate recall Q2 "What does ~ mean in a path?", input `your home folder` rejected ("not quite"), where the lesson (2.4) says `~    your home folder`. `home` accepted.
  - F-b: Stage 2 gate task, "make a folder called practice": the stage never teaches a folder-making command (2.1 to 2.4 cover `pwd`, `ls`, `cd`, paths), so the task is a dead end for a learner without that word; inputs `make practice`, `new folder practice`; no ladder rung at the shell prompt.
  - F-c: Stage 2 gate recall Q2 hint "It is where cd with nothing after it takes you." does not say what is wrong with `your home folder`; it points to a different fact and did not resolve the confusion.
- **Candidate O-nnn**
  - O-a: Welcome, orientation and Stage 1 intro are three reading-only screens before any typing; Leo's friction +1 at "Five short lessons (about 10 minutes) followed by a small task."
  - O-b: Stage 2 gate recall screen has no "this is not the shell" sentence (Stage 1 gate has "Type your answer in words; this is not the shell."); Leo relied on `answer in words:` and the `┃` mark, and did not mistype to the wrong prompt this sitting.
  - O-c: 2.3 prints nothing for `cd ..`; Leo needed `pwd` to see any effect.
  - O-d: Stage 1 gate Q1 ("which character usually ends the prompt") answer lives in 1.3's second sentence "A normal bash window's prompt usually ends in $", which Leo did not read; he passed by guessing from the listed options.
- **Debrief** (out of character):
  1. "You'll see hello printed, then the prompt comes back." and the first-three-screens run before typing are what cost the one reading point.
  2. The 2.4 line "~    your home folder" and the Q2 answer check disagree about "your home folder"; the hint sentence "It is where cd with nothing after it takes you." does not bridge them.
  3. Q3's answer depends on "Predict before you act. In ~/projects, cat notes.txt reads ~/projects/notes.txt." which sits in a paragraph whose first sentence carries nothing.
  4. The gate task sentence "make a folder called practice (inside this stage's folder)" asks for something no lesson in Stage 1 or 2 introduced.
  5. "I will check that the folder exists, and how you got there." gave no help at the shell prompt after two rejections.
