# Synthetic walkthrough — Arthur, sitting 7

## Sitting

- Date: 2026-11-10
- Persona: `docs/sim-personas/arthur.md` (Arthur, 64, retired logistics manager, `dos-literalist`); learner role: adult with some shell
- Persona sheet version: 0.2.0
- Scripted errors performed: none scripted (Arthur has habits, not a schedule); habits performed are listed under End of sitting
- Turn cap: 240 (round 7). One turn = one `send` or one `raw`. Turns used: 187 (my count of sends and raws; `events.jsonl` is authoritative)
- Simulation rules confirmed: zero forward knowledge, Arthur's reading rule (every line; stall at undefined terms; density charge only when a long screen later causes a wrong turn or rejection), friction meter per README rule 6, quit at 8. A silent command is verified with ONE check.
- Tutor revision: 40c11cf (script a7cd1ac); invocation: `sitting.py start`, no `--arg` (begins at the welcome screen), Bash `/opt/homebrew/bin/bash` 5.3.20
- `--info` lines shown: none

Login name appears as `[user]` below; screens print it from `whoami`.

## Per screen

Screens that only repeat a pattern are grouped; every undefined term and every habit is quoted.

### welcome / orientation / Stage 1 intro (turns 1-3)

- **Read**: all
- **Jargon**: none
- **Monologue**: Five stages, a practice folder, "Type next to begin". Orientation says "press Enter", so the Enter question never arises.
- **Input** `[nav]` → `next` ×3 → accepted
- **Ladder rung**: none. **Friction**: 0

### 1.1 — Running a command

- **Read**: all
- **Jargon**: "quotes make them one word" (one word of what?)
- **Monologue**: Try all three. Typed each; the quotes did not print, as the screen said.
- **Input** `[bash]` → `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` → output seen, then `next`
- **Ladder rung**: none. **Friction**: 0

### 1.2 — Four keys

- **Read**: all
- **Jargon**: none new. Habit: "clears the screen" read as `cls`.
- **Monologue**: Tab: `echo p` + Tab gave `echo poem.txt`, Enter ran it. Up brought the line back, Enter. Ctrl+C on `echo oops` gave `^C` and a fresh prompt. For Ctrl+L I typed `cls` out of habit.
- **Input** `[bash]` → `raw 'echo p\t'`, Enter (empty send), `raw '\x1b[A'`, Enter, `raw 'echo oops\x03'`, **`cls`**, `raw '\x0c'`, `show`, `next`
- **Response to `cls`**: `bash: cls: command not found`
- **Interpretation**: cls is DOS only; the lesson names Ctrl+L two lines up. Understood, no charge.
- **Ladder rung**: message only; recovered by the screen's own Ctrl+L line, not by the error text. **Friction**: 0

### 1.3 — Where am I, who am I, when is it

- **Read**: all
- **Jargon**: "An ordinary bash prompt usually ends in $." (bash undefined at this point; named as the shell in 1.4)
- **Monologue**: pwd printed a path beginning with `/`: where is the drive letter? The screen does not say; I carry on. whoami printed my user name `[user]`.
- **Input** `[bash]` → `pwd`, `whoami`, `date` → output seen, `next`
- **Ladder rung**: none. **Friction**: 0

### 1.4 — The shell, caught in the act

- **Read**: all
- **Jargon**: "terminal → shell → program: the window, bash, and date." (three words used as a chain before any is defined; only bash is named the shell)
- **Input** `[bash]` → `date`, `dtae` → `bash: dtae: command not found` (expected, the screen printed it) → `next`
- **Ladder rung**: none. **Friction**: 0

### 1.5 — Who else types here

- **Read**: all
- **Jargon**: "An AI assistant that "runs commands" for you goes the same way" (out of the blue; harmless)
- **Input** `[nav]` → `next`. **Friction**: 0

### Stage 1 gate (recall Q1-3, task, follow-ups)

- **Read**: all
- **Input** `[recall]` → `$` ✓; `the full name of the folder you are in` ✓; `on the screen` ✓ (Q3 "where does its output go?" answered from what I saw on screen; "output" is the word I had not been taught as a place)
- **Input** `[bash]` → `whoami`, `pwd`, `date`, then `check`
- **Input** `[follow-up]` → `[user]`, full pwd path typed out, `Tue` → all accepted
- **Friction**: -1 (gate cleared) → **-1**

### Stage 2 intro and 2.1 — Where you are

- **Read**: all
- **Jargon**: "the current directory" (folder and directory are the same to me)
- **Input** `[bash]` → `pwd` → matches the "you are here" line. `next`. **Friction**: -1

### 2.2 — What is here

- **Read**: all
- **Jargon**: "also the hidden names, which start with a dot" (a hidden name was new). After `ls -a`: entries `.` and `..` appeared with no explanation (the screen defines them only in 2.5).
- **Monologue**: ls lists names: that is DIR, so I typed `dir`.
- **Input** `[bash]` → **`dir`**, `ls`, `ls -p`, `ls -a`, `ls /` → `next`
- **Response to `dir`**: `bash: dir: command not found`. Recovered at once: the first sentence of the screen names ls. No charge.
- **`ls /`**: "the top of everything" answered my "where is the drive?" for the moment.
- **Friction**: -1

### 2.3 — Moving

- **Read**: all (the last sentence, "cd.. with no space is a different word", I read after typing)
- **Input** `[bash]` → **`cd..`**, `cd ..`, `pwd` (my one check of the silent cd), `cd -`, `next`
- **Response to `cd..`**: `bash: cd..: command not found`. The screen's last sentence explained it; recovered. No charge.
- **Friction**: -1

### 2.4 — Home and back

- **Read**: all
- **Jargon**: "~ is its short name." (tilde never typed here)
- **Input** `[bash]` → `cd`, `pwd` (check; a different folder, `…userhome…`), `cd /var/folders/.../shelltutor-sim-home-el7lsro4`, `pwd` (check) → `next`
- **Note**: the long `cd` wraps on screen; silent, no error. **Friction**: -1

### 2.5 — Names for places

- **Read**: all
- **Jargon**: "relative path" / "absolute path" (explained in the next sentence)
- **Input** `[bash]` → `cd stage1`, `pwd` (check), `ls ..`, `cd ..`, `pwd` (check), `echo ~` → `next`
- **Friction**: -1

### 2.6 — Making a folder

- **Read**: all
- **Input** `[bash]` → `mkdir demo`, `ls -p` (the screen's next line is my check), `cd demo`, `pwd` (check) → `next`
- **Friction**: -1

### Stage 2 gate

- **Input** `[recall]` → `goes up one level to the folder that contains this one` ✓; `your home folder` ✓; `~/projects/notes` ✓
- **Task**: `pwd` (to learn where "this stage's folder" was; I had been in `demo`; it was already `.../stage2`), `mkdir practice`, `ls -p` (check), **`cd .\practice`**, `cd practice`, `pwd`, `check`
- **Response to `cd .\practice`**: `bash: cd: .practice: No such file or directory`
- **Interpretation**: it says `.practice` and "no such file", but `practice/` was in the listing a minute ago, and my backslash vanished from the message. I do not understand why. **+2**. Recovered only by imitating `cd stage1` from 2.5; the backslash was never explained.
- **Ladder rung**: message only; it did not resolve the confusion; I recovered by copying a pattern, not from the message.
- **Gate**: `check` first time → cleared (-1). **Friction**: -1 +2 -1 = **0**

### Stage 3 intro, 3.1 — Making files

- **Read**: all
- **Jargon**: "an empty file"; "> sends what echo prints into a file instead of the screen." (explained in place)
- **Input** `[bash]` → `touch hello.txt`, `echo hi > words.txt`, `mkdir notes`, `ls -p` (one check for the three) → `next`
- **Friction**: 0

### 3.2 — Reading a file

- **Input** `[bash]` → `cat words.txt`, `cat hello.txt` (nothing, announced), `cat ../poem.txt` → `next`. **Friction**: 0

### 3.3 — Reading a long file

- **Jargon**: "you are inside a program" (program was loosely defined in 1.4)
- **Input** `[bash]` → `less ../numbers.txt`, `raw ' '`, `raw 'q'` → `next`. **Friction**: 0

### 3.4 — Copy and move

- **Input** `[bash]` → `cp hello.txt backup.txt`, `mv hello.txt hi.txt`, `mv hi.txt notes/`, `ls -p notes` (one check) → `next`. **Friction**: 0

### 3.5 — Removing

- **Input** `[bash]` → `ls`, `rm backup.txt` (silent, no confirmation: uneasy), `ls` (check) → `next`. **Friction**: 0

### Stage 3 gate

- **Input** `[recall]` → `touch` ✓; `gone` ✓; `mv old.txt new.txt` ✓
- **Task**: `echo hello > notes.txt`, `cat notes.txt`, `cp notes.txt backup.txt`, `ls`, `mv notes.txt done.txt`, `rm backup.txt`, `ls`, `check` → cleared first check
- **Friction**: 0 -1 = **-1**

### Stage 4 intro, 4.1 — The parts of a command

- **Jargon**: "streams" in the Stage 4 title and intro, undefined; "asks where a program lives, if it exists" / "installed" (read as Windows install)
- **Input** `[bash]` → `wc -l poem.txt` (4), `echo "hello world"`, `command -v vim` (`/usr/bin/vim`) → `next`. **Friction**: -1

### 4.2 — Spaces and quotes

- **Input** `[bash]` → `touch my notes.txt`, `ls` (check), `touch "my notes.txt"`, `ls` (check) → `next`. **Friction**: -1

### 4.3 — The pipe

- **Jargon**: "What a command prints is a stream of lines." (stream undefined; the sentence defines it only as "what a command prints")
- **Input** `[bash]` → `seq 1 100 | wc -l`, `ls /usr/bin | wc -l`, `ls /usr/bin | sort | head` (capital-letter names sort first; unexpected) → `next`. **Friction**: -1

### 4.4 — Into a file / 4.5 — Pipe, then file / 4.6 — Many names at once

- **Input** `[bash]` → `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt`; `ls /usr/bin | wc -l > count-of-programs.txt`, `cat count-of-programs.txt`; `ls *.txt`, `wc -l *.txt` → `next` each. "glob" is defined on screen in 4.6. **Friction**: -1

### Stage 4 gate

- **Input** `[recall]` → `a path, /usr/bin/vim` ✓; `> replaces the file, >> adds to the end` ✓; `the shell splits the line on spaces, so it needs quotes` ✓
- **Task**: `seq 1 100 | wc -l > count.txt`, `cat count.txt`, `ls *.txt`, `check` → cleared first check
- **Friction**: -1 -1 = **-2**

### Stage 5 intro, 5.1 — Programs that take over the screen

- **Jargon**: "vimtutor" and "Vim" in the Stage 5 title and intro, never defined before the screen that says "Vim is a text editor" (5.2)
- **Input** `[bash]` → `man ls`, `raw 'q'` → `next`. The man page is dense (square-bracket synopsis); I did not read past the first screen. **Friction**: -2

### 5.2 — Leaving Vim

- **Read**: all
- **Monologue**: The Vim opening screen says "type  :q<Enter>  to exit". I typed it exactly as printed, brackets and all.
- **Input** `[bash]` → `vim` (skipping the repeated `command -v vim`), **`:q<Enter>`**, `:q`, `next`
- **Response to `:q<Enter>`**: `E488: Trailing characters: <Enter>`; Vim stayed open
- **Interpretation**: it points at `<Enter>`, which is the key, not letters; lesson 5.2 had said "type :q and press Enter". Understood, no charge (a borderline call: "Trailing characters" alone would not have told me).
- **Ladder rung**: message; resolved because the lesson text sat two screens back. **Friction**: -2

### 5.3 — The copy and the file / 5.4 — Throw it away / 5.5 — Keep it / 5.6 — vimtutor

- **Jargon**: 5.3 "working copy" (read as a buffer, fine). 5.6 "On Linux, install the full vim package. On macOS with Homebrew, brew install vim adds it." (Linux, macOS, Homebrew, package all undefined; not acted on).
- **Input** `[bash]` → 5.4: `vim practice.txt`, `raw 'i'`, `raw 'abc'`, `raw '\x1b'`, `:q!`, `cat practice.txt` (still `before`). 5.5: same with `xyz` and `:wq`, `cat practice.txt` (`xyzbefore`). 5.6: `command -v vimtutor` (`/usr/bin/vimtutor`). After Esc the screen text I received did not visibly change (`-- INSERT --` stayed); I could not tell whether Esc had worked and went on as told.
- **Friction**: -2

### Stage 5 gate

- **Input** `[recall]` → `press q` ✓; `:wq` ✓; `no, the changes were thrown away` ✓ ("on disk" read as the saved file)
- **Task phase 1**: `cat practice.txt`, `vim practice.txt`, `i`, `qrs`, Esc, `:q!`, `cat practice.txt`, `check`. **Phase 2**: `vim practice.txt`, `i`, `k`, Esc, `:wq`, `cat practice.txt` (`kbefore`), `check`.
- **Cleared** first check each phase. **Friction**: -2 -1 = **-3**

### Finale — You're ready for vimtutor

- **Read**: all. `[exited 0]`. The finale names `sudo apt install vim`, `sudo dnf install vim-enhanced`, `brew install vim` and "distro" without defining them.

## Per gate

| Gate | Recall attempts | Rejected inputs | Task checks | Rung | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1,1,1 | 0 | 1 (3 follow-ups right) | none | cleared |
| 2 | 1,1,1 | 0 (one `bash` rejection in the task, `cd .\practice`) | 1 | message only | cleared |
| 3 | 1,1,1 | 0 | 1 | none | cleared |
| 4 | 1,1,1 | 0 | 1 | none | cleared |
| 5 | 1,1,1 | 0 | 1 per phase (2) | none | cleared |

No task `check` ever showed a `○`; every first check passed.

First-check results per gate task: 1 pass, 2 pass, 3 pass, 4 pass, 5 phase 1 pass, 5 phase 2 pass.

## End of sitting

- **Final friction**: -3 at the finale (screen "You're ready for vimtutor", `[exited 0]`). Did not quit.
- By source: reading-limit/density charges 0; rejections (+2 each) 1 (the `.\practice` rejection, +2); mode confusion 0; gates cleared -5. Total +2 -5 = -3.
- **Stages cleared**: 1, 2, 3, 4, 5 (all five); turns used 187 of 240.
- **Equivalent human sitting time (estimate)**: about 75 to 90 minutes, from roughly 187 inputs plus stalls on `:q<Enter>`, `.\practice`, the `.`/`..` names and the Stage 5 install sentences.

### Habits performed

| Screen | Exact input | Reply verbatim | Recovered from the reply? |
| --- | --- | --- | --- |
| 1.2 | `cls` | `bash: cls: command not found` | Yes, via the lesson's own "Ctrl+L" line, not via the error |
| 2.2 | `dir` | `bash: dir: command not found` | Yes, via the screen's first line naming `ls` |
| 2.3 | `cd..` | `bash: cd..: command not found` | Yes, the screen's last sentence names this exact mistake |
| Stage 2 gate task | `cd .\practice` | `bash: cd: .practice: No such file or directory` | No, the reply did not help; recovered by copying `cd stage1` from 2.5. +2 |
| 5.2 (Vim splash) | `:q<Enter>` (literal brackets) | `E488: Trailing characters: <Enter>` | Yes, with the lesson text (borderline) |
| 1.3 / 2.2 | looked for a drive letter at `/` | n/a (no command) | Mostly: "the top of everything" in 2.2 |

### Undefined terms met before a screen defined them

- 1.1: "quotes make them one word" (what word)
- 1.3: "An ordinary bash prompt usually ends in $." (bash; defined in 1.4)
- 1.4: "terminal → shell → program: the window, bash, and date." (terminal, shell)
- 1.5: "An AI assistant that "runs commands" for you goes the same way"
- 2.2: "also the hidden names, which start with a dot" (hidden); `ls -a` output `.` and `..`, with no explanation until 2.5
- 3.3: "you are inside a program"
- Stage 4 title/intro: "Commands and streams"; 4.3 "a stream of lines"
- 4.1: "asks where a program lives, if it exists", "installed"
- Stage 5 title/intro: "vimtutor", "Vim" (first defined in 5.2: "Vim is a text editor")
- 5.2 Vim splash: "type  :q<Enter>  to exit" (`<Enter>` notation)
- 5.3: "working copy"
- 5.6 and finale: "Linux", "macOS", "Homebrew", "package", "distro", "sudo"

### Candidate F-nnn (valid input rejected, dead end, false statement)

- Candidate F-001: none confirmed. Nothing valid was rejected by the tutor and every first `check` passed.

### Candidate O-nnn (ambiguous phrasing, jargon, pace)

- Candidate O-001 (Stage 2 gate task, input `cd .\practice`): the reply `bash: cd: .practice: No such file or directory` drops the backslash and names a different path; nothing on any prior screen mentions the backslash. This was the only +2 of the sitting.
- Candidate O-002 (Vim opening screen, input `:q<Enter>`): the tutor's `[prompt] E488: Trailing characters: <Enter>` is the only message; the splash text `type  :q<Enter>  to exit` is Vim's own notation and differs from 5.2's "type :q and press Enter".
- Candidate O-003 (2.2, input `ls -a`): the listing prints `.` and `..` before 2.5 defines them: "Three short names:  .  here, the current directory    ..  one level up".
- Candidate O-004 (Stage 4 title, 4.3 sentence "What a command prints is a stream of lines."): "streams" is the stage name, but the sentence gives no definition, and the Stage 1 recall question 3 ("where does its output go?") asks about output before any screen says where output goes.
- Candidate O-005 (5.2, 5.4, 5.5, 5.6): after `raw '\x1b'` in Vim the received text showed `-- INSERT --` unchanged, so there was no visible sign Esc had worked (sitting-client rendering, not necessarily the tutor).
- Candidate O-006 (5.6 and finale): "On Linux, install the full vim package. On macOS with Homebrew, brew install vim adds it." and "install your distro's full vim package (Debian/Ubuntu: sudo apt install vim; ...)" use Linux, macOS, Homebrew, distro, sudo without definition (not needed when vimtutor is present).
- Candidate O-007 (Stage 2 gate task intro): "make a folder called practice (inside this stage's folder)" was ambiguous after 2.6 had left me in `demo`; `pwd` showed the shell had been reset to `.../stage2`.
- Candidate O-008 (2.4): the screen's `cd /var/folders/.../shelltutor-sim-home-el7lsro4` wraps across two lines at 80 columns, so the typed command looks broken on screen.

### Debrief (out of character)

1. "cd .\practice" produced ".practice" in the error; no screen says a backslash is not a path separator, so the sentence "A full name works from anywhere" and the 1.4 sentence "A stray / in front or a missing space earns the same kind of message" do not cover it.
2. Vim's "type  :q<Enter>  to exit" contradicts nothing in 5.2 but uses a notation the tutor never explains.
3. "the current directory", "hidden names" and the `.`/`..` entries in 2.2 appear before the sentence that names them (2.5: "Three short names").
4. "What a command prints is a stream of lines." and the Stage 4 title use "stream"; the Stage 1 gate asks "where does its output go?" with no teaching sentence for it (answered "on the screen").
5. Stage 5 title and intro say "vimtutor" and "Vim" before "Vim is a text editor"; 5.6 and the finale list Linux, macOS, Homebrew and distro commands without definition.
