# Synthetic walkthrough — Leo, sitting 5

## Sitting

- Date: 2026-11-09
- Persona (file in `docs/sim-personas/`) and learner role: `leo.md`, Leo, 13, gamer and modder (`gamer-brute-forcer`), learner role: child
- Persona sheet version: 0.2.0
- Turn cap: 160. One turn = one `send` or one `raw`. Turns used: 132 (bundle `persona_inputs: 132`). The cap was not reached; the sitting ended on the finale.
- Simulation rules confirmed (zero forward knowledge, reading limit, friction meter): yes. Reading limit (v0.2): commands, `▶` lines, command-coloured text, and the first sentence of each paragraph; screens under eight lines read whole; everything else "did not read". Friction +1 per reading-only screen after the second in a row; +2 per rejection not understood; +1 mode confusion; -1 per gate cleared; quit at 8.
- Tutor revision and invocation: `d88c564` (script `7e126cf`); `sitting.py start` with no `--arg` (begins at the welcome screen), Bash `/bin/bash` 3.2.57. This is Leo's fifth sitting; no memory of earlier ones.
- `--info` lines the persona was shown, if any: none.

Process notes from the persona session (not tutor findings): twice I put a `note` and a `send` (and once a `note` and a second `send`) into one shell call against the one-command-per-call rule, and once a malformed `note` call went to a nonexistent path and was discarded. The note text is still attached to the right input in every case I can see; a maintainer reading `events.jsonl` should check the three notes around the 1.3 `pwd`/`date` turns and the 2.2 `ls -a` turn. One `note` was also run without the sandbox flag, was refused by the sandbox, and was re-run.

## Per screen

Friction is shown as the running total after each screen. "Reading-only" means the screen had no practice prompt. Reading-only streak is counted per README rule 6 and persona Reading section (charge from the third consecutive reading-only screen).

### SHELLTUTOR — a vimtutor prerequisite course (welcome, 18 lines)

- **Read**: skimmed. Read the `▶` line and the first sentence of each paragraph; did not read the second sentences ("Retry as much as you like", "the tutor never writes outside that folder", "Commands you run yourself have your full authority").
- **Jargon or assumed concept**: none quoted.
- **Monologue**: Lots of words. The arrow line says type next. Ok.
- **Input** `[context: nav]` → `next` → accepted.
- **Interpretation**: Orientation screen next.
- **Ladder rung shown**: none.
- **Friction**: 0 (reading-only streak 1).

### Orientation (21 lines)

- **Read**: skimmed. Read `shelltutor>`, the four navigation words, the `▶` line. Did not read: "The terminal is keyboard-only; you can't click mid-line", "Resize your terminal larger", "A fifth word, check, appears at gate tasks".
- **Jargon or assumed concept**: none.
- **Monologue**: shelltutor> is the thing I type at. Four words. Arrow says next.
- **Input** `[context: nav]` → `next` → accepted.
- **Ladder rung shown**: none.
- **Friction**: 0 (streak 2, no charge yet).

### STAGE 1 — Where am I? (intro, 11 lines)

- **Read**: all (under eight lines of body, read whole).
- **Jargon or assumed concept**: none.
- **Monologue**: Third talking screen, no game yet. Short though. next.
- **Input** `[context: nav]` → `next` → accepted.
- **Ladder rung shown**: none.
- **Friction**: 1 (reading charge: third reading-only screen in a row).

### 1.1 — running commands

- **Read**: skimmed. Read the three `echo` lines, the `▶` line. Did not read: "If bash says command not found or No such file, you mistyped…", "echo just repeats its words back. It is the simplest command…".
- **Jargon or assumed concept**: "spaces separate words" (comment, read, not understood as a rule).
- **Monologue**: Magic word echo hello. Type it exactly at shelltutor>.
- **Input** `[context: bash]` → `echo hello` → `hello`; then `echo I am at the shell` → `I am at the shell`; then `echo "I am at the shell"` → same. All accepted.
- **Interpretation**: Works. Quote marks make no visible difference to me.
- **Ladder rung shown**: none.
- **Friction**: 1 (practice screen; streak reset).

### 1.2 — keyboard habits

- **Read**: skimmed. Read the Tab line and the `▶`. Did not read the Ctrl+L, Ctrl+C and `↑` descriptions.
- **Jargon or assumed concept**: "shared part", "escape hatch" (not read).
- **Monologue**: Tab thing looks like autocomplete from game chat. Type echo p then Tab. It filled in poem.txt, like it said. The other keys are boring, skipping.
- **Input** `[context: bash]` → raw `echo p\t` → prompt shows `echo poem.txt`; then `""` (Enter) → `poem.txt`. Then `[nav]` `next`. All accepted.
- **Ladder rung shown**: none.
- **Friction**: 1.

### 1.3 — where am I, who am I, when is it

- **Read**: skimmed. Read the three command lines with their comments, the `▶`, and "Your prompt here ends in >." Did not read "A normal bash window's prompt usually ends in $; same idea, different decoration." (second sentence of its paragraph).
- **Jargon or assumed concept**: "pwd # print working directory — the folder you're in".
- **Monologue**: Three magic words. whoami first. It tells my name. pwd. Long folder name. date.
- **Input** `[context: bash]` → `whoami` → `[user]`; `pwd` → `/…/shelltutor-sim-home-…`; `date` → `Mon Nov  9 …`. Then `next`. All accepted.
- **Ladder rung shown**: none.
- **Friction**: 1.

### 1.4 — the shell, caught in the act

- **Read**: skimmed. Read `date` and `dtae` lines and the `▶`. Did not read "Read who is speaking. bash: is the shell…" or the terminal → shell → program paragraph.
- **Jargon or assumed concept**: none quoted.
- **Monologue**: I already did date. Type the wrong one on purpose: dtae. Error on purpose, fine.
- **Input** `[context: bash]` → `dtae` → `bash: dtae: command not found`. Then `next`.
- **Interpretation**: It says command not found, that is what the page said would happen.
- **Ladder rung shown**: none.
- **Friction**: 1.

### 1.5 — who else types here

- **Read**: skimmed. Read the first sentence of each paragraph and the `▶`. Did not read the AI-assistant paragraph or the three habits list.
- **Jargon or assumed concept**: "An AI assistant that "runs commands" for you is no exception." (not read past first sentence of paragraph).
- **Monologue**: Something about AI helpers. Not for me. Arrow says next for the gate.
- **Input** `[context: nav]` → `next` → accepted (reading-only, streak 1).
- **Ladder rung shown**: none.
- **Friction**: 1.

### STAGE 1 — GATE (recall, 9 lines)

- **Read**: all (under eight body lines), including "Type your answer in words; this is not the shell."
- **Jargon or assumed concept**: none on this screen; Q1 text "which character usually ends the prompt?".
- **Monologue**: A quiz. It says not the shell, type in words. The prompt I saw ended in >. Guess >.
- **Input** `[context: recall]` → `>` → rejected: "not quite. try again." + "Hint: Lesson 1.3: this tutor's prompt compared with a normal one." (+2)
- **Interpretation**: Wrong. I don't remember 1.3. The question lists four characters in brackets; try one.
- **Ladder rung shown**: hint on the first miss (lesson pointer). Not re-read; Leo did not return to 1.3. Not copied; it resolved nothing for him.
- **Friction**: 3.

Q1 second input `[recall]` → `$` → accepted. Q2 "What does pwd print?" → `the folder you are in` → accepted. Q3 "After whoami runs, where does its output go?" → `the screen` → accepted.

### STAGE 1 — GATE TASK

- **Read**: all (commands, `▶`).
- **Jargon or assumed concept**: "not in your history" (appeared in the check reply).
- **Monologue**: I already did all three a while ago. Just type check. ... But I DID run them! Whatever, it says run the circle ones.
- **Input** `[context: nav]` → `check` → rejected: `○ whoami  not yet: not in your history`, same for `pwd` and `date`; "Run the ones marked ○, then type check again." (+2 for a rejection not understood: he had run all three in 1.3)
- **Interpretation**: It does not believe me. I run them again.
- **Ladder rung shown**: message ("Run the ones marked ○"). Followed.
- **Friction**: 5.

Then `[bash]` `whoami`, `pwd` (output now ends in `/stage1`, different from the earlier path; he noted "weird"), `date`; `[nav]` `check` → three follow-ups. `[follow-up]` `[user]` for whoami; the full `…/stage1` path pasted; `Mon` for the weekday. All accepted.

### ✓ Stage 1 cleared.

- **Read**: skimmed (list of commands learned). Gate cleared, friction -1.
- **Friction**: 4 (reading-only streak 1).

### STAGE 2 — Paths and the filesystem (intro, 21 lines)

- **Read**: skimmed. Read the first sentence, the three command lines (`pwd`, `ls`, `cd`) and the `.` `..` `~` list, `▶`.
- **Jargon or assumed concept**: "path symbols", "the parent folder".
- **Monologue**: pwd, ls, cd - those look like game commands. next.
- **Input** `[nav]` `next` → accepted.
- **Friction**: 4 (streak 2, no charge).

### 2.1 — where you are

- **Read**: skimmed. Read the tree, `pwd` line and `▶`. Did not read "A folder can hold files and other folders. You are always standing in one folder; the shell calls it the current directory."
- **Jargon or assumed concept**: "the current directory".
- **Monologue**: Arrow line says run pwd. Like a map of folders.
- **Input** `[bash]` `pwd` → `/…/shelltutor-sim-home-…` (matches "you are here"). Then `next`.
- **Friction**: 4.

### 2.2 — ls: what is here

- **Read**: skimmed. Read the `ls`, `ls -p`, `ls -a` lines, `▶`. Did not read the `ls /` and `ls /usr/bin` lines' explanation.
- **Monologue**: ls shows names. Hidden stuff, cool (like hidden mods).
- **Input** `[bash]` `ls -p` → `numbers.txt poem.txt stage1/ stage2/`; `ls -a` → `. .. .progress .shelltutor_history …`; `next`.
- **Friction**: 4.

### 2.3 — cd: moving

- **Read**: skimmed. Read the `cd` command lines and the `▶`. Did not read "cd.. with no space is a different word" or the paragraph about where practice prompts start.
- **Jargon or assumed concept**: "go up one level (to the parent folder)".
- **Monologue**: Like /tp. Arrow line: cd .. then pwd then cd -.
- **Input** `[bash]` `cd ..` → no output; `pwd` → `/var/folders/…/T`; `cd -` → prints the previous path. Then `next`.
- **Interpretation**: Moved up one, then back.
- **Friction**: 4.

### 2.4 — names for places

- **Read**: skimmed. Read the symbol list, the path examples, the `mkdir name` line and `▶`. Did not read "Predict before you act. In ~/projects, the bare name notes means ~/projects/notes." (the answer to gate Q3 is in this paragraph).
- **Jargon or assumed concept**: "Relative paths start where you are", "Absolute paths start from the root, /".
- **Monologue**: Make a folder called demo, like making a mod folder.
- **Input** `[bash]` `mkdir demo`; `ls -p` → `demo/ …`; `next`. All accepted.
- **Friction**: 4.

### STAGE 2 — GATE

- **Read**: all (under eight body lines).
- **Q1** "What does cd .. do?" → `goes up one level` → accepted. **Q2** "What does ~ mean in a path?" → `your home folder` → accepted. **Q3** "If I'm in ~/projects and I type cd notes, what folder am I in?" → `notes` → **accepted** (no rejection, no hint). Monologue: I type cd notes so I'm in notes. Obvious.
- **Interpretation**: Right, apparently.
- **Ladder rung shown**: none.
- **Friction**: 4.

### STAGE 2 — GATE TASK

- **Read**: all (commands, `▶`).
- **Jargon or assumed concept**: "inside this stage's folder".
- **Input** `[bash]` `mkdir practice`; `cd practice`; `pwd` → `…/stage2/practice`; `[nav]` `check` → accepted.
- **Friction**: 4.

### ✓ Stage 2 cleared. (-1) → friction 3

### STAGE 3 — Files and operations (intro, 22 lines)

- **Read**: skimmed. Read first sentence, command list. Did not read "rm is immediate. It does not move things to a trash." in the paragraph's second sentence (the one-line sentence is the first of its paragraph after the heading's first sentence; Leo read it as "rm is immediate, ok").
- **Input** `[nav]` `next`. **Friction**: 3 (streak 2).

### 3.1 — creating: touch, mkdir

- **Read**: skimmed. Read the command lines and `▶`; did not read "(more on > in Stage 4)" or the closing "So: touch for empty files…".
- **Jargon or assumed concept**: "updates the timestamp of an existing one".
- **Input** `[bash]` `touch hello.txt`; `echo hello > notes.txt`; `next`. All accepted.
- **Friction**: 3.

### 3.2 — reading: cat, less

- **Read**: skimmed. Read the command lines and `▶`. Did not read the "Inside less, the screen takes over…" paragraph.
- **Jargon or assumed concept**: "the screen takes over".
- **Monologue**: Numbers filled the screen, prompt is gone. Screen said q leaves.
- **Input** `[bash]` `cat ../poem.txt` (4 lines); `less ../numbers.txt` (prompt replaced by the file name); raw `q` → back at `shelltutor>`; `next`.
- **Friction**: 3.

### 3.3 — copy, move, delete

- **Read**: skimmed. Read the command lines and `▶`. Did not read "There is no Trash and no undo. Look before you press Enter — you, or an assistant typing for you." beyond its first words.
- **Input** `[bash]` `cp hello.txt backup.txt`; `mv hello.txt hi.txt`; `rm backup.txt`; `next`. All accepted.
- **Friction**: 3.

### STAGE 3 — GATE

- **Read**: all.
- **Q1** "Which command creates an empty file?" → `touch` ✓. **Q2** "After rm important.txt, where is the file?" → `gone` ✓ (Screen said no trash, permanent). **Q3** "What single command renames old.txt to new.txt?" → `mv old.txt new.txt` ✓.
- **Friction**: 3.

### STAGE 3 — GATE TASK

- **Read**: all.
- **Input** `[bash]` `echo hello > notes.txt`; `cp notes.txt backup.txt`; `mv notes.txt done.txt`; `rm backup.txt`; `[nav]` `check` → cleared.
- **Friction**: 3.

### ✓ Stage 3 cleared. (-1) → friction 2

### STAGE 4 — Commands, streams, composition (intro, 18 lines)

- **Read**: skimmed. Read the symbol list and `▶`. Did not read the first paragraph.
- **Jargon or assumed concept**: title "streams", "composition".
- **Monologue**: Weird symbols list. next.
- **Input** `[nav]` `next`. **Friction**: 2 (streak 2).

### 4.1 — reading a command

- **Read**: skimmed. Read the grammar line and the examples. Did not read "Spaces matter. The shell splits on spaces; quote a name that has one:" explanation beyond its first sentence.
- **Jargon or assumed concept**: "command options arguments", "# option + argument", "an argument with a space — quoted".
- **Input** `[bash]` `command -v ls` → `/bin/ls`; `command -v vim` → `/usr/bin/vim`; `next`.
- **Friction**: 2.

### 4.2 — the pipe

- **Read**: skimmed. Read the pipeline examples and `▶`. Did not read "Most important idea in the shell." second sentence or the "Each piece is a normal command; only the connector is new" line.
- **Input** `[bash]` `seq 1 100 | wc -l` → `100`; `ls /usr/bin | grep ^a | wc -l` → `41`; `next`.
- **Friction**: 2.

### 4.3 — redirection

- **Read**: skimmed. Read the `>` `>>` `<` list and examples.
- **Jargon or assumed concept**: "A redirect sends it to a file, and > replaces it without asking, whoever typed the line."
- **Input** `[bash]` `echo first > greeting.txt`; `echo second >> greeting.txt`; `cat greeting.txt` → `first` / `second`; `next`.
- **Friction**: 2.

### 4.4 — globs (reading-only, 17 lines)

- **Read**: skimmed. Read the three `*.txt` command lines and `▶`; first sentence only of "Predict before you act. rm * removes everything…".
- **Jargon or assumed concept**: "The shell expands them before the command sees them."
- **Monologue**: Star matches many files. Arrow says next for the gate.
- **Input** `[nav]` `next`. **Friction**: 2 (streak 1).

### STAGE 4 — GATE

- **Read**: all.
- **Q1** "What does command -v vim print, if Vim is installed?" → `/usr/bin/vim` ✓. **Q2** "What is the difference between > and >>?" → `> replaces and >> adds` ✓. **Q3** "Why does vim my notes.txt open two files instead of one?" → `because of the space, it splits into my and notes.txt` ✓.
- **Friction**: 2.

### STAGE 4 — GATE TASK

- **Read**: all.
- **Input** `[bash]` `seq 1 100 | wc -l > count.txt`; `ls *.txt` → `count.txt greeting.txt poem.txt seed.txt`; `[nav]` `check` → cleared first time.
- **Friction**: 2.

### ✓ Stage 4 cleared. (-1) → friction 1

### STAGE 5 — Ready for vimtutor (intro, 15 lines)

- **Read**: all (first sentences and `▶`; screen body at eight lines).
- **Jargon or assumed concept**: "a command that prints-and-exits and one that takes over the terminal".
- **Input** `[nav]` `next`. **Friction**: 1 (streak 2).

### 5.1 — print-and-exit vs full-screen

- **Read**: skimmed. Read the exit-keys line, `man ls` and `▶`.
- **Input** `[bash]` `man ls` (no visible change in the captured screen); raw `q` → back at `shelltutor>`; `next`.
- **Friction**: 1.

### 5.2 — entering and leaving Vim

- **Read**: skimmed. Read the `vim --version`, `vim`, and `:q!` lines and `▶`.
- **Monologue**: Whole screen is tildes. It says type :q Enter to exit. Same as the tutor said.
- **Input** `[bash]` `vim --version` (a long page of build text); `vim`; `:q` → back at `shelltutor>`; `next`.
- **Friction**: 1.

### 5.3 — buffer vs file (reading-only, 21 lines)

- **Read**: skimmed. Read the `:w` `:q` `:q!` `:wq` list and `▶`; first sentence only of the opening paragraph.
- **Jargon or assumed concept**: "Vim reads it into a buffer — a copy in memory", "buffer".
- **Monologue**: Buffer? No idea. The list has :w :q :q! :wq like game commands. Arrow says next to practise.
- **Input** `[nav]` `next`. **Friction**: 1.

### 5.4 — practice: discard, then save

- **Read**: skimmed. Read every indented step.
- **Jargon or assumed concept**: "type i to enter insert mode (vimtutor will teach modes)".
- **Input** `[bash]` `vim practice.txt` ([file shows `before`]); raw `i`; raw `abc`; raw `\x1b`; `:q!`; `cat practice.txt` → `before`. Then `vim practice.txt`; raw `i`; raw `xyz`; raw `\x1b`; `:wq`; `cat practice.txt` → `xyzbefore`; `[nav]` `next`.
- **Interpretation**: It saved xyz. Cool.
- **Friction**: 1.

### 5.5 — calling vimtutor (reading-only, 19 lines)

- **Read**: skimmed. Read `command -v vimtutor` and `▶`.
- **Monologue**: Install stuff, not me. Arrow says next for the gate.
- **Input** `[nav]` `next`. **Friction**: 1 (streak 1).

### STAGE 5 — GATE (recall)

- **Q1** "How do you exit man ls?" → `press q` ✓. **Q2** "After vim notes.txt, what makes Vim write your edit to the file?" → `:wq` ✓. **Q3** "If you open notes.txt in vim, type some letters, and quit with :q! — did the file on disk change?" → `no` ✓.
- **Friction**: 1.

### STAGE 5 — GATE TASK (phase 1 and 2)

- **Read**: all.
- **Input** phase 1: `[bash]` `cat practice.txt` → `before`; `vim practice.txt`; raw `i`; raw `qqq`; raw `\x1b`; `:q!`; `cat practice.txt` → `before`; `[nav]` `check` → phase 2 screen. Phase 2: `vim practice.txt`; raw `i`; raw `z`; raw `\x1b`; `:wq`; `cat practice.txt` → `zbefore`; `check` → finale text ending `[exited 0]`.
- **Ladder rung shown**: none.
- **Friction**: 0 (gate cleared, -1).

## Per gate

| Gate | Recall attempts and rejected inputs | Rung reached | Task attempts | `check` results | Cleared |
| --- | --- | --- | --- | --- | --- |
| Stage 1 | Q1 `>` rejected, then `$`; Q2, Q3 first try | hint (lesson 1.3 pointer) | 2 `check`s | first: `○ whoami`, `○ pwd`, `○ date` ("not in your history"); second: all ✓ then three follow-ups right first try | yes |
| Stage 2 | all first try (Q3 `notes` accepted) | none | 1 | pass | yes |
| Stage 3 | all first try | none | 1 | pass | yes |
| Stage 4 | all first try | none | 1 | pass | yes |
| Stage 5 | all first try | none | 1 per phase | pass, pass | yes |

## End of sitting

- Final friction and where the persona quit: 0 (never reached 8). He did not quit; the sitting ended on the finale (`[exited 0]`, "You're ready for vimtutor.").
- Friction by source: reading charges +1 (Stage 1 intro, third reading-only screen); rejections +4 (2 x +2: Stage 1 gate Q1 `>`; Stage 1 task first `check`); mode confusion 0; gates cleared -5 (stages 1 to 5). Running total 1 + 4 - 5 = 0. Peak 5 at the Stage 1 gate task.
- Stages or module cleared: Stages 1, 2, 3, 4 and 5. Finale reached.
- Equivalent human sitting time (estimate): about 35 to 45 minutes for a real thirteen-year-old with this much skipping, mostly in the Stage 5 Vim steps and the stage 3 and 4 practice; no wall clock was taken.

### Candidate F-nnn

- **F-A (a wrong answer accepted)** Stage 2 gate, Q3 "If I'm in ~/projects and I type cd notes, what folder am I in?" — input `notes` was accepted. The correct answer is `~/projects/notes`. Leo had not read the sentence that teaches it (2.4: "In ~/projects, the bare name notes means ~/projects/notes.") and still passed with the bare name. A recall check that accepts the word the question repeats does not test the relative-path idea.
- **F-B (a true statement the learner reads as false)** Stage 1 gate task, input `check` right after `whoami`, `pwd` and `date` were run during lesson 1.3: the reply listed all three as `○ … not yet: not in your history`. He ran them in the lesson, so the message reads as the tutor not believing him. Candidate if a maintainer decides history before the gate task should count; otherwise an O.

### Candidate O-nnn

- **O-A (hint on the first miss that does not help a learner who skipped the lesson)** Stage 1 gate Q1, input `>`: "Hint: Lesson 1.3: this tutor's prompt compared with a normal one." The answer sentence in 1.3, "A normal bash window's prompt usually ends in $; same idea, different decoration." is the second sentence of its paragraph, which Leo does not read. He then answered by trying the four characters listed in the question.
- **O-B (pace)** Stage 1 intro: welcome, orientation and Stage 1 intro are three reading-only screens before the first practice prompt (`1.1`). Streak charge +1 at "STAGE 1 — Where am I?" (11 lines).
- **O-C (jargon)** 1.3 "pwd # print working directory — the folder you're in"; 2.1 "the shell calls it the current directory"; 2.4 "Relative paths start where you are"; 4.1 "an argument with a space — quoted"; 5.3 "Vim reads it into a buffer — a copy in memory"; 5.4 "type i to enter insert mode (vimtutor will teach modes)". Leo passed every gate that quoted these words by using what he did at the prompt, not the sentence.
- **O-D (cwd shift without a statement Leo reads)** Stage 1 task: after `check`, the first `pwd` on re-run ended in `/stage1`, where the earlier `pwd` in 1.3 ended in the sandbox root. Nothing on the screen he read said the practice folder had changed; he called it "weird".
- **O-E (mode, no confusion this sitting)** No input went to the wrong prompt. "Type your answer in words; this is not the shell." (Stage 1 gate) was read in full because the screen is under eight lines, and held for all five recall gates. Recorded because Leo's v0.1 sittings failed here.
- **O-F (screen capture)** 5.2, input `vim`: the `screen` text for a full-screen program is one long line of tildes with the splash text run together; readable only for the `:q<Enter>` line. This is a capture limit, not a tutor sentence.

### Debrief (out of character)

Sentences that mattered: "A normal bash window's prompt usually ends in $; same idea, different decoration." sits in the second sentence of a paragraph, so a skimmer misses the only place the Stage 1 Q1 answer lives. "In ~/projects, the bare name notes means ~/projects/notes." is the sentence Q3 depends on, and it was skipped and not needed. "Run the ones marked ○, then type check again." followed "not in your history", which contradicted what the learner had just done, and cost 2 points. "this is not the shell" was read this time and no recall answer went to bash. Stages 3 to 5 produced no friction because every instruction was a command line to copy.
