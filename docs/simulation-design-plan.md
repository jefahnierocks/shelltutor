---
title: shelltutor Simulation Design Plan
category: planning
component: simulation-design
status: draft
version: 0.3.0
last_updated: 2026-05-23
tags: [simulation, pty, evidence, personas, planning, lesson-flow]
priority: high
---

# shelltutor Simulation Design Plan

This document turns the May 2026 research references into a concrete
design plan for future `shelltutor` simulation, lesson-flow testing, and
practice-shell hardening.

It is a planning artifact, not a runtime contract. Any change that alters
the production script, practice shell, CLI, sandbox layout, or contributor
commands still needs to update `docs/contracts.md`, `CONTRIBUTING.md`,
`Makefile`, and related audit/status artifacts as appropriate.

## Source References

- `docs/audit/references/pty-harness-research.md`
- `docs/audit/references/simulation-evidence-model.md`
- `docs/audit/references/persona-simulation-research.md`
- `docs/audit/references/practice-shell-hardening-research.md`
- `docs/audit/references/educational-design-research.md`
- `docs/audit/references/shell-research.md`

## Planning Position

The core decision is to observe before hardening.

The first implementation slice should be a minimal contributor-side PTY
harness that drives the current Stage 1 flow and captures baseline
evidence. Practice-shell hardening follows only after baseline transcripts
exist, so behavior changes can be reviewed against a known prior run.

The Stage 1 baseline must not silently become an artifact of one
operator's `/etc/bashrc`. Slice 1 therefore captures two back-to-back
baselines:

- `current-rc`: the current production script exactly as learners run it.
- `no-system-rc-preview`: a temporary generated copy of the script with
  only the `/etc/bashrc` source line disabled.

The preview run is diagnostic, not production evidence. Its purpose is to
show the system-rcfile leak signature before the hardening slice removes
that source line from the real script.

The preview mechanism must be a harness-generated patched copy in a
temporary directory. Do not add an environment-gated branch to the real
script for Slice 1, and do not patch by fixed line number. The patch
should target the exact rcfile source statement and fail loudly if that
statement is not found.

The preview isolates only the system rcfile. It still inherits the
operator's terminal, platform, `TERM`, geometry, `PATH`, and other host
inputs unless the harness explicitly records or controls them. `summary.md`
must state those captured host inputs so later reviewers do not over-read
the current-vs-preview diff.

If `current-rc` and `no-system-rc-preview` diverge substantially, Slice 1
is still independently committable. Commit both baselines and record the
diff as evidence. Do not block Slice 1 or discard the preview solely
because the diff is large; a large diff is the data that justifies Slice 2.

This keeps the production contract intact:

- `make smoke` remains dependency-free and Bash-only.
- PTY-driven lesson flow becomes a separate contributor target.
- No production `--simulate` mode is added unless a future product reason
  justifies a second execution contract.
- Runtime hardening happens after the project has evidence for current
  learner-visible behavior.

## Implementation Ladder

Treat FF-006 as a ladder, not one binary state.

| Rung | Target | Scope | Intended command |
| --- | --- | --- | --- |
| FF-006a | Static smoke | Current syntax/help/structure/bad-arg checks | `make smoke` |
| FF-006b | Minimal lesson flow | `careful-beginner` through Stage 1 lessons and gate via PTY | `make lesson-flow` |
| FF-006c | Simulation depth | all stages, then multiple personas | `make sim` |

FF-006b is the release-readiness milestone for automated lesson-flow
coverage. FF-006c is depth and regression confidence, not a prerequisite
for the first PTY slice.

`make smoke` should stay minimal indefinitely. Its value is that it runs
on stock macOS and ordinary Linux with no optional contributor tooling.

## Code Layout

Simulation code should live under:

```text
scripts/sim/
```

Rationale:

- It is adjacent to existing contributor tooling.
- It is visibly separate from Bash-only static checkers.
- It avoids implying pytest or a broader test framework.
- It keeps the optional Python dependency boundary easy to explain.

The first driver should use Python stdlib `pty` plus `selectors`, not
Pexpect. Pexpect remains a possible later fallback or convenience layer,
but the v1 harness does not need enough pattern-matching machinery to
justify a stale third-party dependency.

Contributor Python floor:

- Require Python 3.9+ for `scripts/sim/`.
- Avoid syntax and stdlib features newer than Python 3.9.
- `make lesson-flow` must skip with a clear message if `python3` is
  missing or too old; it must not crash with a traceback.
- PTY targets are optional contributor tooling and are not included in
  `make verify` unless a future project decision changes that boundary.

Slice 1 implementation must update `CONTRIBUTING.md`, `Makefile`, and
`STATUS.md` in the same commit that adds `make lesson-flow`. The project
has already paid down STATUS-vs-implementation drift once; the new Python
contributor floor, FF-006b target, and first audit evidence bundle should
not land without matching current-truth documentation.

## Evidence Locations

Synthetic persona evidence and human walkthrough evidence have different
privacy and retention rules.

| Source | Location | Commit posture |
| --- | --- | --- |
| Synthetic curated runs | `audit/<date>/sim/` | Committable when sanitized by construction. |
| Real human walkthroughs | `$SHELLTUTOR_HOME/.sessions/<run-id>/` | Never committed. |
| Redacted human findings | `audit/<date>/findings.md` | Hand-written summaries only. |
| Local development scratch | `notes/` | Local/untracked only. |

Real human terminal transcripts should not be committed. If a human run
surfaces a finding, commit only a redacted reviewer summary.

## Evidence Bundle

The v1 synthetic run bundle should contain four files:

```text
terminal.jsonl
events.jsonl
summary.md
result.tap
```

Optional later addition:

```text
meta.json
```

`terminal.jsonl` is a project-local terminal event stream, not asciicast.
This resolves the v1 format choice before any audit evidence is
committed. A future converter or alternate recorder may produce real
asciicast v3, but v1 should not shell out to `asciinema`, should not
require an asciinema dependency, and should not use a `.cast` extension
unless the file is actually asciicast-compatible.

`events.jsonl` should carry persona actions, intent annotations, gate
outcomes, and UX findings. `summary.md` can be generated or hand-written.
`result.tap` is for automation status only.

Sandbox snapshots are deferred. On failure, the v1 harness can summarize
the relevant sandbox tree in `summary.md`.

## Confusion Events

The first mechanical `confusion` triggers are:

- A wrong control word for the current mode, such as `check` at a lesson
  or `next` at a gate before the task is done.
- Two or more consecutive `show` actions without a state-changing command
  between them.
- A gate check failure.
- A persona command outside the lesson's expected-command set.

Idle time is deferred. It may matter for real human walkthroughs, but it
is weak evidence for deterministic synthetic personas.

Synthetic persona events should include intent annotations from day one.
Human walkthroughs should not; reviewer summaries can add inferred intent
after the fact.

## Persona Scope

The first persona set is:

```text
careful-beginner
confused-novice
```

The first implementation should start with `careful-beginner` only,
Stage 1 only. Add `confused-novice` after the harness and evidence
bundle are stable. Add `skimmer`, `interrupting-user`, and
`overconfident-user` only after the first two personas can drive all five
stages reliably.

The named roster (`Sal`, `Echo`, `Root`, `Splat`, `Syntax`, `Pippin`) is
not part of the simulation track. Simulation personas should use behavior
names. If guide-voice variants ever exist, they should use a separate
namespace such as `guide.echo`.

LLM-generated personas are not acceptance evidence. They may generate
candidate traces, but maintainers must convert useful traces into
deterministic scripts before they count.

## Practice-Shell Hardening Sequence

Do not harden before baseline PTY evidence exists.

After the baseline Stage 1 transcript exists, the first hardening slice
should:

1. Stop sourcing `/etc/bashrc`.
2. Replace inherited rc behavior with explicit shell options.
3. Scrub high-risk shell behavior inputs:
   - `INPUTRC`
   - `CDPATH`
   - `GLOBIGNORE`
   - `BASH_ENV`
   - `PROMPT_COMMAND` before setting the tutor value
4. Ship a minimal project-controlled Readline config only after the Tab
   transfer decision below is reflected in lesson copy.
5. Update `docs/contracts.md` with the practice-shell Readline contract.
6. Re-run the Stage 1 PTY baseline and compare transcript drift.

Do not reset `COLUMNS` or `LINES`; capture them in evidence instead.

Do not reduce `PATH` in v1. Use `--info` to report missing expected
commands instead of treating PATH as a sandbox boundary.

## Tab Completion Contract

The plan now chooses a transfer-first Tab story for v1. The tutor should
not optimize for the cleanest possible in-tutor completion behavior if
that teaches a pattern learners will not see in ordinary Bash after they
leave the tutor.

If a project-controlled Readline config ships, it should freeze a
common-Bash-style behavior:

- A single Tab completes a unique match.
- If there are multiple matches, the first Tab does not insert a match;
  a second Tab shows the candidates.
- Tab does not menu-cycle through candidates.

Lesson copy should also say completion varies across shells and setups;
this tutor is teaching its own practice-shell behavior, not a universal
law of every terminal.

The minimal Readline config should set only the lesson-relevant behavior:

```text
set show-all-if-ambiguous off
set show-all-if-unmodified off
set completion-ignore-case off
set bell-style none
```

Avoid custom key bindings unless a later implementation need proves they
are necessary. The lesson should not rely on an audible bell, since many
terminals suppress it or make it distracting.

## Command Policy

The practice shell remains real Bash with the learner's normal user-level
authority. Do not implement broad runtime blocking in v1.

Runtime blocking by function override is leaky and can create a false
safety promise. The honest v1 stance is pedagogical containment:

- Live exercises use local, visible, reversible commands.
- Lesson text does not teach unsafe or host-specific commands.
- The welcome/safety text stays honest that the tutor is not a container.

Keep `rm` live in Stage 3, scoped to lesson-created files inside the
stage sandbox. Do not teach or require `rm -r`, `rm -f`, or recursive
deletion.

Do not teach live exercises using:

- `sudo`
- `sudoedit`
- `ssh`
- `curl`
- package managers
- service managers
- `dd`
- host-specific install recipes

A future `SHELLTUTOR_STRICT=1` mode can be considered later, but it is
not part of the v1 design.

## Pedagogy And UX

The target audience is adult beginners first, child-friendly compatible
second.

Default tone:

- concise
- concrete
- task-focused
- non-condescending
- low on praise-heavy copy

The tutor should keep using concrete "places and names" language for the
filesystem. Do not add anthropomorphic, adversarial, or prize-like
framing around permissions or root.

Stage 1 needs a focused density audit before Slice 1 implementation.
This is now a planning decision, not a hedge. The existing local `notes`
file is already a seed for this audit; formalize it before writing the
PTY harness so the harness can label known rough edges rather than
discovering them as if they were new failures.

The audit should tag each screen with:

- concepts introduced
- action requested
- number of distinct actions
- split recommendation

Any screen that introduces two or more new concepts or asks for two or
more distinct actions is a split candidate. Record that audit under:

```text
audit/<date>/stage1-density.md
```

Ordering rule: record the density audit first, but do not change Stage 1
lesson text before the initial `current-rc` baseline unless the project
explicitly chooses a separate "clean lesson baseline" slice. The first
baseline is therefore a record of current committed behavior, with known
rough edges labeled separately in both the density audit and the
simulation `summary.md`.

Gate feedback should not be centralized before PTY evidence exists.
The intended sequence is:

1. harness
2. baseline transcripts
3. gate feedback refactor
4. transcript comparison
5. land only if learner-visible behavior improves or remains coherent

Repeated gate failure should eventually escalate:

1. first failure: one-line task restatement
2. second failure: hint naming the relevant command family
3. third failure: worked example, with the learner still required to type
   the command

Do not auto-pass after repeated failures.

## Phase 2 Relationship

ROADMAP Phase 2 should close without waiting for PTY work.

Minimum Phase 2 closure matrix:

- macOS stock `/bin/bash` 3.2.57, full five-stage manual walkthrough
- one Debian/Ubuntu-family Bash 5.x, full five-stage manual walkthrough
- no-TTY negative test

Fedora is useful but optional for Phase 2 closure. The PTY harness is a
separate track and should not expand the already-scoped Phase 2 gate.

Record platform validation results in `STATUS.md` with dates and exact
surfaces tested.

## Findings Flow

Simulation-surfaced findings should flow into dated audit notes first.

Default location:

```text
audit/<date>/findings.md
```

Severity 3 and 4 findings from the simulation evidence scale should also
get a one-line current-truth entry in `STATUS.md`. Lower-severity issues
stay in dated audit evidence unless they become release-blocking.

Do not let `STATUS.md` become a general backlog.

## First Three Slices

### Slice 1: Stage 1 PTY Baseline

- Add or update `audit/<date>/stage1-density.md` before coding the
  harness.
- Add `scripts/sim/run.py`.
- Use Python stdlib `pty` plus `selectors`.
- Drive `careful-beginner` through Stage 1 lessons and gate.
- Use a fresh `SHELLTUTOR_HOME`.
- Capture the v1 evidence bundle.
- Assert only stable outcomes.
- Produce both `current-rc` and `no-system-rc-preview` baselines.
- Record the diff between those baselines in `summary.md`.
- Generate `no-system-rc-preview` by writing a patched script copy in a
  temporary directory, targeting only the exact `/etc/bashrc` source
  statement.
- Update `Makefile`, `CONTRIBUTING.md`, and `STATUS.md` in the same
  implementation commit.

### Slice 2: Practice-Shell Hardening

- Stop sourcing `/etc/bashrc`.
- Add explicit practice-shell setup.
- Add project-controlled Readline config using the transfer-first Tab
  contract.
- Scrub high-risk env variables.
- Update contracts by adding `C-007 — Practice-shell environment and
  Readline behavior` to `docs/contracts.md`. Keep C-004 focused on
  script startup environment variables; C-007 owns the interactive
  practice-shell environment, shell-option, rcfile, and Readline contract.
- Compare against Slice 1 evidence.

### Slice 3: Confusion Events And Second Persona

- Add mechanical confusion-event triggers.
- Add intent annotations for synthetic actions.
- Add `confused-novice`.
- Keep scope at Stage 1 until evidence shape is stable.

## Deferred

- Full five-stage simulation.
- Additional personas.
- LLM-generated trace exploration.
- Guide voice variants.
- Runtime command blocking.
- `SHELLTUTOR_STRICT=1`.
- Production `--simulate`.
- Real human transcript capture beyond local-only sessions.
