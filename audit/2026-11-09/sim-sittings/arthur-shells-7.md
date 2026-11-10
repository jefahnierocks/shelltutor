# Synthetic walkthrough — arthur-shells-7

## Sitting

- Date: 2026-11-10
- Persona: `docs/sim-personas/arthur.md`, Arthur, 64 (`dos-literalist`); learner role: adult with some shell. Background for this sitting: finished the five-stage course last week; knows ls, cd, pwd, echo, `>` and next/prev/show/quit/check; does not know "shell" as distinct from the window.
- Persona sheet version: 0.2.0
- Scripted errors performed: none (Arthur has none scripted)
- Turn cap: 70 (module sitting). Turns used: 16
- Simulation rules confirmed: zero forward knowledge, reading limit (v0.2: density charge only when a long screen later causes a rejection or wrong turn), friction meter (quit at 8).
- Tutor revision and invocation: 40c11cf (script a7cd1ac); started with `--arg shells`, module `shells`; Bash `/opt/homebrew/bin/bash` 5.3.20
- `--info` lines shown: none

## Per screen

### Module intro — shells: what runs your commands

- **Read**: all.
- **Jargon**: "You'll look at the shell as a program, at other shells, and at the difference between your login shell and this one."
- **Monologue**: I thought the shell was the window. "The shell as a program" is odd but it says type next.
- **Input** `[nav]` → `next` → lesson 1.
- **Friction**: 0.

### Lesson 1/3 — The shell is a program

- **Read**: all.
- **Jargon**: "Two of those lines are shells: the tutor's own, and the one you are typing into." ("variable" is defined on the same screen.)
- **Monologue**: Two shells? I thought one. The grey `#` text looks like a note, so I type only the command.
- **Input** `[bash]` → `echo $BASH_VERSION` → `5.3.20(1)-release`. Matches the aside ("the version of the shell running now").
- **Input** `[bash]` → `ps -o pid,comm` → header plus 96 process rows (counted by hand): the whole machine's processes for this user, many of them shells, some shown with full paths (the listing itself is not copied here). MISMATCH: the aside says "the programs on this terminal, by name"; the screen says "Two of those lines are shells". Output was the whole machine's processes, far more than a terminal's few, and many shell-like lines (more than two).
- **Interpretation**: Did I break something? A hundred lines scrolled past. I cannot tell which two are "the shells". Typed `next` because the screen said so.
- **Could Arthur say in one sentence what the lesson showed?** First half yes ("the shell has a version number"); second half no ("I couldn't find the two shells in the list").
- **Ladder rung**: none.
- **Friction**: 0 (no rejection; no density charge since the long output caused no rejection or wrong turn).
- **Input** `[nav]` → `next`.

### Lesson 2/3 — Other shells exist

- **Read**: all.
- **Jargon**: "What differs between shells is setup and prompt; ls, paths and pipes are the same in all of them." ("pipes" never defined.)
- **Input** `[bash]` → `command -v zsh fish` → `/opt/homebrew/bin/zsh` and `/opt/homebrew/bin/fish`. Matches the aside ("one path for each that is installed").
- **Could say in one sentence?** Yes: bash, zsh and fish are different shell programs and a machine can have several.
- **Friction**: 0.
- **Input** `[nav]` → `next`.

### Lesson 3/3 — Your login shell and this shell

- **Read**: all.
- **Jargon**: "Your login shell is the one a new terminal window starts." (defined here.)
- **Input** `[bash]` → `echo $SHELL` → `/bin/zsh`. Matches the aside ("your login shell").
- **Input** `[bash]` → `echo $BASH_VERSION` → `5.3.20(1)-release`. Matches.
- **Could say in one sentence?** Yes: my window starts zsh but the tutor runs bash.
- **Friction**: 0.
- **Input** `[nav]` → `next`.

### Gate — recall

- **Q1** "The shell runs the programs you name. What kind of thing is the shell itself?" `[recall]` → `a program` → [✓].
- **Q2** "What do you type to ask whether zsh is installed?" `[recall]` → `command -v zsh` → [✓].
- **Q3** "echo $SHELL prints which shell?" `[recall]` → `your login shell` → [✓].
- Gate cleared: friction -1.

### Gate — task

- **Read**: all. Jargon: none new; "Send what it prints into a file" read as the course's `>`.
- **Input** `[bash]` → `command -v zsh > zsh.txt` → silent. He checks: `[bash]` → `ls` → `zsh.txt`. (Arthur trigger: silent command.)
- **Input** `[nav]` → `check` → the "shells cleared." screen, listing four commands, with no separate pass line.
- **Friction**: -2 (task gate cleared).

### Cleared screen

- Lists `ps -o pid,comm the programs on this terminal`, repeating the aside that did not match. `[nav]` → `quit` → "Bye. A module saves nothing; run 'shelltutor shells' to start it again." `[exited 0]`.

## Per gate

- Recall: one attempt per question, no rejected inputs, no rung shown.
- Task: one attempt, one `check`, result verbatim: the cleared screen ("shells cleared."). Nothing marked `○`.
- Cleared.

## End of sitting

- Final friction: -2 (rejections 0; reading charges 0; mode confusion 0; gates cleared -2). No quit; module cleared.
- Module cleared: `shells`.
- Equivalent human sitting time: estimate 10 to 15 minutes (the process list would cost a stall of a minute or two).
- **Candidate F-nnn**
  - F-a. Lesson 1/3, input `ps -o pid,comm`: the screen says "the programs on this terminal, by name" and "Two of those lines are shells", but the output was 96 process rows from the whole machine, many of them shells. Also appears in the cleared screen: "ps -o pid,comm the programs on this terminal". Some rows were full paths under the user's home. (Likely depends on how the sitting server's environment is shared, to be reproduced.)
- **Candidate O-nnn**
  - O-a. Lesson 1/3: "Two of those lines are shells: the tutor's own, and the one you are typing into." The learner cannot tell which lines they are, and Arthur believes one shell exists.
  - O-b. Lesson 2/3: "ls, paths and pipes are the same in all of them." "pipes" is not yet defined in this module (an assumed-knowledge point for a stand-alone module; Arthur had no taught meaning).
  - O-c. Task 2, input `command -v zsh > zsh.txt`: silent; Arthur ran `ls` to confirm, and `check` itself printed no pass line beyond the cleared screen.
  - O-d. Gate recall Q1: the four options (a program / a file / a folder / a window) include "a window", the thing Arthur thought the shell was; he got it right only from lesson 1's sentence "It is itself a program".
- **Debrief** (out of character): the one real damage came from `ps -o pid,comm`, whose output does not match the grey aside and the sentence "Two of those lines are shells". The rest of the module matched its asides. The intro's "the shell as a program" and "Two of those lines are shells: the tutor's own, and the one you are typing into" assume a model (several shells running at once) that nothing before it built. "pipes" in lesson 2 is undefined.
