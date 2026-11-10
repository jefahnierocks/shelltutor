# Synthetic walkthrough — one sitting (leo-6)

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/leo.md` (Leo, 13, gamer and modder, `gamer-brute-forcer`); learner role: child
- Persona sheet version: 0.2.0
- Turn cap: 220 (round 6). One turn = one `send` or one `raw`. Turns used: 166 (the bundle reports `persona_inputs: 166`, `notes: 166`)
- Simulation rules confirmed (zero forward knowledge, reading limit, friction meter): yes. Reading limit per leo.md: commands, `▶` lines, command-colour text and the first sentence of each paragraph, unless the screen is under eight lines (then all). Friction +1 per reading-only screen after the second in a row; +2 per rejection; +1 mode confusion; -1 per gate cleared; quit at 8.
- Tutor revision and invocation: `2579f68` (script `2cb3f53`); `sitting.py start` with no `--arg` (begins at the welcome screen), Bash `/bin/bash` 3.2.57. This is Leo's sixth sitting; no memory of earlier ones.
- `--info` lines the persona was shown: none.
- Protocol note: on the second turn (Stage 1 intro, `next`) I chained `note` and `send` in one shell call by mistake. It was a single call, but it broke the "never combine note/send" rule. Every later turn was separate. The note was still recorded before the send.
- Login name is written `[user]` throughout.

## Per screen

Compact form: every screen gets Read / Jargon / Monologue / Input / Response / Ladder / Friction. "Ladder: none" means the tutor never showed a hint rung, because no input was rejected. Friction is an unfloored running total.

### welcome — shelltutor (5 stages)
- **Read**: skimmed. Read the `▶ Type next to begin.` line and the stage list names; did not read the "Everything you type runs in a real shell..." paragraph beyond its first sentence.
- **Jargon**: "Unix shell", "practice folder".
- **Monologue**: It says type next. Five stages, ok.
- **Input** `[nav]` → `next` → accepted.
- **Ladder**: none. **Friction**: 0 (reading-only screen 1).

### orientation — Orientation
- **Read**: all (under eight lines of prose) but the paragraph on "a fifth, check" skimmed.
- **Jargon**: "real shell prompt".
- **Monologue**: shelltutor> is where I type. Four words steer it. next.
- **Input** `[nav]` → `next` → accepted. **Ladder**: none. **Friction**: 0 (reading-only screen 2).

### Stage 1 intro — Stage 1: Where am I?
- **Read**: all. **Monologue**: lesson 1.1. next.
- **Input** `[nav]` → `next` (note and send were chained here, see protocol note). **Friction**: 1 (third reading-only screen in a row, +1).

### 1.1 — Running a command
- **Read**: commands and `▶` line; skipped "A command is a name, then the words you hand it".
- **Jargon**: "the words you hand it".
- **Monologue**: Three lines to try. Type them.
- **Input** `[bash]` → `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` → all printed. The quotes did not print. Typed all three.
- **Ladder**: none. **Friction**: 1.

### 1.2 — Four keys
- **Read**: commands/keys list. Skipped "Ctrl+C is the way out at a prompt. Inside a full-screen program...".
- **Monologue**: Tab thing sounds like a cheat code. Try it. The rest is boring.
- **Input** `[bash]` → raw `echo p<Tab>` → filled `poem.txt`; raw Enter → printed `poem.txt`. Did **not** try the up arrow, Ctrl+C or Ctrl+L. → `next`.
- **Typed or skipped**: partly typed (Tab only).
- **Ladder**: none. **Friction**: 1.

### 1.3 — Where am I, who am I, when is it
- **Read**: all commands, `▶` line, the prompt sentence ("This prompt ends in >").
- **Input** `[bash]` → `pwd`, `whoami`, `date` → each printed; `whoami` printed `[user]`. → `next`. Typed all three.
- **Friction**: 1.

### 1.4 — The shell, caught in the act
- **Read**: commands, the `bash:` paragraph's first sentence.
- **Jargon**: "terminal → shell → program".
- **Input** `[bash]` → `dtae` → `bash: dtae: command not found` (a taught error, not a rejection). Did not type `date` again. → `next`.
- **Typed or skipped**: partly typed (only the scrambled one).
- **Friction**: 1.

### 1.5 — Who else types here
- **Read**: first sentence of each paragraph; did not read "three habits count twice".
- **Jargon**: "An AI assistant that 'runs commands' for you".
- **Input** `[nav]` → `next`. **Friction**: 1 (reading-only screen 1 after the 1.4 practice).

### Stage 1 gate (recall, then task)
- Q1 "which character usually ends the prompt?" `$ ; : #` → typed `$` → accepted first try.
- Q2 "What does pwd print?" → `the folder you are in` → accepted first try.
- Q3 "After whoami runs, where does its output go?" → `the screen` → accepted first try.
- Task: `whoami`, `pwd`, `date`, then `check` → follow-ups: username (`[user]`), the full path (typed out from the screen), `Mon` → all accepted. **First check passed**.
- **Friction**: 0 (gate cleared, -1).

### Stage 1 cleared / Stage 2 intro
- Read the "You can now" list as commands. `next` x2. Reading-only screens 1 and 2; no charge.

### 2.1 — Where you are
- **Read**: tree and `▶` line; skipped "The line pwd prints is the full name...".
- **Input** `[bash]` → `pwd` → printed the practice folder. Typed. **Friction**: 0.

### 2.2 — What is here
- **Input** `[bash]` → `ls`, `ls -p`, `ls -a`, `ls /` → all printed. Typed all four. `ls -a` showed `.progress` and `.shelltutor_history`; Leo reads them as part of the game files.
- **Friction**: 0.

### 2.3 — Moving
- **Jargon**: "the folder that contains this one".
- **Input** `[bash]` → `cd ..`, `pwd`, `cd -` → typed all three. Worked. **Friction**: 0.

### 2.4 — Home and back
- **Read**: commands. The third command is the practice folder's full path in a code line followed by a comment.
- **Jargon**: "full name works from anywhere".
- **Input** `[bash]` → `cd`, `pwd`, `cd <full path>` → worked (the display wrapped the long line). Typed all. **Friction**: 0.

### 2.5 — Names for places
- **Read**: commands and first sentences. First sentence of the second paragraph carries "in ~/projects, the name notes means ~/projects/notes".
- **Jargon**: "relative path", "absolute path".
- **Input** `[bash]` → `ls ..` → a wall of about 600 names (the practice folder's parent is the host temp directory). Leo: "whoa, hundreds of weird names". → `ls ~` → printed nothing. → `next`. Typed both. No friction charged (no rule fires), but see O-001.
- **Friction**: 0.

### 2.6 — Making a folder
- **Input** `[bash]` → `mkdir demo`, `ls -p`, `cd demo`, `pwd` → typed all four; worked. **Friction**: 0.

### Stage 2 gate
- Q1 "What does cd .. do?" → `goes up one folder` → accepted first try.
- Q2 "What does ~ mean in a path?" → `your home folder` → accepted first try.
- Q3 "If I'm in ~/projects and I type cd notes, what folder am I in?" → `~/projects/notes` → accepted first try.
- Task: `mkdir practice`, `cd practice`, `pwd`, `check` → cleared. **First check passed**. (The shell was already standing in `stage2`.)
- **Friction**: -1.

### Stage 3 intro, 3.1 Making files
- `touch hello.txt`, `echo hi > words.txt`, `mkdir notes`, `ls -p` → typed all. `>` explained as "sends what echo prints into a file". **Friction**: -1.

### 3.2 Reading a file
- `cat words.txt`, `cat hello.txt`, `cat ../poem.txt` → typed all three; empty file printed nothing as the lesson said.

### 3.3 Reading a long file
- `less ../numbers.txt` → raw space (paged to 46) → raw `q` → back at the prompt. Typed and left cleanly. No mode confusion.

### 3.4 Copy and move
- `cp hello.txt backup.txt`, `mv hello.txt hi.txt`, `mv hi.txt notes/`, `ls -p notes` → typed all four; worked.

### 3.5 Removing
- `ls`, `rm backup.txt`, `ls` → typed all three.

### Stage 3 gate
- Q1 "Which command creates an empty file?" → `touch` → accepted. Q2 "After rm important.txt, where is the file?" → `gone` → accepted. Q3 "What single command renames old.txt to new.txt?" → `mv old.txt new.txt` → accepted. All first try.
- Task: `echo hello > notes.txt`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt`, `check` → cleared. **First check passed**.
- **Friction**: -2.

### Stage 4 intro, 4.1 The parts of a command
- `wc -l poem.txt` (printed 4), `echo "hello world"`, `command -v vim` (printed `/usr/bin/vim`) → typed all.
- **Jargon**: "options", "arguments" (read in the first sentence, not understood).

### 4.2 Spaces and quotes
- `touch my notes.txt`, `ls`, `touch "my notes.txt"`, `ls` → typed all four. `ls` showed `my`, `my notes.txt`, `notes.txt`.

### 4.3 The pipe
- `seq 1 100 | wc -l` (100), `ls /usr/bin | wc -l` (932), `ls /usr/bin | sort | head` → typed all three.

### 4.4 Into a file
- `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt` (two lines) → typed all three.

### 4.5 Pipe, then file
- `ls /usr/bin | wc -l > count-of-programs.txt`, `cat count-of-programs.txt` (932) → typed both.

### 4.6 Many names at once
- `ls *.txt`, `wc -l *.txt` → typed both. Did not run `rm *` (the line says it would remove everything).

### Stage 4 gate
- Q1 "What does command -v vim print, if Vim is installed?" → `a path`. Q2 "difference between > and >>" → `> writes over the file and >> adds to the end`. Q3 "Why does vim my notes.txt open two files instead of one?" → `because the space splits it into two names`. All accepted first try.
- Task: `seq 1 100 | wc -l > count.txt`, `ls *.txt`, `check` → cleared. **First check passed**.
- **Friction**: -3.

### Stage 5 intro, 5.1 Programs that take over the screen
- `man ls`, then raw `q` → back to the prompt. Typed.

### 5.2 Leaving Vim
- `command -v vim`, `vim`, `:q` (sent with Enter) → back at the prompt. Typed all.

### 5.3 The copy and the file
- **Read**: the diagram and the `:w :q :q! :wq` list; skipped the first paragraph beyond its first sentence.
- **Jargon**: "working copy", "write the copy to the file".
- **Monologue**: no prompt to try anything here. "Type next to try both" - both what?
- **Input** `[nav]` → `next`. Reading-only screen; **skipped** (no commands to type). **Friction**: -3 (first reading-only screen after a practice screen).

### 5.4 Throw it away
- `vim practice.txt`, raw `i`, raw `abc`, raw Esc, `:q!`, `cat practice.txt` → `before`. Typed all. Insert mode showed on the screen.

### 5.5 Keep it
- `vim practice.txt`, raw `i`, raw `xyz`, raw Esc, `:wq`, `cat practice.txt` → `xyzbefore`. Typed all.

### 5.6 vimtutor
- `command -v vimtutor` → `/usr/bin/vimtutor`. Typed.

### Stage 5 gate
- Q1 "How do you exit man ls?" → `q`. Q2 "After vim notes.txt, what makes Vim write your edit to the file?" → `:wq`. Q3 ":q! — did the file on disk change?" → `no`. All accepted first try.
- Task phase 1: `cat practice.txt`, `vim practice.txt`, `i`, `lol`, Esc, `:q!`, `cat practice.txt`, `check` → passed first check.
- Task phase 2: `vim practice.txt`, `i`, `gg`, Esc, `:wq`, `cat practice.txt` (`ggbefore`), `check` → passed first check.
- **Friction**: -4. The finale printed "You're ready for vimtutor." and `[exited 0]`.

## Per gate

| Gate | Recall attempts (Q1/Q2/Q3) | Rejections | Rung reached | Task first `check` | Cleared |
| --- | --- | --- | --- | --- | --- |
| Stage 1 | 1/1/1 | none | none | passed (3 follow-ups, all first try) | yes |
| Stage 2 | 1/1/1 | none | none | passed (checklist all met) | yes |
| Stage 3 | 1/1/1 | none | none | passed | yes |
| Stage 4 | 1/1/1 | none | none | passed | yes |
| Stage 5 | 1/1/1 | none | none | phase 1 passed, phase 2 passed | yes |

No checklist item was ever marked `○` after a `check`.

## End of sitting

- **Final friction and where it ended**: -4 (unfloored; reads as 0 if floored at 0). Ended at the finale (Stage 5 cleared, `[exited 0]`); no quit.
- **Friction by source**: reading charges +1 (Stage 1 intro, third reading-only screen in a row); rejections 0; mode confusion 0; gates cleared -5.
- **Stages cleared**: all five.
- **Turns used**: 166 of 220.
- **Lessons**: 28. Fully typed (all lesson commands): 24. Partly typed: 2 (1.2: only Tab; 1.4: only `dtae`). Reading-only, nothing to type: 2 (1.5 and 5.3). Went straight to `next` without typing anything: 0 of the lessons that have commands.
- **Equivalent human sitting time (estimate)**: roughly 55 to 75 minutes for a 13-year-old at this pace, mostly 24 lessons of typing and five gates with no stalls. This is an estimate.
- **Candidate F-nnn** (valid answer rejected, broken hint, dead end, false statement): none observed.
- **Candidate O-nnn**:
  - **O-001** — screen 2.5, input `ls ..`: the parent of the practice folder is the host's temporary directory, and `ls ..` printed about 600 unrelated names (system and tool files, named sockets, logs). The lesson says only "look one level up without moving". A learner whose practice folder is under a busy `TMPDIR` would meet a wall of output that no sentence prepared them for. Possibly specific to the sim host and `TMPDIR`; maintainer to confirm on a clean run.
  - **O-002** — screen 5.3: the last line "Type next to try both." has no practice prompt and nothing to try on the screen; "both" has no clear referent (`:w` and `:q`? the two Vim commands in 5.4 and 5.5?).
  - **O-003** — screen 1.2: Ctrl+C and Ctrl+L are listed as keys to "try now", but Leo skipped them (boredom, no check) and the later gate never asks. Pace/optional-step candidate, not a defect.
  - **O-004** — screen 4.1: `wc -l poem.txt` and `ls /usr/bin | wc -l` both print numbers with leading spaces and no explanation of what the number means; the screen says nothing after the commands about reading the output. Minor.
  - **O-005** — screens 2.5, 4.1: "relative path", "absolute path", "options", "arguments" appear in prose Leo skims; they never blocked him because the gate asks only what the commands did. Jargon flagged for the record, no stall.
  - **O-006** — pass-through observation: none of Leo's listed triggers (brute-force guessing, leading slashes such as `/pwd`) fired, because every gate question was answerable from a line he had just typed and every lesson named its commands. This sitting therefore did not exercise the rejection ladder at all.
- **Debrief** (out of character):
  - The only sentence that hit a real wall of noise was the instruction under 2.5 ("ls ..  # look one level up without moving"), whose output depends on the parent directory.
  - "Type next to try both." on 5.3 invites a search for something to type; it is the only practice-less lesson where `▶` implies an action.
  - Leo never failed because the lessons print the exact commands and the recall questions repeat words from them ("the folder you are in", "goes up one folder", "gone"); this is a pass for pacing but a weak test of the persona's guessing trigger.
  - The model playing Leo knows the commands; it typed what the screen printed and could not honestly produce the leading-slash or mode-confusion errors the persona sheet expects.
