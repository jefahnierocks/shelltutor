---
title: shelltutor
category: reference
component: project-overview
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [shell, bash, tutor, education, unix, posix]
priority: high
---

# shelltutor

`shelltutor` is a self-contained interactive tutor for the Unix shell. It teaches
the small set of commands that turn a terminal from a wall of text into a
navigable workspace — `pwd`, `ls`, `cd`, `cat`, `man`, `whoami`, `hostname`,
`date`, `uptime`, `df`, `free`, and a handful of friends — through short
lessons paired with safe, sandboxed practice.

The tutor is intentionally **user-agnostic**: it does not assume a particular
operator name, home layout, distro, hostname, prompt theme, or pre-existing
shell setup. A learner sitting at any Linux or macOS terminal should be able
to read it, run it, and complete the lessons without first having to
configure their environment.

## Current Shape

```text
shelltutor/
├── README.md         # This file
├── AGENTS.md         # Operating contract for coding agents
├── CLAUDE.md         # Claude Code pointer to AGENTS.md
├── CONTRIBUTING.md   # Change discipline
├── STATUS.md         # Current truth, posture, deferrals
├── ROADMAP.md        # Phase sequence
├── shelltutor        # The tutor itself (bash script, executable)
├── .editorconfig
└── .gitignore
```

## Run

The tutor is a single bash script with no installation step:

```bash
./shelltutor
```

Requirements:

- A POSIX-ish terminal (any modern Linux or macOS terminal works).
- `bash` 4+ on `PATH`. macOS ships bash 3.2 by default; install a newer
  bash via Homebrew (`brew install bash`) or run on a Linux host if you
  hit bash-version-specific syntax.
- ANSI color support in the terminal (the standard default).

The tutor never writes outside its own working directory, never asks for
elevated privileges, and never reaches the network.

## Goals

- Teach a learner the first ~15 shell commands they actually need.
- Stay portable across Linux and macOS without environment assumptions.
- Be readable as a single script — a learner can open it and inspect
  the code that just ran them through a lesson.
- Be safe to run on a stranger's machine.

## Non-Goals

- Replace `man`, `info`, or a full shell course.
- Teach scripting, sysadmin, or shell programming patterns (a future
  companion may, but not this script).
- Bundle into a package manager or framework. The tutor is one file
  on purpose.

## Provenance

The initial script is imported from prior-art at
`fedora-top:~/Projects/shelltutor/shelltutor` (commit `136f6a3`,
2026-05-17). The prior-art repo carried user-specific framing
(`WYN OPS` accent comments and a sibling `wyn-setup/` installer);
the user-specific surface is intentionally not carried forward into
this repository.

## License Posture

A license has not yet been chosen. Until one is added, default copyright
applies and external reuse is not granted. See `STATUS.md` for the
deferral entry.
