---
title: shelltutor
category: reference
component: project-overview
status: active
version: 0.2.0
last_updated: 2026-11-07
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
plus one practical task that the script verifies on the filesystem and,
for Stages 1, 2 and 4, against the commands you actually ran. **Passing
means passing** — unlimited retries, no time pressure, no skip; a repeated
miss earns a hint and then a worked example, never a free pass. About 45–60
minutes for a motivated learner.

The tutor is intentionally **user-agnostic**: it does not assume a
particular operator name, home layout, distro, hostname, prompt theme,
or pre-existing shell setup. Its design target is a clean Linux or macOS
terminal with no prerequisite configuration. The full Phase 2 manual
walkthrough on both platform families remains pending; see `STATUS.md`.

## Stages

| # | Title | Commands introduced |
| --- | --- | --- |
| 1 | Where am I? | `echo`, `pwd`, `whoami`, `date`, `clear`, `exit` |
| 2 | Paths and the filesystem | `pwd`, `ls`, `ls -p`, `ls -a`, `cd`, `cd ..`, `cd ~` |
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
├── LICENSE           # MIT License
├── project.yaml      # Specification 1 project/workstation declaration
├── shelltutor        # The tutor itself (single bash script, executable)
├── Makefile          # Local quality gates and optional lesson-flow / sim targets
├── scripts/          # Static checkers, smoke test, and optional PTY harness (scripts/sim)
├── tests/            # Declaration-check regression tests (make verify)
├── vendor/           # Vendored Specification 1 release, byte-exact
├── docs/
│   ├── contracts.md  # De-facto interface contracts (CLI, exit codes, layout)
│   ├── design-description.md        # Formal design baseline (four lenses, glossary, tensions)
│   ├── direction-decisions-2026-11.md  # Directive: decisions D1–D8, Phases A–D, module standard
│   ├── design-direction-2026-11.md  # Superseded record of the operator's stated direction
│   ├── walkthrough-notes-template.md   # Phase A observer sheet (one sitting per copy)
│   ├── workplan/     # Current cycle plan: decisions + worker-executable packages
│   ├── audit/        # Audit-spec authority package + reference docs
│   └── audit/references/  # Curriculum reference: shell-research.md
├── .github/          # Hosted workflows: verify (gate), sim-evidence (non-gating Linux transcripts)
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

Contributors use `make verify` after preparing Python 3.11+ and Git 2.56+;
`make sim` (optional, not part of `verify`) drives the five-stage PTY harness
and needs Python 3.9+ and a real pseudo-terminal (`scripts/sim/README.md`).
These are validation tools, not learner prerequisites. See
[project declaration and verification](docs/project-manifest.md) for offline
release binding, linked-worktree arguments and CI setup. The tutor remains a
single Bash script with no installation step.

Requirements:

- A POSIX-ish terminal on the target Linux or macOS surface; cross-platform
  Phase 2 walkthrough evidence is still pending.
- `bash` 3.2+ on `PATH`. The stock macOS `/bin/bash` (3.2.57) is fine —
  no install step is required on macOS. Linux distros ship modern bash.
  The tutor's practice prompts explicitly spawn `bash --rcfile`, so lessons
  run in Bash regardless of your login shell (bash, zsh, fish). The practice
  shell does not source `/etc/bashrc` or `~/.bashrc` and resets the variables
  that change shell behaviour; `PATH`, `TERM` and locale are inherited (see
  `docs/contracts.md` C-007 for the exact environment).
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

`shelltutor` is released under the MIT License (SPDX id `MIT`), chosen on
2026-11-07 (`docs/license-decision.md`). The full text, with the copyright
line `Copyright (c) 2026 Jefahnierocks`, is in [`LICENSE`](LICENSE), and the
script carries an `SPDX-License-Identifier: MIT` header.
