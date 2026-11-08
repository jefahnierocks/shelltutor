---
title: WP-03 — Practice-shell hardening (Simulation Slice 2, contract C-007)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-07
tags: [workplan, simulation, slice-2, hardening, readline, c-007]
priority: high
---

# WP-03 — Practice-shell hardening (Slice 2, C-007)

**Depends on**: WP-01, WP-02. **Blocks**: WP-04. **Touches `shelltutor`**:
yes (the `practice()` function and one line of lesson 1.1).
**Operator gate**: none. This is the "sensitive work" class in `AGENTS.md`
(practice-shell boundary), and it is explicitly requested by
`docs/simulation-design-plan.md` §Slice 2 and `docs/sim-slice-2-sketch.md`.

## Goal

Make the practice shell project-controlled: stop sourcing `/etc/bashrc`,
set shell options explicitly, scrub the environment variables that change
history, globbing, `cd`, idle timeout and Readline behaviour, ship the
minimal Readline contract, document it as C-007, retire the harness's
`no-system-rc-preview` variant, and record before/after evidence.

## Read first

- `docs/workplan/README.md` decisions D-09, D-10, D-11, D-12.
- `docs/simulation-design-plan.md` §Practice-Shell Hardening Sequence,
  §Tab Completion Contract, §Slice 2.
- `docs/sim-slice-2-sketch.md` (all of it; this package overrides two of
  its recommendations, see D-10 and D-12).
- `audit/2026-11-07/findings.md` observations O-D and O-E.
- `shelltutor` `practice()`; `docs/contracts.md` C-002 and C-004;
  `scripts/sim/patcher.py`, `run.py`, `README.md`.

## Verified facts this package relies on

Checked on this workstation on 2026-11-07 through a pty with both
`/bin/bash` 3.2.57 and Bash 5.3.20:

- `bind 'set bell-style none'` and `bind 'set show-all-if-ambiguous off'`
  inside an `--rcfile` file take effect (`bind -v` reports them).
- `INPUTRC=/dev/null` placed in the child's environment is visible inside
  the rcfile and makes Readline skip the user's and system's inputrc.
- `unset -f command_not_found_handle` returns 0 when no such function
  exists.

## Change 1 — `practice()` rcfile (D-09)

Replace the invocation line and the rcfile body with the following. Keep
the fd-3 feed and `< /dev/tty` exactly (F-009).

```bash
    # Feed the rcfile on fd 3 instead of process substitution. macOS Bash
    # 3.2 can parse <(...) here but does not reliably load it as --rcfile.
    # INPUTRC=/dev/null keeps Readline on its defaults so the practice
    # prompt behaves the same on every host (contract C-007).
    INPUTRC=/dev/null bash --rcfile /dev/fd/3 -i 3<<RCFILE < /dev/tty
# shelltutor practice shell — contract C-007 in docs/contracts.md.
# Nothing from /etc/bashrc is sourced. Distributions that compile Bash
# with a system rcfile still read it before this file; the settings
# below override what matters to the lessons.

# Inherited variables that would change what the lessons show or record.
unset -v CDPATH GLOBIGNORE HISTIGNORE HISTCONTROL HISTTIMEFORMAT TMOUT BASH_ENV
unset -v PROMPT_COMMAND
# Distribution hook that advertises package installs for unknown commands.
unset -f command_not_found_handle

set -o emacs
shopt -s histappend
shopt -u cdspell

cd "$pd"

HISTFILE="$SANDBOX/.shelltutor_history"
HISTSIZE=2000
HISTFILESIZE=4000
history -r 2>/dev/null || true
PROMPT_COMMAND='history -a'

PS1='shelltutor> '
PS2='> '

# Readline: common-Bash completion behaviour, no bell (see lesson 1.1).
bind 'set show-all-if-ambiguous off'
bind 'set show-all-if-unmodified off'
bind 'set completion-ignore-case off'
bind 'set bell-style none'

# Navigation builtins: functions, not aliases, so alias chains can't
# recurse. \`exec >/dev/null 2>&1\` immediately before \`builtin exit\`
# suppresses bash's "exit\n" interactive-logout print (which beginners
# read as a separate command being run); the subshell then exits with
# the navigation code the outer dispatcher interprets.
next()  { exec >/dev/null 2>&1; builtin exit  0; }
check() { exec >/dev/null 2>&1; builtin exit 96; }
prev()  { exec >/dev/null 2>&1; builtin exit 98; }
show()  { exec >/dev/null 2>&1; builtin exit 97; }
quit()  { exec >/dev/null 2>&1; builtin exit 99; }
exit()  { exec >/dev/null 2>&1; builtin exit 99; }

printf "${DIM}${footer}${RST}\n"
RCFILE
```

Notes for the implementer:

- `PROMPT_COMMAND` is unset before being set so a Bash 5.1+ array value
  inherited from the environment cannot keep extra entries.
- Do not reset `PATH`, `COLUMNS`, `LINES`, `LANG`/`LC_*`, `TERM`
  (plan: capture, do not control).
- `shopt -u cdspell` is explicit because some system rcfiles enable it and
  it would make a mistyped `cd` silently succeed during the Stage 2 gate.
- The `PATCH_NEEDLE` string `[ -r /etc/bashrc ] && . /etc/bashrc` must no
  longer appear anywhere in the script (Change 3 retires the patcher).
- Run `shellcheck -s bash -S warning shelltutor`; the heredoc body is
  data to ShellCheck, so no new directives should be needed.

## Change 2 — Lesson 1.1 Tab line (D-10)

Replace the three Tab lines in `stage1_lesson_1` with:

```
  ${KEY}Tab${RST}        bash finishes a word. Try ${CMD}echo p${RST}+${KEY}Tab${RST} → ${CMD}echo poem.txt${RST}.
             Several matches? The first ${KEY}Tab${RST} fills in the shared part;
             ${KEY}Tab${RST} again lists them. (Other shells and setups differ.)
```

Same line count as before; the screen's vertical budget is unchanged. This
is the only lesson-copy change in this package; the 1.1 split is WP-04.

## Change 3 — Retire the preview variant (D-11)

- Delete `scripts/sim/patcher.py`. Keep `PatchTargetMissingError` in
  `errors.py` only if something still imports it; otherwise delete it and
  mark exit code 3 as "retired (Slice 2)" in the README table so later
  codes keep their numbers.
- `run.py`: `--variant` accepts only `current-rc` (default). Passing
  `no-system-rc-preview` or `both` prints
  `scripts/sim/run.py: variant retired in Slice 2 (practice shell no longer sources /etc/bashrc); use --variant current-rc` and exits 2. Remove
  the `_write_diff` call path; keep the projection helper that
  `compare.py` uses.
- `Makefile` `lesson-flow` and `sim`: no flag changes needed (defaults).
- `scripts/sim/README.md`: remove the preview description; point to
  `compare.py` for before/after comparisons; update the exit-code table.
- `recorder.py` summary text: replace the "Slice 1 isolates only the
  `/etc/bashrc` source statement" paragraph with "The practice shell is
  project-controlled since Slice 2 (C-007); the host inputs below still
  reach the transcript."

## Change 4 — Contract C-007

Append to `docs/contracts.md` after C-006:

```markdown
## C-007 — Practice-shell environment and Readline behaviour

The practice prompt is a real interactive Bash started by `practice()` as
`INPUTRC=/dev/null bash --rcfile /dev/fd/3 -i < /dev/tty`. The rcfile is
generated by the script; nothing from `/etc/bashrc` or `~/.bashrc` is
sourced. On distributions whose Bash is built with a system rcfile
(Debian-family `/etc/bash.bashrc`), Bash reads that file before the
generated rcfile; the rcfile then overrides the prompt, history settings,
and the `command_not_found_handle` hook, and does not attempt to undo
anything else it did.

| Surface | Value in the practice shell |
| --- | --- |
| Unset on entry | `CDPATH`, `GLOBIGNORE`, `HISTIGNORE`, `HISTCONTROL`, `HISTTIMEFORMAT`, `TMOUT`, `BASH_ENV`, `PROMPT_COMMAND` (before being set), function `command_not_found_handle` |
| Shell options | `set -o emacs`; `shopt -s histappend`; `shopt -u cdspell` |
| History | `HISTFILE=$SANDBOX/.shelltutor_history`, `HISTSIZE=2000`, `HISTFILESIZE=4000`, `PROMPT_COMMAND='history -a'`; the file is read on entry |
| Prompts | `PS1='shelltutor> '`, `PS2='> '` |
| Readline | `INPUTRC=/dev/null`; `show-all-if-ambiguous off`, `show-all-if-unmodified off`, `completion-ignore-case off`, `bell-style none` |
| Working directory | the stage folder passed by the caller (see C-003) |
| Navigation words | per C-002 |
| Not controlled | `PATH`, `TERM`, `COLUMNS`, `LINES`, locale variables, exported functions other than `command_not_found_handle`, programmable-completion specs loaded by a system rcfile |

Tab contract taught by lesson 1.1: a single Tab completes a unique match;
with several matches the first Tab inserts the shared prefix and a second
Tab lists the candidates; Tab never cycles; no bell.

Stability commitment: the unset list, shell options, prompts and Readline
settings are stable for the lifetime of the 5-stage curriculum. Adding an
item to the unset list is additive; removing one or changing a Readline
setting the lessons describe is breaking. The history variables remain an
implementation detail shared with C-004's "inside the practice subshell"
table, which this section now owns.
```

Then trim C-004's "Inside the practice subshell only" table to a pointer:
"See C-007." Update the audit cross-reference table with a C-007 row.

## Change 5 — Evidence and status

- Re-run `python3 scripts/sim/run.py --stage all` and `--stage 1` under
  Bash 3.2 and 5.x. Commit the bundles under `audit/<date>/sim/`.
- Run `scripts/sim/compare.py` against the WP-02 post-fix `all/current-rc`
  bundle. Expected: differences only in the lesson 1.1 Tab lines and any
  prompt-adjacent noise. Record the diff summary in
  `audit/<date>/slice2-comparison.md` (hand-written, short).
- `docs/simulation-design-plan.md` Implementation State: Slice 2 complete
  (date, short SHA). `docs/sim-slice-2-sketch.md` frontmatter `status:
  implemented` plus a two-line note at the top pointing at the commit and
  at D-10/D-12 for the overridden recommendations.
- `STATUS.md`: one-liner "Slice 2 practice-shell hardening landed (C-007)";
  the Linux before/after comparison remains pending until WP-06 or the
  operator's Phase 2 Linux session.

## Acceptance criteria

1. `make check lint smoke` and `make self-test` pass; the smoke structural
   invariants still hold.
2. `grep -c '/etc/bashrc' shelltutor` is 0.
3. Harness `--stage all` passes under Bash 3.2 and 5.x; the Stage 1 Tab
   action (`echo p` + Tab → `echo poem.txt`) still completes.
4. Manual check in a real terminal, recorded in the report: start
   `HISTIGNORE='pwd:date' TMOUT=5 CDPATH=/tmp ./shelltutor 1`, idle for
   more than 5 seconds at the practice prompt (the shell must survive), run
   `pwd` and `date` at the gate, and confirm `check` accepts them.
5. `--variant both` exits 2 with the retirement message.
6. C-007 present; C-004 trimmed; contracts cross-reference table updated.

## Commits (in order)

1. `feat(practice): project-controlled practice shell — stop sourcing /etc/bashrc, scrub env, Readline contract (C-007)`
   — includes the lesson 1.1 Tab lines (D-10); body cites O-D, O-E,
   FF-006b.
2. `docs(contracts): add C-007 practice-shell environment and Readline behaviour`
3. `chore(sim): retire the no-system-rc-preview variant (Slice 2)`
4. `chore(audit): post-hardening five-stage evidence and Slice 2 status`

## Report

Template in `docs/workplan/README.md`. Include the `compare.py` summary
and the result of acceptance item 4.
