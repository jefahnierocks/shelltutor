# Synthetic walkthrough — Maya, sitting 3

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/maya.md` (Maya, 19, `search-first-skimmer`); learner role: adult beginner
- Persona sheet version: 0.2.0
- Simulation rules confirmed: zero forward knowledge, reading limit (four prose lines; bold and `▶` lines always read; the +1 reading charge applies only at the later turn where a skipped line causes a rejection or wrong turn), friction meter (+2 rejection not understood, +1 mode confusion, -1 gate cleared, quit at 8).
- Tutor revision: 7204741 (script 5d1d689). Invocation: `sitting.py start`, no `--arg` (begins at the welcome screen), Bash `/bin/bash` 3.2.57. Third Maya sitting; no memory of earlier ones.
- `--info` lines shown: none.
- Process note: three early turns (1.1 `echo hello`, and 1.2 `echo p` + Tab sent back to back) issued note and send/raw in adjacent calls rather than strictly separated; the tutor-side events are unaffected. All later turns follow the protocol.
- Login name appears on screen; written here as `[user]`.

## Per screen (compact; navigation-only screens grouped)

### welcome / orientation / Stage 1 intro — next x3
- **Read**: skimmed (orientation: skipped the middle; read the `▶` line). **Jargon**: "a vimtutor prerequisite course", "keyboard-only; you can't click mid-line to move the cursor".
- **Monologue**: "Black app, vimtutor, whatever. It says type next."
- **Input** [nav] `next` x3 → accepted. **Ladder**: none. **Friction**: 0.

### 1.1 — running commands
- **Read**: skimmed (skipped "If bash says command not found…" and "echo just repeats…"). **Jargon**: "the shell runs it".
- **Input** [bash] `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` → output seen each. [nav] `next`. **Friction**: 0.

### 1.2 — keyboard habits
- **Read**: skimmed; tried only Tab. **Jargon**: "bash finishes a word", "the escape hatch".
- **Input** [bash] `echo p` (raw), Tab (raw `\t`) → `echo poem.txt`; Enter → `poem.txt`. [nav] `next`. Did not try Up, Ctrl+L, Ctrl+C. **Friction**: 0.

### 1.3 — where am I, who am I, when is it
- **Read**: skimmed (skipped "Your prompt here ends in >. A normal bash window's prompt usually ends in $"). **Input** [bash] `whoami`, `pwd`, `date` → output seen. `next`. **Friction**: 0.

### 1.4 / 1.5
- 1.4 [bash] `dtae` → `bash: dtae: command not found`, as the screen said; understood. 1.5 skipped ("AI talk"). `next` x2. **Friction**: 0.

### Stage 1 gate
- Q1 `$` accepted (a guess she half-recalled, not a known-wrong guess); Q2 `the folder you are in` accepted; Q3 `back to me on the screen` accepted. Task: `whoami`, `pwd`, `date`, `check`; follow-ups `[user]`, full path, `Mon` accepted. **Cleared.** Friction -1 (running total -1).

### 2.1 – 2.4 (Stage 2 lessons)
- 2.1 `pwd`; 2.2 `ls -p`, `ls /`; 2.3 `cd ..`, `pwd`, `cd -` (followed the `▶` line; skipped the `cd..` and "cd on its own" prose, with no consequence); 2.4 `next` (no commands on the screen). **Friction**: -1.

### Stage 2 gate — Recall
- Q1 `goes up one folder` accepted. Q2 `your home folder` → "not quite. try again." with hint "It is where cd with nothing after it takes you." Her answer was the words from 2.4 ("~ your home folder"). She did not understand the rejection. **+2 (total 1).** Retry `home` → accepted; ladder rung: hint, which she did not use (she shortened the answer by guess). Q3 `~/projects/notes` accepted.
- Task (make `practice`, cd, pwd): the lessons never named `mkdir`. Guess `new folder practice` → `bash: new: command not found` (known guess, 0). `check` listed only "○ cd into it (cd practice) not yet: not in your history". `cd practice` → `No such file or directory` (understood, 0). Guess `make folder practice` → `make: *** No rule to make target `folder'.  Stop.` Unreadable; **+2 (total 3)**. `show` → same task text. `help` → a wall of builtin signatures with no mkdir (not a rejection, 0; noted). Guess `create practice` → command not found (0). Second `check` → "○ practice folder not yet… Hint: mkdir makes the folder; cd moves into it; pwd shows where you are." (ladder: hint; copied). `mkdir practice`, `cd practice`, `pwd` → `…/stage2/practice`, `check` → Stage 2 cleared. **-1 (total 2).**

### Stage 3 intro / 3.1
- Intro lists `mkdir   create a folder` (first appearance of mkdir, after the Stage 2 gate needed it). 3.1 [bash] `touch hello.txt`, `mkdir notes`, `ls` → `hello.txt  notes`. Friction 2.

### 3.2 — reading: cat, less
- **Read**: skimmed. Four prose lines read ended at "Inside less, the screen takes over. Press Space"; skipped "or f to page down, b to page back, and q to exit" and the "Important: … q returns you to the shell." paragraph.
- Input [bash] `cat hello.txt`, `cat ../poem.txt`, `less ../numbers.txt` → full-screen pager, no shell prompt.
- Stuck in `less`. [nav, believed] `next` → the keystrokes went to `less` ("No previous regular expression", "No next tag"). **Mode confusion +1 (total 3).** [nav, believed] raw Ctrl+C → still in `less`. [nav, believed] `quit` → `q` left `less`, then `bash: uit: command not found`. **Mode confusion +1 (total 4).** **Reading charge +1 (total 5)**, at this turn, for the skipped sentence "q to exit" (and "q returns you to the shell"). Left `less` by accident.

### 3.3 — copy, move, delete
- Skimmed; the `▶` line says only `next`, so she did not try cp/mv/rm. `next`. Friction 5.

### Stage 3 gate
- Recall: Q1 `touch` accepted; Q2 `gone` accepted; Q3 `mv old.txt new.txt` accepted. Task: `echo hello > notes.txt` (copied the shape from 3.1's redirection example), `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt`, `check` → Stage 3 cleared. **-1 (total 4).**

### Stage 4 intro, 4.1 – 4.4
- 4.1 [bash] `command -v vim` → `/usr/bin/vim`. 4.2 `ls /usr/bin | wc -l` → 932. 4.3 `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt` → two lines. 4.4 `next` without trying anything. Friction 4.

### Stage 4 gate — Recall Q1 ("What does command -v vim print, if Vim is installed?")
- Input [recall] `the path /usr/bin/vim` → "not quite. try again." Hint: "It answers with the folder and name of the program file." She had just seen exactly `/usr/bin/vim`. **+2 (total 6).**
- Input [recall] `the folder and name of the program file` (the hint's own words) → "not quite. try again." + hint + "Answer in a few words, like the lesson did, not a full sentence." + a block "Passed stages are saved. Type quit to leave now; the next run starts this stage from its first lesson. Type show to see the question again." **+2 (total 8).**
- Input [recall] `show` → echoed as an answer line, question redisplayed; no further charge. **QUIT at 8, Stage 4 gate Q1.**

## Per gate

- Stage 1: recall 3/3, no rejections; task cleared first try. Cleared.
- Stage 2: recall Q2 rejected once ("your home folder"), hint rung used by shortening to "home"; task: 3 wrong guesses, 2 `check` calls, `mkdir` surfaced only in the second `check` hint; `○` marked: first "cd into it", then "practice folder". Cleared.
- Stage 3: recall 3/3; task done in order, first `check`. Cleared.
- Stage 4: recall Q1 rejected twice (hint copied verbatim, also rejected). Not cleared.

## End of sitting

- Final friction **8**; quit at Stage 4 gate, Q1 (`command -v vim`).
- By source: rejections not understood 8 (Stage 2 Q2 +2, Stage 2 task `make folder practice` +2, Stage 4 Q1 twice +4); mode confusion +2 (`next`, `quit` typed into `less`); reading charges +1 (3.2 skipped "q to exit"); gates cleared -3 (Stages 1, 2, 3). 8 + 2 + 1 - 3 = 8. (Sum is unfloored; the running total never went below -1.)
- Stages cleared: 1, 2, 3 (Stage 4 lessons seen, gate not passed).
- Equivalent human sitting time: roughly 30 to 40 minutes (estimate from about 85 turns, a three-guess stall at the Stage 2 task and a `less` stall).
- Density notes (no friction): 3.2 and 2.3 screens exceed her four-line limit; the Stage 3 intro and Stage 4 intro (command lists) were long but not charged.

### Candidate F-nnn
- **F-a** Stage 4 gate Q1. Input `the path /usr/bin/vim`, then `the folder and name of the program file`, both rejected for a question whose answer she had just seen on screen. The second input is the hint's own words, so the hint cannot be used as given.
- **F-b** Stage 2 gate recall Q2. Input `your home folder` rejected; the 2.4 screen says "~ your home folder". The accepted answer was `home`.
- **F-c** Stage 2 gate task. `mkdir` is not taught before the task that needs it (Stage 2 lessons; first appears at the Stage 3 intro), and the first `check` marks only "cd into it", not the missing folder. A dead end for a learner with zero forward knowledge.
- **F-d** Stage 4 gate recall, `show`. The recall prompt said "Type show to see the question again"; typing `show` was echoed as an answer line ("answer in words: show"). Needs reproducing to see if it counted as an attempt.

### Candidate O-nnn
- **O-a** Stage 2 gate task, input `make folder practice` → `make: *** No rule to make target `folder'.  Stop.` A real macOS program answered; the message is unreadable to her.
- **O-b** Stage 2 gate task, input `help` → a full page of bash builtin signatures with no `mkdir`; a dead end that looks like help.
- **O-c** 3.2 — "Inside less, the screen takes over. Press Space / or f to page down, b to page back, and q to exit." The exit key sits in the fifth prose line; the `▶` line ("Try both, then next") does not mention it. She entered `less` without the exit key. Inputs `next`, raw `\x03`, `quit` (mode confusion).
- **O-d** 1.2 — "Ctrl+C the escape hatch. If anything feels stuck, press it and you get a fresh prompt." Inside `less` it did nothing; the sentence is untrue there.
- **O-e** 3.3 — `▶ Type next to take Stage 3's gate.` with no practice prompt to try cp, mv or rm; she arrived at the gate task without having typed them.
- **O-f** Stage 4 gate hint, "Answer in a few words, like the lesson did, not a full sentence." The lesson gave no answer-format example.
- **O-g** 2.1 vs gate — the 2.1 tree says "you are here" at the practice root, while the Stage 1 task `pwd` printed `…/stage1`; the Stage 2 task prompt was in `…/stage2`. Positions shift between screens.

## Debrief (out of character)

- Stage 4 Q1: the hint "It answers with the folder and name of the program file." is what she retyped; "Answer in a few words, like the lesson did, not a full sentence." came after the second miss.
- Stage 2 task: "1. make a folder called practice (inside this stage's folder)" with no `mkdir` anywhere earlier; the first `check` line "○ cd into it (cd practice) not yet: not in your history".
- Stage 2 Q2: the question "What does ~ mean in a path?" against the lesson line "~   your home folder".
- 3.2: "Inside less, the screen takes over. Press Space or f to page down, b to page back, and q to exit." placed after the "Try both" example, with the exit key in the skipped part.
- 1.2: "Ctrl+C the escape hatch. If anything feels stuck, press it and you get a fresh prompt."
