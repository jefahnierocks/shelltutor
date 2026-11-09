# Synthetic walkthrough — one sitting (arthur-5)

## Sitting

- Date: 2026-11-09
- Persona (file in `docs/sim-personas/`) and learner role: `arthur.md`, Arthur, 64, retired logistics manager, `dos-literalist`; adult with some shell
- Persona sheet version: 0.2.0
- Turn cap: 160. One turn = one `send` or one `raw`. Turns used: 150 (the bundle's `persona_inputs`; the sitting ended on the finale, 10 turns under the cap)
- Simulation rules confirmed (zero forward knowledge, reading limit, friction meter): yes. Arthur reads every line; the density charge applies only where a long screen's content later causes a rejection or wrong turn, quoted at that turn (none occurred). Friction per README rule 6: +2 rejection not understood, +1 mode confusion, -1 gate cleared, quit at 8. Not floored at 0 (as in maya-3).
- Tutor revision and invocation: `d88c564` (script `7e126cf`); `sitting.py start` with no `--arg` (welcome screen); Bash `/opt/homebrew/bin/bash` 5.3.20; fifth Arthur sitting, no memory of earlier ones.
- `--info` lines the persona was shown, if any: none

Process note: in the first ten turns some `note` and `send` calls were issued in the same shell call (sequentially, never in parallel); one pair of `note`/`send` calls was issued in a single message. Order in `events.jsonl` was preserved. One `note` call at the 2.4 screen also ran an erroneous extra command against a mistyped `--out` path that did nothing to the sitting.

## Per screen

Convention: "silent" = the command printed nothing; Arthur's stock reaction was "Did it do it?" followed by an `ls`/`pwd`/`cat` check, which cost turns but no friction. No input in this sitting was rejected. Ladder rung: none shown anywhere. Friction stayed at 0 until a gate cleared, then fell by 1 per gate.

### welcome — SHELLTUTOR — a vimtutor prerequisite course (18 lines)

- **Read**: all
- **Jargon or assumed concept**: "a vimtutor prerequisite course"; "this is the real thing, not a simulation" (what is real?)
- **Monologue**: Never heard of vimtutor. Long folder name I will not worry about. Screen says type next.
- **Input** `[nav]` → `next` → accepted
- **Interpretation**: Orientation follows.
- **Ladder rung**: none
- **Friction**: 0

### Orientation (21 lines)

- **Read**: all
- **Jargon**: "the shell runs it"; "keyboard-only; you can't click mid-line to move the cursor"
- **Monologue**: The shell is not defined yet but I carry on.
- **Input** `[nav]` → `next` → accepted
- **Ladder rung**: none
- **Friction**: 0

### Stage 1 intro (11 lines)

- **Read**: all. **Jargon**: none. **Input** `[nav]` → `next` → accepted. **Friction**: 0

### 1.1 — running commands (22 lines)

- **Read**: all
- **Jargon**: "# spaces separate words" (is the # typed?)
- **Monologue**: Three commands, I will type them as shown. First echo hello.
- **Input** `[bash]` → `echo hello` → `hello`; `echo I am at the shell      # spaces separate words` → `I am at the shell` (the remark was ignored); `echo "I am at the shell"` → same output; `[nav]` `next`
- **Interpretation**: The hash part is a remark, not output.
- **Ladder rung**: none
- **Friction**: 0

### 1.2 — keyboard habits (19 lines)

- **Read**: all
- **Jargon**: "bash finishes a word"; "program like less (Stage 3)"; "full-screen program"; "escape hatch"
- **Monologue**: What is bash, what is less? Not defined. I do the Tab one as told.
- **Input** `[bash]` → raw `echo p\t` → line became `echo poem.txt`; `""` (Enter) → `poem.txt`; raw up arrow → `echo poem.txt` returned; `""` → `poem.txt`; raw Ctrl+L → screen cleared; raw Ctrl+C → fresh prompt; `[nav]` `next`
- **Interpretation**: All four keys did what the screen said. Ctrl+C at an empty prompt showed `^C` and nothing else.
- **Ladder rung**: none
- **Friction**: 0 (long screen, no wrong turn, no charge)

### 1.3 — where am I, who am I, when is it (19 lines)

- **Read**: all
- **Jargon**: none new
- **Monologue**: pwd prints a long path starting with a slash and no drive letter. Odd.
- **Input** `[bash]` → `whoami` → `[user]`; `pwd` → the practice folder; `date` → date; `[nav]` `next`
- **Ladder rung**: none
- **Friction**: 0

### 1.4 — the shell, caught in the act (22 lines)

- **Read**: all
- **Jargon**: none ("bash:" is explained)
- **Input** `[bash]` → `date` → date; `dtae` → `bash: dtae: command not found` (expected); `[nav]` `next`
- **Ladder rung**: none
- **Friction**: 0

### 1.5 — who else types here (20 lines)

- **Read**: all
- **Jargon**: "An AI assistant that 'runs commands' for you"
- **Monologue**: Not sure why an assistant is in a shell course, but I take it as a safety remark.
- **Input** `[nav]` → `next` → accepted
- **Friction**: 0

### STAGE 1 GATE (recall) — Q1 to Q3 (16 lines)

- **Read**: all
- **Input** `[recall]` → `$` → ✓ (Q1); `the folder you are in` → ✓ (Q2); `it comes back to me on the screen` → ✓ (Q3)
- **Interpretation**: "Type your answer in words; this is not the shell." registered; no mode confusion.
- **Ladder rung**: none
- **Friction**: 0

### STAGE 1 GATE TASK — follow-ups (16 lines)

- **Read**: all
- **Monologue**: pwd now ends in /stage1; it was the top folder at 1.3. I was not asked to move. Odd.
- **Input** `[bash]` → `whoami`, `pwd`, `date`, `check`; `[follow-up]` → `[user]` ✓; the full pwd path typed by hand ✓; `Mon` ✓
- **Ladder rung**: none
- **Friction**: -1 (gate cleared)

### Stage 1 cleared / Stage 2 intro (19 and 21 lines)

- **Read**: all
- **Jargon**: none
- **Input** `[nav]` → `next`, `next`. **Friction**: -1

### 2.1 — where you are (20 lines)

- **Read**: all
- **Input** `[bash]` → `pwd` → the top practice folder (matched the tree); `[nav]` `next`
- **Interpretation**: Different from the /stage1 value at the Stage 1 gate; nobody said the tutor changed folders.
- **Friction**: -1

### 2.2 — ls: what is here (20 lines)

- **Read**: all
- **Jargon**: "the top of everything"; "hidden names: those starting with ."
- **Monologue**: Is `/` like the DOS root? ls / showed no drive letters. Moving on.
- **Input** `[bash]` → `ls -p` → `numbers.txt poem.txt stage1/ stage2/`; `ls /` → many names; `[nav]` `next`
- **Friction**: -1

### 2.3 — cd: moving (22 lines)

- **Read**: all
- **Jargon**: none new ("cd.. with no space is a different word" noted, taken as a DOS warning)
- **Input** `[bash]` → `cd ..` → silent; `pwd` → one level up; `cd -` → printed the old folder; `[nav]` `next`
- **Interpretation**: After the silent `cd ..` he used pwd, as instructed, to see that it worked.
- **Friction**: -1

### 2.4 — names for places (22 lines)

- **Read**: all
- **Jargon**: "~" (home) taught only in the earlier screen; "bare name" ("the bare name notes means ~/projects/notes")
- **Input** `[bash]` → `mkdir demo` → silent; `ls -p` → `demo/ ...`; `[nav]` `next`
- **Friction**: -1

### STAGE 2 GATE (recall) and TASK (18 lines)

- **Read**: all
- **Input** `[recall]` → `it goes up one level to the parent folder` ✓; `your home folder` ✓; `~/projects/notes` ✓; `[bash]` `mkdir practice`, `cd practice`, `pwd` → path ending `stage2/practice`; `check`
- **Interpretation**: "this stage's folder" resolved by itself (the prompt was already in stage2).
- **Friction**: -2 (gate cleared)

### Stage 2 cleared / Stage 3 intro (19 and 22 lines)

- **Read**: all
- **Jargon**: "timestamp"; "rm is immediate. It does not move things to a trash." (nervous)
- **Input** `[nav]` → `next`, `next`. **Friction**: -2

### 3.1 — creating: touch, mkdir (21 lines)

- **Read**: all
- **Jargon**: "send echo's output into it (more on > in Stage 4)"
- **Monologue**: What is > ? Vague, but they say later.
- **Input** `[bash]` → `touch hello.txt` silent; `ls` → `hello.txt`; `mkdir notes` silent; `ls`; `echo hello > notes.txt` silent (no `hello` printed); `ls`; `[nav]` `next`
- **Interpretation**: Silent three times; each time he checked with `ls`.
- **Friction**: -2

### 3.2 — reading: cat, less (22 lines)

- **Read**: all
- **Jargon**: "(More on full-screen programs in Stage 5.)"
- **Input** `[bash]` → `cat hello.txt` (nothing, as warned); `cat ../poem.txt` (poem); `less ../numbers.txt` (screen taken over); raw `q` → prompt back; `[nav]` `next`
- **Friction**: -2

### 3.3 — copy, move, delete (22 lines)

- **Read**: all
- **Jargon**: "rm <only-now-that-you-are-sure>" (read as advice, not typed)
- **Input** `[bash]` → `cp hello.txt backup.txt`, `ls`, `mv hello.txt hi.txt`, `mv hi.txt notes/`, `ls`, `rm backup.txt`; `[nav]` `next`
- **Friction**: -2

### STAGE 3 GATE (recall) and TASK (21 lines)

- **Read**: all
- **Input** `[recall]` → `touch` ✓; `gone` ✓; `mv old.txt new.txt` ✓; `[bash]` `echo hello > notes.txt`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `ls`, `rm backup.txt`, `check`
- **Interpretation**: Step 1 "create a file notes.txt" duplicated a file already made in 3.1; he re-created it anyway.
- **Friction**: -3 (gate cleared)

### Stage 3 cleared / Stage 4 intro (19 and 22 lines)

- **Read**: all
- **Jargon**: "pipe: send one command's output into the next"; "glob: match many filenames at once" (listed before taught); "redirect"
- **Input** `[nav]` → `next`, `next`. **Friction**: -3

### 4.1 — reading a command (22 lines)

- **Read**: all
- **Jargon**: "prints the path; exits 0"
- **Monologue**: Exits what? Not defined.
- **Input** `[bash]` → `command -v ls` → `/bin/ls`; `command -v vim` → `/usr/bin/vim`; `[nav]` `next`
- **Friction**: -3

### 4.2 — the pipe (22 lines)

- **Read**: all
- **Jargon**: "ls /usr/bin | grep ^a  # names starting with 'a'" (the `^` is not explained); "Shift+Backslash" (he found the key)
- **Input** `[bash]` → `seq 1 100 | wc -l` → `100`; `ls /usr/bin | sort | head` → ten names; `ls /usr/bin | grep ^a | wc -l` → `41`; `[nav]` `next`
- **Friction**: -3

### 4.3 — redirection (22 lines)

- **Read**: all
- **Input** `[bash]` → `echo first > greeting.txt`; `echo second >> greeting.txt`; `cat greeting.txt` → two lines; `wc -w < poem.txt` → `28`; `ls /usr/bin | sort > programs.txt`; `wc -l programs.txt` → `932`; `[nav]` `next`
- **Friction**: -3

### 4.4 — globs (17 lines)

- **Read**: all
- **Jargon**: none (he knows DOS wildcards); "rm * removes everything" (not run)
- **Input** `[bash]` → `ls *.txt` → four files; `[nav]` `next`
- **Friction**: -3

### STAGE 4 GATE (recall) and TASK (21 lines)

- **Read**: all
- **Input** `[recall]` → `its path, /usr/bin/vim` ✓; `> overwrites the file and >> appends to the end of it` ✓; `the shell splits on spaces so my and notes.txt are two separate files, quotes would make it one` ✓; `[bash]` `seq 1 100 | wc -l > count.txt`, `ls *.txt`, `check`
- **Interpretation**: "count from 1 to 100 and save the count" read as the 4.2 pipeline; passed first check. The other reading (`seq 1 100 > count.txt`) was not tried.
- **Friction**: -4 (gate cleared)

### Stage 4 cleared / Stage 5 intro (19 and 15 lines)

- **Read**: all
- **Jargon**: "takes over the terminal"
- **Input** `[nav]` → `next`, `next`. **Friction**: -4

### 5.1 — print-and-exit vs full-screen (21 lines)

- **Read**: all
- **Input** `[bash]` → `man ls` (took over screen, `:` prompt) → raw `q` → prompt; `[nav]` `next`
- **Friction**: -4

### 5.2 — entering and leaving Vim (22 lines)

- **Read**: all
- **Jargon**: "If Vim refuses (unsaved changes), use the discard form: :q! then Enter" (shown before any change exists); ":q!" before it is explained (explained in 5.3)
- **Input** `[bash]` → `vim --version` (pages of text, prompt back); `vim` (empty screen with tildes and a Vim welcome); `:q` → prompt back; `[nav]` `next`
- **Friction**: -4

### 5.3 — buffer vs file (21 lines)

- **Read**: all
- **Jargon**: "buffer"
- **Monologue**: A copy in memory, like Word's open document versus the saved one. Clear.
- **Input** `[nav]` → `next`, `next`. **Friction**: -4

### 5.4 — practice: discard, then save (22 lines)

- **Read**: all
- **Jargon**: "type i to enter insert mode (vimtutor will teach modes)"
- **Monologue**: What is insert mode? No sign on screen that it began. No Enter said after `i`, so none sent.
- **Input** `[bash]` → `vim practice.txt`; raw `i`; raw `abc`; raw Esc; `:q!`; `cat practice.txt` → `before`; again `vim practice.txt`; raw `i`; raw `xyz`; raw Esc; `:wq`; `cat practice.txt` → `xyzbefore`; `[nav]` `next`
- **Interpretation**: Both outcomes matched the screen.
- **Friction**: -4

### 5.5 — calling vimtutor (19 lines)

- **Read**: all
- **Input** `[bash]` → `command -v vimtutor` → `/usr/bin/vimtutor`; `[nav]` `next`
- **Friction**: -4

### STAGE 5 GATE (recall) and TASK phases 1 and 2 (22 and 18 lines)

- **Read**: all
- **Input** `[recall]` → `press q` ✓; `the :w command writes the buffer to the file, :wq writes and quits` ✓; `no, the file did not change` ✓; phase 1: `cat practice.txt`, `vim practice.txt`, raw `i`, raw `qrs`, raw Esc, `:q!`, `cat practice.txt`, `check`; phase 2: `vim practice.txt`, raw `i`, raw `z`, raw Esc, `:wq`, `cat practice.txt` → `zbefore`, `check` → finale, `[exited 0]`
- **Ladder rung**: none
- **Friction**: -5 (gate cleared)

## Per gate

- **Stage 1**: Recall one attempt per question (3/3). Task one attempt; `check` follow-ups: whoami, pwd (full path typed by hand), day of week, all accepted first time. Rejected inputs: none. Rung: none. Cleared.
- **Stage 2**: Recall one attempt per question (3/3). Task one `check`. Rejected inputs: none. Rung: none. Cleared.
- **Stage 3**: Recall one attempt per question (3/3). Task one `check`. Rejected inputs: none. Rung: none. Cleared.
- **Stage 4**: Recall one attempt per question (3/3). Task one `check` after `seq 1 100 | wc -l > count.txt` and `ls *.txt`. Rejected inputs: none. Rung: none. Cleared.
- **Stage 5**: Recall one attempt per question (3/3). Two-phase task, one `check` per phase. Rejected inputs: none. Rung: none. Cleared.

## End of sitting

- Final friction: -5 (unfloored). Breakdown: reading/density charges 0; rejections 0 (0 x +2); mode confusion 0; gates cleared 5 (5 x -1). The persona did not quit; the sitting ended on the finale screen with `[exited 0]` at 150 of 160 turns (`persona_inputs` 150).
- Stages or module cleared: Stages 1, 2, 3, 4 and 5 (all five gates, each on the first `check`).
- Equivalent human sitting time: roughly 55 to 75 minutes (estimate). 150 turns, no retries, about 40 turns spent on "did it do it?" verification (`ls`, `pwd`, `cat`) after silent commands, and about 12 on hand-typed Vim key steps.
- Density notes (no friction applied): screens over 14 lines are nearly all of them (every screen but the Stage 1 intro, welcome-sized screens and a few cleared screens); no long screen caused a wrong turn or rejection, so no +1 was charged. The longest content-heavy screens were 1.2 (four keys, 19 lines), 4.1/4.2/4.3 (22 lines each) and 5.4 (22 lines).

- **Candidate F-nnn**: none. No valid answer was rejected, no hint was broken, no dead end, no false statement observed. (One observation sits close: see O-001.)

- **Candidate O-nnn**:
  - O-001: screen `1.3 — where am I, who am I, when is it` says "Here pwd shows the tutor's own folder, because that is where this practice prompt starts." At `STAGE 1 — GATE TASK` the same `pwd` printed a path ending `/stage1`, and at `2.1 — where you are` it printed the top folder again. Input: `pwd` (verbatim) at each. No screen says the prompt's folder changes.
  - O-002: screen `1.2 — keyboard habits`: "bash finishes a word." and "Inside a full-screen program like less (Stage 3), q is the way out." use "bash", "less" and "full-screen program" before they are defined (bash is defined in 1.4). Also screen 1.2 carries four keys on one screen; no friction followed.
  - O-003: screen `1.2`, input raw Ctrl+L then raw Ctrl+C: both gave a nearly blank screen with no confirmation, which a learner who treats silence as failure cannot distinguish from nothing happening.
  - O-004: screen `2.2 — ls: what is here`: "ls /          # the top of everything" shows no drive letter; Arthur's "where is the drive?" question was never answered on any screen. Input `ls /`.
  - O-005: screen `3.1 — creating: touch, mkdir`: "To put words in a file, send echo's output into it (more on > in Stage 4)". Input `echo hello > notes.txt` printed nothing, and no screen in 3.1 shows reading it back.
  - O-006: screen `STAGE 3 — GATE TASK`: "create a file notes.txt containing the word hello" when `notes.txt` already exists from lesson 3.1 in the same folder. Input `echo hello > notes.txt` overwrote it silently.
  - O-007: screen `STAGE 4 — Commands, streams, composition` lists "pipe" and "glob" (and "redirect") as one-line definitions before the lessons; screen `4.1`: "command -v ls  # prints the path; exits 0" uses "exits 0" undefined; screen `4.2`: "ls /usr/bin | grep ^a  # names starting with 'a'" leaves `^` undefined.
  - O-008: screen `STAGE 4 — GATE TASK`: "Use seq and a pipe to count from 1 to 100 and save the count to count.txt." admits two readings (the numbers 1 to 100, or the count 100). Input `seq 1 100 | wc -l > count.txt` was accepted.
  - O-009: screen `5.2 — entering and leaving Vim`: "If Vim refuses (unsaved changes), use the discard form: :q! then Enter" and "You will need :q! the first few times you use Vim. Memorize it." appear before any lesson on changes; `5.3` explains it.
  - O-010: screen `5.4 — practice: discard, then save`: "type i to enter insert mode (vimtutor will teach modes)". No visible mode indicator appeared in the captured screen after raw `i`, raw `abc`, raw Esc. "type i" carries no Enter while ":q! then Enter" does; the difference is stated only by wording.

- **Debrief** (out of character):
  - The sitting never rejected an input; Arthur's usual traps (silence, `cd..`, backslash, placeholders, case) were each answered by an earlier sentence: "cd.. with no space is a different word; bash cannot find it." and "rm is immediate."
  - Sentences that made him stall without costing friction: "bash finishes a word." (1.2), "prints the path; exits 0" (4.1), "names starting with 'a'" / `grep ^a` (4.2), "type i to enter insert mode (vimtutor will teach modes)" (5.4).
  - Sentences that contradicted what he saw: "Here pwd shows the tutor's own folder, because that is where this practice prompt starts." (1.3) against the `/stage1` path at the gate.
  - Unanswered Arthur question: where the drive letter is, after "ls /  # the top of everything" (2.2).
  - Silence checks (about 40 turns) were self-initiated; the screens themselves told him which check to run (`ls`, `pwd`) in most cases.
