# Synthetic walkthrough — maya-env-7 (module `env`)

## Sitting

- Date: 2026-11-10
- Persona (file in `docs/sim-personas/`) and learner role: `maya.md`, Maya, adult beginner (`search-first-skimmer`). Background for this sitting: finished the five-stage course last week; knows ls, cd, pwd, echo, `>` and next/prev/show/quit/check; has never seen a shell variable.
- Persona sheet version: 0.2.0
- Scripted errors performed: none (Maya has no scripted schedule)
- Turn cap: 90 (module sitting). One turn = one `send` or one `raw`. Turns used: 30 (30 `send`, 0 `raw`)
- Simulation rules confirmed (zero forward knowledge, reading limit, friction meter): yes; four-line reading limit, +1 density charge only where a skipped line later causes a rejection or wrong turn, friction quit at 8.
- Tutor revision and invocation: 40c11cf (script a7cd1ac); `sitting.py start --arg env`, bash `/bin/bash` 3.2.57; sitting dir `sitting-maya-env-7`.
- `--info` lines the persona was shown, if any: none.
- Procedure note: three early calls broke the one-command-per-call rule (one call chained a `note` and a `send`; one pair of `send`/`note` calls ran in parallel; the `$PATH` pipeline echoed once more than needed). No effect on tutor behaviour was seen.
- Environment values: `env | head` printed ten names (SHELL, TERM, TMPDIR, OLDPWD, LC_ALL, USER, VIMINIT, BASH_SILENCE_DEPRECATION_WARNING, COLUMNS, PAGER); values not copied. Login name written as `[user]`.

## Per screen

### intro — env: variables and the prompt

- **Read**: all (short).
- **Jargon**: "Everything stays inside this practice shell"; "setup files".
- **Monologue**: six lessons, type next. Easy.
- **Input** `[nav]` → `next` → accepted.
- **Friction**: 0.

### 1/6 — Variables

- **Read**: all prose (about three lines); the four commands.
- **Jargon**: "A variable is a name that holds a value"; "the shell swaps $name for the value before it runs the line"; "programs receive".
- **Monologue**: a name with a value, dollar sign gets swapped. Four things to type; do them one at a time.
- **Inputs** `[bash]`: `echo $HOME` → a long temp-folder path (aside "one the shell already has": matches). `pet=owl` → no output. `echo $pet` → `owl` (matches). `env | head` → ten NAME=value lines; `pet` not among them (matches "pet is not in that list yet").
- **Interpretation**: variable = a name with a value; `$` fills it in. (One sentence: yes.)
- **Rung**: none. **Friction**: 0.

### 2/6 — Export

- **Read**: skimmed. Read the first four prose lines; skipped "The single quotes matter: they leave $pet for the child to fill in." (no consequence: copied the printed command exactly).
- **Jargon**: "A program the shell starts is a child"; "marked for children"; "each screen is a new shell".
- **Monologue**: child program, only sees what you export. Copy all four as printed.
- **Inputs** `[bash]`: `pet=owl` → none. `bash -c 'echo pet=$pet'` → `pet=` (matches). `export pet` → none. `bash -c 'echo pet=$pet'` → `pet=owl` (matches).
- **Interpretation**: export lets other programs see it. (One sentence: yes.)
- **Friction**: 0.

### 3/6 — PATH is a list

- **Read**: all prose.
- **Jargon**: "PATH holds folders separated by colons"; `tr : '\n'`; `command -v ls`.
- **Inputs** `[bash]`: `echo "$PATH"` → one very long colon-joined line (matches "one long line"). `echo "$PATH" | tr : '\n'` → one folder per line (matches). `command -v ls` → `/bin/ls` (matches "its folder, then ls").
- **Interpretation**: PATH is the list of folders where commands live; ls is in /bin. (One sentence: yes.)
- **Friction**: 0.

### 4/6 — The prompt is a variable

- **Read**: all.
- **Jargon**: "PS1".
- **Inputs** `[bash]`: `PS1='me> '` → prompt became `me>` (matches). `PS1='$ '` → prompt became `$` (matches). Then `next` typed at the `$` prompt.
- **Interpretation**: the prompt is just a setting. The screen promised the next screen's prompt would be `shelltutor>`; it was.
- **Friction**: 0.

### 5/6 — A program that reads a variable

- **Read**: all.
- **Jargon**: "SHELLTUTOR_HOME".
- **Inputs** `[bash]`: `echo "[$SHELLTUTOR_HOME]"` → `[<long temp path>]`. **Mismatch**: aside says `# [] means: not set, so the default is used`; the output was not `[]` but a filled-in path in a temp folder. Maya cannot tell why; she moves on without friction because nothing is rejected. `pwd` → `<temp path>/env` (aside "where you are now, inside the practice folder": matches).
- **Interpretation**: the tutor reads a variable to know where to put the folder. The aside about `[]` neither helped nor was true here.
- **Friction**: 0.

### 6/6 — Where this lives for real

- **Read**: skimmed. Skipped the three dotfile lines (`~/.bashrc`, `~/.zshrc`, `~/.bash_profile`): does not know which login shell she has. Read "settings last" and the `▶` line.
- **Jargon**: "login shell", "~/.bashrc", "~/.zshrc", "~/.bash_profile".
- **Interpretation**: settings last if put in a dotfile. (One sentence: yes, vaguely.)
- **Input** `[nav]` → `next` → gate.
- **Friction**: 0.

### gate — Recall (3 questions)

- Q1 "Which command makes a variable visible to the programs the shell starts? set export env echo" → `export` ✓.
- Q2 "What does PATH hold? a list of folders / one folder / a file name" → `a list of folders` ✓.
- Q3 "You type PS1='me> ', then next. What is the prompt on the next screen? me> / shelltutor>" → `shelltutor>` ✓.
- Attempts: 1 each; no rejections; no hint.
- **Friction**: -1 (recall gate cleared) → -1.

### task — env — task

- **Read**: all.
- **Monologue**: three steps; copy the shape of lesson 2.
- **Inputs** `[bash]`: `TOPIC=shell`; `export TOPIC`; `bash -c 'echo $TOPIC > seen.txt'` (all silent).
- **Input** `[nav]` → `check` → "env cleared." The cleared screen printed no checklist and no `○` rows, only the summary of commands and keys. Verbatim check results: one `check`, passed on the first attempt.
- **Interpretation**: it worked; a child saw the variable.
- **Friction**: -2 (task gate cleared).

### cleared — env cleared.

- Lists the module's commands and keys (name=value, export name, echo "$PATH", env, PS1='$ ', SHELLTUTOR_HOME). `quit` → "Bye. A module saves nothing; run 'shelltutor env' to start it again." `[exited 0]`.

## Per gate

- Recall: 1 attempt per question, no rejected inputs, no rung shown.
- Task: 1 attempt, one `check`, passed; nothing marked `○`.
- Cleared.

## End of sitting

- Final friction: -2 (unfloored). Reading-limit charges 0; rejections (+2 each) 0; mode confusions 0; gates cleared -2 (recall, task). Did not quit; ended on the cleared screen, then `quit` (`[exited 0]`).
- Module cleared: `env`.
- Equivalent human sitting time: about 12 to 15 minutes (estimate), 30 turns, no stalls.
- Per lesson, did the output match the aside, and could Maya say what it showed: 1 matched, yes; 2 matched, yes; 3 matched, yes; 4 matched, yes; 5 one mismatch (`[]` vs filled path), vaguely; 6 no commands, vaguely.

### Candidate F-nnn

- **F-a (false statement on screen)**: screen 5/6, `echo "[$SHELLTUTOR_HOME]"`. The aside says `[] means: not set, so the default is used`; in this sitting it printed `[<path>]`, so the learner sees a set variable while the screen's following text implies it is not set. Likely the sim harness sets the variable; a maintainer should check whether a real learner also gets a non-empty value (the tutor sets it for its own use) and whether the aside should describe that case.

### Candidate O-nnn

- **O-a**: screen 2/6, "set it again: each screen is a new shell". Reads as a fact about the tutor, not yet explained; lesson 6 explains it in retrospect ("The prompt went back because each screen starts a fresh shell"). Maya registers it only as "do it again".
- **O-b**: screen 2/6, "The single quotes matter: they leave $pet for the child to fill in." Sits below the commands, after the reading limit, so it was skipped. No harm here because the commands were copyable; in the task the quote shape had to be reused from memory.
- **O-c**: screen 6/6, "~/.bashrc if your login shell is bash ... ~/.zshrc ... ~/.bash_profile on macOS with bash". Maya does not know her login shell and the screen does not say how to find it.
- **O-d**: task screen: "Run a child with bash -c that prints $TOPIC into seen.txt." The quoting is not stated; Maya relied on the lesson 2 example. The task does not mention that the command needs single quotes.
- **O-e**: gate intro, "Type your answer in words; this is not the shell." The Q1 to Q3 options were given, so "in words" is accurate but unneeded.
- **O-f**: `check` on the task printed the cleared screen with no per-step checklist, so a pass gives no confirmation of what was verified.

### Debrief (out of character)

- Lesson 5's "[] means: not set" is the only statement the screen contradicted; it is the one sentence a learner could not reconcile.
- "set it again: each screen is a new shell" (2/6) and "The prompt went back because each screen starts a fresh shell" (6/6) carry the same idea in two places, one before it is needed and one after.
- Lesson 6's three dotfile lines assume the learner knows her login shell.
- The task's "bash -c that prints $TOPIC into seen.txt" leaves quoting to the lesson 2 example.
- Density: every screen was within or at the four-line limit; no density-charged turn occurred.
