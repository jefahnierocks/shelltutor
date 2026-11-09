# Synthetic walkthrough: Arthur, sitting 3

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/arthur.md` (Arthur, 64, `dos-literalist`); learner role: adult with some shell
- Persona sheet version: 0.1.0
- Simulation rules confirmed: zero forward knowledge, reading limit (reads every line; +1 for a screen over 14 lines), friction meter (quit at 8)
- Tutor revision: 7204741 (script 5d1d689); `sitting.py start` with no `--arg` (begins at the welcome screen); Bash: /opt/homebrew/bin/bash 5.3.20
- `--info` lines shown: none
- Process note: once, a `note` and a `send` were issued in parallel tool calls (1.1, second echo). The order held (note first); the sheet treats it as normal.

## Per screen

### welcome: SHELLTUTOR, a vimtutor prerequisite course
- **Read**: all (17 lines)
- **Jargon**: "a vimtutor prerequisite course"
- **Monologue**: Long screen. "vimtutor" means nothing to me. It says type next.
- **Input** [nav] `next` accepted.
- **Ladder**: none. **Friction**: 1 (density).

### orientation: Orientation
- **Read**: all (17 lines). **Jargon**: "the practice prompt", "The terminal is keyboard-only".
- **Monologue**: Four words steer it: next, prev, show, quit. A fifth, check, later.
- **Input** [nav] `next` accepted. **Ladder**: none. **Friction**: 2 (density).

### Stage 1 intro
- **Read**: all (short). **Input** [nav] `next` accepted. **Friction**: 2.

### 1.1 running commands
- **Read**: all (16 lines). **Jargon**: "bash says command not found or No such file"; "bash" never introduced here.
- **Monologue**: Try all three. I leave off the # notes.
- **Inputs** [bash] `echo hello` -> hello; `echo I am at the shell` -> printed; `echo "I am at the shell"` -> same. Then [nav] `next`.
- **Interpretation**: The quoted and unquoted lines print the same; I see no difference.
- **Ladder**: none. **Friction**: 3 (density).

### 1.2 keyboard habits
- **Read**: all (14 lines, not over). **Jargon**: "Ctrl+C the escape hatch".
- **Inputs** [bash] raw `echo p\t` -> `echo poem.txt`; raw `\r` -> poem.txt; raw `\x1b[A` -> last line back; raw `\x03` -> ^C fresh prompt; raw `\x0c` -> cleared. [nav] `next`.
- **Ladder**: none. **Friction**: 3.

### 1.3 where am I, who am I, when is it
- **Read**: all (13 lines). **Jargon**: "print working directory"; the pwd path starts with `/` and has no drive letter.
- **Monologue**: Where is the drive? No C:. Stage 2 will say.
- **Inputs** [bash] `whoami` -> [user]; `pwd` -> long path; `date`. [nav] `next`.
- **Ladder**: none. **Friction**: 3.

### 1.4 the shell, caught in the act
- **Read**: all (16 lines). **Jargon**: "terminal -> shell -> program"; "the program named bash".
- **Inputs** [bash] `dtae` -> `bash: dtae: command not found` (asked for, no charge). [nav] `next`.
- **Ladder**: none. **Friction**: 4 (density).

### 1.5 who else types here
- **Read**: all (13 lines). Jargon: "An AI assistant that runs commands". Input [nav] `next`. **Friction**: 4.

### Stage 1 gate (recall and task)
- **Read**: all. Jargon: "this is not the shell".
- Q1 [recall] `$` accepted. Q2 [recall] `the folder you are in` accepted. Q3 [recall] `it comes back to me on the screen` accepted.
- Task [bash] `whoami`, `pwd`, `date`, then `check`. Follow-ups [follow-up]: `[user]`, the full pwd path (typed by hand), `Mon`. All accepted.
- Observation: pwd in the task printed `.../stage1`, while the lesson 1.3 pwd (before the gate) printed the home folder with no `/stage1`. Arthur noticed and moved on.
- **Result**: cleared. **Friction**: 3 (-1 for gate cleared).

### Stage 1 cleared
- Read all. Input [nav] `next`. **Friction**: 3.

### Stage 2 intro
- **Read**: all (17 lines). **Jargon**: "the path symbols"; `~`, `..`.
- Input [nav] `next`. **Friction**: 4 (density).

### 2.1 where you are
- Read all (13 lines). Input [bash] `pwd` -> matches the picture; `next`. **Friction**: 4.

### 2.2 ls: what is here
- **Read**: all (16 lines). **Jargon**: "hidden names: those starting with ."; "the top of everything".
- **Inputs** [bash] `ls -p` -> numbers.txt poem.txt stage1/ stage2/; `ls -a` -> shows . .. .progress .shelltutor_history; `ls /` -> Applications, Users, etc ...; [nav] `next`.
- **Monologue**: No drive letter at the top of everything.
- **Friction**: 5 (density).

### 2.3 cd: moving
- **Read**: all (16 lines). **Jargon**: "cd # your home folder, outside this practice area".
- **Inputs** [bash] `cd ..` (silent) -> `pwd` shows one level up -> `cd -` prints the path back; [nav] `next`.
- **Interpretation**: "Did it do it?" after the silent cd; the screen's own instruction to run pwd answered it. `cd -` did print, unlike `cd ..`.
- **Friction**: 6 (density).

### 2.4 names for places
- **Read**: all (18 lines). **Jargon (stall, sentence)**: "In ~/projects, cat notes.txt reads ~/projects/notes.txt." (cat not taught, ~/projects not in the tree); "Absolute paths start from the root, /:" (root not defined).
- Input [nav] `next`. **Friction**: 7 (density).

### Stage 2 gate
- Q1 [recall] `it goes up one level to the parent folder` accepted.
- Q2 "What does ~ mean in a path?" [recall] `your home folder` -> "not quite. try again." with Hint: "It is where cd with nothing after it takes you." (+2, rejected input not understood).
- **Ladder**: hint (message plus hint); did not resolve the confusion, because the answer typed was the tutor's own wording from 2.4.
- **Friction**: 9. Quit at the Q2 prompt.

## Per gate

- Stage 1: Q1, Q2, Q3 one attempt each, no rejections; task one attempt; cleared.
- Stage 2: Q1 one attempt; Q2 one attempt, rejected `your home folder`, rung reached: hint; not cleared.

## End of sitting

- Final friction: 9, quit at Stage 2 gate Q2 ("What does ~ mean in a path?"). Friction by source: reading (density) charges 8 (welcome, orientation, 1.1, 1.4, Stage 2 intro, 2.2, 2.3, 2.4), rejections 1 x 2 = 2, mode confusion 0, gate cleared -1. Check: 8 + 2 + 0 - 1 = 9.
- Stages cleared: Stage 1 (gate). Stage 2 not cleared.
- Equivalent human sitting time: estimate 25 to 30 minutes.
- **Candidate F-nnn**
  - F-a: Stage 2 gate Q2, input `your home folder`, rejected as "not quite." The phrase is verbatim from 2.4 ("~ your home folder") and 2.3 ("# your home folder"). The hint then describes what he had already said.
- **Candidate O-nnn**
  - O-a: welcome, "a vimtutor prerequisite course": vimtutor is never defined.
  - O-b: density: 8 of 15 learner-facing screens exceed 14 lines (welcome, orientation, 1.1, 1.4, Stage 2 intro, 2.2, 2.3, 2.4); the course reached friction 7 on reading alone.
  - O-c: 2.4, "In ~/projects, cat notes.txt reads ~/projects/notes.txt": cat and ~/projects are not taught or present.
  - O-d: 2.4, "Absolute paths start from the root, /": "root" is not defined.
  - O-e: 1.1, "If bash says command not found or No such file": "bash" not yet introduced; "# spaces separate words" lines are ambiguous as to whether to type the comment.
  - O-f: Stage 1 gate task, pwd printed `.../stage1` whereas lesson 1.3 and 2.1 pwd printed the folder without it; nothing on screen says why the folder changed.
  - O-g: 2.3, "cd # your home folder, outside this practice area": a silent command that leaves the sandbox folder; `cd ..` prints nothing while `cd -` prints a path, which is inconsistent for someone who reads silence as failure.
  - O-h: 1.3 and 2.2, `/` and `ls /` with no drive letter: Arthur looked for one twice; no sentence says there is none.
- **Debrief** (out of character):
  - The gate Q2 rejection is the deciding event: his answer matched the tutor's own words.
  - Reading charges alone brought him to 7 before any recall question in Stage 2.
  - Sentences that stalled him: "a vimtutor prerequisite course"; "In ~/projects, cat notes.txt reads ~/projects/notes.txt."; "Absolute paths start from the root, /:".
  - The drive-letter and silence triggers were answered by the screens' own pwd and "predict" prompts, so they cost no friction.
