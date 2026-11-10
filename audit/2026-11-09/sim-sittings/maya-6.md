# Synthetic walkthrough — one sitting (maya-6)

## Sitting

- Date: 2026-11-09
- Persona (file in `docs/sim-personas/`) and learner role: `maya.md`
  (Maya, 19, graphic design student, `search-first-skimmer`); adult beginner
- Persona sheet version: 0.2.0
- Turn cap: 220 (round 6). One turn = one `send` or one `raw`. Turns used: 171
  (matches `persona_inputs: 171` in the bundle summary)
- Simulation rules confirmed (zero forward knowledge, reading limit,
  friction meter): yes. Reading limit four lines of prose per screen; bold
  and arrow lines always read. Per v0.2 the density charge applies only when
  a skipped line later causes a rejection or wrong turn. Friction: +2
  rejection, +1 mode confusion, -1 gate cleared, quit at 8. A guess Maya knows
  is a guess scores 0.
- Tutor revision and invocation: revision 2579f68 (script 2cb3f53);
  `sitting.py start` with no `--arg` (begins at the welcome screen), Bash
  `/bin/bash` 3.2.57. Sixth Maya sitting; no memory of earlier ones.
- `--info` lines the persona was shown, if any: none

## Per screen

Convention for every block below. "Skipped" counts prose lines beyond the
fourth that Maya did not read (list items, code blocks and arrow lines are
not prose). Friction is the running total after the screen.

### welcome — shelltutor (five stages)
- **Read**: all (no lesson prose; stage list and one arrow line). Skipped: 0.
- **Jargon**: "working in a Unix shell", "Everything you type runs in a real shell".
- **Monologue**: The black hacker app. Five levels, fine. Arrow says type next.
- **Input** `[nav]` `next` -> accepted.
- **Ladder rung**: none. **Friction**: 0.

### orientation — Orientation
- **Read**: skimmed. Skipped: 1 ("A fifth, check, appears when a stage's task is ready to be tested.").
- **Jargon**: "a real shell prompt".
- **Monologue**: Prompt looks like `shelltutor>`. Skipped the line about a fifth word.
- **Input** `[nav]` `next` -> accepted. **Rung**: none. **Friction**: 0.

### Stage 1 intro
- **Read**: all. Skipped: 0. **Input** `[nav]` `next` -> accepted. **Friction**: 0.

### 1.1 — Running a command
- **Read**: all (3 prose lines). Skipped: 0.
- **Jargon**: "A command is a name, then the words you hand it".
- **Monologue**: Type the three lines. Quotes do not print.
- **Inputs** `[bash]`: `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` -> each printed as the comments said; then `[nav]` `next`.
- **Rung**: none. **Friction**: 0.

### 1.2 — Four keys
- **Read**: all (3 prose lines). Skipped: 0.
- **Jargon**: "Ctrl+C is the way out at a prompt".
- **Monologue**: Four keys to try. Tab filled in `poem.txt`, nice.
- **Inputs**: `[bash]` raw `echo p<Tab>` -> completed to `echo poem.txt`; raw Enter -> `poem.txt`; raw Up arrow -> recalled the line; raw Enter -> ran it; raw `oops` + Ctrl+C -> fresh prompt; raw Ctrl+L -> screen cleared; `[nav]` `show` -> lesson back; `[nav]` `next`.
- **Interpretation**: All four keys did what the screen said. Ctrl+L plus `show` worked as promised.
- **Rung**: none. **Friction**: 0.

### 1.3 — Where am I, who am I, when is it
- **Read**: all (4 prose lines). Skipped: 0.
- **Jargon**: "This prompt ends in >. An ordinary bash prompt usually ends in $."
- **Inputs** `[bash]`: `pwd` -> long temp path; `whoami` -> [user]; `date` -> date; `[nav]` `next`.
- **Rung**: none. **Friction**: 0.

### 1.4 — The shell, caught in the act
- **Read**: skimmed. Skipped: 2 ("of message: read it, then type the line again." and "terminal -> shell -> program: the window, bash, and date.").
- **Jargon**: "command not found", "terminal -> shell -> program".
- **Monologue**: Real one, then scrambled one. The error is on the screen already.
- **Inputs** `[bash]`: `date` -> date; `dtae` -> `bash: dtae: command not found` (as shown); `[nav]` `next`.
- **Rung**: none. No later turn was caused by the skipped lines. **Friction**: 0.

### 1.5 — Who else types here
- **Read**: all (4 prose lines + three habit lines). Skipped: 0.
- **Input** `[nav]` `next` -> accepted. **Friction**: 0.

### Stage 1 gate (recall and task)
- **Read**: all. Skipped: 0.
- **Recall inputs** `[recall]`: Q1 `$` (accepted); Q2 `the folder you are in` (accepted); Q3 "After whoami runs, where does its output go?" -> `the screen` (accepted). Maya noted Q3 as a guess at the wanted word, but it was accepted, so no charge.
- **Task inputs** `[bash]`: `whoami`, `pwd`, `date`; `[nav]` `check` -> three follow-ups; `[follow-up]` `[user]`, the full path copied from the screen, `Mon` -> all accepted.
- **Result**: Stage 1 cleared at first `check`. **Friction**: -1.

### Stage 2 intro, 2.1 — Where you are
- **Read**: all (3 prose lines + tree). Skipped: 0.
- **Jargon**: "current directory", the tree with "you are here".
- **Monologue**: Looks like a folder view, ok. Predict, then pwd.
- **Inputs** `[bash]` `pwd` -> matched the arrow folder; `[nav]` `next`. **Friction**: -1.

### 2.2 — What is here
- **Read**: all (3 prose lines). Skipped: 0.
- **Jargon**: "hidden names, which start with a dot".
- **Inputs** `[bash]`: `ls`, `ls -p`, `ls -a`, `ls /` -> each as described; `[nav]` `next`. **Friction**: -1.

### 2.3 — Moving
- **Read**: all (3 prose lines). Skipped: 0.
- **Jargon**: "up one level, to the folder that contains this one".
- **Inputs** `[bash]`: `cd ..` (prints nothing, as warned), `pwd` (parent), `cd -` (printed the practice path); `[nav]` `next`. **Friction**: -1.

### 2.4 — Home and back
- **Read**: all (3 prose lines). Skipped: 0.
- **Jargon**: "~ is its short name", "full name".
- **Monologue**: `cd` alone goes home; a different folder than the practice one. Copy the long cd line.
- **Inputs** `[bash]`: `cd`, `pwd` (a different, empty "userhome" folder), `cd <full practice path>` (the example line wraps at 80 columns on screen, but typing it worked); `[nav]` `next`. **Friction**: -1.

### 2.5 — Names for places
- **Read**: skimmed. Skipped: 1 ("/usr/bin is the same place wherever you stand.").
- **Jargon**: "relative path", "absolute path".
- **Inputs** `[bash]`: `ls ..` -> a very long scroll of several hundred unfamiliar names (the practice folder's parent is the host temp directory); `ls ~` -> nothing; `[nav]` `next`.
- **Interpretation**: Not an error, but the `ls ..` wall of names meant nothing to Maya and the screen buffer stayed full of it until `next`. `ls ~` printing nothing was unexplained (she guessed home is empty). No rejection; no charge.
- **Rung**: none. **Friction**: -1.

### 2.6 — Making a folder
- **Read**: all (2 prose lines). Skipped: 0.
- **Inputs** `[bash]`: `mkdir demo`, `ls -p`, `cd demo`, `pwd` -> ends in /demo; `[nav]` `next`. **Friction**: -1.

### Stage 2 gate (recall and task)
- **Read**: all. Skipped: 0.
- **Recall** `[recall]`: Q1 `goes up one level`; Q2 `your home folder`; Q3 `~/projects/notes` -> all accepted first try.
- **Task** `[bash]`: `pwd` (tutor had already placed her in the stage2 folder), `mkdir practice`, `cd practice`, `pwd`; `[nav]` `check` -> Stage 2 cleared at first check. **Friction**: -2.

### Stage 3 intro and 3.1 — Making files
- **Read**: all (4 prose lines; the "rm removes for good. There is no Trash." warning on the intro was read). Skipped: 0.
- **Jargon**: "> sends what echo prints into a file instead of the screen".
- **Inputs** `[bash]`: `touch hello.txt`, `echo hi > words.txt`, `mkdir notes`, `ls -p`; `[nav]` `next`. **Friction**: -2.

### 3.2 — Reading a file
- **Read**: all (1 prose line). **Inputs** `[bash]`: `cat words.txt`, `cat hello.txt` (empty), `cat ../poem.txt`; `[nav]` `next`. **Friction**: -2.

### 3.3 — Reading a long file
- **Read**: all (4 prose lines). Skipped: 0.
- **Jargon**: "you are inside a program", "Space pages down, b pages back, q leaves".
- **Inputs**: `[bash]` `less ../numbers.txt`; raw Space (paged); raw `q` (prompt back); `[nav]` `next`. **Friction**: -2.

### 3.4 — Copy and move
- **Read**: all (1 prose line). **Inputs** `[bash]`: `cp hello.txt backup.txt`, `mv hello.txt hi.txt`, `mv hi.txt notes/`, `ls -p notes` -> `hi.txt`; `[nav]` `next`. **Friction**: -2.

### 3.5 — Removing
- **Read**: all (2 prose lines). **Inputs** `[bash]`: `ls`, `rm backup.txt`, `ls` (gone); `[nav]` `next`. **Friction**: -2.

### Stage 3 gate (recall and task)
- **Recall** `[recall]`: Q1 `touch`; Q2 `gone`; Q3 `mv old.txt new.txt` -> all accepted.
- **Task** `[bash]`: `echo hello > notes.txt`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt`; `[nav]` `check` -> Stage 3 cleared at first check. **Friction**: -3.

### Stage 4 intro and 4.1 — The parts of a command
- **Read**: all (3 prose lines). Skipped: 0.
- **Jargon**: "name, then options, then arguments", "option -l, argument poem.txt".
- **Inputs** `[bash]`: `wc -l poem.txt` -> `4 poem.txt`; `echo "hello world"`; `command -v vim` -> a path; `[nav]` `next`. **Friction**: -3.

### 4.2 — Spaces and quotes
- **Read**: all (3 prose lines). Skipped: 0.
- **Monologue**: Maya's habit is to name files with spaces unquoted; the screen shows both on purpose.
- **Inputs** `[bash]`: `touch my notes.txt`, `ls` (two files, `my` and `notes.txt`), `touch "my notes.txt"`, `ls` (one more); `[nav]` `next`. **Friction**: -3.

### 4.3 — The pipe
- **Read**: all (3 prose lines). Skipped: 0.
- **Jargon**: "A pipe, |, sends what one command prints into the next command".
- **Inputs** `[bash]`: `seq 1 100 | wc -l`, `ls /usr/bin | wc -l`, `ls /usr/bin | sort | head`; `[nav]` `next`. **Friction**: -3.

### 4.4 — Into a file
- **Read**: all (3 prose lines). Skipped: 0.
- **Inputs** `[bash]`: `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt`; `[nav]` `next`. **Friction**: -3.

### 4.5 — Pipe, then file
- **Read**: all (3 prose lines). **Inputs** `[bash]`: `ls /usr/bin | wc -l > count-of-programs.txt`, `cat count-of-programs.txt`; `[nav]` `next`. **Friction**: -3.

### 4.6 — Many names at once
- **Read**: all (3 prose lines). Skipped: 0.
- **Jargon**: "* matches any run of characters in a file name".
- **Inputs** `[bash]`: `ls *.txt`, `wc -l *.txt`; `[nav]` `next`. **Friction**: -3.

### Stage 4 gate (recall and task)
- **Recall** `[recall]`: Q1 `its path`; Q2 `> replaces the file and >> adds to the end`; Q3 `the shell splits on spaces unless you quote the name` -> all accepted.
- **Task** `[bash]`: `seq 1 100 | wc -l > count.txt`, `ls *.txt`; `[nav]` `check` -> Stage 4 cleared at first check. **Friction**: -4.

### Stage 5 intro and 5.1 — Programs that take over the screen
- **Read**: all (3 prose lines on the intro, 3 on 5.1). Skipped: 0.
- **Inputs**: `[bash]` `man ls` (wall of manual text); raw `q`; `[nav]` `next`. **Friction**: -4.

### 5.2 — Leaving Vim
- **Read**: all (3 prose lines). Skipped: 0.
- **Jargon**: ":q", ":q!".
- **Inputs**: `[bash]` `vim` (welcome screen, which itself says type :q to exit); `[bash]` `:q` -> prompt back; `[nav]` `next`. **Friction**: -4.

### 5.3 — The copy and the file
- **Read**: all (2 prose lines + diagram + four commands). Skipped: 0.
- **Jargon**: "working copy".
- **Monologue**: Like Save and Don't Save.
- **Input** `[nav]` `next`. **Friction**: -4.

### 5.4 — Throw it away
- **Read**: all (3 prose lines). Skipped: 0.
- **Inputs**: `[bash]` `vim practice.txt`; raw `i`; raw `abc`; raw Esc; `[bash]` `:q!`; `[bash]` `cat practice.txt` -> `before`; `[nav]` `next`.
- **Interpretation**: After Esc the visible mode text still read "-- INSERT --"; Maya was not sure Esc had worked but followed the next step and it was fine.
- **Friction**: -4.

### 5.5 — Keep it
- **Read**: all (3 prose lines). Same sequence with `:wq`; `cat practice.txt` -> `xyzbefore`; `[nav]` `next`. **Friction**: -4.

### 5.6 — vimtutor
- **Read**: all (3 prose lines). Skipped: 0.
- **Monologue**: The arrow line says just type next; she did not run `command -v vimtutor`.
- **Input** `[nav]` `next`. **Friction**: -4.

### Stage 5 gate (recall and two-phase task)
- **Recall** `[recall]`: Q1 `press q`; Q2 `:wq`; Q3 `no` -> all accepted.
- **Task phase 1** `[bash]`: `cat practice.txt`, `vim practice.txt`, raw `i`, raw `oops`, raw Esc, `:q!`, `cat practice.txt`; `[nav]` `check` -> phase 2.
- **Task phase 2** `[bash]`: `vim practice.txt`, raw `i`, raw `saved`, raw Esc, `:wq`, `cat practice.txt` -> `savedbefore`; `[nav]` `check` -> finale ("You're ready for vimtutor", `[exited 0]`).
- **Friction**: -5.

### finale — You're ready for vimtutor
- **Read**: skimmed; the finale screen is a long summary (about 14 lines of prose plus install notes). Maya read the stage recap and the "Four habits to keep"; the install paragraph was skipped. It caused no later turn (sitting over). Sitting stops here (`[exited 0]`).

## Per gate

| Gate | Recall attempts (rejections) | Task attempts, first `check` | Result |
| --- | --- | --- | --- |
| Stage 1 | 1 / 1 / 1 (0) | passed on first `check` (three follow-up answers accepted first try) | cleared |
| Stage 2 | 1 / 1 / 1 (0) | passed on first `check` | cleared |
| Stage 3 | 1 / 1 / 1 (0) | passed on first `check` | cleared |
| Stage 4 | 1 / 1 / 1 (0) | passed on first `check` | cleared |
| Stage 5 | 1 / 1 / 1 (0) | phase 1 passed on first `check`; phase 2 passed on first `check` | cleared |

- Rejected recall inputs verbatim: none. Ladder rung reached: none at any point.
- Checklist `○` marks: none seen.

## End of sitting

- **Final friction**: -5, and the sitting did not quit. It ended at the finale (`[exited 0]`). By source: reading charges 0, rejections 0, mode confusion 0, gates cleared -5. Persona v0.2 charges density only when a skipped line causes a rejection or wrong turn; no skipped line did.
- **Stages cleared**: 1, 2, 3, 4, 5 (all five), then the finale. Turns used: 171 of 220.
- **Prose skipped under the four-line rule** (screens with skipped prose: 3 lesson or intro screens, plus the finale):
  - orientation: 1 line (the fifth word, `check`).
  - 1.4: 2 lines (the "read it, then type the line again" close, and the "terminal -> shell -> program" line).
  - 2.5: 1 line ("/usr/bin is the same place wherever you stand.").
  - finale: the install paragraph.
  - All 28 lesson screens plus gates otherwise fit within her four-line limit; nothing was skipped on the other lesson screens.
- **First-check result per gate task**: Stage 1 pass, Stage 2 pass, Stage 3 pass, Stage 4 pass, Stage 5 phase 1 pass, Stage 5 phase 2 pass. No gate task needed a second `check`.
- **Equivalent human sitting time (estimate)**: about 25 to 30 minutes for a fast beginner, with no stalls; the only slow moments were the two screens with large output (`ls ..`, `man ls`).
- **Candidate F-nnn**: none. No valid answer was rejected, no hint was broken, no dead end, and no false statement was found on screen.
- **Candidate O-nnn**:
  - O-a (screen 2.5, input `ls ..`): the listing ran to several hundred names of the host's temporary directory, unrelated to the lesson, and stayed in the scroll until `next`. The screen text "look one level up without moving" does not warn that the parent may be large. Maya had no way to tell which names were hers.
  - O-b (screen 2.5, input `ls ~`): printed nothing; the screen does not say home is empty here, so "look at home without moving" ends in silence. Maya guessed it was empty.
  - O-c (screen 2.4, input `cd /var/folders/.../shelltutor-sim-home-...`): the example `cd` line is longer than the 80-column panel and wraps mid-word on screen; it worked when copied, but the wrapped display could mislead a learner who retypes it.
  - O-d (screens 5.4, 5.5, stage 5 gate, input raw Esc after `i` and letters): the mode line still showed "-- INSERT --" after Esc, so Maya could not see that Esc had worked. May be a harness redraw artefact; reproduce before calling it a tutor issue.
  - O-e (screen 5.2, input `vim`): the Vim splash printed as one run-together block of text; the real Vim shows it laid out. Likely harness rendering only.
  - O-f (Stage 1 gate Q3, input `the screen`): the question "where does its output go?" has no word list and the accepted answer set is unknown to the learner; Maya called it a guess and it passed. If the intended answer is narrower, a learner could be rejected on a correct idea.
  - O-g (density notes, plain over-length screens): no screen exceeded her four lines in a way that mattered. The longest lesson prose was 1.4 (five lines, two skipped) and 2.5 (five lines, one skipped); the finale screen is long but follows completion.
- **Debrief** (out of character):
  - The lessons are now short enough that Maya's four-line rule almost never bites; the three skipped sentences ("A fifth, check, appears...", "terminal -> shell -> program: the window, bash, and date.", "/usr/bin is the same place wherever you stand.") were all non-load-bearing for the next step.
  - "inside this stage's folder" (Stage 2 gate) did not trip her because the screen's last line named the folder and the tutor had already placed her there.
  - The confusing moments came from output the lesson did not predict: the "Names for places" lesson's `ls ..` flood and the empty `ls ~`, and the unchanged "-- INSERT --" text after Esc.
  - "More on > in Stage 4." (3.1) and "> replaces the file without asking, whoever typed the line." (4.4) landed; she did not overwrite anything by accident.
