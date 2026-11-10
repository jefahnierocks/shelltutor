---
title: WP-28 — Modules to the lesson skeleton; the SHELLTUTOR_HOME beat
category: planning
component: workplan
status: ready
version: 0.2.0
last_updated: 2026-11-09
tags: [workplan, modules, shells, env, content, a12, a13]
priority: medium
---

# WP-28 — Modules to the lesson skeleton

**Governing text**: A13's skeleton rule applied to the `shells` and `env`
modules; A12's last thread beat (`SHELLTUTOR_HOME` in `env`);
`audit/2026-11-09/wp26-lesson-skeleton.md` (module screens at 21–23 rows
since the squeeze was removed). **Status**: approved by the operator on 2026-11-10 with the review corrections of §Review (A15); the copy below already carries them.
**Tier**: module standard, plus one synthetic round shared with WP-29.

## What changes

- Every module screen within the 20-row harness budget, which then
  applies to module runs as it does to the core.
- `env` grows from five lessons to six: the variable lesson loses its
  `grep` lines (`grep` left the core in A13), and a new lesson shows the
  tutor itself reading a variable.
- `shells` keeps three lessons.
- Intros lose their bullet lists. Task screens lose their "(hint: …)"
  parentheses: the ladder's hint rung carries them (A3.8).

## Proposed copy

### shells — intro

```text
shells: what runs your commands

Three short lessons, then a task. This module stands alone and saves
nothing. You'll look at the shell as a program, at other shells, and
at the difference between your login shell and this one.

Assumes the five stages, or that you know ls, cd and >.

▶ Type next for lesson 1.
```

### shells 1 — the shell is a program

```text
The shell is a program

The shell reads your line, finds the program you named, and runs it.
It is itself a program, and you can look at it.

  echo $BASH_VERSION     # the version of the shell running now
  ps -o pid,comm         # the programs on this terminal, by name

Two of those lines are shells: the tutor's own, and the one you are
typing into. $BASH_VERSION is a variable: a name that holds a value.

▶ Run both, then type next.
```

### shells 2 — other shells exist

```text
Other shells exist

bash is common on Linux and is what this tutor runs. zsh is the
default on macOS. fish is another, installed separately.

  command -v zsh fish     # one path for each that is installed

No line for a shell means it is not installed. That is normal. What
differs between shells is setup and prompt; ls, paths and pipes are
the same in all of them.

▶ Run it, then type next.
```

### shells 3 — your login shell and this shell

```text
Your login shell and this shell

Your login shell is the one a new terminal window starts. It can
differ from the shell running now.

  echo $SHELL            # your login shell
  echo $BASH_VERSION     # the shell running now

This tutor always runs its lessons in bash, whatever your login shell
is. What you practise here works the same under zsh.

▶ Compare the two lines, then type next for the task.
```

### shells — task

```text
shells — task

Find out whether zsh is installed, and keep the answer in a file.

  1. Ask the shell where zsh is.
  2. Send what it prints into a file named zsh.txt.

If zsh is not installed the file is empty, and that is a right answer.
This task runs in the module's own folder; pwd shows it.

▶ Do both steps, then type check.
```

### env — intro

```text
env: variables and the prompt

Six short lessons, then a task. This module stands alone and saves
nothing. Everything stays inside this practice shell; your own setup
files are not touched.

Assumes the five stages, or that you know ls, cd and >.

▶ Type next for lesson 1.
```

### env 1 — variables

```text
Variables

A variable is a name that holds a value. The shell swaps $name for
the value before it runs the line.

  echo $HOME        # one the shell already has
  pet=owl           # set your own: no spaces around =
  echo $pet         # prints owl
  env | head        # some of the variables programs receive

pet is not in that list yet. The next lesson shows why.

▶ Try all four, then type next.
```

### env 2 — export

```text
Export

A program the shell starts is a child. It receives only the variables
you exported.

  pet=owl                    # set it again: each screen is a new shell
  bash -c 'echo pet=$pet'    # pet=    : the child sees nothing
  export pet                 # mark it for children
  bash -c 'echo pet=$pet'    # pet=owl

The single quotes matter: they leave $pet for the child to fill in.

▶ Run all four in order, then type next.
```

### env 3 — PATH is a list

```text
PATH is a list

PATH holds folders separated by colons. When you type a command name,
the shell looks in those folders, in order, and runs the first match.

  echo "$PATH"                  # one long line
  echo "$PATH" | tr : '\n'      # one folder per line
  command -v ls                 # the full name of ls: its folder, then ls

A program in a folder that is not on the list is not found by name.

▶ Run all three, then type next.
```

### env 4 — the prompt is a variable

```text
The prompt is a variable

The text before your cursor is the variable PS1. Change it and the
prompt changes at once.

  PS1='me> '        # the prompt is now me>
  PS1='$ '          # and now a plain dollar sign

That last one is the prompt most terminals show. Watch the next
screen: the prompt will be back to shelltutor>.

▶ Change it twice, then type next.
```

### env 5 — a program that reads a variable (new)

```text
A program that reads a variable

This tutor is configured the same way. It reads SHELLTUTOR_HOME to
decide where your practice folder goes.

  echo "[$SHELLTUTOR_HOME]"     # [] means: not set, so the default is used
  pwd                           # where you are now, inside the practice folder

To put the folder somewhere else, set the variable on the line that
starts the tutor:   SHELLTUTOR_HOME=~/practice ./shelltutor

▶ Run both, then type next.
```

### env 6 — where this lives for real (nothing to type)

```text
Where this lives for real

The prompt went back because each screen starts a fresh shell. A real
terminal reads one file when it starts, and settings there last:

  ~/.bashrc     if your login shell is bash
  ~/.zshrc      if it is zsh
  ~/.bash_profile   on macOS with bash

A line like  PS1='me> '  in that file gives you your own prompt every
time. Edit it in a normal terminal, not here; the tutor never touches it.

▶ Type next for the task.
```

### env — task

```text
env — task

Show that a child program can see a variable you exported.

  1. Set TOPIC to the word shell.
  2. Export it.
  3. Run a child with bash -c that prints $TOPIC into seen.txt.

This task runs in the module's own folder; pwd shows it.

▶ Do the steps, then type check.
```

## Review (A15) — corrections carried above, and the rules behind them

1. **No bare brackets in a child's `echo`** (`[owl]` is a glob in the
   child): env 2 prints `pet=` and `pet=owl`.
2. **env 4 changes the prompt, and the harness must follow it**: the
   persona types both `PS1=` lines and the sentinel table for that screen
   expects `me> ` and then `$ ` as prompts, in order. The walk does not
   skip the commands.
3. **`SHELLTUTOR_HOME` in the practice shell is the learner's own value,
   never the normalised one**: unset stays unset (so `[]` is true and the
   aside is true); a value the learner set is passed through as typed.
   Check C-004 (normalisation) and the C-007 scrub list, implement that
   rule, and record it in both contracts.
4. **The env task verifier requires `export` of `TOPIC` in the history as
   well as `shell` in `seen.txt`**; without it a double-quoted
   `bash -c "echo $TOPIC"` passes with no export. The gate cannot tell
   single from double quotes in the `bash -c` line; it checks what it can,
   and the report says so.
5. **No path placeholder on task screens**: "the module's own folder".
6. **shells 1 uses `ps -o pid,comm`** (POSIX; FF-008 must pass). macOS
   prints `comm` as a full path, Linux as a bare name; the notice is true
   for both.
7. env 3's aside says what `command -v ls` prints.
8. Both intros carry the assumption line.
9. **Module titles lose the position prefix; the header shows
   `<module>  k/n`** (for example `shells  1/3`), `task` at the task.
   Sentinels and `selftest_modules` follow.
10. env 1 and env 2 have four-command blocks: within the skeleton's 1–4,
    recorded as "one family" in the density rows.
11. **Module standard amended**: three to six lesson screens (was three to
    five), in `docs/direction-decisions-2026-11.md` §module standard, same
    commit series.
12. env 6 shows the prompt line a learner wants to take home.

Notes also carried: env 4 says the `$` prompt is the one most terminals
show; the shells task is verified by file content (what `command -v zsh`
prints on this host, or empty), so `which zsh > zsh.txt` passes, and the
history check for that task is dropped or widened to either command;
a script comment at env 2 says `bash -c` resolves `bash` through `PATH`
and need not be the practice shell's binary (not F-014); before any module
bundle is committed, confirm the D-19 redaction replaces the login name
across the whole bundle (`env | head` prints `USER=` and `LOGNAME=`), and
add a self-test case if it does not.

## Notes for the worker

- Hints: the removed "(hint: …)" lines become each task's attempt-2 hint
  if they are not already; FF-010 anchors renumbered for `env`; FF-009
  clean.
- Recall questions unchanged; `env` Q3's anchor stays lesson 4.
- Cleared lists follow the copy (`ps -o pid,comm`; nothing lists `grep`).
- Harness: module personas type the new blocks; the 20-row budget is
  enforced for module runs; Linux evidence via the workflow.

## Commits

1. `feat(shells): three lessons and the task to the skeleton (A13)`
2. `feat(env): six lessons — grep lines out, the SHELLTUTOR_HOME lesson in (A12, A13)`
3. `feat(modules): header shows k/n; titles without prefix; assumption line; SHELLTUTOR_HOME passed through as typed (C-004, C-007)`
4. `fix(env): task requires export in history; shells task verified by content`
5. `chore(sim): module personas and prompt sentinels for env 4; budget for modules; redaction check; hints; density rows; module standard three to six; STATUS`
