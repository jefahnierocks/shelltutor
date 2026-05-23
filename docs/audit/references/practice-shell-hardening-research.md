---
title: Practice Shell Hardening Research for shelltutor
category: research
component: practice-shell-hardening
status: draft
version: 0.2.0
last_updated: 2026-05-22
tags: [research, bash, readline, portability, sandbox, tab-completion, planning, verified]
priority: medium
---

# Practice Shell Hardening Research for shelltutor

This document ingests the operator-supplied research report
`deep-research-report (12).md` into repo-local planning form. It covers
interactive Bash behavior, parent-shell differences, Readline and Tab
completion, sandbox hardening, command-safety policy, PTY evidence, and a
practical portability matrix.

The source report did not include a concrete bibliography or stable
source URLs; its citations were placeholder tokens from the research
environment. Treat its external claims as design evidence pending source
link cleanup, not as final citation-grade authority.

Reviewer note (2026-05-22): the env-var, Readline, and zsh facts below
have been spot-checked against `man bash` (5.x), the GNU Bash manual,
and `zshoptions(1)`. They are factual. The "hardening posture"
recommendations (which variables to scrub, whether to ship an
`INPUTRC`, command-policy lists) are **judgment** — they describe what
this project could choose to do, not what is universally required.

Ground-truth note on current shelltutor behavior (May 2026): the
practice rcfile at [shelltutor](../../../shelltutor:341) sources
`/etc/bashrc` if readable, then resets only `HISTFILE`, `HISTSIZE`,
`HISTFILESIZE`, `PROMPT_COMMAND`, and `PS1`. It does **not** currently
scrub `INPUTRC`, `CDPATH`, `GLOBIGNORE`, `PATH`, `COLUMNS`, or `LINES`.
That is the gap the "hardening targets" table below describes; it is
not a description of present behavior.

## Core Constraint

The report reinforces the same foundational point as the PTY research:
`shelltutor` is not just a command-line program. It is an interactive
Bash teaching environment that depends on terminal semantics.

Important implications:

- Interactive Bash is not the same execution path as piped stdin.
- The practice shell should be evaluated as Bash attached to a terminal,
  not as a generic stream processor.
- `/dev/tty` and PTY behavior are central to the product path.
- A production simulation path would be a second execution model and must
  not be treated as equivalent to the real practice shell.

Design implication: strengthen and test the real practice-shell path
before adding any product-side simulation mode.

## Cross-Platform Shell Boundary

The report identifies the main portability issue as a shell-boundary
problem rather than a broad Unix-vs-Unix problem.

| Surface | Planning implication |
| --- | --- |
| macOS default shell | Many learners start in zsh even though `shelltutor` explicitly launches Bash for practice. The zsh-to-Bash boundary should be expected and tested. |
| Bash startup | `bash --rcfile ... -i` is the right general shape for an explicit non-login interactive practice shell. |
| Parent dotfiles | Host settings can leak into an interactive shell unless the practice shell controls or scrubs relevant variables. |
| Terminal emulator | Mostly affects display width, key sequences, color, wrapping, and completion-list presentation. |
| zsh completion | zsh uses ZLE/compsys, not GNU Readline, so zsh behavior is not a model for Bash completion inside the tutor. |

Design implication: documentation and tests should be clear that the
learner may launch `shelltutor` from zsh, fish, or Bash, but the practice
prompt is intentionally Bash.

## Environment Variables To Control

The report flags these variables and settings as high-value hardening
targets because they can make the practice shell host-specific:

All risks below are documented in the GNU Bash manual and Readline
manual — they are objective behavior, not opinion.

| Variable / setting | Risk | Citation |
| --- | --- | --- |
| `PROMPT_COMMAND` | Executes as a command prior to issuing each primary prompt; a host rcfile can inject behavior into each lesson prompt unless reset. (shelltutor currently resets it to `history -a`.) | Bash manual §Shell Variables |
| `INPUTRC` | Overrides the default `~/.inputrc` Readline init file; `/etc/inputrc` is the system fallback. Can rebind keys and change completion behavior. | Bash manual §Shell Variables; Readline manual §Readline Init File |
| `HISTFILE` | Controls the history file location; default `~/.bash_history`. Leak risk in both directions if not isolated. | Bash manual §Shell Variables |
| `CDPATH` | Documented as "The search path for the cd command." Changes `cd` resolution of simple directory names. | Bash manual §Shell Variables |
| `GLOBIGNORE` | "Setting GLOBIGNORE to a non-null value has the effect of enabling the dotglob shell option, so all other filenames beginning with a '.' match." Non-obvious dotfile side effect is real. | Bash manual §Pathname Expansion |
| `PATH` | Controls command lookup. Current-directory execution risk applies only when `.` or an empty entry (`::`, leading/trailing `:`) is present. | Bash manual §Shell Variables |
| `COLUMNS` / `LINES` | Readline's `completion-display-width` falls back to `$COLUMNS`, then the screen width; affects completion-list and wrapping behavior. | Bash manual §Readline Variables |

Design implication: the practice-shell rcfile should intentionally set,
unset, or isolate these surfaces. Do not rely on whatever the parent
environment happens to provide.

## Tab Completion Model

The report makes a specific point about the known `ec` + Tab + Tab
complaint: completion behavior is a stack, not one simple rule.

In Bash:

- `TAB` is a Readline keybinding.
- Completion may be filename completion, Bash command completion, or
  programmable completion depending on context.
- Ambiguous completions commonly ring the bell before listing matches.
- Immediate listing, repeated-listing, and menu cycling depend on
  Readline settings and bindings.
- `menu-complete` exists but is not the same as ordinary completion.

In zsh:

- Completion is handled through ZLE/compsys rather than Readline.
- Options such as `AUTO_LIST`, `AUTO_MENU`, `BASH_AUTO_LIST`,
  `MENU_COMPLETE`, and `LIST_AMBIGUOUS` change repeated-Tab behavior.

Design implication: if Tab behavior matters to the lesson surface,
`shelltutor` should either standardize the practice shell's Readline
configuration or explicitly document/test the expected behavior. A user
who expects repeated Tab to cycle is not necessarily wrong; they may be
carrying a different shell or Readline configuration into the lesson.

## Sandboxing Posture

The report recommends treating the sandbox as pedagogical containment,
not adversarial containment.

Recommended safety posture:

- Use a fresh per-run directory for tests and simulations.
- Keep mutable tutor state inside the sandbox.
- Keep practice history inside the sandbox or disable host history
  effects.
- Use a deliberate `PATH`.
- Avoid relying on Bash restricted mode as a security boundary. (The
  Bash manual itself documents that `rbash` turns off restrictions in
  the shell spawned to execute a shell script — i.e., the bypass is
  intentional and documented.)
- Avoid network, privileges, and host-specific package/service surfaces.

Design implication: the tutor should remain honest about its safety
model. It can keep learner practice local and reversible, but it is not a
container or hostile-code sandbox.

## Live Command Policy

The report separates commands into safe live-teaching candidates and
commands that should be omitted, blocked, simulated, or narrated.

Good live-teaching candidates:

- `pwd`
- `ls`
- `cd`
- `mkdir`
- `rmdir`
- `touch`
- `cp` on known files inside the sandbox
- `mv` on known filenames inside the sandbox
- `cat`
- `less`
- `head`
- `tail`
- `wc`
- scoped `grep`

Avoid live execution in practice mode:

- `sudo`
- `sudoedit`
- `ssh`
- `curl`
- package managers such as `apt` or `brew`
- service managers such as `launchctl`
- recursive or forced deletion such as `rm -r` and `rm -f`
- raw device operations such as `dd`
- host-specific install or service-management recipes

Treat with care:

- `rm` should stay conservative and sandbox-scoped.
- `mv` should stay on known local files and avoid cross-filesystem or
  symlink edge cases.
- `echo -e` should be avoided in favor of `printf` where exact output
  behavior matters.

Design implication: curriculum and gates should prefer local, visible,
reversible commands. Anything that changes privileges, crosses the
network, modifies package/system state, or has destructive semantics
belongs outside beginner-live practice.

## Portability Matrix

The report recommends a small but meaningful validation matrix:

| Check type | Purpose |
| --- | --- |
| macOS normal terminal launch | Covers the common parent-shell mismatch where the user starts from zsh but practice uses Bash. |
| Debian/Ubuntu-family Bash | Covers mainstream GNU Bash and GNU userland. |
| Fedora-family Bash | Optional second Linux family for distro-assumption checks. |
| No-TTY negative test | Confirms the tutor fails quickly and readably when there is no controlling terminal. |
| PTY deterministic smoke | Exercises real lesson navigation and representative terminal behavior. |
| Human-reviewed transcript | Captures beginner UX friction that strict assertions miss. |

Design implication: distro count matters less than testing the right
axes: oldest supported Bash, current GNU Bash, parent-shell mismatch,
TTY presence/absence, and human-readable walkthrough evidence.

## Relationship To Existing Research Docs

This reference complements:

- `pty-harness-research.md`, which focuses on the driver/tooling
  architecture.
- `simulation-evidence-model.md`, which focuses on evidence artifacts.
- `persona-simulation-research.md`, which focuses on learner/test
  personas.

This document adds the practice-shell environment rules those later tools
should assume and verify.

## Design Decisions Suggested By This Research

These are planning recommendations, not accepted implementation
decisions:

1. Keep practice execution as explicit interactive Bash.
2. Scrub or set environment variables that alter prompt, history,
   completion, globbing, directory resolution, and available commands.
3. Standardize or explicitly document the Readline completion environment
   before treating Tab behavior as a learner failure.
4. Treat sandboxing as pedagogical containment, not a security boundary.
5. Keep live commands local, visible, reversible, and sandbox-scoped.
6. Add no-TTY negative validation as part of portability testing.
7. Validate parent-shell mismatch separately from Bash practice-shell
   behavior.

## Open Questions For Later Research

- Should `shelltutor` set a project-controlled `INPUTRC` for practice?
- Should the practice shell scrub `PROMPT_COMMAND`, `CDPATH`, and
  `GLOBIGNORE` explicitly?
- Should the practice shell use a reduced `PATH`, and if so, which
  commands must remain available per stage?
- What exact Tab behavior should Stage 1 teach or avoid teaching?
- Should no-TTY negative behavior become a named `make` target or remain
  part of smoke/portability checks?

