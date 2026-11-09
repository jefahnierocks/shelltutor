---
title: shelltutor Contracts
category: reference
component: contracts
status: active
version: 0.3.0
last_updated: 2026-11-08
tags: [contracts, cli, exit-codes, sandbox, environment]
priority: medium
---

# shelltutor Contracts

This document defines the de-facto interface contracts the tutor
presents to operators, learners, downstream tooling, and future
contributors. None of these are machine-readable schemas — the audit
Phase 4 inventory (`audit/2026-05-21/04-contracts.md`) classifies them
all `ad-hoc`, which is appropriate for a single-file CLI with no
public SDK. They are documented here so a contributor can change them
deliberately rather than accidentally.

Closure of audit finding F-007. Map of surfaces below mirrors the
audit's contract IDs (C-001 … C-006) and the later C-007.

## Versioning posture

- Current: pre-1.0. The project carries no semver tag yet (deferred to
  ROADMAP Phase 4). Breaking changes to the contracts below are
  allowed in this window, but each one must be documented in the
  relevant section here and called out in the commit body.
- After v0.1.0: semver applies. Breaking changes to CLI shape,
  practice-subshell exit codes, or sandbox file layout bump the major
  version. Additive changes (new env var, new stage, new navigation
  word) bump the minor version.

## C-001 — CLI arguments

The tutor accepts five argument shapes:

| Invocation                | Behaviour                                                                            |
| ---                       | ---                                                                                  |
| `./shelltutor`            | Resume at the next un-passed stage (or run the finale if all stages are passed).     |
| `./shelltutor N`          | Enter stage `N` ∈ {1, 2, 3, 4, 5} for re-take or first-time. Bypasses the `.progress` resume; does not regress stored progress. |
| `./shelltutor <module>`   | Run a stand-alone module, where `<module>` is a lowercase word from the fixed list in the script (`MODULES`; currently `shells` and `env`). A module needs no stage, saves nothing and exits 0; it never reads or writes `.progress`. `-h` lists the modules under their own heading. |
| `./shelltutor -h`         | Print usage to stdout, exit 0. `--help` is an accepted alias.                         |
| `./shelltutor --info`     | Print an informational environment check and exit 0; does not start lessons.         |

Any other invocation (a word that is neither a stage number nor a listed
module) prints an error to stderr and exits 1.

The numeric range is **inclusive 1 through 5**. Adding a sixth stage
is a breaking change (CLI accepts a new value); removing the upper
bound or adding `0` is also breaking. Adding a module name to `MODULES` is
not breaking; removing or renaming one is.

Stability commitment: stable for the lifetime of the 5-stage
curriculum. If the curriculum expands to 6+ stages in a future cycle,
the argv check broadens accordingly and the new value range becomes
the contract.

## C-002 — Practice-subshell exit codes

The `practice()` subshell defines six navigation functions so that the
learner's navigation words exit with
codes the outer dispatcher interprets:

| Word          | Exit code | Meaning                                       |
| ---           | ---:      | ---                                           |
| `next`        | 0         | Advance to the next lesson within a stage.     |
| `check`       | 96        | Verify the gate task (gate context only).      |
| `show`        | 97        | Redisplay the current screen.                  |
| `prev`        | 98        | Step back one lesson within a stage.           |
| `quit`        | 99        | Leave the tutor; progress is saved.            |
| `exit`        | 99        | Alias of `quit` (overrides bash's own `exit`). |

Any other exit code from the subshell is treated as the bash default
(`exit $?` after the last command) and routed by the lesson runner as
a control signal — currently equivalent to `next` if zero, otherwise
propagated.

The choice of 96–99 reserves a small contiguous range for navigation
codes while keeping 0 as the natural "advance" path. Adding a new
navigation word that needs its own code uses the next unused value
(e.g., 95 for `restart`); changing the meaning of an existing code is
breaking.

## C-003 — `$SANDBOX` file layout

`$SANDBOX` defaults to `$HOME/.shelltutor` and may be overridden via
the `SHELLTUTOR_HOME` environment variable (see C-004). Everything
the tutor writes lives inside `$SANDBOX`.

```
$SANDBOX/
├── .progress                  single non-negative integer: stages passed
├── .shelltutor_history        practice subshell's HISTFILE
├── poem.txt                   4-line educational fixture (constant)
├── numbers.txt                seq 1 50 fixture (constant)
├── stage1/                    created on stage 1 entry (currently empty)
├── stage2/
│   └── practice/              (created by the learner during the gate task)
├── stage3/
│   ├── hello.txt              (created by the learner in lesson 3.1; not contractual)
│   ├── notes/                 (created by the learner in lesson 3.1; not contractual)
│   ├── notes.txt              (created by the learner; renamed to done.txt)
│   ├── backup.txt             (created by the learner; removed)
│   └── done.txt               (the gate-task end state)
├── stage4/
│   ├── poem.txt               copy of the fixture, seeded on stage entry
│   ├── seed.txt               seeded on stage entry so the *.txt glob has a match
│   └── count.txt              (created by the learner: `seq 1 100 | wc -l > count.txt`)
└── stage5/
    └── practice.txt           seeded on stage entry; re-seeded to `before` at gate entry
```

Where practice prompts start: stages 1 and 2 start in `$SANDBOX`; stages 3
to 5 start in their stage folder (`$SANDBOX/stage3` to `$SANDBOX/stage5`) for
lessons and gates.

Modules: a module's fixtures live in `$SANDBOX/<module>/` (for example
`$SANDBOX/shells/`), created on entry and self-healing like the stage
folders; its practice prompts start there. A module writes only under its own
folder and never touches `.progress` (`./shelltutor shells` leaves `.progress`
byte-identical, or absent).

Stability commitment:

- The four constant files (`.progress`, `.shelltutor_history`,
  `poem.txt`, `numbers.txt`) are stable across versions.
- The five stage subdirs are stable.
- The names of script-created files inside each stage subdir
  (`poem.txt` in stage 4, `seed.txt`, `practice.txt`) are stable.
- Learner-created file names inside stage subdirs are not part of the
  contract — they are taught by the lesson text and reflected in the
  gate verification logic, but a future redesign could rename them.

Reset path: removing `$SANDBOX` (or `$SHELLTUTOR_HOME` if set) resets
everything; the next run recreates fixtures via `setup_sandbox()`.
Removing individual files inside `$SANDBOX` self-heals on the next
`setup_sandbox` call. Progress is preserved unless the user deletes
`.progress` or completes the finale.

## C-004 — Environment variables read by the script

| Variable             | Read at        | Effect                                                          | Default                      |
| ---                  | ---            | ---                                                             | ---                          |
| `HOME`               | startup        | Parent of the default sandbox root.                              | shell default                |
| `SHELLTUTOR_HOME`    | startup        | Overrides the entire sandbox root path. Wins over `$HOME`. Normalised at startup: made absolute against the invoking directory and stripped of trailing slashes; `--info` and all lesson copy show the normalised value. | unset                        |
| `NO_COLOR`           | startup        | When set and non-empty, disables ANSI colour output and selects the ASCII glyph set. | unset                        |
| `SHELLTUTOR_ASCII`   | startup        | When `1`, selects the ASCII glyph set (A3.7) while colours stay on. The ASCII set is also used when stdout is not a terminal. Never selected by locale (A3.7). | unset                        |
| `SHELL`              | `--info`       | Reported as the login shell; does not choose the practice shell.   | unset shown explicitly       |
| `TERM`               | `--info`       | Reported as terminal context.                                      | unset shown explicitly       |
| `PATH`               | runtime        | Resolves external commands; `--info` reports selected tool paths.  | inherited                    |
| `BASH_VERSION`, `BASH_VERSINFO` | startup / `--info` | Enforce and report the Bash 3.2 floor.                | set by Bash                  |

Inside the practice subshell only: see C-007.

At startup, the script sets `BASH_COMPAT=5.0` so current Bash releases use
the here-document behavior needed by this here-doc-heavy script. This is a
script-owned compatibility setting, not a caller-provided configuration knob.

Stability commitment: the read-by-script variables above are stable.
The variables set inside the practice subshell are owned by C-007.

Other inherited environment can affect external command behavior and the
interactive practice shell; it is not interpreted as project identity,
authorization, or a user-specific configuration contract.

## C-005 — `-h` / `--help` text

The `usage()` text is part of the contract because
it enumerates C-001 (argv shape), C-004 (env vars), and the five
stages. Drift between the usage text and either of those is caught by
`scripts/smoke-test.sh` (FF-006a).

Stability commitment: structural content (Usage section, Stages
table, Sandbox folder line, navigation-word list) is stable. Cosmetic
phrasing is not.

## C-006 — Lesson heredoc text

The welcome, lesson, and finale heredocs in `shelltutor` carry user-facing
instruction. The audit Phase 8
classifies these surfaces `not-a-prompt` — they are CLI UI, not
model-mediated prompts.

Stability commitment: no specific wording is contractual. Lesson
**content** (commands taught, gate questions, gate task requirements)
follows the curriculum spec in `ROADMAP.md` Phase 3. A redesign of the
curriculum is a major-version event after v0.1.0; a wording rewrite is
not. Gate feedback wording is likewise not contractual, but the escalation
order on repeated gate failure (restatement, then hint, then worked example,
with no auto-pass) is part of the curriculum design.

Recall escalation: two rungs (A7; it was three under A1.1). A first miss
prints the message and the question's hint; the second and later print the
hint and the three navigation facts (A10 removed the A8 answer-shape line;
passed stages are saved; `quit` leaves
now and the next run starts this stage from its first lesson; `show` repeats
the question). The task ladder (restatement, hint, worked example) keeps its
three rungs. There
is no reveal of an accepted form at any rung. `show` repeats the question
without counting a miss; `quit` leaves with the same farewell as the practice
prompt. Contractual: the rung order and the three facts. Not contractual: the
wording. Every hint passes FF-009 (no accepted answer appears in it) and
FF-010 (it starts `Lesson N: ` or `Lesson N.k: `, naming where the fact was
taught). The
Stage 1 follow-up prompts accept `show` and `quit` but have no ladder; a
mismatch re-asks only the failing item.

Gate feedback is a `┃` checklist (A3.4): each line of the block starts with
the bar, a `✓` line marks what the gate saw done, a `○` line marks what it did
not with `not yet: <what it sees>`, and one closing line names the action and
`check`. The `not yet:` text is the harness's feedback sentinel `NOT_YET`; the
shape is recorded here, the words after it are not contractual.

## C-007 — Practice-shell environment and Readline behaviour

The practice prompt is a real interactive Bash started by `practice()` as
`INPUTRC=/dev/null BASH_SILENCE_DEPRECATION_WARNING=1 "$BASH" --rcfile /dev/fd/3 -i < /dev/tty`. The rcfile is
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
| Environment set | `INPUTRC=/dev/null`, `BASH_SILENCE_DEPRECATION_WARNING=1` (the latter silences Apple's Bash 3.2 "default shell is now zsh" notice, which that Bash prints after the rcfile has run; the variable stays in the practice shell's environment) |
| Interpreter | `$BASH`, the binary running the outer script (never `bash` resolved through `PATH`) |
| Readline | `INPUTRC=/dev/null`; `show-all-if-ambiguous off`, `show-all-if-unmodified off`, `completion-ignore-case off`, `bell-style none` |
| Working directory | the stage folder passed by the caller (see C-003) |
| Navigation words | per C-002 |
| Not controlled | `PATH`, `TERM`, `COLUMNS`, `LINES`, locale variables, exported functions other than `command_not_found_handle`, programmable-completion specs loaded by a system rcfile |

Tab contract taught by lesson 1.2: a single Tab completes a unique match;
with several matches the first Tab inserts the shared prefix and a second
Tab lists the candidates; Tab never cycles; no bell.

Stability commitment: the unset list, shell options, prompts and Readline
settings are stable for the lifetime of the 5-stage curriculum. Adding an
item to the unset list is additive; removing one or changing a Readline
setting the lessons describe is breaking. The history variables remain an
implementation detail shared with C-004's "inside the practice subshell"
table, which this section now owns.

## Audit cross-reference

| ID    | Audit Phase 4 ID | Status in current revision                          |
| ---   | ---              | ---                                                 |
| C-001 | C-001            | stable for the 5-stage curriculum; extended 2026-11 (WP-13, WP-16): module argument |
| C-002 | C-002            | extended with `check` (RC=96) in curriculum redesign |
| C-003 | C-003            | extended with stage{1..5}/ subdirs; extended 2026-11 (WP-02, WP-13: `$SANDBOX/<module>/`) |
| C-004 | C-004            | extended by `--info`; startup environment documented; extended 2026-11 (WP-02, WP-15) |
| C-005 | C-005            | rewritten in curriculum redesign                     |
| C-006 | C-006            | rewritten in curriculum redesign; extended 2026-11 (WP-05, WP-15, WP-10) |
| C-007 | —                | added 2026-11 (WP-03, Slice 2): practice-shell environment and Readline behaviour; owns what C-004 listed for the practice subshell |

The current revision passes the audit's Phase 4 exit checks: no
unflagged ad-hoc contract remains; every contract has documented
producer + consumer; absent surfaces (HTTP/RPC/MCP/A2A/etc.) are
explicit-absent with the reasons recorded in the audit artefact.

Closes F-007.
