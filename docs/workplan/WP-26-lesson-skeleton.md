---
title: WP-26 — Lesson skeleton: one typeable block, body ≤ 12 rows, the practice-folder thread — awaiting operator approval
category: planning
component: workplan
status: drafted
version: 0.2.0
last_updated: 2026-11-09
tags: [workplan, lessons, density, content, a11, a12]
priority: high
---

# WP-26 — Lesson skeleton (content)

**Governing text**: `docs/design-consultant-response-2026-11.md` §3.7,
adopted in principle by A11; the practice-folder thread of A12;
`audit/2026-11-09/wp25-chrome-v2.md` (screens over the 19-row panel).
**Status**: drafted for operator approval. Nothing here is implemented.
**Tier**: core standard, then one synthetic round (A10: the loop resumes
when lesson content changes).

## 1. The rule

Every lesson is: a model (≤ 2 lines) · ONE typeable block of 1–4 commands,
each with a short `#` aside · a "notice" of ≤ 3 lines · the `▶` line.
Body ≤ 12 rows, aimed at ≤ 10 so the panel is ≤ 19. A lesson that needs
two typeable blocks becomes two lessons. Concept screens with nothing to
type (1.5, 5.3) keep ≤ 8 body lines. Stage intros are ≤ 4 lines and list
no commands (the cleared screen does that, after the fact).

Consequence: lessons get shorter and more numerous.

| Stage | Lessons now | Lessons proposed |
| --- | ---: | ---: |
| 1 Where am I? | 5 | 5 |
| 2 Paths | 4 | 6 |
| 3 Files | 3 | 5 |
| 4 Commands and streams | 4 | 6 |
| 5 Ready for vimtutor | 5 | 6 |
| Total | 21 | 28 |

## 2. What is cut, and what must survive

Cut from the core (each needs the operator's yes):
- `ls /usr/bin` from 2.2 (returns in 4.3); `cd /tmp` from 2.3.
- `grep ^a` pipelines from the pipe lesson (`^` was never defined;
  Arthur stalled on it). `grep` stays out of the core; the finale no
  longer lists it.
- `<` input redirection (not gated, not needed for vimtutor).
- `vim --version` from 5.2 (a 60-line wall; Maya O-001).
- The command and symbol tables in the Stage 2, 3 and 4 intros.
- `rmdir` (listed in the Stage 3 intro, never used).

Must survive, with its new home:
- Stray slash / missing space (O-R, O-AB): 1.4's notice; `cd..` in 2.3.
- `$` as the ordinary prompt ending (F-017): 1.3's notice.
- Ctrl+C at a prompt versus `q` in a full-screen program (F-024): 1.2.
- `mkdir` before the Stage 2 gate (F-022): new 2.6.
- `echo word > file` before the Stage 3 gate (F-028): 3.1.
- `cd -` and "home is outside the practice folder" (O-AC): 2.4.
- 3.3 asks the learner to type its commands (O-AI): 3.4, 3.5.
- The sentence each recall question depends on is the FIRST sentence of
  its paragraph (Leo reads first sentences): checked per question in §5.

## 3. The screens

Colour is implied: typeable lines green, `#` asides grey, a named concept
or key bold, the `▶` line yellow. `<folder>` is the real practice-folder
path printed at run time.

### Orientation

```text
Orientation

Below this panel is a real shell prompt. It looks like:

  shelltutor>

Type a command there and press Enter; the shell runs it. Four words
steer the tutor instead: next, prev, show and quit. A fifth, check,
appears when a stage's task is ready to be tested.

▶ Type next to begin Stage 1.
```

### Stage 1 intro

```text
Stage 1: Where am I?

Five short lessons, then a task. You'll run your first commands and
learn the few keys that make a shell comfortable.

▶ Type next for lesson 1.1.
```

### 1.1 Running a command

```text
Running a command

A command is a name, then the words you hand it. echo is the simplest
one: it repeats its words back to you.

  echo hello                   # prints hello, then the prompt returns
  echo I am at the shell       # spaces separate the words
  echo "I am at the shell"     # quotes make them one word

Notice the quotes never print. They only group.

▶ Try all three, then type next.
```

### 1.2 Four keys

```text
Four keys

These keys make the shell comfortable. Try each one now.

  Tab       finishes a word: type echo p, press Tab, then Enter
  ↑         brings back your last line; Enter runs it again
  Ctrl+C    throws away the line you are typing; a fresh prompt
  Ctrl+L    clears the screen; type show to bring this lesson back

Ctrl+C is the way out at a prompt. Inside a full-screen program
(you'll meet one in Stage 3) the way out is q.

▶ Try each key, then type next.
```

### 1.3 Where am I, who am I, when is it

```text
Where am I, who am I, when is it

The tutor made a folder for you to practise in. Ask the system where
it is, who you are, and what time it is.

  pwd        # where: the folder you are in
  whoami     # who: your user name
  date       # when: the date and time

pwd printed the full name of your practice folder.
This prompt ends in >. An ordinary bash prompt usually ends in $.

▶ Run all three, then type next.
```

### 1.4 The shell, caught in the act

```text
The shell, caught in the act

Type a real command, then the same letters scrambled.

  date     # prints the date and time
  dtae     # bash: dtae: command not found

bash: is the shell speaking. It looked for a program named dtae and
found none. A stray / in front or a missing space earns the same kind
of message: read it, then type the line again.

terminal → shell → program: the window, bash, and date.

▶ Try both, then type next.
```

### 1.5 Who else types here (nothing to type)

```text
Who else types here

Every command goes terminal → shell → program. An AI assistant that
"runs commands" for you goes the same way: it types a line, the shell
finds the program, the program runs.

So three habits count twice, for you and for a helper:
  read the line before anyone presses Enter
  know which folder it will run in
  read what comes back

▶ Type next for Stage 1's task.
```

### Stage 2 intro

```text
Stage 2: Paths

Six short lessons, then a task. The shell is always standing in one
folder. You'll learn to see where, look around, and move.

▶ Type next for lesson 2.1.
```

### 2.1 Where you are

```text
Where you are

You are always standing in one folder: the current directory. Here
is your practice folder, drawn as a tree:

  <folder>  ← you are here
  ├── poem.txt
  ├── numbers.txt
  ├── stage1/
  └── stage2/

  pwd        # predict what it prints, then run it

The line pwd prints is the full name of the "you are here" folder.

▶ Run pwd, then type next.
```

### 2.2 What is here

```text
What is here

ls lists the names in the folder you are standing in.

  ls            # the names
  ls -p         # the same, with / after each folder
  ls -a         # also the hidden names, which start with a dot
  ls /          # a folder you are not in: the top of everything

Notice stage1/ in the second listing: the slash means a folder you
could step into.

▶ Try all four, then type next.
```

### 2.3 Moving

```text
Moving

cd changes the folder you are standing in. It prints nothing; pwd
shows that it worked.

  cd ..      # up one level, to the folder that contains this one
  pwd        # see where you are now
  cd -       # back to where you just were

cd.. with no space is a different word, and bash cannot find it.

▶ Try all three, then type next.
```

### 2.4 Home and back (new)

```text
Home and back

Every user has a home folder. ~ is its short name.

  cd                 # with nothing after it: go home
  pwd                # home is outside your practice folder
  cd <folder>        # come back, using the folder's full name

A full name works from anywhere. That is what makes it a full name.

▶ Go home and come back, then type next.
```

### 2.5 Names for places

```text
Names for places

A path names a place. Three short names:

  .     here, the current directory
  ..    one level up
  ~     your home folder

A relative path starts where you are: in ~/projects, the name notes
means ~/projects/notes. An absolute path starts from /, the top:
/usr/bin is the same place wherever you stand.

  ls ..      # look one level up without moving
  ls ~       # look at home without moving

▶ Try both, then type next.
```

### 2.6 Making a folder (new)

```text
Making a folder

mkdir makes a new folder inside the one you are standing in.

  mkdir demo     # make it
  ls -p          # demo/ is in the list
  cd demo        # step into it
  pwd            # its full name ends in /demo

You'll do exactly this in the task that follows.

▶ Try all four, then type next.
```

### Stage 2 task line (and every gate task)

One grey line under the task's steps: `This task runs in <stage folder>;
pwd shows it.`

### Stage 3 intro

```text
Stage 3: Files

Five short lessons, then a task. You'll make, read, copy, move and
remove files. One warning now: rm removes for good. There is no Trash.

▶ Type next for lesson 3.1.
```

### 3.1 Making files

```text
Making files

The tutor put poem.txt and numbers.txt one folder up. Now make your
own beside them.

  touch hello.txt            # an empty file
  echo hi > words.txt        # a file with the word hi in it
  mkdir notes                # a folder
  ls -p                      # all three are there

> sends what echo prints into a file instead of the screen. It prints
nothing when it works. More on > in Stage 4.

▶ Make all three, then type next.
```

### 3.2 Reading a file

```text
Reading a file

cat prints a whole file at once.

  cat words.txt          # the word you put there
  cat hello.txt          # nothing: the file is empty
  cat ../poem.txt        # the tutor's poem, one folder up

▶ Try all three, then type next.
```

### 3.3 Reading a long file (new)

```text
Reading a long file

less shows a long file one screen at a time. While it runs, the
prompt is gone: you are inside a program.

  less ../numbers.txt    # 50 lines, more than one screen

Space pages down, b pages back, q leaves. Ctrl+C does nothing
here; q is the way out.

▶ Open it, page down, press q, then type next.
```

### 3.4 Copy and move

```text
Copy and move

cp copies and leaves the original. mv moves; the same command renames.

  cp hello.txt backup.txt      # now there are two
  mv hello.txt hi.txt          # rename
  mv hi.txt notes/             # move into the folder
  ls -p notes                  # hi.txt is inside

▶ Try all four, then type next.
```

### 3.5 Removing (new)

```text
Removing

rm removes a file at once and for good. There is no Trash and no undo.

  ls                 # look first
  rm backup.txt      # remove it
  ls                 # it is gone

List before you remove: you, or an assistant typing for you.

▶ Try all three, then type next.
```

### Stage 4 intro

```text
Stage 4: Commands and streams

Six short lessons, then a task. You'll read a command's parts, then
join commands together and send what they print into files.

▶ Type next for lesson 4.1.
```

### 4.1 The parts of a command

```text
The parts of a command

A command line is a name, then options, then arguments.

  wc -l poem.txt         # name wc, option -l, argument poem.txt
  echo "hello world"     # one argument, because of the quotes
  command -v vim         # asks where a program lives, if it exists

command -v prints a path when the program is installed, and nothing
when it is not.

▶ Try all three, then type next.
```

### 4.2 Spaces and quotes (new)

```text
Spaces and quotes

The shell splits a line on spaces. Quote a name that has a space.

  touch my notes.txt       # two files: my, and notes.txt
  ls
  touch "my notes.txt"     # one file with a space in its name
  ls

It is the same for every command: vim my notes.txt would open two
files; vim "my notes.txt" opens one.

▶ Try them, then type next.
```

### 4.3 The pipe

```text
The pipe

A pipe, |, sends what one command prints into the next command.

  seq 1 100 | wc -l              # 100: wc counted seq's lines
  ls /usr/bin | wc -l            # how many programs live there
  ls /usr/bin | sort | head      # pipes stack: list, sort, first ten

Each piece is an ordinary command. Only the connector is new. | is
Shift+Backslash.

▶ Try all three, then type next.
```

### 4.4 Into a file

```text
Into a file

> sends what a command prints into a file. >> adds to the end.

  echo first > greeting.txt      # writes over whatever was there
  echo second >> greeting.txt    # adds a line at the end
  cat greeting.txt               # two lines

> replaces the file without asking, whoever typed the line.

▶ Try all three, then type next.
```

### 4.5 Pipe, then file (new)

```text
Pipe, then file

A pipe and a > work in one line: the last command's output goes to
the file.

  ls /usr/bin | wc -l > count-of-programs.txt
  cat count-of-programs.txt      # one number

You'll do this in the task that follows.

▶ Try both, then type next.
```

### 4.6 Many names at once

```text
Many names at once

* matches any run of characters in a file name. The shell fills in
the names before the command runs.

  ls *.txt         # every name ending in .txt
  wc -l *.txt      # count the lines in each one

Predict before you act: rm * would remove everything in the folder.

▶ Try both, then type next for Stage 4's task.
```

### Stage 5 intro

```text
Stage 5: Ready for vimtutor

Six short lessons, then a task. Some programs take over the whole
screen. You'll learn to enter and leave them, Vim included. After
this stage comes vimtutor.

▶ Type next for lesson 5.1.
```

### 5.1 Programs that take over the screen

```text
Programs that take over the screen

Most commands print and return. A few take over the screen until you
leave them; the prompt is gone while they run.

  man ls       # the manual page for ls; q leaves

man and less leave with q. Vim leaves differently; that is next.

▶ Open it, press q, then type next.
```

### 5.2 Leaving Vim

```text
Leaving Vim

Vim is a text editor. Learn the way out before anything else.

  command -v vim     # a path means it is installed
  vim                # opens with no file

To leave, type :q and press Enter. If Vim refuses, type :q! and
press Enter: that leaves and throws away any changes.

▶ Open vim, leave with :q, then type next.
```

### 5.3 The copy and the file (nothing to type)

```text
The copy and the file

Vim does not edit the file. It reads the file into a working copy
and you edit that. The file changes only when you write it back.

  file  →  working copy (you edit here)  →  file

  :w     write the copy to the file
  :q     quit, if nothing is unsaved
  :q!    quit and throw the changes away
  :wq    write, then quit

▶ Type next to try both.
```

### 5.4 Throw it away

```text
Throw it away

A file called practice.txt is in this folder.

  vim practice.txt

Inside Vim: press i, type a few letters, press Esc. Then type :q!
and press Enter.

  cat practice.txt       # unchanged: the changes were thrown away

▶ Do it, then type next.
```

### 5.5 Keep it (new)

```text
Keep it

The same again, but this time write the copy back.

  vim practice.txt

Inside Vim: press i, type a few letters, press Esc. Then type :wq
and press Enter.

  cat practice.txt       # now the file has your letters

▶ Do it, then type next.
```

### 5.6 vimtutor

```text
vimtutor

vimtutor is a command too. It opens Vim on a copy of a lesson file.

  command -v vimtutor    # a path means it is installed

No path? On Linux, install the full vim package. On macOS,
brew install vim adds it.

▶ Type next for Stage 5's task.
```

## 4. Vocabulary changes in these screens

"buffer" becomes "working copy" (5.3; Leo and Arthur both stalled on
"buffer"); the Stage 5 recall hint and accepted forms keep `buffer` as an
accepted word. "current directory" appears once (2.1) and "folder" is used
elsewhere. "print working directory" is dropped. Stage intro titles take
the short stage names ("Stage 2: Paths").

## 5. Recall questions: the sentence each depends on

| Question | First sentence that answers it |
| --- | --- |
| 1.Q1 `$` | 1.3 notice, its own line ("This prompt ends in >. An ordinary bash prompt usually ends in $.") |
| 1.Q2 pwd | 1.3 block aside and notice |
| 1.Q3 where output goes | 1.4: no sentence says "the screen" now; add to 1.1's aside ("prints hello") and keep the question; hint → `Lesson 1.1:` |
| 2.Q1 `cd ..` | 2.3 block aside |
| 2.Q2 `~` | 2.4 model |
| 2.Q3 `cd notes` in `~/projects` | 2.5, second paragraph's first sentence |
| 3.Q1 touch | 3.1 block |
| 3.Q2 after rm | 3.5 model |
| 3.Q3 rename | 3.4 model |
| 4.Q1 `command -v` | 4.1 notice |
| 4.Q2 `>` vs `>>` | 4.4 model |
| 4.Q3 two files | 4.2 model |
| 5.Q1 exit man | 5.1 block aside |
| 5.Q2 write | 5.3 list |
| 5.Q3 `:q!` | 5.4 |

Hints are renumbered to the new lesson numbers (FF-010 checks the anchor).

## 6. Implementation notes for the worker (after approval)

- New lesson functions and the stage loops' lesson counts; `prev`/`show`
  work across the new screens; stage intros' counts as written.
- Sentinels: one per new title; persona tables (`careful-beginner`,
  `second-try`) gain the new lessons' actions; the Stage 2 gate rehearsal
  (2.6) and Stage 4 rehearsal (4.5) do not pre-create the gate's files
  (gate setup resets its folder, as today).
- The interim squeeze in `show_screen` is removed; the 19-row panel is
  enforced by the height check (cap 19; concept screens included).
- `--info` label column re-aligned ("Practice folder").
- Gate task screens: the "This task runs in …" line.
- Cleared screens and the finale: command lists follow the cuts (no
  `grep`, `head` stays, `rmdir` gone).
- Density rows for every screen; FF-011 unaffected; FF-009/FF-010 re-run.
- Modules (`shells`, `env`) are NOT in this package: WP-28 applies the
  skeleton to them and adds the `SHELLTUTOR_HOME` beat (A12).

## 7. Evidence

One synthetic round (three personas, v0.2 sheets, same revision) after the
implementation; intake as before. The comparison of interest: lessons read
versus skipped, and whether the Stage 2 and Stage 4 tasks are passed on the
first `check` now that each is rehearsed in the lesson before it.
