# Synthetic walkthrough — maya-5

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/maya.md` (Maya, 19, graphic design student, `search-first-skimmer`); learner role: adult beginner
- Persona sheet version: 0.2.0
- Turn cap: 160. One turn = one `send` or one `raw`. Turns used: 131 (the client's `persona_inputs`; my own running tally was 130, so I take the client's count)
- Simulation rules confirmed (zero forward knowledge, reading limit of four prose lines with bold and `▶` lines always read, friction meter with quit at 8; v0.2 density charge only where a skipped line later causes a rejection or wrong turn): confirmed
- Tutor revision: d88c564 (script 7e126cf). Invocation: `sitting.py start` with no `--arg` (begins at the welcome screen), Bash `/bin/bash` 3.2.57. Maya's fifth sitting; no memory of earlier ones.
- `--info` lines the persona was shown: none
- Procedure note: on one early turn (welcome to 1.1) I put `note` and `send` in one shell call; every later call was one command. The `note` text was still written before the `send`.

## Per screen (condensed; screens whose block repeats are grouped)

### welcome — SHELLTUTOR, a vimtutor prerequisite course
- **Read**: skimmed (read to the `▶` line; skipped the sandbox-folder paragraph)
- **Jargon**: "vimtutor prerequisite course"
- **Monologue**: Welcome blah. The arrow says type next.
- **Input** `[nav]` → `next` → accepted
- **Ladder rung**: none. **Friction**: 0

### orientation / Stage 1 intro / 1.1 (running commands)
- **Read**: skimmed (skipped "Resize your terminal larger..." and "If bash says command not found..."); 1.1 read in full, short
- **Jargon**: "practice prompt", "the shell runs it", "a name, then the words you hand it"
- **Inputs** `[nav]` `next` x3; `[bash]` `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` → all printed as expected
- **Interpretation**: the last two print the same thing. "Whatever."
- **Ladder rung**: none. **Friction**: 0

### 1.2 — keyboard habits
- **Read**: skimmed (read Tab line; skipped the other three keys)
- **Input** `[bash]` `raw "echo p\t"` → screen showed `echo poem.txt`; `send ""` → `poem.txt`
- **Interpretation**: Tab worked, cool. Arrow keys, Ctrl+L, Ctrl+C never tried.
- **Ladder rung**: none. **Friction**: 0

### 1.3 — where am I, who am I, when is it
- **Read**: skimmed (skipped "Your prompt here ends in >... usually ends in $")
- **Jargon**: "print working directory"
- **Inputs** `[bash]` `whoami`, `pwd`, `date` → each accepted. pwd printed the practice folder.
- **Friction**: 0

### 1.4 — the shell, caught in the act
- **Read**: skimmed (read the first command pair; skipped "Read who is speaking..." and the terminal/shell/program paragraph)
- **Jargon**: "bash: is the shell", "terminal → shell → program"
- **Inputs** `[bash]` `dtae` → `bash: dtae: command not found`; `[nav]` `next`
- **Interpretation**: expected typo error. I could not say what "shell" versus "terminal" is.
- **Friction**: 0

### 1.5 — who else types here
- **Read**: skimmed (skipped the AI-assistant paragraph and the three habits)
- **Input** `[nav]` `next`. **Friction**: 0

### Stage 1 gate, recall (task screen)
- **Read**: all (screen is 3 lines of prose)
- **Q1** "which character usually ends the prompt?" → `$` ✓ (remembered 1.3; the line I had skimmed was lucky, because the question was also answerable from "$" in the options)
- **Q2** "What does pwd print?" → `the folder you are in` ✓
- **Q3** "After whoami runs, where does its output go?" → `it comes back to me on the screen` ✓ (first try)
- **Interpretation**: Q3's answer was inferable from "what the program prints comes back to you" on 1.4 plus the screen itself.

### Stage 1 gate task
- Inputs `[bash]` `whoami`, `pwd`, `date`; `[nav]` `check`; `[follow-up]` `[user]`, the full path (copied from screen), `Mon`. All accepted. Stage 1 cleared.
- Note: the `pwd` here printed `.../stage1`, a different folder from the one lesson 1.3 showed. I did not notice or care.
- **Friction**: -1 (gate cleared)

### Stage 2 intro / 2.1 — where you are
- **Read**: all (short). **Jargon**: "current directory", the tree diagram with `◀ you are here`
- **Input** `[bash]` `pwd` → matched the tree. `[nav]` `next`. **Friction**: -1

### 2.2 — ls: what is here
- **Read**: skimmed (skipped the "tutor keeps its own hidden files" line and the `ls /` part)
- **Input** `[bash]` `ls -p` → `numbers.txt poem.txt stage1/ stage2/`. `[nav]` `next`. **Friction**: -1

### 2.3 — cd: moving
- **Read**: skimmed. **Skipped**: "cd.. with no space is a different word; bash cannot find it." and the "Stages 1 and 2 start every practice prompt in ..." paragraph (both in the 3rd-to-last block; neither bold nor `▶`)
- **Jargon**: "current folder", "outside this practice area"
- **Inputs** `[bash]` `cd ..` (no output); `pwd` → one level above the practice folder; `cd -` → printed the path it returned to. `[nav]` `next`
- **Interpretation**: `cd -` is a back button. The skipped lines caused no wrong turn this time, so no reading charge.
- **Friction**: -1

### 2.4 — names for places
- **Read**: skimmed (skipped the path-jargon paragraph; kept `▶`)
- **Jargon**: "Relative paths start where you are", "Absolute paths start from the root, /"
- **Inputs** `[bash]` `mkdir demo`, `ls -p` → `demo/` appeared. `[nav]` `next`. **Friction**: -1

### Stage 2 gate, recall
- Q1 "What does cd .. do?" → `goes up one level to the parent folder` ✓
- Q2 "What does ~ mean in a path?" → `your home folder` ✓
- Q3 "If I'm in ~/projects and I type cd notes, what folder am I in?" → `~/projects/notes` ✓. I half-remembered a line; this was partly a guess from "a folder inside a folder", but I did not know it was a guess, so it scores 0.

### Stage 2 gate task
- **Read**: skimmed (skipped "(inside this stage's folder)" and "The task runs in this stage's own folder; pwd shows it.")
- Inputs `[bash]` `mkdir practice`, `cd practice`, `pwd` → `.../stage2/practice`; `[nav]` `check` → Stage 2 cleared.
- **Interpretation**: I did not notice that "this stage's folder" is a place I should be standing in; it happened to be where I already was. **Friction**: -2 (gate cleared)

### Stage 3 intro / 3.1 — creating
- **Read**: skimmed (read "rm is immediate. It does not move things to a trash." as it sits in the first four lines)
- **Inputs** `[nav]` `next` x2; `[bash]` `touch hello.txt`, `echo hello > notes.txt` → silent. `[nav]` `next`. **Friction**: -2

### 3.2 — reading: cat, less
- **Read**: skimmed (skipped "Important: when less takes over, the prompt is gone" paragraph; read the `▶` line "q leaves less")
- **Jargon**: "the screen takes over", "page through"
- **Inputs** `[bash]` `cat notes.txt` → `hello`; `less ../numbers.txt` → numbers 1 to 23 and a prompt `../numbers.txt`; `[nav]` `raw "q"` → back at `shelltutor>`.
- **Interpretation**: the `▶` line saved me; had I missed it I would not have known to press q. **Friction**: -2

### 3.3 — copy, move, delete
- **Read**: all (short)
- **Inputs** `[bash]` `cp hello.txt backup.txt`, `mv hello.txt hi.txt`, `ls` → `backup.txt hi.txt notes.txt`, `rm backup.txt`. All silent or as expected. **Friction**: -2

### Stage 3 gate, recall
- Q1 `touch` ✓, Q2 `gone` ✓ (I read "no Trash"), Q3 `mv old.txt new.txt` ✓. First try each.

### Stage 3 gate task
- **Read**: all (short)
- Inputs `[bash]` `echo hello > notes.txt`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt`; `[nav]` `check` → Stage 3 cleared. **Friction**: -3 (gate cleared)

### Stage 4 intro (the symbol table)
- **Read**: skimmed (a column of eleven symbols; I read none of it)
- **Jargon**: "pipe", "redirect", "glob", "append"
- **Input** `[nav]` `next`. **Friction**: -3

### 4.1 — reading a command
- **Read**: skimmed
- **Jargon**: "option + argument"
- **Inputs** `[bash]` `command -v ls` → `/bin/ls`; `command -v vim` → `/usr/bin/vim`. `[nav]` `next`. **Friction**: -3

### 4.2 — the pipe
- **Read**: skimmed
- **Jargon**: "A pipe ( | ) sends one command's output into the next command's input"
- **Inputs** `[bash]` `seq 1 100 | wc -l` → `100`; `ls /usr/bin | grep ^a | wc -l` → `41`. `[nav]` `next`.
- **Interpretation**: pipes work like chaining. I could copy them but not explain `grep ^a`. **Friction**: -3

### 4.3 — redirection
- **Read**: skimmed (read the first sentence of the 2nd line; skipped `<` and the `programs.txt` line)
- **Inputs** `[bash]` `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt` → two lines. `[nav]` `next`. **Friction**: -3

### 4.4 — globs
- **Read**: all (short). Arrow said just `next`; I did not try `ls *.txt` here.
- **Input** `[nav]` `next`. **Friction**: -3

### Stage 4 gate, recall
- Q1 `the path to it, /usr/bin/vim` ✓; Q2 `> replaces the file and >> adds to the end of it` ✓; Q3 `because the shell splits on the space, so my and notes.txt are two files; you need quotes` ✓. First try each.

### Stage 4 gate task
- **Read**: all
- **Jargon**: "Use seq and a pipe to count from 1 to 100 and save the count to count.txt" (I read "count" as the `wc -l` thing from 4.2; it took me a guess to decide between "write 1 to 100" and "write the number 100"; I took the second)
- Inputs `[bash]` `seq 1 100 | wc -l > count.txt`; `ls *.txt` → `count.txt greeting.txt poem.txt seed.txt`; `[nav]` `check` → Stage 4 cleared. **Friction**: -4 (gate cleared)

### Stage 5 intro / 5.1 — print-and-exit vs full-screen
- **Read**: skimmed (read the exit-keys line and `▶` line)
- **Jargon**: "full-screen", "print-and-exit", "take over the terminal"
- **Inputs** `[nav]` `next` x2; `[bash]` `man ls` → manual page, prompt shown as `:`; `[nav]` `raw "q"` → back. **Friction**: -4

### 5.2 — entering and leaving Vim
- **Read**: skimmed
- **Jargon**: "discard form", "vim --version"
- **Inputs** `[bash]` `vim --version` → about 60 lines of feature flags and file paths; `vim` → black screen of `~` and a splash; `[bash]` `:q` → back at `shelltutor>`.
- **Interpretation**: `vim --version` dumped a wall nobody asked me to read. The splash told me `:q<Enter>` to exit, so I knew what to do. **Friction**: -4

### 5.3 — buffer vs file
- **Read**: skimmed (read the first four lines: "buffer — a copy in memory"; the `:w :q :q! :wq` list is code-block, read in passing)
- **Jargon**: "buffer", "a copy in memory"
- **Input** `[nav]` `next`. **Friction**: -4

### 5.4 — practice: discard, then save
- **Read**: all (it is a numbered recipe)
- **Jargon**: "insert mode (vimtutor will teach modes)"
- **Inputs** `[bash]` `vim practice.txt`; `raw "i"` → `-- INSERT --`; `raw "xyz"`; `raw "\x1b"`; `send ":q!"`; `send "cat practice.txt"` → `before`. Then `vim practice.txt`, `raw "i"`, `raw "abc"`, `raw "\x1b"`, `send ":wq"`, `cat practice.txt` → `abcbefore`.
- **Interpretation**: the discard/keep difference is clear. The escape key sequence `\x1b` showed no visible change on the captured screen; I only trusted it because `:q!` and `:wq` then worked. **Friction**: -4

### 5.5 — calling vimtutor
- **Read**: skimmed (skipped the install bullets; read `▶`)
- **Input** `[nav]` `next` x1 to the gate. **Friction**: -4

### Stage 5 gate, recall
- Q1 "How do you exit man ls?" → `press q` ✓
- Q2 "After vim notes.txt, what makes Vim write your edit to the file?" → `:wq (or :w) writes the buffer to the file` → **"not quite. try again."** with the hint "Lesson 5.3: the colon command for putting the buffer into the file."
  - **Interpretation**: I had typed the right answer, twice over. The tutor did not tell me what it didn't like. Rejected, not understood: **+2**.
  - Retry `:w` → ✓. Friction after Q2: -4 + 2 = -2.
- Q3 "If you open notes.txt in vim, type some letters, and quit with :q! — did the file on disk change?" → `no, the file did not change` ✓
- **Ladder rung**: hint (message "not quite" then hint). The hint said "the colon command", which I read as a pointer toward a single bare command; it resolved the confusion, and I copied it as `:w`.

### Stage 5 gate task, phase 1 and 2
- Phase 1: `cat practice.txt` → `before`; `vim practice.txt`; `raw "i"`; `raw "qqq"`; `raw "\x1b"`; `send ":q!"`; `cat practice.txt` → `before`; `check`.
- Phase 2: `vim practice.txt`; `raw "i"`; `raw "m"`; `raw "\x1b"`; `send ":wq"`; `cat practice.txt` → `mbefore`; `check` → finale. `[exited 0]`.
- **Friction**: -3 (gate cleared, -1 after the +2: final total -3)

### finale — You're ready for vimtutor
- Ended with `[exited 0]`. Not read in full; the `commands` list contains `clear`, `exit`, `head`, `sort`, `grep`, `vimtutor` as "met" (`exit` and `vimtutor` were never run by me; see O-004).

## Per gate

| Gate | Recall attempts per question | Rejections | Rung | Task | Cleared |
| --- | --- | --- | --- | --- | --- |
| Stage 1 | 1, 1, 1 | none | none | 1 attempt, `check` passed, 3 follow-ups right first try | yes |
| Stage 2 | 1, 1, 1 (Q3 a partial guess I did not know was a guess: 0) | none | none | 1 attempt | yes |
| Stage 3 | 1, 1, 1 | none | none | 1 attempt | yes |
| Stage 4 | 1, 1, 1 | none | none | 1 attempt; task 1 involved a reading of "count" | yes |
| Stage 5 | 1, 2, 1 | Q2: `:wq (or :w) writes the buffer to the file` | hint | 2 phases, 1 attempt each | yes |

## End of sitting

- **Final friction**: -3 (unfloored). Did not quit; the sitting ended at the finale (`[exited 0]`).
- **By source**: reading-limit charges 0 (no skipped line caused a rejection or wrong turn); rejections 1 x +2 = +2 (Stage 5 gate Q2); mode confusion 0; gates cleared 5 x -1 = -5. Total 0 + 2 + 0 - 5 = -3.
- **Stages cleared**: all five (Stages 1 to 5), and the finale.
- **Equivalent human sitting time (estimate)**: about 35 to 45 minutes, given one rejected answer, no re-reads, and a lot of skimmed prose; the tutor advertises 45 to 60.
- **Density notes (no friction)**: Maya skipped prose on 1.2, 1.4, 1.5, 2.2, 2.3, 2.4, 3.2, Stage 4 intro, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3 and 5.5. The Stage 4 intro (11-row symbol table) and the `vim --version` dump on 5.2 are the two places the screen exceeded what she would read at all. Per v0.2, none caused a rejection or wrong turn.

### Candidate F-nnn

- **F-A (Stage 5 gate, Q2 "After vim notes.txt, what makes Vim write your edit to the file?")**: the input `:wq (or :w) writes the buffer to the file` was rejected ("not quite. try again."), while the bare `:w` was accepted. A valid answer containing a correct command, wrapped in extra words, is refused. Repro: send exactly that string at Q2.
- **F-B (Stage 5 gate, Q2)**: `:wq` alone was not tested. The hint says "the colon command", singular, which does not tell the learner which of `:w` or `:wq` is meant, and the lesson 5.3 list shows both.

### Candidate O-nnn

- **O-001 (5.2 "vim --version   # prints version info and exits")**: the output is about 60 lines of compile flags and file paths. The sentence promises "version info"; the learner gets a wall. Pace and noise, not an error.
- **O-002 (Stage 1 gate task, "pwd" vs 1.3 "Here pwd shows the tutor's own folder")**: `pwd` in the gate printed `.../stage1`, a different path from the one 1.3 told the learner to expect. Not a defect (the tutor said "later stages start in a stage folder"), but a Maya-type learner who "forgets which folder she is in" gets no cue that the folder changed.
- **O-003 (Stage 2 gate task, "(inside this stage's folder)")**: the learner is told to make `practice` "inside this stage's folder" but nothing on the screen says she is already standing there; she only passes because the prompt starts there.
- **O-004 (finale, "commands ... clear, exit, ... head, sort, grep, man, vim, vim --version, vimtutor")**: the closing list claims `exit`, `head`, `sort`, `grep` and `vimtutor` as "met" though this sitting never ran them; a learner who skips a command-line exercise still sees it listed.
- **O-005 (Stage 4 gate task, "Use seq and a pipe to count from 1 to 100 and save the count to count.txt")**: "count" can mean "the sequence 1 to 100" or "the number 100"; Maya chose `seq 1 100 | wc -l > count.txt` (the number). The checker accepted it ("contains 100"), but the phrasing allows `seq 1 100 > count.txt`, which also contains 100 on a line.
- **O-006 (5.4, `raw "\x1b"` in the vim practice)**: after Esc, the captured screen showed no change from `-- INSERT --`, so the learner cannot confirm the mode switched. (Capture artefact more than tutor behaviour; recorded as a sitting limitation.)
- **O-007 (Stage 2 gate recall Q3, "If I'm in ~/projects and I type cd notes, what folder am I in?")**: the answer is in a sentence on 2.4 that sits after the path-jargon paragraph and is easy to skip; Maya answered `~/projects/notes` from a half-memory plus a plausible guess and passed.

### Debrief (out of character)

- The only friction in the sitting came from one rejected recall answer; the sentence that triggered it is Stage 5 gate Q2, "After vim notes.txt, what makes Vim write your edit to the file?", together with the hint "Lesson 5.3: the colon command for putting the buffer into the file."
- The sentences Maya skipped and would have been punished for under the v0.1 charge ("cd.. with no space is a different word; bash cannot find it." on 2.3; the Stage 4 intro symbol table) cost nothing under v0.2.
- The screens a persona with this reading limit leaned on were always the `▶` lines: "Try each key, then type next", "Try a few command -v probes", "Try both; q leaves less; then next".
- The sentence "Here pwd shows the tutor's own folder, because that is where this practice prompt starts." on 1.3 is the one a spatially disoriented learner would hold up against the `stage1` path at the gate.
- The `vim --version   # prints version info and exits` line on 5.2 produced the longest unread output of the sitting.
