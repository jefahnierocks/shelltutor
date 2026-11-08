---
title: WP-14 — Module `shells` (what a shell is, other shells, login shell)
category: planning
component: workplan
status: drafted-frozen
version: 0.1.0
last_updated: 2026-11-08
tags: [workplan, phase-d, modules, shells, d1, d6, module-standard]
priority: medium
---

# WP-14 — Module `shells`

**Governing text**: `docs/direction-decisions-2026-11.md` D1, D4, D6, §5
(module standard), §6 (template and the `shells` outline), A1.1 (recall
ladder). **Tier**: module standard. **Depends on**: WP-13 (module entry,
heading convention, persona tables, `screen-height` events) and WP-10
(`ask_question` signature with a hint argument; `gate_escalate`).
**Landing**: first module; Commits C and D of WP-13 land in the same
series. **Script freeze**: nothing here lands before the Phase A summary
exists (A1.9). **Touches `shelltutor`**: yes, one module block.

## Goal

A learner who has finished Stage 1, or who never will, can run
`./shelltutor shells` and in about five minutes learn: the shell is a
program they can inspect; other shells exist and differ in configuration,
prompt and completion but not in programs, paths, pipes or redirection;
their login shell and the shell the tutor runs can differ. One small task
proves they can ask the shell a question about installed software.

## Read first

- `AGENTS.md`; `CONTRIBUTING.md` §Module standard and the lesson-screen
  template (WP-13 Commit D; until it lands, `docs/direction-decisions-2026-11.md`
  §5 and §6).
- `stage3_*` in `shelltutor` (`stage3_intro` to `run_stage3`) as the one
  model block. Do not read the rest of the script.
- `docs/workplan/WP-13-module-infrastructure.md` (heading convention,
  module block pattern).

## Writing rules for the copy (apply to every screen)

- **Escape every literal `$` as `\$`** inside the heredocs: they are
  unquoted, so `$SHELL`, `$0` and `$BASH_VERSION` would otherwise expand in
  the tutor's own shell. `${H1}`, `${CMD}`, `${SANDBOX}` and the other role
  variables are the only unescaped expansions. No backticks.
- Colour roles as in `stage3_*`: `H1` heading, `SUB` concept word, `CMD`
  anything typeable, `KEY` a keypress, `EM` a warning, `DIR` a path,
  `INSTR` the action line, `DIM` an aside, `Q` a question. Under `NO_COLOR`
  the text still reads correctly (`▶`, `#` and `✓` survive).
- At most 20 lines per heredoc, blanks included; each ends in a `▶` line;
  one idea per screen. The harness `screen-height` event is the arbiter.
- Tone: concise, concrete, task-focused, no praise, no mascots.
- Every command demonstrated exists in the base install on macOS and Linux
  (D6): `echo`, `ps`, `command -v`. `zsh` and `fish` are concept-only; the
  module runs `command -v zsh fish` and nothing else about them (D1).

## Fixtures

`$SANDBOX/shells/`, created by `setup_module_dir shells` on entry
(self-healing, C-003). **No seeded files.** The gate removes
`$SANDBOX/shells/zsh.txt` at gate-task entry (clean slate, as
`stage3_gate` does for its files).

## Screens

Headings follow the WP-13 convention and are the harness sentinels.

### Intro — heading `MODULE — shells: what runs your commands`

```bash
module_shells_intro() {
    lesson "$SANDBOX/shells" <<EOF
${H1}MODULE — shells: what runs your commands${RST}

Three short lessons, then a gate. This module stands alone and saves
nothing. Type ${CMD}quit${RST} to leave at any point.

You will look at three things:
  the shell is a program you can inspect
  other shells exist, and what they change
  your login shell and this tutor's shell can differ

Everything is read-only except one small file at the gate, written
inside ${DIR}${SANDBOX}/shells${RST}.

${INSTR}▶ Type ${CMD}next${INSTR} to begin lesson 1.${RST}
EOF
}
```

(14 lines.)

### Lesson 1 — heading `shells 1 — the shell is a program`

```bash
module_shells_lesson_1() {
    lesson "$SANDBOX/shells" <<EOF
${H1}shells 1 — the shell is a program${RST}

The shell reads the line you type, finds the program you named, runs
it, and shows what it printed. The shell is itself a program.

  ${CMD}echo \$BASH_VERSION${RST}   ${DIM}# the version of the shell running now${RST}
  ${CMD}ps${RST}                    ${DIM}# one line is this shell, one is ps itself${RST}

${CMD}\$BASH_VERSION${RST} is a ${SUB}variable${RST}: a name that holds a value. The
shell swaps ${CMD}\$name${RST} for its value before it runs the line.

Notice that ${CMD}ps${RST} lists the shell next to the command you just ran.

${INSTR}▶ Run both commands, then type ${CMD}next${INSTR}.${RST}
EOF
}
```

(14 lines. `echo $0` was dropped in review: under the `"$BASH"` launch it
prints a path here and a bare name in a real terminal, which does not
transfer.)

### Lesson 2 — heading `shells 2 — other shells exist`

```bash
module_shells_lesson_2() {
    lesson "$SANDBOX/shells" <<EOF
${H1}shells 2 — other shells exist${RST}

Four shells you will meet:
  ${CMD}bash${RST}   common on Linux; the shell this tutor runs
  ${CMD}zsh${RST}    the default on current macOS
  ${CMD}fish${RST}   a shell with its own syntax, installed separately
  ${CMD}sh${RST}     the minimal standard shell, used by scripts

Ask which of two are installed here:
  ${CMD}command -v zsh fish${RST}   ${DIM}# one path per shell found${RST}

${SUB}Different${RST}: configuration syntax, prompt, completion.
${SUB}The same${RST}: the programs (${CMD}ls${RST}, ${CMD}cat${RST}), paths, pipes, redirection.

Notice that no output means that shell is not installed. That is normal.

${INSTR}▶ Run the check, then type ${CMD}next${INSTR}.${RST}
EOF
}
```

(17 lines.)

### Lesson 3 — heading `shells 3 — your login shell and this shell`

```bash
module_shells_lesson_3() {
    lesson "$SANDBOX/shells" <<EOF
${H1}shells 3 — your login shell and this shell${RST}

Your account has a ${SUB}login shell${RST}: the one a new terminal window
starts. It can differ from the shell running now.

  ${CMD}echo \$SHELL${RST}          ${DIM}# your login shell${RST}
  ${CMD}echo \$BASH_VERSION${RST}   ${DIM}# the shell running now${RST}

${CMD}\$SHELL${RST} comes from your account. It does not change when you start
another shell from inside it.

This tutor runs its lessons in Bash whatever your login shell is, so
every learner sees the same thing. The programs you practise here
behave the same under ${CMD}zsh${RST}.

${INSTR}▶ Compare the two lines, then type ${CMD}next${INSTR} to take the gate.${RST}
EOF
}
```

(16 lines.)

### Gate — heading `shells — gate`

Recall, in the WP-10 signature (prompt, hint, accepted forms, one
argument per line):

```bash
module_shells_gate() {
    show_screen <<EOF
${H1}shells — gate${RST}

${SUB}Recall${RST} (three questions, all three must be correct).
Then a ${SUB}practical task${RST}.
EOF

    ask_question \
        "Q1: The shell runs the programs you name. What kind of thing is the shell itself?  (a program, a file, a folder, a window)" \
        "Lesson 1: it showed up in ps next to the commands you ran." \
        'a program' \
        'program' \
        "it's a program" \
        'its a program' || return $?

    ask_question \
        "Q2: What do you type to ask whether zsh is installed?" \
        "Lesson 2 did it with two names at once; the first word of the line is 'command'." \
        'command -v zsh' \
        'command -v' \
        'which zsh' \
        'type zsh' || return $?

    ask_question \
        "Q3: ${CMD}echo \$SHELL${RST} prints which shell?  (the running one, your login shell, the newest one)" \
        "Lesson 3: it is the one a new terminal window starts, and it can differ from the shell running now." \
        'login shell' \
        'your login shell' \
        'the login shell' \
        'login' || return $?
    # ... task below
}
```

Hint check (A1.2, case-insensitive substring): Q1 hint contains none of
`a program`, `program`, `it's a program`, `its a program`. Q2 hint
contains the word `command` but none of `command -v zsh`, `command -v`,
`which zsh`, `type zsh`. Q3 hint contains none of `login shell`, `your
login shell`, `the login shell`, `login`. No accepted form is one or two
characters. Accepted lists are the draft set; `[from Phase A]` widen only
from the rejected-answer list.

### Task — heading `shells — task`

```bash
    # task screen (shown at gate entry and after a bare `show`)
    show_screen <<EOF
${H1}shells — task${RST}

Find out whether ${CMD}zsh${RST} is installed here, and record the answer in a
file. You will work inside ${DIR}${SANDBOX}/shells${RST}.

  1. ask the shell where ${CMD}zsh${RST} is
  2. send what it prints to a file named ${DIR}zsh.txt${RST}
     ${DIM}(hint: Stage 4's ${CMD}>${RST}${DIM} sends output to a file)${RST}

If zsh is not installed, the shell prints nothing, and the file is
empty. That is a correct answer.

${DIM}I will check: zsh.txt exists and holds exactly what ${RST}${CMD}command -v zsh${RST}
${DIM}prints on this machine, and your history shows you asked.${RST}

${INSTR}▶ Type ${CMD}check${INSTR} when done.${RST}
EOF
```

(16 lines.) The task text says "ask the shell where zsh is" without
naming the command: lesson 2 and Q2 taught it, and naming it again would
make the history check a formality. [decision] 1: if the Phase A walks
show learners stuck here, fade back to naming `command -v zsh` in the
hint.

**Verifier** (state and history, same order as `stage4_gate`: history
first, then state):

```bash
module_shells_verify_task() {
    local want
    want=$(command -v zsh 2>/dev/null || true)
    [ -f "$SANDBOX/shells/zsh.txt" ] || return 1
    [ "$(cat "$SANDBOX/shells/zsh.txt")" = "$want" ] || return 1
    return 0
}
```

- **History**: `hist_mark=$(history_mark)` at task entry;
  `gate_require_history "$hist_mark" 'ask the shell where zsh is: command -v zsh' 'command[[:space:]]+-v[[:space:]]+zsh'`.
  The label gives away the command, which is the rung-2 behaviour of the
  existing "Almost" list. [decision] 2: accept `which zsh` or `type -p
  zsh` in the history pattern, for symmetry with Q2's accepted forms? Draft
  says no: the file content check already accepts only `command -v` output
  (`which` prints the same path on most systems, but not all), and the
  task wording does not name the command.
- **State**: `zsh.txt` exists and equals `command -v zsh` evaluated by the
  script at verification time (empty when zsh is absent). The verifier
  runs in the tutor's shell, which has the same `PATH` as the practice
  shell.
- **On miss**: print "The file doesn't match yet." with
  `What I expected:` (`zsh.txt holds the path zsh is installed at`, or
  `zsh.txt exists and is empty (zsh is not installed here)` according to
  `want`) and `What I see in <dir>:` (`ls -1`), then
  `gate_escalate "$attempt" "command -v zsh prints where zsh is, or nothing; > sends it to a file." "command -v zsh > zsh.txt"`.
  No auto-pass.

### Cleared — line `✓ shells cleared.`

```bash
module_shells_cleared() {
    show_screen <<EOF
${OK}✓ shells cleared.${RST}

Commands and keys from this module:
  ${CMD}echo \$BASH_VERSION${RST}   the shell running now
  ${CMD}ps${RST}                    the shell is one of the running programs
  ${CMD}command -v NAME${RST}       is NAME installed, and where
  ${CMD}echo \$SHELL${RST}          your login shell

${INSTR}▶ Type ${CMD}quit${INSTR} to leave, or ${CMD}next${INSTR} to return to the start of this module.${RST}
EOF
}
```

(10 lines; recap ≤ 8 per WP-13.) Called after the verifier passes; the
runner then reads one line at the module prompt: `next` restarts the
module, `quit` exits 0. Modules never call `save_progress`.

## Runner

```bash
run_module_shells() {
    setup_module_dir shells
    local lessons=(module_shells_intro module_shells_lesson_1 module_shells_lesson_2 module_shells_lesson_3)
    # same dispatch loop as run_stage3 (next / show / prev / check note / quit)
    module_shells_gate
}
```

After the cleared screen, `next` restarts the module; `quit` exits 0.

## Harness: persona table

```python
MODULES["shells"] = dict(
    lessons=3,                       # intro + 3 lesson screens
    recall=["a program", "command -v zsh", "login shell"],
    task=["command -v zsh > zsh.txt"],
    check=True,
)
```

| Step | Wait for (prefix match) | Send |
| --- | --- | --- |
| 1 | `MODULE — shells: ` | `next` |
| 2–4 | `shells 1 — `, `shells 2 — `, `shells 3 — ` | `next` |
| 5 | `shells — gate` | three recall answers, one per question |
| 6 | `shells — task` | task command, then `check` |
| 7 | `✓ shells cleared.` | `quit` |

Oracle assertions: each sentinel exactly once; no `Almost — you still
need to`; exit 0; `.progress` byte-identical before and after; no file
written outside `$SANDBOX/shells/`. [decision] 4: add one deliberate miss
on Q2 ("zsh") so the hint rung appears in the module's bundle (A1.3 asks
this of core stages only; modules are not required to).

## Acceptance

1. `./shelltutor shells` runs to the cleared screen; `./shelltutor -h`
   lists the module; `./shelltutor bogus` still exits 1.
2. Every screen is ≤ 20 lines in the harness `screen-height` table;
   report the values.
3. `.progress` unchanged; only `$SANDBOX/shells/` written.
4. `make check lint smoke`, `make self-test`, `make verify` green; FF-004
   clean (no `/bin/bash`, no platform text beyond `command -v`); FF-001 to
   FF-008 (and FF-009 once WP-10 lands) clean.
5. Hint check passes on all three questions.
6. Harness green on macOS (Bash 3.2 and 5.x) and hosted Linux; commit
   `result.tap` and `summary.md` only (module standard item 6).
7. `STATUS.md` three-line entry (module standard item 8).

## Commits

1. `feat(shells): module block — intro, three lessons, recall gate, zsh-lookup task (D1)`
2. `chore(sim): shells persona table; module bundle result.tap and summary.md; STATUS entry`

(WP-13 Commits C and D precede or accompany commit 1.)

## Open points (resolved in review, 2026-11-08)

Coordinator decisions: 1 keep (do not name the command; the first miss
names it); 2 keep `command -v zsh` only; 3 resolved by dropping `echo $0`;
4 no deliberate miss in module personas (module standard); 5 `<name> — task`
adopted into WP-13's convention; 6 the count is lessons only (intro, gate,
task and cleared screens are not counted); 7 keep the stage precedent: the
gate opening screen has no `▶` because the first question follows at once
(recorded in WP-13).

Original points:

- **[decision] 1** Task wording does not name `command -v zsh`. Keep, or
  name it in the hint after Phase A?
- **[decision] 2** History pattern accepts only `command -v zsh`. Keep, or
  also accept `type -p zsh` and `which zsh`?
- **[decision] 3** Lesson 1 does not say what `echo $0` prints on the
  learner's own terminal (a path here, a bare name there). Add a line, or
  leave as the aside "the name or path it was started under"?
- **[decision] 4** A deliberate recall miss in the persona for hint-rung
  evidence.
- **[decision] 5** WP-13's convention gives intro, `shells k`, `shells —
  gate` and the cleared line; it does not name the task screen. This draft
  uses `shells — task`; WP-13 Commit B's wait list needs the same word, or
  the harness waits on the gate heading only and sends the task commands
  after the recall answers.
- **[decision] 7** The gate's opening screen (`shells — gate`, four lines) has no `▶` line, as in `stage3_gate`, because the recall prompt follows at once. The template says every screen ends in `▶`; keep the stage precedent or add one?
- **[decision] 6** "Three to five screens" (§5): this module is intro +
  three lessons + gate + task + cleared. If the count is meant to include
  the intro, it is within bounds; if not, lesson 3 merges into lesson 2.
