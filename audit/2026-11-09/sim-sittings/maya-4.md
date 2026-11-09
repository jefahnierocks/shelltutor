---
title: Synthetic sitting - maya-4
category: process
component: sim-sittings
status: active
version: 0.1.0
last_updated: 2026-11-09
tags: [phase-a-sim, sitting, maya, round-4]
priority: medium
---

# Synthetic walkthrough - maya-4

## Sitting

- Date: 2026-11-09
- Persona (file in `docs/sim-personas/`) and learner role: `maya.md`, Maya, 19, search-first-skimmer; adult beginner
- Persona sheet version: 0.2.0
- Simulation rules confirmed (zero forward knowledge, reading limit, friction meter): yes. Four prose lines then commands; bold and `▶` lines always read; density charge only at the turn where a skipped line causes a rejection or wrong turn; +2 per rejection she does not understand; +1 mode confusion; -1 per gate cleared (unfloored); quit at 8.
- Tutor revision and invocation: `3045f88` (script `13847ef`); `sitting.py start` with `--bash /bin/bash` (3.2.57), no `--arg` (begins at the welcome screen).
- `--info` lines the persona was shown, if any: none.

Method note: one input per turn, `note` before every `send`/`raw`. In three early turns a `note` and a `send` were issued in the same shell message (strictly ordered, results unaffected); everything after was one command per call. `raw` accepted typed text such as `echo p\t` and `iabc`.

## Per screen

(Compact blocks. Where nothing is listed under Jargon the screen carried none she registered. Friction is the running total.)

### welcome - SHELLTUTOR
- **Read**: all. **Jargon**: "vimtutor prerequisite course". **Monologue**: black hacker app, a course; says type next. **Input** `[nav]` `next` -> accepted. **Rung**: none. **Friction** 0.

### orientation - Orientation
- **Read**: skimmed (skipped the four-words list and the "fifth word, check" line). **Jargon**: "keyboard-only; you can't click mid-line to move the cursor". **Monologue**: next to begin. **Input** `[nav]` `next` -> accepted. **Friction** 0.

### 1 intro - STAGE 1
- **Read**: all (short). **Input** `[nav]` `next` -> accepted. **Friction** 0.

### 1.1 - running commands
- **Read**: skimmed (skipped "If bash says command not found or No such file..." and "echo just repeats..."). **Jargon**: "bash", "the shape of every command you'll meet". **Monologue**: three lines to type, do them in order. **Inputs** `[bash]` `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` -> all printed their words. **Interpretation**: the quotes did nothing visible; "why quotes then". **Rung**: none. **Friction** 0.

### 1.2 - keyboard habits
- **Read**: all (four key rows are command-like). **Jargon**: "Tab bash finishes a word", "escape hatch". **Inputs** `[bash]` raw `echo p<Tab>` -> `echo poem.txt` ; raw Enter -> `poem.txt`; raw Up -> `echo poem.txt` back; raw Ctrl+C -> fresh prompt; raw Ctrl+L -> screen cleared (lesson text gone, as promised). `[nav]` `next`. **Interpretation**: all four keys did what the screen said. **Friction** 0.

### 1.3 - where am I, who am I, when is it
- **Read**: skimmed (skipped "Your prompt here ends in >. A normal bash window's prompt usually ends in $; same idea, different decoration." - the fifth prose line). **Jargon**: "print working directory", "logged in as". **Inputs** `[bash]` `whoami`, `pwd`, `date` -> `[user]`, a long path, a date. `[nav]` `next`. **Friction** 0.

### 1.4 - the shell, caught in the act
- **Read**: skimmed (skipped "Three parts, kept apart..." paragraph; read the terminal -> shell -> program line only as a diagram). **Jargon**: "bash: is the shell", "terminal -> shell -> program". **Inputs** `[bash]` `dtae` -> `bash: dtae: command not found`; `[nav]` `next`. **Interpretation**: the computer told me I made a typo. Fine. **Friction** 0.

### 1.5 - who else types here
- **Read**: skimmed (four lines; the "AI assistant" paragraph and the three habits list skipped except the bold-free list). **Input** `[nav]` `next`. **Friction** 0.

### Stage 1 gate - recall
- Q1 "which character usually ends the prompt?": monologue: "Don't remember reading this, something about > vs a dollar sign; guess the dollar sign." This was a knowing guess from the answer options; input `$` -> accepted. No friction for a guess she knows is a guess (0). Skipped sentence was "A normal bash window's prompt usually ends in $".
- Q2 "What does pwd print?": `the folder you are in` -> accepted.
- Q3 "After whoami runs, where does its output go?": `it comes back to me on the screen` -> accepted.
- **Rung**: none needed. **Friction** 0.

### Stage 1 gate task
- **Inputs** `[bash]` `whoami`, `pwd`, `date`; `[nav]` `check`; `[follow-up]` `[user]` (username), the full path (typed out, ending `/stage1`), `Mon` -> all accepted. Cleared. Note: this `pwd` ended in `/stage1`, the earlier one in 1.3 did not. **Friction** -1 (gate cleared).

### Stage 2 intro, 2.1 - where you are
- **Read**: all. **Jargon**: "current directory", tree diagram with "stage1/ stage2/". **Inputs** `[nav]` `next`; `[bash]` `pwd` -> the practice folder, matching "you are here". **Friction** -1.

### 2.2 - ls: what is here
- **Read**: skimmed (skipped hidden-files line and `ls /usr/bin` row). **Inputs** `[bash]` `ls -p` -> `numbers.txt poem.txt stage1/ stage2/`. `[nav]` `next`. **Friction** -1.

### 2.3 - cd: moving
- **Read**: skimmed (skipped everything after "Later stages start in a stage folder inside it" including the long cd path). **Jargon**: "parent folder". **Inputs** `[bash]` `cd ..` (no output, "nothing happened"), `pwd` -> parent path, `cd -` -> printed the practice path. `[nav]` `next`. **Interpretation**: first time I understood folders go up and down; the last bit of the path disappears. **Friction** -1.

### 2.4 - names for places
- **Read**: skimmed (read bold-free; skipped the path symbol list and "Absolute paths" row). **Jargon**: "relative", "absolute", "root". **Inputs** `[bash]` `mkdir demo`, `ls -p` -> `demo/` appears. `[nav]` `next`. **Friction** -1.

### Stage 2 gate - recall
- Q1 `goes up one folder` -> accepted. Q2 `your home folder` -> accepted. Q3 "If I'm in ~/projects and I type cd notes" `~/projects/notes` -> accepted (from the "Predict before you act" line on 2.4). **Friction** -1.

### Stage 2 gate task
- **Inputs** `[bash]` `mkdir practice`, `cd practice`, `pwd` (ended `/stage2/practice`); `[nav]` `check` -> cleared. **Friction** -2 (gate cleared).

### Stage 3 intro, 3.1 - creating
- **Read**: skimmed (read to "To create a file with content, use redirection (Stage 4)"; skipped the closing paragraph). **Inputs** `[bash]` `touch hello.txt`, `mkdir notes`. `[nav]` `next`. **Friction** -2.

### 3.2 - reading: cat, less
- **Read**: skimmed (skipped "Inside less ... Space or f ... b" and "Important: when less takes over, the prompt is gone"). **Jargon**: "the screen takes over". **Inputs** `[bash]` `cat ../poem.txt` -> four lines of poem; `less ../numbers.txt` -> numbers, no shell prompt (reply showed `[prompt] ../numbers.txt`); raw `q` -> back at `shelltutor>`. **Interpretation**: the ▶ line said q leaves less, so I pressed q. **Friction** -2.

### 3.3 - copy, move, delete
- **Read**: skimmed (read bold "rm deletes. Immediately and permanently."; skipped the "no Trash and no undo" line and safety-habit line partly). **Inputs** `[bash]` `cp hello.txt backup.txt`, `mv hello.txt hi.txt`, `mv hi.txt notes/`, `ls` -> `backup.txt notes`, `rm backup.txt` -> accepted. **Friction** -2.

### Stage 3 gate - recall
- Q1 `touch` -> accepted. Q2 `gone` -> accepted. Q3 `mv old.txt new.txt` -> accepted. **Friction** -2.

### Stage 3 gate task
- Monologue at step 1: "need a file containing the word hello; touch only makes empty ones; earlier there was an echo ... > greeting.txt line; copy its shape." Inputs `[bash]` `echo hello > notes.txt`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt`; `[nav]` `check` -> cleared on the first try. **Friction** -3 (gate cleared).

### Stage 4 intro, 4.1 - reading a command
- **Read**: skimmed (skipped the "Spaces matter. The shell splits on spaces; quote a name that has one" paragraph, which is the sentence that matters later). **Jargon**: "options", "arguments", "exits 0". **Inputs** `[bash]` `command -v ls` -> `/bin/ls`; `command -v vim` -> `/usr/bin/vim`. `[nav]` `next`. **Friction** -3 (no charge yet; the skipped line surfaces at the gate, see below).

### 4.2 - the pipe
- **Read**: skimmed. **Jargon**: "pipe", "input", "pipeline". **Inputs** `[bash]` `seq 1 100 | wc -l` -> `100`; `ls /usr/bin | grep ^a | wc -l` -> `41`. `[nav]` `next`. **Friction** -3.

### 4.3 - redirection
- **Read**: skimmed. **Jargon**: "redirect", "append". **Inputs** `[bash]` `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt` -> `first second`. `[nav]` `next`. Skipped the `wc -w < poem.txt` and `programs.txt` rows. **Friction** -3.

### 4.4 - globs
- **Read**: all (short). **Input** `[nav]` `next`. **Friction** -3.

### Stage 4 gate - recall
- Q1 `the path to vim` -> accepted.
- Q2 "What is the difference between > and >>?": see per-gate. Four inputs, three rejected.
- Q3 "Why does vim my notes.txt open two files instead of one?": `the space splits it into two names` -> rejected; `the shell splits on spaces` -> accepted.
- **Friction**: +2 (Q2 attempt 1), +2 (Q2 attempt 2), +2 (Q2 attempt 3), +2 (Q3 attempt 1) = +8, net 5 after the -3 already banked. **Reading charge**: +0 under v0.2 (the skipped line "Spaces matter. The shell splits on spaces..." did lead to a wrong turn on Q3 attempt 1, but the answer she gave was equivalent in meaning; the rejection is scored as a rejection, not double-counted as a reading charge). Q2 was not a skipped-line failure: she had read 4.3.

### Stage 4 gate task
- **Inputs** `[bash]` `seq 1 100 | wc -l > count.txt`, `ls *.txt` -> `count.txt greeting.txt poem.txt seed.txt`; `[nav]` `check` -> cleared first try. **Friction** 4 (gate cleared, -1).

### Stage 5 intro, 5.1 - print-and-exit vs full-screen
- **Read**: skimmed. **Jargon**: "print-and-exit", "full-screen", "manual page". **Inputs** `[bash]` `man ls` -> full-screen man page, first screen shown; raw `q` -> prompt returned (reply ended with a `:` pager prompt and `[prompt] shelltutor>`). `[nav]` `next`. **Friction** 4.

### 5.2 - entering and leaving Vim
- **Read**: skimmed. **Jargon**: "installed", "discard form". **Inputs** `[bash]` `vim --version` -> long version listing; `vim` -> screen of tildes with "type :q<Enter> to exit"; `:q` -> back at `shelltutor>`. `[nav]` `next`. **Friction** 4.

### 5.3 - buffer vs file
- **Read**: skimmed (read first four lines; skipped the :w/:q/:q!/:wq table's surrounding prose). **Jargon**: "buffer - a copy in memory", "write the buffer". **Monologue**: a buffer is an unsaved doc; :w saves; :q! throws it away. **Input** `[nav]` `next`. **Friction** 4.

### 5.4 - practice: discard, then save
- **Read**: all (mostly a command list). **Jargon**: "insert mode", "vimtutor will teach modes". **Inputs** `[bash]` `vim practice.txt`; raw `iabc` -> `-- INSERT --`; raw Esc; `:q!`; `cat practice.txt` -> `before`; then `vim practice.txt`; raw `ixyz`; raw Esc; `:wq`; `cat practice.txt` -> `xyzbefore`. `[nav]` `next`. **Friction** 4.

### 5.5 - calling vimtutor
- **Read**: skimmed. **Input** `[nav]` `next`. **Friction** 4.

### Stage 5 gate - recall
- Q1 "How do you exit man ls?" `press q`; Q2 "what makes Vim write your edit to the file?" `:wq`; Q3 "did the file on disk change?" `no` -> all accepted first try.

### Stage 5 gate task (two phases)
- Phase 1: `cat practice.txt`, `vim practice.txt`, raw `iqqq`, raw Esc, `:q!`, `cat practice.txt` -> `before`, `check`. Phase 2: `vim practice.txt`, raw `imm`, raw Esc, `:wq`, `cat practice.txt` -> `mmbefore`, `check` -> finale screen "You're ready for vimtutor." and `[exited 0]`. **Friction** 3 (gate cleared, -1).

## Per gate

- **Stage 1**: Recall one attempt per question; no rejections; Q1 answered with a knowing guess (`$`). Task one attempt; follow-ups accepted. Cleared.
- **Stage 2**: Recall one attempt per question; task one attempt. Cleared.
- **Stage 3**: Recall one attempt per question; task one attempt (`echo hello > notes.txt` used the redirection shape from 3.1). Cleared.
- **Stage 4**: Q1 one attempt. **Q2: four attempts**, rejected verbatim: `> overwrites the file and >> appends to the end` (hint: "Lesson 4.3: what each arrow does to a file that already exists."); `one replaces what is in the file and the other adds to the end of it` (hint plus "Answer in a few words, like the lesson did, not a full sentence."); `overwrite vs append` (same hint rung); accepted: `> overwrites, >> appends`. **Q3: two attempts**, rejected: `the space splits it into two names` (hint: "Lesson 4.1: what separates the words after vim, and what quotes do."); accepted: `the shell splits on spaces`. Task one attempt. Cleared.
- **Stage 5**: Recall one attempt per question; both task phases one attempt. Cleared.

## End of sitting

- **Final friction and where the persona stopped**: 3, never reached the quit threshold. Sitting ended at the finale (`[exited 0]`) after the Stage 5 gate. By-source breakdown: reading-limit charges 0; rejections 4 x (+2) = +8 (all at the Stage 4 gate: Q2 x3, Q3 x1); mode confusion 0; gates cleared 5 x (-1) = -5 (unfloored). Peak was 5 at the Stage 4 recall, before that gate cleared. Net 0 + 8 + 0 - 5 = 3. Gross positive friction 8 equals the quit threshold; against the unfloored meter it never reached it.
- **Stages or module cleared**: Stages 1, 2, 3, 4 and 5; finale reached.
- **Equivalent human sitting time (estimate)**: about 40 to 50 minutes for a fast skimmer; the four Stage 4 rejections plus rereading the lesson account for perhaps 5 of those.
- **Candidate F-nnn**
  - **Candidate F-A, Stage 4 gate Q2 ("What is the difference between > and >>?")**: the input `> overwrites the file and >> appends to the end` was rejected, as were `one replaces what is in the file and the other adds to the end of it` and `overwrite vs append`. Only `> overwrites, >> appends` passed. A correct plain-language answer (and one using the lesson's two words) was rejected three times; the hint rung ("what each arrow does to a file that already exists") repeated verbatim and the added "few words" line is the only clue to the accepted shape.
  - **Candidate F-B, Stage 4 gate Q3 ("Why does vim my notes.txt open two files instead of one?")**: `the space splits it into two names` was rejected; accepted only `the shell splits on spaces`. The first answer states the same fact. The 4.1 sentence it matches is "The shell splits on spaces; quote a name that has one."
  - **Candidate F-C, Stage 5.1/5.2 (`man ls` then raw `q`, `vim`, `:q`)**: the replies returned to the persona show raw terminal artifacts (a trailing `:` pager prompt, `Pzz\`, concatenated tilde lines, text run together such as `VIM - Vi IMprovedversion 9.1.1752by Bram Moolenaar`). This is likely a harness rendering matter rather than the tutor; flagged because the persona could not tell from the reply alone that `q` and `:q` had worked, only from the `[prompt] shelltutor>` marker.
- **Candidate O-nnn**
  - **O-A, screen 1.2**: "(Other shells and setups differ.) Try: type echo p, press Tab; it becomes echo poem.txt, then press Enter to run it." The poem.txt completion depends on the folder; the sentence says it becomes `echo poem.txt` and it did, but a learner would not know why `p` found only one file.
  - **O-B, screen 1.3 vs 1.3-task**: "Here pwd shows the tutor's own folder, because that is where this practice prompt starts." The Stage 1 gate-task `pwd` printed a path ending in `/stage1`, while the same command in 1.3 did not, and the gate follow-up asked for the full path with no hint that it had changed.
  - **O-C, screen 3.1/gate task 3**: "To create a file with content, use redirection (Stage 4): echo "first line" > greeting.txt". The Stage 3 gate task step "create a file notes.txt containing the word hello" needs exactly this, and the only place it appears is a single "for later" sentence, in a lesson whose ▶ line says "Make a few". Maya passed only by pattern-copying.
  - **O-D, screen 4.1**: "Spaces matter. The shell splits on spaces; quote a name that has one:" sits in the fifth prose block under the grammar lesson and is what Stage 4 Q3 asks about; at Maya's four-line limit it falls just outside the read lines. (Skipped sentence quoted here, but the +1 reading charge was not applied because the rejection is better explained by F-B.)
  - **O-E, screen 4.2**: "Most important idea in the shell." followed by seven pipelines; the density without a ▶ that picks one.
  - **O-F, screen 5.3**: "Vim reads it into a buffer - a copy in memory." Buffer is introduced as a noun with a diagram that reads `file on disk -> buffer in memory -> file on disk` and a row of parenthesised words "(read) (edit) (write)" that do not align with the arrows on a narrow terminal.
  - **O-G, Stage 4 gate Q2 and Q3 hint rung**: "Answer in a few words, like the lesson did, not a full sentence." appears only from the second rejection of a question; the first rejection on each question shows only the lesson pointer.
- **Debrief** (out of character, five lines at most):
  1. Stage 4 Q2 and Q3 took four of the five gate-sized stalls; both failed on phrasing, not on knowledge, and the passing phrases were the lesson's own ("overwrites", "appends", "the shell splits on spaces").
  2. "Answer in a few words, like the lesson did, not a full sentence." is the first sentence that told Maya how the matcher wanted to be answered, and it arrived after one rejection had already been scored.
  3. "To create a file with content, use redirection (Stage 4)" in 3.1 is the only teaching of Stage 3 gate task step 1.
  4. "Spaces matter. The shell splits on spaces; quote a name that has one:" is the line that Q3 tests and the one Maya skipped.
  5. The guess on Stage 1 Q1 (`$`) passed because the option list included the answer; "Your prompt here ends in >. A normal bash window's prompt usually ends in $" was outside her read lines.
