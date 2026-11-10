# Synthetic walkthrough — arthur-shells-8 (module `shells`)

## Sitting

- Date: 2026-11-10
- Persona (file in `docs/sim-personas/`) and learner role: `arthur.md`, Arthur, 64, `dos-literalist`; adult with some shell. Background: finished the five-stage course last week (knows ls, cd, pwd, echo, `>`, next, prev, show, quit, check); does not know "shell" as distinct from the window.
- Persona sheet version: 0.2.0
- Scripted errors performed: none
- Turn cap: 70 (stated for this sitting; sheet template says 160). One turn = one `send` or one `raw`. Turns used: 15
- Simulation rules confirmed (zero forward knowledge, reading limit, friction meter): yes. Reads every line; density charge only if a long screen later causes a rejection or wrong turn; quit at 8.
- Tutor revision and invocation: 35b9e26 (script 7e01410); `sitting.py start --arg shells`, Bash `/bin/bash` 3.2.57.
- `--info` lines the persona was shown, if any: none

## Per screen

### Module entry — shells: what runs your commands

- **Read**: all.
- **Jargon or assumed concept**: "You'll look at the shell as a program, at other shells, and at the difference between your login shell and this one."
- **Monologue**: I thought the shell was the window. "Login shell" is new. It says type next.
- **Input** `[nav]` → `next` → accepted.
- **Interpretation**: Fine.
- **Ladder rung shown**: none.
- **Friction**: 0.

### Lesson 1/3 — The shell is a program

- **Read**: all.
- **Jargon or assumed concept**: "$$ is its number." ; "echo $BASH_VERSION" and "ps -p $$ -o pid,comm" (what `$`, `pid`, `comm`, `-p`, `-o` are is never said; "its number" is only partly explained).
- **Monologue**: Two commands with dollar signs. The # part looks like a note; I leave it off and type only the command. It tells me what the second one prints before I run it, which helps.
- **Input** `[bash]` → `echo $BASH_VERSION` → printed 1 line (`3.2.57(1)-release`). No claim on screen about this one.
- **Input** `[bash]` → `ps -p $$ -o pid,comm` → printed 2 lines: a heading and one row (number, name `/bin/bash`). Matches the screen: "prints a heading and one row: a number and a name. The name ends in bash."
- **Interpretation**: A version number, and the shell as a running thing with a number. One sentence: the shell is a program that is running, with its own number, and mine is bash.
- **Ladder rung shown**: none.
- **Friction**: 0.

### Lesson 2/3 — Other shells exist

- **Read**: all.
- **Jargon or assumed concept**: "ls, paths and pipes are the same in all of them." (pipes never defined); "What differs between shells is setup and prompt."
- **Monologue**: zsh, fish: other programs of the same kind. "No line for a shell means it is not installed" is reassuring about silence. Pipes: skip it.
- **Input** `[bash]` → `command -v zsh fish` → printed 2 lines, one path each. Matches "one path for each that is installed" (both were installed).
- **Interpretation**: One sentence: there are several shells, they are separate programs, and this command asks where each one is.
- **Ladder rung shown**: none.
- **Friction**: 0.

### Lesson 3/3 — Your login shell and this shell

- **Read**: all.
- **Jargon or assumed concept**: "Your login shell is the one a new terminal window starts." (terminal window vs shell now distinguished here, but "login" never explained beyond that).
- **Monologue**: So my window starts zsh but the tutor runs bash. Two shells at once.
- **Input** `[bash]` → `echo $SHELL` → printed 1 line (`/bin/zsh`).
- **Input** `[bash]` → `echo $BASH_VERSION` → printed 1 line (`3.2.57(1)-release`).
- **Interpretation**: Compared the lines: different shells. One sentence: the shell my window starts is not necessarily the shell running the lesson. No count claims on screen; none mismatched.
- **Ladder rung shown**: none.
- **Friction**: 0.

### Gate — Recall (3 questions)

- **Read**: all.
- **Jargon or assumed concept**: none new.
- **Monologue**: Q1 choices include "a window", my old answer; lesson 1 said program. Q2 I adapt `command -v zsh fish` to one name. Q3 `$SHELL` gave my window's shell.
- **Input** `[recall]` → `a program` → accepted. `[recall]` → `command -v zsh` → accepted. `[recall]` → `your login shell` → accepted.
- **Interpretation**: Fair questions.
- **Ladder rung shown**: none.
- **Friction**: -1 (gate cleared, three first-try answers) → -1.

### Task

- **Read**: all.
- **Jargon or assumed concept**: "Send what it prints into a file named zsh.txt." (I read this as the `>` from the course.) "This task runs in the module's own folder; pwd shows it."
- **Monologue**: Step 1 is the command I know; step 2 is `>`. I do both in one line. Silent, but the course taught me that.
- **Input** `[bash]` → `command -v zsh > zsh.txt` → no output.
- **Input** `[nav]` → `check` → "shells cleared."
- **Interpretation**: Done.
- **Ladder rung shown**: none.
- **Friction**: -2.

### Cleared screen — shells cleared.

- **Read**: all. Summary list of four commands.
- **Input** `[nav]` → `quit` → "Bye. A module saves nothing; run 'shelltutor shells' to start it again." `[exited 0]`.
- **Friction**: -2 (final).

## Per gate

- Recall: one attempt per question, no rejections, no rung reached.
- Task: 1 attempt; `check` result verbatim: "shells cleared." followed by the commands list; checklist `○` never shown.
- Cleared.

## End of sitting

- Final friction: -2 (rejections 0 x 2 = 0, reading charges 0, mode confusion 0, gates cleared -1 for recall, -1 for task). Did not quit on friction; ended at the module's cleared screen, then `quit`, `[exited 0]`.
- Module cleared: `shells`.
- Line counts versus claims:
  - `echo $BASH_VERSION`: 1 line; no claim.
  - `ps -p $$ -o pid,comm`: 2 lines; claim "a heading and one row": matches. "The name ends in bash": `/bin/bash`, matches.
  - `command -v zsh fish`: 2 lines; claim "one path for each that is installed": matches (both installed).
  - `echo $SHELL`: 1 line; `echo $BASH_VERSION`: 1 line; no claim.
  - `command -v zsh > zsh.txt`: 0 lines; the screen said a file results; no mismatch.
- Equivalent human sitting time: estimate 12 to 15 minutes.
- **Candidate F-nnn**: none.
- **Candidate O-nnn**:
  - O-a. Lesson 2 (screen `shells 2/3`): "ls, paths and pipes are the same in all of them." Pipes were not defined by the five stages' words he knows; he skipped it.
  - O-b. Lesson 1 (screen `shells 1/3`): "$$ is its number." and the `-p`, `-o pid,comm` pieces are unexplained; the lesson works by outcome, not by understanding the flags.
  - O-c. Lesson 1: the `# ...` comment text printed in the code lines is ambiguous for a literalist (type it or not). Arthur omitted it; nothing rejected it either way.
  - O-d. Recall Q2 (screen `shells gate`): "What do you type to ask whether zsh is installed?" differs from the lesson command (`command -v zsh fish`); `command -v zsh` was accepted, no mismatch.
- **Debrief**:
  - The lesson 1 sentence "$$ is its number." is the one place a term is used that no screen defined; "pipes" in lesson 2 is the other.
  - "Your login shell is the one a new terminal window starts." was enough for the recall and task; "login" itself is only defined by that sentence.
  - The `# comment` parts of the printed commands left a literal reader unsure whether to type them.
  - All printed line-count claims were accurate against the real output.
  - Procedure note: the `stop` command was run in the same shell call as a directory listing, once, contrary to the one-command-per-call rule (no effect on the sitting).
