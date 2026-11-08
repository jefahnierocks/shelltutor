---
title: WP-17 — Module `env` (variables, export, PATH, the prompt, where they live)
category: planning
component: workplan
status: drafted-frozen
version: 0.1.0
last_updated: 2026-11-08
tags: [workplan, phase-d, modules, env, d2, d6, module-standard]
priority: medium
---

# WP-17 — Module `env`

**Governing text**: `docs/direction-decisions-2026-11.md` D2, D4, D6, §5
(module standard), §6 (template and the `env` outline), A1.1 (recall
ladder). **Tier**: module standard. **Depends on**: WP-13 (module entry,
heading convention, persona tables, `screen-height` events), WP-10
(`ask_question` signature with a hint; `gate_escalate`) and WP-16 (the
first module block; `env` copies its shape and its cleared screen).
**Script freeze**: nothing here lands before the Phase A summary exists
(A1.9). **Touches `shelltutor`**: yes, one module block, and
`MODULES="shells env"` already lists it (WP-13 Commit C).

## Goal

A learner learns that a variable lives in the shell that set it, that
`export` is what lets a child program see it, that `PATH` is a list of
folders searched in order, and that the prompt is a variable. They change
`PS1` at a prompt, watch it revert on the next screen, learn why, and are
handed the exact lines for their real `~/.bashrc` or `~/.zshrc` with the
instruction to quit the tutor and do it there. The tutor never reads or
writes those files (D2; FF-002; `AGENTS.md` §Work Rules).

## Read first

- `AGENTS.md`; `CONTRIBUTING.md` §Module standard and the lesson-screen
  template (WP-13 Commit D).
- `stage3_*` in `shelltutor` as the stage model, and the `module_shells_*`
  block from WP-16 as the module model. Do not read the rest of the script.
- The practice rcfile in `practice()` only for two facts: it sets
  `PS1='shelltutor> '` once, at shell start, and every screen starts a new
  practice shell (C-007). Both are why the prompt reverts, and the module
  depends on both. Do not change `practice()`.

## Writing rules for the copy

Same as WP-16: escape every literal `$` as `\$` in the unquoted heredocs
(`$HOME`, `$PATH`, `$pet`, `$TOPIC`, `$SHELL`); no backticks; colour roles
as in `stage3_*`; ≤ 20 lines per heredoc; each ends in `▶`; one idea per
screen; concise, concrete, no praise, no mascots. Every command
demonstrated exists in the base install on macOS and Linux (D6): `echo`,
`env`, `export`, `bash -c`, `tr`, `head`, `grep`, `command -v`. Other
shells are named, never run (D1). The `env` module also never prints,
reads or edits the learner's real rc files; it shows two lines of text.

**State does not carry between screens.** Each screen starts a fresh
practice shell, so a variable set in lesson 1 is gone in lesson 2. Every
lesson that uses `pet` sets it again on its own screen. Lesson 4 turns
this property into the lesson.

## Fixtures

`$SANDBOX/env/`, created by `setup_module_dir env` on entry (self-healing,
C-003). **No seeded files.** The gate removes `$SANDBOX/env/seen.txt` at
task entry. [decision] 1: seed nothing, or seed a `$SANDBOX/env/notes.txt`
so `env | head` lessons have a file to point at? Draft: nothing; none of
the screens need one.

## Screens

### Intro — heading `MODULE — env: variables and the prompt`

```bash
module_env_intro() {
    lesson "$SANDBOX/env" <<EOF
${H1}MODULE — env: variables and the prompt${RST}

Five short lessons, then a gate. This module stands alone and saves
nothing. Type ${CMD}quit${RST} to leave at any point.

You will see:
  variables, and how the shell uses them
  ${CMD}export${RST}, and what a child program receives
  ${CMD}PATH${RST}, the list the shell searches for programs
  the prompt, which is a variable too
  where these settings live for real

Everything stays inside this tutor's practice shell. Your own
configuration files are not touched.

${INSTR}▶ Type ${CMD}next${INSTR} to begin lesson 1.${RST}
EOF
}
```

(16 lines.)

### Lesson 1 — heading `env 1 — variables`

```bash
module_env_lesson_1() {
    lesson "$SANDBOX/env" <<EOF
${H1}env 1 — variables${RST}

A ${SUB}variable${RST} is a name that holds a value. The shell swaps
${CMD}\$name${RST} for the value before it runs the line.

  ${CMD}echo \$HOME${RST}           ${DIM}# a variable the shell already has${RST}
  ${CMD}pet=owl${RST}               ${DIM}# set one: no spaces around =${RST}
  ${CMD}echo \$pet${RST}            ${DIM}# prints owl${RST}
  ${CMD}env | head${RST}            ${DIM}# the first lines of the variable list${RST}
  ${CMD}env | grep '^pet='${RST}    ${DIM}# prints nothing${RST}

Notice that ${CMD}pet${RST} is missing from the list. A variable you set
is private to this shell until you export it (lesson 2).

${INSTR}▶ Try the five lines, then type ${CMD}next${INSTR}.${RST}
EOF
}
```

(15 lines. `env | grep '^pet='` is used, not `grep pet`, because `TERM=xterm-256color`
and similar values contain common words.)

### Lesson 2 — heading `env 2 — export and child programs`

```bash
module_env_lesson_2() {
    lesson "$SANDBOX/env" <<EOF
${H1}env 2 — export and child programs${RST}

A program the shell starts is a ${SUB}child${RST}. It receives only the
variables that were ${SUB}exported${RST}. Single quotes stop this shell from
replacing ${CMD}\$pet${RST}, so the child does it.

  ${CMD}pet=owl${RST}                          ${DIM}# set it again: new screen, new shell${RST}
  ${CMD}bash -c 'echo [\$pet]'${RST}            ${DIM}# prints [] : the child sees nothing${RST}
  ${CMD}export pet${RST}                       ${DIM}# mark it for children${RST}
  ${CMD}bash -c 'echo [\$pet]'${RST}            ${DIM}# prints [owl]${RST}
  ${CMD}env | grep '^pet='${RST}               ${DIM}# now it is listed${RST}

Notice that ${CMD}export${RST} copies nothing. It marks the name so every
child gets the value at the moment it starts.

${INSTR}▶ Run the five lines in order, then type ${CMD}next${INSTR}.${RST}
EOF
}
```

(16 lines.) "copies nothing / at the moment it starts" is a simplification and
accurate: a child gets a copy at start, later changes in the parent do not
reach a running child. [decision] 2: drop the sentence if it reads as a
second idea.

### Lesson 3 — heading `env 3 — PATH is a list`

```bash
module_env_lesson_3() {
    lesson "$SANDBOX/env" <<EOF
${H1}env 3 — PATH is a list${RST}

${CMD}PATH${RST} is a variable that holds folders separated by ${CMD}:${RST}. When you
type a command name, the shell looks in those folders, in order, and
runs the first match.

  ${CMD}echo "\$PATH"${RST}                  ${DIM}# one long line${RST}
  ${CMD}echo "\$PATH" | tr : '\n'${RST}      ${DIM}# one folder per line${RST}
  ${CMD}command -v ls${RST}                 ${DIM}# the folder where ls was found${RST}

This is why ${CMD}command -v${RST} (Stage 4) could answer: it reads this list.
A program in a folder that is not on the list is not found by name.

${INSTR}▶ Run the three lines, then type ${CMD}next${INSTR}.${RST}
EOF
}
```

(14 lines. In an unquoted heredoc `'\n'` stays `\n`; verify in the
rendered screen.)

### Lesson 4 — heading `env 4 — the prompt is a variable`

```bash
module_env_lesson_4() {
    lesson "$SANDBOX/env" <<EOF
${H1}env 4 — the prompt is a variable${RST}

The text before your cursor is the variable ${CMD}PS1${RST}. Change it and the
prompt changes at once.

  ${CMD}PS1='me> '${RST}       ${DIM}# the prompt is now me>${RST}
  ${CMD}PS1='\$ '${RST}         ${DIM}# and now a plain dollar sign${RST}

Try both. Then type ${CMD}next${RST} and look at the prompt on the next screen.

${INSTR}▶ Change the prompt, then type ${CMD}next${INSTR}.${RST}
EOF
}
```

(11 lines.)
### Lesson 5 — heading `env 5 — where this lives for real`

```bash
module_env_lesson_5() {
    lesson "$SANDBOX/env" <<EOF
${H1}env 5 — where this lives for real${RST}

Your prompt went back because each screen of this tutor starts a fresh
shell, and the tutor ignores your own configuration files on purpose,
so every learner sees the same thing.

A real terminal reads one file when it starts:
  ${DIR}~/.bashrc${RST}   if your login shell is bash
  ${DIR}~/.zshrc${RST}    if it is zsh ${DIM}(check: echo \$SHELL)${RST}
${DIM}macOS with bash reads ~/.bash_profile instead.${RST}

Lines you could add there:
  ${CMD}PS1='\$ '${RST}
  ${CMD}export PATH="\$HOME/bin:\$PATH"${RST}

${EM}Quit the tutor${RST}, open a new terminal, edit the file there. The tutor
will not touch it. Open another new terminal to see the change.

${INSTR}▶ Read the lines, then type ${CMD}next${INSTR} to take the gate.${RST}
EOF
}
```

(19 lines.) [decision] 3: the screen carries two ideas at the margin (why
it reverted; where the settings go). Draft: one idea — "a setting lasts
only where it is saved". If copy review calls it a split, lesson 5 splits
into 5 (why) and 6 (where) and the screen count passes §5's "three to
five". [decision] 4: the `~/.bash_profile` line is accurate for macOS
Terminal with bash but adds a platform special case; keep or drop? Draft
keeps it as a `DIM` aside because the wrong file is the commonest reason a
learner's edit "does nothing".

### Gate — heading `env — gate`

```bash
module_env_gate() {
    show_screen <<EOF
${H1}env — gate${RST}

${SUB}Recall${RST} (three questions, all three must be correct).
Then a ${SUB}practical task${RST}.
EOF

    ask_question \
        "Q1: Which command makes a variable visible to the programs the shell starts?  (set, export, env, echo)" \
        "Lesson 2: it is the line you typed after setting pet, before the second bash -c." \
        'export' || return $?

    ask_question \
        "Q2: What does ${CMD}PATH${RST} hold?  (a list of folders, one folder, a file name)" \
        "Lesson 3: you split it at each colon to read it. It names several places, searched in order." \
        'a list of folders' \
        'list of folders' \
        'folders' \
        'a list' \
        'list' \
        'a list of directories' \
        'list of directories' \
        'directories' || return $?

    ask_question \
        "Q3: You type ${CMD}PS1='me> '${RST}, then ${CMD}next${RST}. What is the prompt on the next screen?  (me> , shelltutor> )" \
        "Each screen starts a new shell, and a new shell starts from the tutor's own setting." \
        'shelltutor>' \
        'shelltutor' \
        'it reverts' \
        'reverts' \
        'reverted' || return $?
    # ... task below
}
```

Hint check (A1.2): Q1 hint contains none of `export`. Q2 hint contains
none of `a list of folders`, `list of folders`, `folders`, `a list`,
`list`, `a list of directories`, `list of directories`, `directories`
(note: "names several places" avoids "list"). Q3 hint contains none of
`shelltutor>`, `shelltutor`, `it reverts`, `reverts`, `reverted`. No
accepted form is one or two characters. The Q2 hint's word "split" and
the Q1 hint's "second bash -c" are fine. Draft accepted lists; `[from
Phase A]` widen only from the rejected-answer list.

### Task — heading `env — task`

```bash
    show_screen <<EOF
${H1}env — task${RST}

Prove that a child program can see a variable you exported. You will
work inside ${DIR}${SANDBOX}/env${RST}.

  1. set ${CMD}TOPIC${RST} to the word ${SUB}shell${RST}
  2. export it
  3. run a child ${CMD}bash -c${RST} that prints ${CMD}\$TOPIC${RST} into ${DIR}seen.txt${RST}
     ${DIM}(hint: single quotes, so the child replaces the variable)${RST}

${DIM}I will check: seen.txt holds the word shell, and your history shows${RST}
${DIM}TOPIC set, exported, and read inside single quotes by a child.${RST}

${INSTR}▶ Type ${CMD}check${INSTR} when done.${RST}
EOF
```

(14 lines.)

**Verifier** (state and history; history first, as in `stage4_gate`):

```bash
module_env_verify_task() {
    [ -f "$SANDBOX/env/seen.txt" ] || return 1
    [ "$(cat "$SANDBOX/env/seen.txt")" = "shell" ] || return 1
    return 0
}
```

- **History** (`hist_mark=$(history_mark)` at task entry):

  ```bash
  gate_require_history "$hist_mark" \
      'set TOPIC to shell: TOPIC=shell' 'TOPIC=shell' \
      'export TOPIC' 'export[[:space:]]+TOPIC' \
      "a child bash -c that reads \$TOPIC inside single quotes" \
      "(ba)?sh[[:space:]]+-c[[:space:]]+'[^']*\\\$\\{?TOPIC"
  ```

  The third pattern is the one that matters: without single quotes the
  *parent* expands `$TOPIC`, `seen.txt` still holds `shell`, and export
  proved nothing. It is an ERE; write it with `'\''` quoting in the
  script and test it against `bash -c 'echo $TOPIC' > seen.txt` (match),
  `bash -c "echo $TOPIC" > seen.txt` (no match), `sh -c 'echo ${TOPIC}'`
  (match). `export TOPIC=shell` satisfies both of the first two.
- **State**: `seen.txt` exists and contains exactly `shell`.
- **On miss**: "The file doesn't match yet.", `What I expected:` (`seen.txt
  holds the word 'shell'`), `What I see in <dir>:` (`ls -1`),
  `gate_escalate "$attempt" "Set it, export it, then bash -c with single quotes around echo \$TOPIC and > seen.txt." "TOPIC=shell" "export TOPIC" "bash -c 'echo \$TOPIC' > seen.txt"`.
  No auto-pass.
- Known limit: a learner can type `echo shell > seen.txt` plus the three
  history lines separately and pass. The history check proves the three
  steps were typed, not that the child's output is the file; the module
  standard does not require more. [decision] 5: if Phase A or the first
  walks show this matters, add a second state check (`seen.txt` mtime is
  later than the history line), at the cost of a portability hazard
  (`stat` differs); draft says no.

### Cleared — line `✓ env cleared.`

```bash
module_env_cleared() {
    show_screen <<EOF
${OK}✓ env cleared.${RST}

Commands and keys from this module:
  ${CMD}name=value${RST}        set a variable in this shell
  ${CMD}export name${RST}       let child programs see it
  ${CMD}echo "\$PATH"${RST}      the folders searched for programs
  ${CMD}env${RST}               list what children receive
  ${CMD}PS1='\$ '${RST}          change the prompt (this shell only)

${INSTR}▶ Type ${CMD}quit${INSTR} to leave, or ${CMD}next${INSTR} to return to the start of this module.${RST}
EOF
}
```

(10 lines.) Modules never call `save_progress`.

## Runner

```bash
run_module_env() {
    setup_module_dir env
    local lessons=(module_env_intro module_env_lesson_1 module_env_lesson_2 \
                   module_env_lesson_3 module_env_lesson_4 module_env_lesson_5)
    # same dispatch loop as run_stage3 / run_module_shells
    module_env_gate
}
```

## Harness: persona table

```python
MODULES["env"] = dict(
    lessons=5,
    recall=["export", "a list of folders", "shelltutor>"],
    task=["TOPIC=shell", "export TOPIC", "bash -c 'echo $TOPIC' > seen.txt"],
    check=True,
)
```

| Step | Wait for (prefix match) | Send |
| --- | --- | --- |
| 1 | `MODULE — env: ` | `next` |
| 2–6 | `env 1 — ` … `env 5 — ` | `next` |
| 7 | `env — gate` | three recall answers |
| 8 | `env — task` | the three task commands, then `check` |
| 9 | `✓ env cleared.` | `quit` |

Oracle assertions: each sentinel exactly once; no `Almost — you still
need to`; exit 0; `.progress` byte-identical; nothing written outside
`$SANDBOX/env/`; **the real `~/.bashrc` and `~/.zshrc` are not opened**
(the harness fixes `HOME` to a scratch directory; assert that directory
holds neither file after the run).

**Prompt-revert check (optional, [decision] 6).** At lesson 4 the persona
sends `PS1='me> '` and waits for the prompt `me> `, then `next`; at lesson
5 it waits for the heading and for `shelltutor> ` after it. This is the
only place the module's central claim ("it reverts") is observed, and the
table form of WP-13 Commit B has no slot for it. Either extend the table
(`lesson_actions={4: ["PS1='me> '"]}` and a post-`next` prompt assertion)
or leave the claim to the human walks.

## Acceptance

1. `./shelltutor env` runs to the cleared screen; `./shelltutor -h` lists
   both modules; `./shelltutor bogus` exits 1.
2. Every screen ≤ 20 lines in the harness `screen-height` table; report
   the values.
3. `.progress` unchanged; only `$SANDBOX/env/` written; the real
   `~/.bashrc` and `~/.zshrc` are neither read nor written (grep the
   module block for those two names: they appear only inside lesson-5 and
   cleared-screen text, never in a command).
4. `make check lint smoke`, `make self-test`, `make verify` green; FF-004
   clean; FF-001 to FF-008 (and FF-009 once WP-10 lands) clean.
5. Hint check passes on all three questions; the single-quote history
   pattern passes the three cases above.
6. Harness green on macOS (Bash 3.2 and 5.x) and hosted Linux; commit
   `result.tap` and `summary.md` only.
7. `STATUS.md` three-line entry.

## Commits

1. `feat(env): module block — intro, five lessons, recall gate, export-and-child task (D2)`
2. `chore(sim): env persona table; module bundle result.tap and summary.md; STATUS entry`

## Open points (resolved in review, 2026-11-08)

Coordinator decisions: 1 seed nothing; 2 keep the sentence; 3 one screen
(the revert explanation is lesson 4's payoff and belongs at the top of
lesson 5; six lessons would exceed §5); 4 keep the `DIM` aside; 5 accepted
as a module-standard limit; 6 yes, the prompt-revert observation goes into
the persona table (WP-13 Commit B gains `lesson_actions` and a post-`next`
prompt assertion); 7 and 8 as in WP-16.

Original points:

- **[decision] 1** Seed nothing under `$SANDBOX/env/` (draft), or a file.
- **[decision] 2** Keep or drop the lesson-2 "export copies nothing" line.
- **[decision] 3** Lesson 5 as one screen (draft) or split into why and
  where (six lessons).
- **[decision] 4** Keep the `~/.bash_profile` aside for macOS bash.
- **[decision] 5** Accept that the task proves the steps were typed, not
  the pipeline end to end.
- **[decision] 6** Add the prompt-revert observation to the persona table.
- **[decision] 8** Same as WP-16 [decision] 7: the opening gate screen has no `▶` line.
- **[decision] 7** Same as WP-16 [decision] 5: the task screen heading
  `env — task` is not in WP-13's convention.
