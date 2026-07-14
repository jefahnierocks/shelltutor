---
title: shelltutor Contracts
category: reference
component: contracts
status: active
version: 0.1.0
last_updated: 2026-07-14
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
audit's contract IDs (C-001 … C-006).

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

The tutor accepts four argument shapes:

| Invocation                | Behaviour                                                                            |
| ---                       | ---                                                                                  |
| `./shelltutor`            | Resume at the next un-passed stage (or run the finale if all stages are passed).     |
| `./shelltutor N`          | Enter stage `N` ∈ {1, 2, 3, 4, 5} for re-take or first-time. Bypasses the `.progress` resume; does not regress stored progress. |
| `./shelltutor -h`         | Print usage to stdout, exit 0. `--help` is an accepted alias.                         |
| `./shelltutor --info`     | Print an informational environment check and exit 0; does not start lessons.         |

Any other invocation prints an error to stderr and exits 1.

The numeric range is **inclusive 1 through 5**. Adding a sixth stage
is a breaking change (CLI accepts a new value); removing the upper
bound or adding `0` is also breaking.

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
│   ├── notes.txt              (created by the learner; renamed to done.txt)
│   ├── backup.txt             (created by the learner; removed)
│   └── done.txt               (the gate-task end state)
├── stage4/
│   ├── seed.txt               script-provided so the *.txt glob has a match
│   └── count.txt              (created by the learner: `seq 1 100 | wc -l > count.txt`)
└── stage5/
    └── practice.txt           seeded by the gate (Phase 1 of the task)
```

Stability commitment:

- The four constant files (`.progress`, `.shelltutor_history`,
  `poem.txt`, `numbers.txt`) are stable across versions.
- The five stage subdirs are stable.
- The names of script-created files inside each stage subdir
  (`seed.txt`, `practice.txt`) are stable.
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
| `SHELLTUTOR_HOME`    | startup        | Overrides the entire sandbox root path. Wins over `$HOME`.        | unset                        |
| `NO_COLOR`           | startup        | When set (any value), disables ANSI colour output.                | unset                        |
| `SHELL`              | `--info`       | Reported as the login shell; does not choose the practice shell.   | unset shown explicitly       |
| `TERM`               | `--info`       | Reported as terminal context.                                      | unset shown explicitly       |
| `PATH`               | runtime        | Resolves external commands; `--info` reports selected tool paths.  | inherited                    |
| `BASH_VERSION`, `BASH_VERSINFO` | startup / `--info` | Enforce and report the Bash 3.2 floor.                | set by Bash                  |

Inside the practice subshell only (not the outer script):

| Variable             | Set by the rcfile                                                                                  |
| ---                  | ---                                                                                                |
| `HISTFILE`           | `$SANDBOX/.shelltutor_history` — sandboxes history away from `~/.bash_history`                      |
| `HISTSIZE`           | 2000                                                                                                |
| `HISTFILESIZE`       | 4000                                                                                                |
| `PROMPT_COMMAND`     | `'history -a'` — append each command to HISTFILE                                                    |
| `PS1`                | `'shelltutor> '`                                                                                    |

At startup, the script sets `BASH_COMPAT=5.0` so current Bash releases use
the here-document behavior needed by this here-doc-heavy script. This is a
script-owned compatibility setting, not a caller-provided configuration knob.

Stability commitment: the read-by-script variables above are stable.
The rcfile-set variables are an implementation detail of the practice
subshell and may change if the subshell pattern is refactored.

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
not.

## Audit cross-reference

| ID    | Audit Phase 4 ID | Status in current revision                          |
| ---   | ---              | ---                                                 |
| C-001 | C-001            | stable for the 5-stage curriculum                    |
| C-002 | C-002            | extended with `check` (RC=96) in curriculum redesign |
| C-003 | C-003            | extended with stage{1..5}/ subdirs                   |
| C-004 | C-004            | extended by `--info`; startup environment documented |
| C-005 | C-005            | rewritten in curriculum redesign                     |
| C-006 | C-006            | rewritten in curriculum redesign                     |

The current revision passes the audit's Phase 4 exit checks: no
unflagged ad-hoc contract remains; every contract has documented
producer + consumer; absent surfaces (HTTP/RPC/MCP/A2A/etc.) are
explicit-absent with the reasons recorded in the audit artefact.

Closes F-007.
