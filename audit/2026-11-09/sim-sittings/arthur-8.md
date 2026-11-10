# Synthetic walkthrough: arthur-8

## Sitting

- Date: 2026-11-10
- Persona (file in `docs/sim-personas/`) and learner role: `arthur.md`, Arthur, 64, retired logistics manager, `dos-literalist`; adult with some shell
- Persona sheet version: 0.2.0
- Scripted errors performed: none scripted. DOS habits played where a screen invited them (table below).
- Turn cap: 240 (round 8). One turn = one `send` or one `raw`. Turns used: 196 (the bundle's `persona_inputs`)
- Simulation rules confirmed (zero forward knowledge, reading limit, friction meter): yes. Arthur reads every line; density charge only when a long screen's content later causes a rejection or wrong turn; +2 per rejection he does not understand; -1 per gate; quit at 8. Silent commands verified with ONE check.
- Tutor revision and invocation: `35b9e26` (script `7e01410`); `sitting.py start` with no `--arg` (welcome screen), Bash `/opt/homebrew/bin/bash` 5.3.20
- `--info` lines the persona was shown, if any: none

## Per screen (condensed: one block per screen; the full exchange is in the bundle's `terminal.jsonl`/`events.jsonl`, not committed)

Reading: all lines read on every screen; nothing skimmed. No screen produced a density charge. Login name written as `[user]`.

### welcome / Orientation / Stage 1 intro
- **Jargon**: none stalled. "real shell prompt" accepted at face value.
- **Monologue**: Five stages, a practice folder; next, next, next.
- **Input** `[nav]` next x3 -> accepted.
- **Friction**: 0.

### 1.1 Running a command
- **Jargon**: the `#` comment text in the examples; he leaves it off.
- **Input** `[bash]` `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` -> all printed as the screen said; `[nav]` next.
- **Ladder rung**: none. **Friction**: 0.

### 1.2 Four keys
- **Input** `[bash]` raw `echo p\t` -> prompt line became `echo poem.txt`; `""` (Enter) -> `poem.txt`; raw up arrow -> `echo poem.txt` back; raw Ctrl+C -> `^C`, fresh prompt; raw Ctrl+L -> screen cleared; `[nav]` `show` -> lesson returned; next.
- **Interpretation**: Tab "finished" a name he never typed in full; felt like DOS wildcard magic. Not a rejection.
- **Friction**: 0.

### 1.3 Where am I, who am I, when is it
- **Jargon**: pwd output begins with `/` and no drive letter: "Where is the drive? No C: in front." (his trigger; the screen did not answer it, 2.2 `ls /` did partially).
- **Input** `[bash]` `pwd`, `whoami`, `date` -> output as taught; next.
- **Friction**: 0.

### 1.4 The shell, caught in the act
- **Jargon**: "terminal → shell → program: the window, bash, and date." (stalled: which word is which; no earlier screen defined "terminal" or "shell").
- **Input** `[bash]` `date`, `dtae` -> `bash: dtae: command not found` (matches the screen); next.
- **Friction**: 0 (understood the error; the stall is an observation).

### 1.5 Who else types here
- **Monologue**: three habits, sensible. **Input** `[nav]` next. **Friction**: 0.

### Stage 1 gate (task screen)
- Recall (see table) accepted at first attempt on all three; task and follow-ups accepted at first attempt. **Friction**: -1 -> -1.

### Stage 2 intro, 2.1 Where you are
- **Input** `[bash]` `pwd` -> matched the tree's top line; next. **Friction**: -1.

### 2.2 What is here
- **Jargon**: after `ls -a`, the names `.` and `..` appeared; no screen had defined them ("the screen did not say what those two are"). `ls /` showed names with no drive letter ("Where is C:?").
- **Input** `[bash]` `dir` (habit) -> `bash: dir: command not found`; `ls`; `ls -p`; `ls -a`; `ls /`; next.
- **Interpretation of `dir` reply**: understood (same message as `dtae`; the screen named `ls`). 0.
- **Friction**: -1.

### 2.3 Moving
- **Input** `[bash]` `cd..` (habit, the screen warned) -> `bash: cd..: command not found`, understood; `cd ..` -> silent; check `pwd` -> one level up; `cd -` -> printed the old place.
- **Friction**: -1.

### 2.4 Home and back
- **Jargon**: "~ is its short name." (not shown in use until 2.5)
- **Input** `[bash]` `cd` (silent), check `pwd` -> `.../shelltutor-sim-userhome-...`; `cd /var/folders/.../shelltutor-sim-home-...` (silent; line wrapped on screen), check `pwd` -> practice folder. Each silent command got one `pwd`.
- **Friction**: -1.

### 2.5 Names for places
- **Input** `[bash]` `cd stage1` (silent), check `pwd`; `ls ..`; `cd ..\stage2` (habit: backslash) -> `bash: cd: ..stage2: No such file or directory`; `cd ..` (silent), check `pwd`; `echo ~` -> home path.
- **Interpretation of backslash reply**: the backslash vanished and two names ran together; the screen had said "never \", so he took it as his error. 0 (he understood; wording noted below).
- **Friction**: -1.

### 2.6 Making a folder
- **Input** `[bash]` `mkdir demo` (silent), check `ls -p`; `cd demo` (silent), check `pwd`; next. **Friction**: -1.

### Stage 2 gate
- Recall: three accepted at first attempt. Task: `pwd`, `mkdir practice`, check `ls -p`, `cd practice`, `pwd`, `check` -> cleared. **Friction**: -2.

### Stage 3 intro, 3.1 Making files
- **Input** `[bash]` `touch hello.txt`, `echo hi > words.txt`, `mkdir notes` (all silent), one check `ls -p`. Noted: the intro says "a few files the tutor put there" but `ls -p` showed only his three files.
- **Friction**: -2.

### 3.2 Reading a file
- **Input** `[bash]` `type words.txt` (DOS habit) -> `bash: type: words.txt: not found`.
- **Interpretation**: "Not found?! I made words.txt a minute ago." He did not understand it (different from "command not found"; it names his file). **+2 -> friction 0.** He recovered with the screen's `cat words.txt` -> `hi`; `cat hello.txt` -> nothing (empty, as the screen said); `cat ../poem.txt` -> poem.
- **Ladder rung**: none.

### 3.3 Reading a long file
- **Input** `[bash]` `less ../numbers.txt`; raw space (paged to 46); raw `q` -> prompt back; next. No `b` tried (the task list did not ask). **Friction**: 0.

### 3.4 Copy and move
- **Input** `[bash]` `copy hello.txt backup.txt` (habit) -> `bash: copy: command not found`, understood, 0; `cp hello.txt backup.txt` (silent), check `ls -p`; `mv hello.txt hi.txt` (silent), check `ls -p`; `mv hi.txt notes/` (silent), check `ls -p notes` -> `hi.txt`. **Friction**: 0.

### 3.5 Removing
- **Input** `[bash]` `ls`; `del backup.txt` (habit) -> `bash: del: command not found`, understood, 0; `rm backup.txt` (silent), check `ls` -> gone. **Friction**: 0.

### Stage 3 gate
- Recall Q2 rejected once (see table, F-1): **+2 -> 2.** Task: `pwd`, `echo hello > notes.txt` (check `cat notes.txt` -> hello), `cp notes.txt backup.txt` (check `ls`), `mv notes.txt done.txt` (check `ls`), `rm backup.txt` (check `ls`), `check` -> cleared. **-1 -> 1.**

### Stage 4 intro, 4.1 The parts of a command
- **Jargon**: "A command line is a name, then options, then arguments." and `wc -l poem.txt  # name wc, option -l, argument poem.txt` (wc and -l not explained until 4.3; the output `4 poem.txt` was a guess).
- **Input** `[bash]` `wc -l poem.txt`, `echo "hello world"`, `command -v vim` -> `/usr/bin/vim`. **Friction**: 1.

### 4.2 Spaces and quotes
- **Input** `[bash]` `touch my notes.txt` (silent), check `ls` -> `my`, `notes.txt`; `touch "my notes.txt"` (silent), check `ls` -> one file with a space. **Friction**: 1.

### 4.3 The pipe
- **Jargon**: "What a command prints is a stream of lines." (stream not defined); wc -l now explained.
- **Input** `[bash]` `seq 1 100 | wc -l` -> 100; `ls /usr/bin | wc -l` -> 932; `ls /usr/bin | sort | head` -> ten names, capitals first. **Friction**: 1.

### 4.4 Into a file / 4.5 Pipe, then file
- **Input** `[bash]` `echo first > greeting.txt`, `echo second >> greeting.txt` (silent), check `cat greeting.txt` -> two lines; `ls /usr/bin | wc -l > count-of-programs.txt` (silent), check `cat count-of-programs.txt` -> 932. **Friction**: 1.

### 4.6 Many names at once
- **Monologue**: a star, like DOS `*.txt`; he knows this one. **Input** `[bash]` `ls *.txt`, `wc -l *.txt`. **Friction**: 1.

### Stage 4 gate
- Recall accepted at first attempt x3. Task: `seq 1 100 | wc -l > count.txt` (check `cat count.txt` -> 100), `ls *.txt`, `check` -> cleared. **-1 -> 0.**

### Stage 5 intro, 5.1 Programs that take over the screen
- **Jargon**: "After this stage comes vimtutor." (vimtutor undefined).
- **Input** `[bash]` `man ls` (dense page; not read in full, he pressed q as told: stated skip is the man page body), raw `q`. **Friction**: 0.

### 5.2 Leaving Vim
- **Input** `[bash]` `command -v vim`; `vim` (splash with tildes); `:q` + Enter -> prompt. "<Enter> means the key, not letters" was read and obeyed. **Friction**: 0.

### 5.3 The copy and the file
- **Monologue**: like a Word working copy; save is `:w`. next. **Friction**: 0.

### 5.4 Throw it away / 5.5 Keep it
- **Input** `[bash]` `vim practice.txt`, raw `i`, raw `abc`, raw Esc, `:q!` ; `cat practice.txt` -> `before`. Then again with `xyz` and `:wq`; `cat` -> `xyzbefore`.
- **Observation**: after Esc the bottom line still read `-- INSERT --` (the last rendered line did not change). He could not tell whether Esc had worked ("Did it do it?"), trusted the next instruction, no friction because the result matched.
- **Friction**: 0.

### 5.6 vimtutor
- **Input** `[bash]` `command -v vimtutor` -> `/usr/bin/vimtutor`; next. **Friction**: 0.

### Stage 5 gate
- Recall Q3 rejected three times, then accepted (see table, F-2): **+6 -> 6.**
- Task phase 1: `cat practice.txt`, `vim practice.txt`, i, `qqq`, Esc, `:q!`, `cat` -> `before`, `check`. Phase 2: `vim`, i, `edit`, Esc, `:wq`, `cat` -> `editbefore`, `check` -> finale. **-1 -> 5.**

## Per gate

Recall answers (verbatim; all fifteen questions; sentences in Arthur's words):

| # | Gate / question | Answer typed | Result |
| --- | --- | --- | --- |
| 1 | S1 Q1, character that ends a normal prompt | An ordinary bash prompt usually ends with the dollar sign | accepted |
| 2 | S1 Q2, what does pwd print | It tells you the directory you are presently in | accepted |
| 3 | S1 Q3, where does whoami output go | Its output goes onto the screen where I can read it | accepted |
| 4 | S2 Q1, what does cd .. do | It moves you up one level into the folder that contains the one you are standing in | accepted |
| 5 | S2 Q2, what does ~ mean | The tilde is a short name that stands for your own personal home folder | accepted |
| 6 | S2 Q3, in ~/projects, cd notes | You would be standing in the notes folder inside projects, which is ~/projects/notes | accepted |
| 7 | S3 Q1, command that creates an empty file | The touch command makes a new empty file | accepted |
| 8 | S3 Q2, after rm important.txt where is the file | first: The file is removed permanently because there is no Trash to recover it from | rejected (hint: "Lesson 3.5: what rm does, and whether it can be undone.") |
| 8b | same | second: The file is gone and cannot be brought back | accepted |
| 9 | S3 Q3, single command that renames old.txt to new.txt | You would type mv old.txt new.txt to rename it | accepted |
| 10 | S4 Q1, what does command -v vim print | It prints the location of the vim program, the folder path where it lives | accepted |
| 11 | S4 Q2, difference between > and >> | The single arrow wipes out the old contents of the file, while the double arrow adds new text after what is already there | accepted |
| 12 | S4 Q3, why does vim my notes.txt open two files | Because the shell breaks the line apart at the space, so my and notes.txt are treated as two separate names | accepted |
| 13 | S5 Q1, how do you exit man ls | You leave the manual page by pressing the letter q on the keyboard | accepted |
| 14 | S5 Q2, what makes Vim write the edit | You have to write the working copy back to the file, which the colon w command does | accepted |
| 15 | S5 Q3, :q! then did the file change | try 1: No, the file on disk stayed exactly as it was, because the changes were thrown away | rejected |
| 15 | same | try 2: No, it did not change, because I never wrote the copy back | rejected |
| 15 | same | try 3: No, the file on disk is unchanged | rejected |
| 15 | same | try 4 (bare, after three rejections): No | accepted |

- Rung: the same hint was shown after each rejection of S5 Q3 ("Lesson 5.4: the working copy is a copy; the disk only changes when you write it.") and did not resolve the confusion; the identical wording three times told him nothing about what was missing. From the second rejection the screen also showed "Passed stages are saved. Type quit to leave now; the next run starts this stage from its first lesson."
- Tasks: all five tasks passed on the first `check`. First-check results per gate task (his one check after each silent step, all matching the intended result):
  - S1: no silent step; follow-up answers (username `[user]`, full path, `Tue`) accepted first time.
  - S2: `mkdir practice` -> `ls -p` showed `practice/`; `cd practice` -> `pwd` ended `/stage2/practice`.
  - S3: `echo hello > notes.txt` -> `cat` showed `hello`; `cp` -> `ls` showed both; `mv` -> `ls` showed `done.txt`; `rm` -> `ls` showed `done.txt  notes  words.txt`.
  - S4: `seq 1 100 | wc -l > count.txt` -> `cat count.txt` showed `100`; `ls *.txt` listed the files.
  - S5: phase 1 `:q!` -> `cat` showed `before`; phase 2 `:wq` -> `cat` showed `editbefore`.
- Cleared: Stages 1 to 5 cleared.

DOS habits performed:

| Screen | Input | Reply | Recovery | Friction |
| --- | --- | --- | --- | ---: |
| 2.2 | `dir` | `bash: dir: command not found` | `ls` (named on the screen) | 0 |
| 2.3 | `cd..` | `bash: cd..: command not found` | `cd ..` | 0 |
| 2.5 | `cd ..\stage2` | `bash: cd: ..stage2: No such file or directory` | `cd ..` | 0 |
| 3.2 | `type words.txt` | `bash: type: words.txt: not found` | `cat words.txt` (screen) | +2 |
| 3.4 | `copy hello.txt backup.txt` | `bash: copy: command not found` | `cp` | 0 |
| 3.5 | `del backup.txt` | `bash: del: command not found` | `rm` | 0 |

`cls` was not typed: Ctrl+L on 1.2 cleared the screen and no later screen invited it. Looking for a drive letter happened at 1.3 (`pwd`) and 2.2 (`ls /`) as a stall, not an input.

## End of sitting

- Final friction: 5 at the finale (not a quit; the sitting ended at the finale `[exited 0]`).
- Friction by source: rejections 5 x 2 = +10 (`type words.txt`; S3 Q2 once; S5 Q3 three times); reading-limit/density charges 0; mode confusion 0; gates cleared 5 x -1 = -5. Total 5. Trajectory: -1, -2, 0 (3.2), 2 (S3 recall), 1, 0, then 6 (S5 recall), 5.
- Stages or module cleared: Stages 1 to 5, finale reached.
- Equivalent human sitting time (estimate): about 50 to 70 minutes at Arthur's careful pace, including about 8 minutes lost to the Stage 5 recall loop and the stalls at 1.4, 2.2, 3.2.
- Candidate F-nnn:
  - **Candidate F-1** (valid answer rejected). Screen S3 gate Q2 "After rm important.txt, where is the file?" (options `~/.Trash on disk gone depends`). Input `The file is removed permanently because there is no Trash to recover it from` was rejected ("not quite. hint: Lesson 3.5..."); `The file is gone and cannot be brought back` accepted. Semantically the first answer is correct and matches the lesson ("rm removes a file at once and for good").
  - **Candidate F-2** (valid answers rejected, hint did not resolve). Screen S5 gate Q3 "If you open notes.txt in vim, type some letters, and quit with :q! - did the file on disk change?". Rejected inputs, verbatim: `No, the file on disk stayed exactly as it was, because the changes were thrown away`; `No, it did not change, because I never wrote the copy back`; `No, the file on disk is unchanged`. Accepted: `No`. Three correct full-sentence answers rejected with the identical hint.
  - **Candidate F-3** (dead-end wording, possible false impression). Screen 3.2, input `type words.txt` -> `bash: type: words.txt: not found`; the message says the just-created file is "not found", which on screen reads as the file being lost.
- Candidate O-nnn:
  - **Candidate O-1** (jargon). Screen 1.4: "terminal → shell → program: the window, bash, and date." The words terminal and shell are used as if known.
  - **Candidate O-2** (undefined terms before use). Screen 2.2 `ls -a` output lists `.` and `..`; they are first defined on 2.5 ("`.` here, the current directory `..` one level up").
  - **Candidate O-3** (backslash feedback). Screen 2.5, input `cd ..\stage2` -> `bash: cd: ..stage2: No such file or directory`; the reply drops the backslash and does not say why.
  - **Candidate O-4** (stage intro vs state). Screen Stage 3 intro / 3.1: "This stage runs in its own folder, stage3, with a few files the tutor put there" but `ls -p` in stage3 showed only the files he had made. (Stages 4 and 5 did have tutor files.)
  - **Candidate O-5** (jargon before definition). Screen 4.1: "`wc -l poem.txt  # name wc, option -l, argument poem.txt`" shows wc and -l with no explanation until 4.3.
  - **Candidate O-6** (undefined word). Screen 4.3: "What a command prints is a stream of lines." and 5.1 / Stage 5 intro: "After this stage comes vimtutor."
  - **Candidate O-7** (ambiguity). Screens 5.4, 5.5, phase 2: after the Esc raw key the last rendered line still read `-- INSERT --` ("i -- INSERT --abcbefore"), so mode could not be seen to change. May be a harness rendering effect; recorded as seen.
  - **Candidate O-8** (pace/ladder). Screen S5 gate Q3: the same hint text three times in a row for three different wrong-looking answers.
  - **Candidate O-9** (ambiguity). Screen S5 gate Q3 grading: bare `No` passes, three explanatory sentences do not; the question does not say a one-word answer is wanted. Screen S1 gate had asked for "words".
- Debrief (out of character):
  - The recall check at S3 Q2 and S5 Q3 rejected answers that say the same thing as the lesson in different words; "Type your answer in words" invites sentences, and only the bare "No" passed.
  - The Stage 5 hint "the working copy is a copy; the disk only changes when you write it" did not change on repeats, so three attempts moved nothing until the answer was shortened.
  - "terminal → shell → program: the window, bash, and date" (1.4) and "stream of lines" (4.3) use terms no earlier screen defined; `.` and `..` appear in `ls -a` (2.2) three lessons before 2.5 names them.
  - `bash: type: words.txt: not found` reads as the file missing, unlike `command not found`; `bash: cd: ..stage2: No such file or directory` hides the backslash that caused it.
  - "with a few files the tutor put there" (Stage 3 intro) did not match what `ls -p` showed.
