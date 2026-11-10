# Synthetic walkthrough — Leo, sitting 8

## Sitting

- Date: 2026-11-10
- Persona (file in `docs/sim-personas/`) and learner role: `leo.md` (Leo, 13, `gamer-brute-forcer`); learner role: child
- Persona sheet version: 0.3.1
- Scripted errors performed: (a) leading slash at the first command of each stage, five of five (`/echo hello` 1.1, `/pwd` 2.1, `/touch hello.txt` 3.1, `/wc -l poem.txt` 4.1, `/man ls` 5.1); (b) one-word guess at the first recall answer of each gate, five of five (`dtae`, `pwd`, `ls`, `wc`, `command`); (c) `check` first at the Stage 1 gate task, once.
- Turn cap: 240 (round 8). One turn = one `send` or one `raw`. Turns used: 174
- Simulation rules confirmed (zero forward knowledge, reading limit, friction meter): yes. Reading limit per leo.md: commands, `▶` lines, command-colour text and the first sentence of each paragraph; screens under eight lines read whole. Friction per README rule 6, leo.md Reading section and the scripted-error scoring; quit at 8.
- Tutor revision and invocation: 35b9e26 (script 7e01410); no `--arg`, so it began at the welcome screen; Bash `/bin/bash` 3.2.57.
- `--info` lines the persona was shown, if any: none.
- Process note: once (Stage 1 task, `pwd` and its note) a `note` and a `send` were issued in the same tool batch instead of strictly one after the other. Order was preserved and nothing was lost.

## Per screen

Compact blocks. "Read" is "all" for screens under eight lines and otherwise "skimmed" with the skipped parts named. Friction is the running total.

### welcome — shelltutor
- **Read**: all (screen is 15 lines; read commands, the stage list and the `▶` line; skipped "Everything you type runs in a real shell...").
- **Jargon**: none.
- **Monologue**: Five stages, no timer. Says type next.
- **Input** `[nav]` → `next` → accepted. **Friction**: 0 (reading-only screen 1).

### orientation — Orientation
- **Read**: all. **Jargon**: none. **Monologue**: A real shell prompt below. next.
- **Input** `[nav]` → `next` → accepted. **Friction**: 0 (reading-only 2).

### Stage 1 intro — Stage 1: Where am I?
- **Read**: all. **Jargon**: none. **Monologue**: More talking. Boring.
- **Input** `[nav]` → `next` → accepted. **Friction**: 1 (third reading-only screen in a row, +1).

### 1.1 — Running a command
- **Read**: skimmed (read the three `echo` lines and `▶`; skipped "Notice the quotes never print" detail beyond the first sentence).
- **Jargon**: "the words you hand it".
- **Monologue**: Commands start with `/` like in Minecraft, so `/echo hello` (scripted a).
- **Input** `[bash]` → `/echo hello` (scripted) → `bash: /echo: No such file or directory`. Ladder: message only (the screen's own line "look for a stray / or a missing space").
- **Interpretation**: The error plus the "stray /" sentence on screen were enough; he took the slash off.
- **Input** `[bash]` → `echo hello` → `hello`; then `echo "I am at the shell"` → `I am at the shell`; `next`.
- **Friction**: 1 (scripted a: recovered in 1 further input, scored 0).

### 1.2 — Four keys
- **Read**: skimmed (read the four key lines; skipped the Ctrl+C paragraph).
- **Jargon**: none. **Monologue**: Keys; skipping trying them.
- **Input** `[nav]` → `next`. Did not try Tab, Up, Ctrl+C or Ctrl+L. **Friction**: 1.

### 1.3 — Where am I, who am I, when is it
- **Read**: all commands; skipped "This prompt ends in >" (a second sentence in its paragraph) at first read.
- **Input** `[bash]` → `pwd`, `whoami`, `date` (all output seen), `next`. **Friction**: 1.

### 1.4 — The shell, caught in the act
- **Input** `[bash]` → `dtae` → `bash: dtae: command not found`; `next`. Expected, not a rejection. **Friction**: 1.

### 1.5 — Who else types here
- **Read**: skimmed (read the three habit lines; skipped the AI-assistant paragraph). **Jargon**: "An AI assistant that 'runs commands' for you".
- **Input** `[nav]` → `next`. **Friction**: 1 (reading-only screen 1 after practice screens, no charge).

### Stage 1 gate — recall (3 questions)
- Q1 "In a normal bash window (not this tutor), which character usually ends the prompt?" `[recall]` → `dtae` (scripted b) → `not quite. hint: Lesson 1.3: this tutor's prompt compared with a normal one.` Rung: hint. Resolved: Leo remembered the ">" sentence and picked from the offered characters → `$` accepted (1 further input, scored 0).
- Q2 "What does pwd print?" → `the folder` → accepted.
- Q3 "After whoami runs, where does its output go?" → `the screen` → accepted.

### Stage 1 gate task
- `[bash]` `check` first (scripted c) → checklist, three `[ ]` rows "seen: none typed since the task began", "Finish the step marked [ ], then type check again." Reply plus the screen were enough: his next input was `whoami` (1 further input, scored 0). The checklist marks open rows `[ ]`, not `○`.
- `whoami`, `pwd`, `date`, `check` → three follow-ups: whoami → `[user]`; pwd → the stage1 path copied from the screen; date day → `Tue`. All accepted. Stage 1 cleared.
- **Friction**: 1 - 1 (gate) = 0.

### Stage 2 intro — Stage 2: Paths
- Reading-only (1). `next`. **Friction**: 0.

### 2.1 — Where you are
- **Read**: skimmed (tree and `pwd` line; skipped the last sentence). **Jargon**: "the current directory".
- **Monologue**: A tree with a you-are-here arrow, like a map.
- **Input** `[bash]` → `/pwd` (scripted a) → `bash: /pwd: No such file or directory`. This screen has no stray-slash sentence; he recovered from the 1.1 memory and the error name. `pwd` next (1 further input, scored 0). **Friction**: 0.

### 2.2 — What is here
- `ls` → `numbers.txt  poem.txt  stage1  stage2`; `ls -p` → slashes on folders; skipped `ls -a` and `ls /`. `next`. **Friction**: 0.

### 2.3 — Moving
- `cd ..` (no output), `pwd` (shorter name), `cd -` (printed the old place). `next`. **Did not read**: "cd.. with no space is a different word", "never \". **Friction**: 0.

### 2.4 — Home and back
- `cd`, `pwd` (a `...-userhome-...` folder), `cd /var/folders/.../shelltutor-sim-home-...` copied from the screen. `next`. **Jargon**: "~ is its short name" (not tried here). **Friction**: 0.

### 2.5 — Names for places
- **Read**: skimmed (commands only). **Jargon**: "A relative path starts where you are", "An absolute path starts from /" ("relative", "absolute", "path" quoted verbatim; not understood, did not read the paragraph beyond its first sentence).
- `cd stage1`, `ls ..`, `cd ..`, `echo ~` (printed the userhome path). `next`. **Friction**: 0.

### 2.6 — Making a folder
- `mkdir demo`, `ls -p`, `cd demo`, `pwd`. `next`. **Friction**: 0.

### Stage 2 gate — recall
- Q1 "What does cd .. do?" → `pwd` (scripted b) → `not quite. hint: Lesson 2.3: the two dots are the name of one particular other folder.` → `goes up` accepted (1 further input, scored 0).
- Q2 "What does ~ mean in a path?" → `home` accepted.
- Q3 "If I'm in ~/projects and I type cd notes, what folder am I in?" → `notes` → rejected: `not quite. hint: Lesson 2.5: a relative name starts from the folder you are already in.` Rung: hint; it contains the word "relative", which Leo does not know; read as static. Unscripted rejection, +2. Next attempt `projects/notes` → accepted.
- **Friction**: 2 (rejection +2).

### Stage 2 gate task
- `mkdir practice`, `cd practice`, `pwd` (stage2/practice, so the tutor had already put him in stage2), `check` → Stage 2 cleared.
- **Friction**: 2 - 1 = 1.

### Stage 3 intro; 3.1 Making files
- Intro: reading-only (1), "rm removes for good. There is no Trash." read.
- 3.1: `/touch hello.txt` (scripted a) → `bash: /touch: No such file or directory`; `touch hello.txt` (1 further input, scored 0); `echo hi > words.txt`; `mkdir notes`; `ls -p` → `hello.txt  notes/  words.txt`. **Did not read**: "> sends what echo prints into a file" (the sentence introducing `>`). **Friction**: 1.

### 3.2, 3.3, 3.4, 3.5
- 3.2: `cat words.txt` → `hi`; `cat ../poem.txt` → the poem; skipped `cat hello.txt`.
- 3.3: `less ../numbers.txt`, raw space (paged), raw `q`; prompt back.
- 3.4: `cp hello.txt backup.txt`, `mv hello.txt hi.txt`, `mv hi.txt notes/`, `ls -p notes` → `hi.txt`.
- 3.5: `ls`, `rm backup.txt`, `ls`. **Friction**: 1.

### Stage 3 gate — recall
- Q1 "Which command creates an empty file?" → `ls` (scripted b) → `not quite. hint: Lesson 3.1: the file command that can also update a timestamp.` Resolved by the offered choices and by his own `touch hello.txt` from 3.1 (he could not read "timestamp"). `touch` accepted (1 further input, scored 0).
- Q2 "After rm important.txt, where is the file?" → `gone` accepted.
- Q3 "What single command renames old.txt to new.txt?" → `mv old.txt new.txt` accepted.
- Task: `echo hello > notes.txt`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt`, `check` → Stage 3 cleared. **Friction**: 1 - 1 = 0.

### Stage 4 intro; 4.1 to 4.6
- Intro: reading-only (1).
- 4.1 "The parts of a command": **Jargon**: "A command line is a name, then options, then arguments" (quoted; not understood; did not read the "name wc, option -l, argument poem.txt" comment). `/wc -l poem.txt` (scripted a) → `bash: /wc: No such file or directory`; `wc -l poem.txt` → `4 poem.txt` (1 further input, scored 0); `echo "hello world"`; `command -v vim` → `/usr/bin/vim`.
- 4.2: `touch my notes.txt`, `ls`, `touch "my notes.txt"`, `ls`.
- 4.3: `seq 1 100 | wc -l` → 100; `ls /usr/bin | wc -l` → 932; `ls /usr/bin | sort | head`. **Jargon**: "What a command prints is a stream of lines". Did not read it.
- 4.4: `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt`.
- 4.5: `ls /usr/bin | wc -l > count-of-programs.txt`, `cat count-of-programs.txt`.
- 4.6: `ls *.txt`, `wc -l *.txt` (the glob was shown, not understood as a word: "A name with * in it is called a glob" skimmed). **Friction**: 0.

### Stage 4 gate — recall
- Q1 "What does command -v vim print, if Vim is installed?" → `wc` (scripted b) → `not quite. hint: Lesson 4.1: command -v asks the shell about a command and answers in one line.` → `/usr/bin/vim` accepted (1 further input, scored 0).
- Q2 "What is the difference between > and >>?" → `>> adds more, > replaces` → rejected: `not quite. hint: Lesson 4.4: what each arrow does to a file that already exists.` Unscripted rejection, +2. Leo's reading: his answer says the same as the lesson, so the rejection is unexplained. Next attempt `single one writes over it and double puts at the end` → accepted.
- Q3 "Why does vim my notes.txt open two files instead of one?" → `because of the space` accepted.
- Task: `seq 1 100 | wc -l > count.txt`, `ls *.txt`, `check` → Stage 4 cleared.
- **Friction**: 0 + 2 - 1 = 1.

### Stage 5 intro; 5.1 to 5.6
- Intro: reading-only (1).
- 5.1: `/man ls` (scripted a) → `bash: /man: No such file or directory`; `man ls` (1 further input, scored 0); raw `q` left it.
- 5.2: **Jargon**: none new; "<Enter> means the key, not letters to type" read. `vim`, `:q`, prompt back.
- 5.3 "The copy and the file": reading-only. **Jargon**: "working copy". Skimmed. 
- 5.4: `vim practice.txt`, raw `i`, raw `abc`, raw Esc, `:q!`, `cat practice.txt` → `before`.
- 5.5: same with raw `xyz` and `:wq`; `cat practice.txt` → `xyzbefore`.
- 5.6: `command -v vimtutor` → `/usr/bin/vimtutor`. **Friction**: 1.

### Stage 5 gate — recall
- Q1 "How do you exit man ls?" → `command` (scripted b) → `not quite. hint: Lesson 5.1: the same single key leaves less.` → `q` accepted (1 further input, scored 0).
- Q2 "After vim notes.txt, what makes Vim write your edit to the file?" → `:wq` accepted.
- Q3 "If you open notes.txt in vim, type some letters, and quit with :q! — did the file on disk change?" → `no` accepted.
- Task phase 1: `cat practice.txt`, `vim practice.txt`, `i`, `qwe`, Esc, `:q!`, `cat practice.txt`, `check`. Phase 2: `vim practice.txt`, `i`, `lol`, Esc, `:wq`, `cat practice.txt`, `check` → finale, `[exited 0]`. Stage 5 cleared.
- **Friction**: 1 - 1 = 0.

## Per gate

| Gate | Recall attempts per question | Inputs rejected (verbatim) | Rung | Task | Cleared |
| --- | --- | --- | --- | --- | --- |
| 1 | Q1 2, Q2 1, Q3 1 | `dtae` (scripted b) | hint, once | `check` first (scripted c) showed three `[ ]` rows; then `whoami`, `pwd`, `date`, `check`; three follow-ups right first time | yes |
| 2 | Q1 2, Q2 1, Q3 2 | `pwd` (scripted b); `notes` | hint on each | `mkdir practice`, `cd practice`, `pwd`, `check` | yes |
| 3 | Q1 2, Q2 1, Q3 1 | `ls` (scripted b) | hint, once | four steps, `check` first time | yes |
| 4 | Q1 2, Q2 2, Q3 1 | `wc` (scripted b); `>> adds more, > replaces` | hint on each | `seq 1 100 \| wc -l > count.txt`, `ls *.txt`, `check` | yes |
| 5 | Q1 2, Q2 1, Q3 1 | `command` (scripted b) | hint, once | two phases, each `check` first time | yes |

## End of sitting

- **Final friction**: 0, at the finale (`[exited 0]`), turns used 174 of 240. Not quit. By source: reading charges +1 (Stage 1 intro, third reading-only screen in a row); unscripted rejections +4 (`notes` at the Stage 2 gate, `>> adds more, > replaces` at the Stage 4 gate); mode confusions 0; scripted errors 0 (all eleven recovered within one further input); gates cleared -5. Total 1 + 4 - 5 = 0.
- **Stages cleared**: 1, 2, 3, 4, 5 (all five), then the finale.
- **Scripted errors performed** (screen, exact input, reply verbatim, enough to recover, further inputs, friction):

| Screen | Input | Reply | Enough to recover | Further inputs | Friction |
| --- | --- | --- | --- | --- | --- |
| 1.1 (a) | `/echo hello` | `bash: /echo: No such file or directory` | yes (the screen's "look for a stray /" line plus the error) | 1 | 0 |
| Stage 1 recall Q1 (b) | `dtae` | `not quite. hint: Lesson 1.3: this tutor's prompt compared with a normal one.` | yes (offered characters plus 1.3's ">" sentence) | 1 | 0 |
| Stage 1 task (c) | `check` | three `[ ]` rows, "seen: none typed since the task began"; "Finish the step marked [ ], then type check again." | yes | 1 | 0 |
| 2.1 (a) | `/pwd` | `bash: /pwd: No such file or directory` | yes (relied on memory of 1.1; this screen carries no stray-slash line) | 1 | 0 |
| Stage 2 recall Q1 (b) | `pwd` | `not quite. hint: Lesson 2.3: the two dots are the name of one particular other folder.` | yes ("goes up", from the shorter `pwd` output in 2.3) | 1 | 0 |
| 3.1 (a) | `/touch hello.txt` | `bash: /touch: No such file or directory` | yes | 1 | 0 |
| Stage 3 recall Q1 (b) | `ls` | `not quite. hint: Lesson 3.1: the file command that can also update a timestamp.` | yes, by the offered choices and his own `touch`; "timestamp" was not read | 1 | 0 |
| 4.1 (a) | `/wc -l poem.txt` | `bash: /wc: No such file or directory` | yes | 1 | 0 |
| Stage 4 recall Q1 (b) | `wc` | `not quite. hint: Lesson 4.1: command -v asks the shell about a command and answers in one line.` | yes (`/usr/bin/vim` remembered) | 1 | 0 |
| 5.1 (a) | `/man ls` | `bash: /man: No such file or directory` | yes | 1 | 0 |
| Stage 5 recall Q1 (b) | `command` | `not quite. hint: Lesson 5.1: the same single key leaves less.` | yes (`q`) | 1 | 0 |

- **Every rejected recall answer, verbatim**: `dtae` (S1 Q1, scripted); `pwd` (S2 Q1, scripted); `notes` (S2 Q3); `ls` (S3 Q1, scripted); `wc` (S4 Q1, scripted); `>> adds more, > replaces` (S4 Q2); `command` (S5 Q1, scripted).
- **Equivalent human sitting time (estimate)**: about 45 to 60 minutes for a thirteen-year-old with 174 inputs, most of them one-line copies from the screen, plus two short stalls at the gate hints.

### Candidate F-nnn

- **F-a (Stage 4 gate, recall Q2, "What is the difference between > and >>?")**: the input `>> adds more, > replaces` was rejected with `not quite. hint: Lesson 4.4: what each arrow does to a file that already exists.`; `single one writes over it and double puts at the end` was accepted. Lesson 4.4 itself says "> replaces the file" and ">> adds to the end", so the first answer matches the lesson's own words. The accepted vocabulary appears narrower than the lesson's.
- **F-b (Stage 2 gate, recall Q3, "If I'm in ~/projects and I type cd notes, what folder am I in?")**: `notes` was rejected, which is defensible, but the screen has no hint that a full path is wanted; the hint then says "a relative name starts from the folder you are already in." A learner who answers `notes` has not been told which form of answer counts.
- No broken hint, dead end or false statement on screen was seen. Candidate F-a is a valid-answer rejection that needs a maintainer to reproduce it.

### Candidate O-nnn

- **O-a (Stage 2 gate hint, S2 Q3)**: "a relative name starts from the folder you are already in." uses "relative", which the persona cannot read; the hint did not resolve the confusion, Leo guessed `projects/notes`.
- **O-b (Stage 3 gate hint, S3 Q1)**: "the file command that can also update a timestamp." uses "timestamp"; recovery came from the offered choices and from his own `touch`, not from the hint.
- **O-c (2.5, "Names for places")**: "A path names a place. ... A relative path starts where you are ... An absolute path starts from /, the top" is the densest jargon screen; skimmed, and Q3 of the Stage 2 gate then failed (first rejection there).
- **O-d (4.1)**: "A command line is a name, then options, then arguments." read as static; the three example lines were typed without the labels.
- **O-e (2.1)**: after `/pwd` the screen offers no stray-slash line (1.1 has one); recovery relied on remembering 1.1.
- **O-f (Stage 1 gate task, `check` first)**: the checklist marks open rows `[ ]`; the persona sheet's brief mentions `○`. No effect on Leo, a note for the maintainer.
- **O-g (welcome, orientation, Stage 1 intro)**: three reading-only screens in a row before the first command; Leo's friction was charged once, here.
- **O-h (1.2 "Four keys")**: Tab, Up, Ctrl+C and Ctrl+L were not tried; nothing later in the sitting required them (the Stage 1 recap lists "Tab Up" and "Ctrl+C" as things he can now do).

### Debrief (out of character)

- The one rejection that read as unfair was the Stage 4 gate Q2: "> replaces the file without asking" (4.4) and the answer `>> adds more, > replaces` say the same thing, yet the reply was "not quite. hint: Lesson 4.4: what each arrow does to a file that already exists."
- The Stage 2 gate Q3 hint, "a relative name starts from the folder you are already in", and the Stage 3 gate Q1 hint, "the file command that can also update a timestamp", both lean on a word the persona cannot read.
- The sentence "A path names a place..." in 2.5 and "A command line is a name, then options, then arguments." in 4.1 are the two places the jargon stood in front of a command he could simply copy.
- The scripted slash errors were all cleared in one input: "bash: /echo: No such file or directory" is enough once "look for a stray /" has been seen once, and the memory of 1.1 carried through the other four stages.
- No input ever put a tutor word to the shell or a shell word to recall; the "this is not the shell" line and the `┃` marker held for every gate.
