# Synthetic walkthrough — maya-7

## Sitting

- Date: 2026-11-10
- Persona: `docs/sim-personas/maya.md`, Maya, 19, graphic design student (`search-first-skimmer`); learner role: adult beginner
- Persona sheet version: 0.2.0
- Scripted errors performed: none scripted for Maya. Habits performed (persona triggers): `touch my notes.txt` unquoted (3.1), `undo` after `rm` (3.5). See "Habits" below.
- Turn cap: 240 (round 7). One turn = one `send` or one `raw`. Turns used: 169 (the client's `persona_inputs` count in `maya-7.summary.md`; my running tally drifted to about 177 and I defer to the client).
- Simulation rules confirmed (zero forward knowledge, reading limit of four prose lines with bold and `▶` lines read, friction meter per README rule 6 and the Reading section; quit at 8): yes
- Tutor revision and invocation: `40c11cf` (script `a7cd1ac`); `sitting.py start` with `--bash /bin/bash` (Bash 3.2.57), no `--arg`, so it began at the welcome screen.
- `--info` lines the persona was shown: none.
- Process note: for roughly the first dozen turns I issued `note` and `send` in one shell call (strictly sequential, never parallel); from then on one command per call.

## Per screen (grouped; Maya read the `▶` line and commands on each, skipped later prose lines where stated)

### welcome — "Five stages..."
- **Read**: skimmed (skipped the "Everything you type runs in a real shell... practice folder" paragraph).
- **Jargon**: "working in a Unix shell", "real shell".
- **Monologue**: Boring list. The arrow line says type next.
- **Input** `[nav]` → `next` → accepted. **Ladder**: none. **Friction**: 0.

### Orientation, Stage 1 intro
- **Read**: skimmed. **Jargon**: "real shell prompt". **Input** `[nav]` → `next`, `next` → accepted. **Friction**: 0.

### 1.1 — Running a command
- **Read**: all (short). **Jargon**: "A command is a name, then the words you hand it".
- **Input** `[bash]` → `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` → output seen; `next`. **Friction**: 0.

### 1.2 — Four keys
- **Read**: skimmed (skipped "Ctrl+C is the way out at a prompt. Inside a full-screen program..."). **Jargon**: "Ctrl+C", "Tab".
- **Input** `[nav]` → raw `\x1b[A` (Up) → recalled `next`; then Enter (`""`), which ran it. Tab, Ctrl+C and Ctrl+L not tried. **Friction**: 0.

### 1.3 — Where am I, who am I, when is it
- **Read**: all. Ran `pwd`, `whoami`, `date` → output seen. **Jargon**: "This prompt ends in >. An ordinary bash prompt usually ends in $." **Friction**: 0.

### 1.4 — The shell, caught in the act
- **Read**: skimmed (skipped the "bash: is the shell speaking..." paragraph). **Jargon**: "terminal → shell → program".
- **Input** `[bash]` → `dtae` → `bash: dtae: command not found` (expected, taught). `date` already run. **Friction**: 0.

### 1.5 — Who else types here
- **Read**: skimmed. **Input** `[nav]` → `next`. **Friction**: 0.

### Stage 1 gate (recall + task)
- Recall: Q1 `$` accepted; Q2 `the folder you are in` accepted; Q3 `on the screen` accepted. First attempt each.
- Task: ran `whoami`, `pwd`, `date`, then `check`. First check: follow-ups `[user]`, the full stage1 path, `Tue` all accepted. **Cleared.** **Friction**: -1.

### 2.1 Where you are / 2.2 What is here / 2.3 Moving / 2.4 Home and back / 2.5 Names for places / 2.6 Making a folder
- 2.1: `pwd` matched the tree top. 2.2: `ls`, `ls -p`, `ls -a`, `ls /`. 2.3: `cd ..`, `pwd`, `cd -`. 2.4: `cd`, `pwd` (a different "userhome" folder), `cd <full practice path>` typed by hand (no error). 2.5: `cd stage1`, `ls ..`, `cd ..`, `echo ~`. 2.6: `mkdir demo`, `ls -p`, `cd demo`, `pwd`. All accepted; no rejections.
- **Skipped** on 2.3: "cd.. with no space is a different word, and bash cannot find it." (after the command block). On 2.5: the whole relative/absolute paragraph ("A relative path starts where you are: in ~/projects, the name notes means ~/projects/notes...").
- Maya was left standing in `demo` when she typed `next` to the gate.
- **Friction**: -1 (unchanged).

### Stage 2 gate
- Recall: Q1 `goes up one folder` accepted; Q2 `your home folder` accepted; Q3 `~/projects/notes` accepted (inferred from `cd stage1` and `cd demo`, having skipped the 2.5 paragraph that states it; she knew it was an inference but a reasoned one, so no friction either way).
- Task: `mkdir practice`, `cd practice`, `pwd` → `.../stage2/practice`; `check` passed first time. The shell was already in `stage2` when the task began, so the "forgot which folder" habit (she was in `demo`) did not produce a wrong-folder file. **Cleared.** **Friction**: -2.

### 3.1 — Making files
- **Read**: skimmed (skipped the `>` explanation paragraph). **Jargon**: "`>` sends what echo prints into a file". Ran `touch hello.txt`, `echo hi > words.txt`, `mkdir notes`; then the habit below; `ls -p`. **Friction**: -2.

### 3.2 Reading a file / 3.3 Reading a long file
- `cat words.txt`, `cat hello.txt`, `cat ../poem.txt`. `less ../numbers.txt`, Space, `q`. All fine. Ctrl+C-in-less line read, not tried. **Friction**: -2.

### 3.4 Copy and move / 3.5 Removing
- `cp hello.txt backup.txt`, `mv hello.txt hi.txt`, `mv hi.txt notes/`, `ls -p notes`. `ls`, `rm backup.txt`, habit `undo`, `ls`. **Friction**: -2.

### Stage 3 gate
- Recall: Q1 `touch`; Q2 `gone`; Q3 `mv old.txt new.txt`, all accepted first time.
- Task: `echo hello > notes.txt`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt`, `check` passed first time. **Cleared.** **Friction**: -3.

### 4.1 to 4.6
- 4.1: `wc -l poem.txt` (worked: poem.txt present in stage4), `echo "hello world"`, `command -v vim` → `/usr/bin/vim`. 4.2: `touch my notes.txt`, `ls`, `touch "my notes.txt"`, `ls` (see habit recovery). 4.3: three pipes, 932 programs, sorted head. 4.4: `>`, `>>`, `cat`. 4.5: pipe plus `>`. 4.6: `ls *.txt`, `wc -l *.txt`. No rejections.
- **Skipped**: 4.6 "Predict before you act: rm * would remove everything in the folder." (no command invited it).

### Stage 4 gate
- Recall: Q1 `the path to vim`; Q2 `> writes over the file and >> adds to the end`; Q3 `because the space splits it into two names` (she had lived it). All accepted first time.
- Task: `seq 1 100 | wc -l > count.txt`, `ls *.txt`, `check` passed first time. **Cleared.** **Friction**: -4.

### 5.1 to 5.6
- 5.1 `man ls`, raw `q`. 5.2 `command -v vim`, `vim`, `:q`. 5.3 read only. 5.4 `vim practice.txt`, raw `i`, raw `abc`, raw Esc, `:q!`, `cat practice.txt` (still `before`). 5.5 same with `:wq` (`xyzbefore`). 5.6 `command -v vimtutor` → `/usr/bin/vimtutor`.
- 5.3 ends "Type next to try them in Vim." but `next` moves to 5.4 and nothing opens Vim; Maya typed `next` as told and noticed nothing happened.
- While in Vim the captured screen showed the tilde column and `-- INSERT --` text jumbled together; after Esc the capture looked identical to before Esc, so she could not see from the screen that she was back in normal mode; she followed the printed `:q!` / `:wq` anyway and it worked.

### Stage 5 gate
- Recall: Q1 `press q`; Q2 `:wq`; Q3 `no`. Accepted first time.
- Task phase 1 (`cat`, `vim`, `i`, letters, Esc, `:q!`, `cat`, `check`) passed; phase 2 (`vim`, `i`, `m`, Esc, `:wq`, `cat`, `check`) passed. **Cleared.** **Friction**: -5.

### Finale — "You're ready for vimtutor."
- Reply ended `[exited 0]`. Stopped.

## Per gate

- **Stage 1** — Recall: Q1 1 attempt, Q2 1, Q3 1; no rejections, no ladder rung. Task: 1 attempt, `check` first time; all three follow-ups accepted first time; nothing marked `○`. Cleared.
- **Stage 2** — Recall 1/1/1, no rejections. Task: 1 attempt, `check` first time. Cleared.
- **Stage 3** — Recall 1/1/1. Task: 1 attempt, `check` first time. Cleared.
- **Stage 4** — Recall 1/1/1. Task: 1 attempt, `check` first time. Cleared.
- **Stage 5** — Recall 1/1/1. Task: phase 1 and phase 2 each `check` first time. Cleared.
- Rejections with a ladder rung shown: none in the whole sitting. Message / hint / facts / worked example: never reached.

## Habits performed

1. **Spaces in names without quotes** (screen 3.1 "Making files"). Input `touch my notes.txt` → reply: nothing (silent success, no message). Follow-up `ls -p` → `hello.txt	my		notes/		notes.txt	words.txt`. The reply itself was not enough: no error, and the listing shows `my` and `notes.txt` as separate names with no explanation at that point. Recovery came about 30 turns later at 4.2 "Spaces and quotes" ("touch my notes.txt # two files: my, and notes.txt"), where she recognised it. Stray files `my` and `notes.txt` stayed in stage3; `notes.txt` was later overwritten by the Stage 3 task. Friction: 0 (not rejected, nothing she was misled about after the fact).
2. **Undo reflex** (screen 3.5 "Removing"). Input `undo` after `rm backup.txt` → reply `bash: undo: command not found`. The on-screen line "There is no Trash and no undo" plus the 1.4 lesson on that message format was enough to recover immediately. Friction: 0 (she understood the message).
3. **Forgetting which folder she is in** (2.6 to the Stage 2 gate). She typed `next` while standing in `demo` and began the task thinking she was still there. No wrong-folder error resulted because the task launch placed the shell in `stage2`; the spatial habit was performed but did not bite. The task screen's "This task runs in .../stage2; pwd shows it" was skimmed past.
4. Cmd+Z, select-and-Backspace and mouse placement of the cursor cannot be sent through `raw`; not performed.

## End of sitting

- **Final friction and where the persona quit**: -5. Did not quit; finished at the finale.
- **Friction by source**: reading-limit charges 0; rejections (+2 each) 0; mode confusions 0; gates cleared -5 (unfloored); net -5.
- **Stages cleared**: all five (1 to 5); `result.tap` shows "Stage 5 cleared." Turns used 169 of 240.
- **Equivalent human sitting time (estimate)**: about 35 to 45 minutes for a fast, skimming reader with no rejections.
- **Density notes (no friction under persona 0.2.0)**: over-budget screen: the very first welcome screen (21 rows against a budget of 20). Screens at 20 rows: 1.4, Stage 1 task, 2.1, 2.5, 3.1, Stage 2 task, Stage 4 cleared, both Stage 5 task screens. Prose skipped by Maya that was never needed: 1.2 Ctrl+C paragraph, 3.1 `>` paragraph, 4.6 `rm *` warning, 2.3 `cd..` warning. None of these later caused a rejection or wrong turn, so no reading charge applied.

### Candidate F-nnn
- **Candidate F-001** (false or misleading statement on screen): screen 5.3 "The copy and the file" ends "▶ Type next to try them in Vim." Input `next` moved to 5.4; no Vim opened.
- **Candidate F-002** (screen capture unreadable, possible dead end for a learner who cannot see mode): screen 5.4 "Throw it away", after `vim practice.txt` then raw `i`, `abc`, `\x1b`: the capture shows the `~` column fused with `-- INSERT --abcbefore` and the frame after Esc is identical to the frame before Esc (still `-- INSERT --`). Input that worked: `:q!`. This may be an artifact of the pty recorder rather than the tutor.
- **Candidate F-003** (stray state): screen 3.1 input `touch my notes.txt` leaves files `my` and `notes.txt` that the tutor never mentions again; the Stage 3 task's `notes.txt` precondition ("create a file notes.txt containing the word hello") is met by a pre-existing empty file with no warning. Low severity.

### Candidate O-nnn
- **Candidate O-001**: screen 3.1 gives no warning about spaces; `touch my notes.txt` succeeds silently and the lesson on this is at 4.2, a stage later ("The shell splits a line on spaces. Quote a name that has a space.").
- **Candidate O-002**: screen 2.4 "pwd # home is outside your practice folder" followed by `pwd` printing `.../shelltutor-sim-userhome-ocwjnxj9`; the tree on 2.1 called the practice folder "your practice folder" and its parent a different folder from "home". Two meanings of "home" (the `~` folder and the practice root) sit on adjacent screens.
- **Candidate O-003**: screen 2.1 draws the "you are here" marker at the practice root while Maya had last been in `stage1` (Stage 1 task path ends in `/stage1`) and the shell then printed the root; the tutor silently moves the shell between stages and tasks, which hides the "forget which folder" habit.
- **Candidate O-004**: screen 2.5 "in ~/projects, the name notes means ~/projects/notes" is the only statement of the fact asked in Stage 2 recall Q3 ("If I'm in ~/projects and I type cd notes, what folder am I in?"); a skimmer who skips that paragraph can only infer the answer from `cd stage1`.
- **Candidate O-005**: screen 1.2 "Try each key" invites four keys but nothing checks them; Maya tried only Up and went on.
- **Candidate O-006**: screen 4.1 `wc -l poem.txt` works in stage4 while 3.1 said "The tutor put poem.txt and numbers.txt one folder up"; a copy of poem.txt appears in each stage folder and 3.2's `../poem.txt` is the only place that relationship is shown.

## Debrief (out of character)

- 3.1: no sentence warns that a space splits a name; the first quoting rule is the 1.1 note "quotes make them one word", which a skimming learner does not connect to filenames.
- 5.3: "Type next to try them in Vim." does not match what `next` does.
- 2.5 and Stage 2 recall Q3: the answer lives in "A relative path starts where you are: in ~/projects, the name notes means ~/projects/notes."
- 2.4: "home is outside your practice folder" and the 2.1 tree label are two different homes.
- The Stage 2 and Stage 3 task screens say "This task runs in .../stageN; pwd shows it" but the learner's last `cd` is silently overridden, so the "know which folder you are in" habit (1.5, 5.x summary) is never contradicted by an error.
