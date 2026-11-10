---
title: WP-28 — Modules to the lesson skeleton; the SHELLTUTOR_HOME beat — awaiting operator approval
category: planning
component: workplan
status: drafted
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, modules, shells, env, content, a12, a13]
priority: medium
---

# WP-28 — Modules to the lesson skeleton

**Governing text**: A13's skeleton rule applied to the `shells` and `env`
modules; A12's last thread beat (`SHELLTUTOR_HOME` in `env`);
`audit/2026-11-09/wp26-lesson-skeleton.md` (module screens at 21–23 rows
since the squeeze was removed). **Status**: drafted for operator approval.
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

▶ Type next for lesson 1.
```

### shells 1 — the shell is a program

```text
shells 1 — the shell is a program

The shell reads your line, finds the program you named, and runs it.
It is itself a program, and you can look at it.

  echo $BASH_VERSION     # the version of the shell running now
  ps                     # the programs running here: bash, and ps

$BASH_VERSION is a variable: a name that holds a value. The shell
swaps $name for its value before it runs the line.

▶ Run both, then type next.
```

### shells 2 — other shells exist

```text
shells 2 — other shells exist

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
shells 3 — your login shell and this shell

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
This task runs in <practice folder>/shells; pwd shows it.

▶ Do both steps, then type check.
```

### env — intro

```text
env: variables and the prompt

Six short lessons, then a task. This module stands alone and saves
nothing. Everything stays inside this practice shell; your own setup
files are not touched.

▶ Type next for lesson 1.
```

### env 1 — variables

```text
env 1 — variables

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
env 2 — export

A program the shell starts is a child. It receives only the variables
you exported.

  pet=owl                    # set it again: each screen is a new shell
  bash -c 'echo [$pet]'      # [] : the child sees nothing
  export pet                 # mark it for children
  bash -c 'echo [$pet]'      # [owl]

The single quotes matter: they leave $pet for the child to fill in.

▶ Run all four in order, then type next.
```

### env 3 — PATH is a list

```text
env 3 — PATH is a list

PATH holds folders separated by colons. When you type a command name,
the shell looks in those folders, in order, and runs the first match.

  echo "$PATH"                  # one long line
  echo "$PATH" | tr : '\n'      # one folder per line
  command -v ls                 # the folder where ls was found

A program in a folder that is not on the list is not found by name.

▶ Run all three, then type next.
```

### env 4 — the prompt is a variable

```text
env 4 — the prompt is a variable

The text before your cursor is the variable PS1. Change it and the
prompt changes at once.

  PS1='me> '        # the prompt is now me>
  PS1='$ '          # and now a plain dollar sign

Watch the prompt on the next screen: it will be back to shelltutor>.

▶ Change it twice, then type next.
```

### env 5 — a program that reads a variable (new)

```text
env 5 — a program that reads a variable

This tutor is configured the same way. It reads SHELLTUTOR_HOME to
decide where your practice folder goes.

  echo "[$SHELLTUTOR_HOME]"     # [] means: not set, the default is used
  pwd                           # where the practice folder really is

To put the folder somewhere else, set the variable on the line that
starts the tutor:   SHELLTUTOR_HOME=~/practice ./shelltutor

▶ Run both, then type next.
```

### env 6 — where this lives for real (nothing to type)

```text
env 6 — where this lives for real

The prompt went back because each screen starts a fresh shell. A real
terminal reads one file when it starts, and settings there last:

  ~/.bashrc     if your login shell is bash
  ~/.zshrc      if it is zsh
  ~/.bash_profile   on macOS with bash

A line like  export PATH="$HOME/bin:$PATH"  belongs in that file. Edit
it in a normal terminal, not here; the tutor never touches it.

▶ Type next for the task.
```

### env — task

```text
env — task

Show that a child program can see a variable you exported.

  1. Set TOPIC to the word shell.
  2. Export it.
  3. Run a child with bash -c that prints $TOPIC into seen.txt.

This task runs in <practice folder>/env; pwd shows it.

▶ Do the steps, then type check.
```

## Notes for the worker (after approval)

- Check whether `SHELLTUTOR_HOME` reaches the practice shell (C-007 scrub
  list). If it is scrubbed, pass it through and record the change in
  C-007; `echo "[$SHELLTUTOR_HOME]"` must print the real value or `[]`.
- Hints: the two removed "(hint: …)" lines become each task's attempt-2
  hint if they are not already; FF-010 anchors renumbered for `env`
  (lesson 6 was 5); FF-009 clean.
- Recall questions unchanged; `env` Q3's lesson anchor stays lesson 4.
- Cleared lists follow the copy (`env` keeps `env`; nothing lists `grep`).
- Harness: module personas type the new blocks; the 20-row budget is
  enforced for module runs; Linux evidence via the workflow.

## Commits

1. `feat(shells): three lessons and the task to the skeleton (A13)`
2. `feat(env): six lessons — grep lines out, the SHELLTUTOR_HOME lesson in (A12, A13)`
3. `chore(sim): module personas, sentinels, budget for modules; hints; density rows; C-007 if changed; STATUS`
