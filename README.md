---
title: shelltutor
category: reference
component: project-overview
status: active
version: 0.1.0
last_updated: 2026-07-14
tags: [shell, bash, tutor, education, unix, posix]
priority: high
---

# shelltutor

`shelltutor` is a **vimtutor prerequisite course** delivered as a single
bash script. It teaches the small set of shell concepts a learner needs
before sitting down to `vimtutor`: where am I, how do paths work, how do
I create and edit files safely, how do commands and pipes combine, and
how do I tell when I'm at the shell prompt versus inside a full-screen
program like Vim.

The course is structured as **five mastery-gated stages**. Each stage
closes with a gate: three recall questions (all three must be correct)
plus one practical task that the script verifies on the filesystem.
**Passing means passing** — unlimited retries, no time pressure, no
skip. About 45–60 minutes for a motivated learner.

The tutor is intentionally **user-agnostic**: it does not assume a
particular operator name, home layout, distro, hostname, prompt theme,
or pre-existing shell setup. Its design target is a clean Linux or macOS
terminal with no prerequisite configuration. The full Phase 2 manual
walkthrough on both platform families remains pending; see `STATUS.md`.

## Stages

| # | Title | Commands introduced |
| --- | --- | --- |
| 1 | Where am I? | `echo`, `pwd`, `whoami`, `date`, `clear`, `exit` |
| 2 | Paths and the filesystem | `ls`, `ls -l`, `ls -a`, `cd`, `cd ..`, `cd ~` |
| 3 | Files and operations | `touch`, `mkdir`, `rmdir`, `cat`, `less`, `cp`, `mv`, `rm` |
| 4 | Commands, streams, composition | `command -v`, `wc`, `seq`, `head`, `sort`, `grep`, `\|`, `>`, `>>`, `<`, `*` |
| 5 | Ready for `vimtutor` | `man`, `less` (full-screen), `vim`, `:q!`, `:wq`, `vimtutor` |

The full curriculum spec, learning goals, and gate definitions live in
`ROADMAP.md` Phase 3.

## Current Shape

```text
shelltutor/
├── README.md         # This file
├── AGENTS.md         # Operating contract for coding agents
├── CLAUDE.md         # Claude Code pointer to AGENTS.md
├── CONTRIBUTING.md   # Change discipline + Quality Gates
├── STATUS.md         # Current truth, posture, deferrals
├── ROADMAP.md        # Phase sequence; Phase 3 carries the curriculum spec
├── project.yaml      # Meta-inventory project-intelligence manifest
├── shelltutor        # The tutor itself (single bash script, executable)
├── Makefile          # Local quality gates and optional lesson-flow target
├── scripts/          # Static checkers, smoke test, and optional PTY harness
├── docs/
│   ├── contracts.md  # De-facto interface contracts (CLI, exit codes, layout)
│   ├── audit/        # Audit-spec authority package + reference docs
│   └── audit/references/  # Curriculum reference: shell-research.md
├── .claude/          # Claude Code agentic context (settings.json)
├── profile/          # Dated project-profile snapshots
├── audit/            # Dated audit-cycle artifacts
├── .editorconfig
└── .gitignore
```

The interface contracts (CLI arguments, practice-subshell exit codes,
sandbox file layout, environment variables read at startup) live in
`docs/contracts.md`. Read that before adding a flag, changing an exit
code, or relocating a sandbox file.

## Run

The tutor is a single bash script with no installation step:

```bash
./shelltutor          # resume where you left off
./shelltutor 3        # re-take or jump to stage 3
./shelltutor -h       # help
```

Requirements:

- A POSIX-ish terminal on the target Linux or macOS surface; cross-platform
  Phase 2 walkthrough evidence is still pending.
- `bash` 3.2+ on `PATH`. The stock macOS `/bin/bash` (3.2.57) is fine —
  no install step is required on macOS. Linux distros ship modern bash.
  The tutor's practice prompts explicitly spawn `bash --rcfile`, so lessons
  run in Bash regardless of your login shell (bash, zsh, fish). Inherited
  host rc behavior remains a Phase 2/Slice 2 validation and hardening surface.
- ANSI color support in the terminal (the standard default; set
  `NO_COLOR=1` to disable).

The tutor's own setup and progress code never writes outside its configured
sandbox directory (`~/.shelltutor` by default; override with
`SHELLTUTOR_HOME=/path`), never asks for elevated privileges, and never
reaches the network. Commands entered at a practice prompt retain the
learner's normal account authority.

Inside the practice prompt the learner has five navigation words:

```text
next   advance to the next lesson
prev   go back one lesson
show   redisplay the current screen
quit   leave (progress is saved); also: exit
check  verify a gate task (only at a gate)
```

## Goals

- Land a learner ready to run `vimtutor` without panic.
- Teach the ~25 commands a learner actually needs before their first
  Vim session.
- Stay portable across Linux and macOS without environment assumptions.
- Verify mastery at the end of each stage with both recall questions
  and a filesystem-checked task.
- Be readable as a single script — a learner can open it and inspect
  the code that just walked them through a stage.
- Be safe to run on a stranger's machine.

## Non-Goals

- Teach the inside of Vim. That is `vimtutor`'s job; the final stage
  hands you off.
- Teach shell scripting, sysadmin, or shell programming patterns (a
  future companion may, but not this script).
- Replace `man` or `info`. The course points learners at `man` and
  exits cleanly with `q`; the manual itself is the manual.
- Bundle into a package manager or framework. The tutor is one file
  on purpose.

## Provenance

The initial script was imported from prior-art at
`fedora-top:~/Projects/shelltutor/shelltutor` (commit `136f6a3`,
2026-05-17). The prior-art repo carried user-specific framing
(`WYN OPS` accent comments and a sibling `wyn-setup/` installer); the
user-specific surface is intentionally not carried forward into this
repository (commit `e6257aa`, 2026-05-21).

The curriculum redesign that produced the current five-stage structure
is recorded in `ROADMAP.md` Phase 3 and tracks the operator-supplied
reference at `docs/audit/references/shell-research.md`. The first
project profile and first audit cycle (snapshot 2026-05-21) live under
`profile/2026-05-21/` and `audit/2026-05-21/`.

## License Posture

A license has not yet been chosen. Until one is added, default copyright
applies and external reuse is not granted. See `STATUS.md` for the
deferral entry.
