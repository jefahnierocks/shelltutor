---
title: Synthetic Walkthrough Telemetry (Phase A-Sim)
category: process
component: walkthrough-notes-sim
status: active
version: 0.1.0
last_updated: 2026-11-09
tags: [phase-a-sim, walkthrough, synthetic-learner, telemetry, evidence]
priority: high
---

# Synthetic walkthrough — one sitting

The parallel of `docs/walkthrough-notes-template.md` for an AI session
playing a persona from `docs/sim-personas/` against the real tutor through
`scripts/sim/sitting.py`. It asks for what a model can report truthfully
(what it read, what it typed, what it believed, why it stalled) and not
for what it cannot (clock time). Completed sheets are committed under
`audit/<date>/sim-sittings/<persona>-<n>.md`; their candidates are
summarised into `audit/<date>/walkthroughs.md` only after a maintainer
reproduces them (decisions amendment A6).

## Sitting

- Date:
- Persona (file in `docs/sim-personas/`) and learner role:
- Persona sheet version:
- Turn cap: 160. One turn = one `send` or one `raw`. Turns used:
- Simulation rules confirmed (zero forward knowledge, reading limit,
  friction meter):
- Tutor revision (`git rev-parse --short HEAD`) and invocation
  (`sitting.py start` arguments, including the Bash used):
- `--info` lines the persona was shown, if any:

## Per screen (repeat; one block per screen the server returned)

### <screen id as the server labels it> — <heading on screen>

- **Read**: all / skimmed (which lines skipped) / did not read.
- **Jargon or assumed concept** (quote the exact words):
- **Monologue** (in character, two to six lines):
- **Input** `[context: recall | bash | nav | follow-up]` → typed
  (verbatim) → tutor response (accepted / rejected / output seen).
- **Interpretation of the response** (in character, one or two lines).
- **Ladder rung shown** (none / message / hint / facts / worked example)
  and whether it resolved the specific confusion or was copied.
- **Friction** after this screen (running total; note the reason for any
  change).

## Per gate

- Recall: attempts per question, inputs rejected verbatim, rung reached.
- Task: attempts, `check` results, what the checklist marked `○`.
- Cleared / not cleared.

## End of sitting

- Final friction and where the persona quit, if it quit (screen id).
- Stages or module cleared.
- Equivalent human sitting time (estimate from attempts and stalls; say
  "estimate").
- **Candidate F-nnn** (a valid answer rejected, a broken hint, a dead end,
  a false statement on screen), each with the screen id and the exact
  input.
- **Candidate O-nnn** (ambiguous phrasing, mode confusion, jargon, pace),
  each with the screen id and the quoted sentence.
- **Debrief** (out of character, five lines at most): which sentences
  triggered the confusion. Name sentences, not fixes.
