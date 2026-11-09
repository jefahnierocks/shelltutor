---
title: WP-19 — Synthetic sittings: sitting server, personas, telemetry
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, phase-a-sim, harness, personas, telemetry, a6]
priority: high
---

# WP-19 — Synthetic sittings

**Governing text**: `docs/direction-decisions-2026-11.md` amendment A6.
**Tier**: harness and process; no change to `shelltutor`. **Depends on**:
nothing open. **Evidence status of the output**: candidate findings only
(A6).

## Goal

Let an AI session play a learner persona against the real tutor, one
screen at a time, through a pseudo-terminal the project controls, and
record a telemetry sheet whose candidates a maintainer can reproduce.

## Read first

- A6; `docs/sim-personas/README.md` and the three persona sheets;
  `docs/walkthrough-notes-sim-template.md`.
- `scripts/sim/driver.py` (pty + selectors loop, normalisation,
  redaction), `recorder.py`, `run.py` (`controlled_inputs`, child env).
- `docs/simulation-design-plan.md` §Evidence Locations, §Persona Scope
  ("LLM-generated personas are not acceptance evidence").

## Commit A — `scripts/sim/sitting.py` (stdlib, Python 3.9+)

A long-lived **server** that owns one tutor under a pty, and a **client**
that an AI session calls from a shell, one command per turn.

```
python3 scripts/sim/sitting.py start [--bash /bin/bash] [--cols 80 --rows 24] [--arg N|module] [--out DIR]
python3 scripts/sim/sitting.py screen            # current normalised screen since the last clear, plus the pending prompt
python3 scripts/sim/sitting.py send "<text>"     # type text + Enter; returns the new screen
python3 scripts/sim/sitting.py raw "<escape>"    # type bytes with no Enter (Tab, Ctrl+L, Esc, arrows), returns the screen
python3 scripts/sim/sitting.py note "<context>" "<monologue>"   # records a persona event, sends nothing
python3 scripts/sim/sitting.py stop              # SIGTERM the tutor, close, flush the bundle
```

- Server: `start` forks the pty exactly as `driver.py` does (same child
  env rules: fresh `SHELLTUTOR_HOME`, empty `HOME`, `LC_ALL=C`, `VIMINIT`,
  `PAGER`, geometry, `TERM`; `--bash` selects the interpreter by running
  `<bash> ./shelltutor` so F-014 semantics hold), listens on a Unix socket
  in `--out` (default `$TMPDIR/shelltutor-sitting/`), and writes the usual
  bundle (`terminal.jsonl`, `events.jsonl` with `persona-input` rows tagged
  by the declared context, `note` rows for monologue, `summary.md`,
  `result.tap` stating what was cleared) through the existing `Recorder`
  with D-19 redaction.
- `screen` returns the text since the last clear sequence with ANSI
  stripped and the pending prompt line marked `[prompt] …`; the
  `screen-height` logic labels the screen id when a heading matches.
- `send` waits up to 10 s for output to settle (no new bytes for 0.4 s),
  then returns the screen. `raw` accepts `\t`, `\x0c`, `\x1b`, `\x1b[A`
  spellings.
- One sitting per `--out` dir; `start` refuses if a socket exists.

## Commit B — Runner protocol for a persona session

`docs/sim-personas/README.md` gains "Running a sitting": the exact
sequence a Claude Code session follows. The session is given only the
persona file, the rules, the telemetry template and the four client
commands. It must not read `shelltutor`, `docs/`, or the harness. Per
turn: `screen` → write the monologue block → `note` → `send`/`raw` →
record the response. On quit or finale: `stop`, then write the sheet to
`audit/<date>/sim-sittings/<persona>-<n>.md` and report.

## Commit C — Evidence rules and intake

- `docs/simulation-design-plan.md` §Evidence Locations gains the row
  "Synthetic sittings | `audit/<date>/sim-sittings/` | committable;
  candidates only". §Persona Scope notes the three learner personas are
  LLM-played, distinct from the deterministic harness personas, and that
  their findings are promoted only after reproduction.
- `scripts/sim/README.md` documents `sitting.py`.
- Intake: a maintainer reads each candidate, reproduces it on the real
  tutor (by hand or as a `second-try`-style persona step), and only then
  records F-nnn/O-nnn in `audit/<date>/walkthroughs.md`, citing the sheet.

## Acceptance

1. `make check lint smoke`, `make self-test`, selftest_modules green;
   Python 3.9 syntax.
2. A scripted probe (not a persona) drives `start` → `screen` → `send next`
   ×3 → `raw \t` → `stop` and the bundle contains the typed inputs, the
   notes, and `[user]` in place of the login name.
3. One real synthetic sitting (Leo, `--bash /bin/bash`) is run by a
   separate AI session and its sheet is committed; its candidates are
   listed in the report, none yet promoted.

## Commits

- A `feat(sim): sitting server and client for AI-played learner sittings`
- B `docs(sim-personas): running a sitting — the persona session protocol`
- C `docs(sim): synthetic sittings as candidate evidence; README`
